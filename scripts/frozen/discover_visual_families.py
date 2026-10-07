"""Train neutral visual family models on train images, select on validation.

No transcription contents or positional outcomes enter the features. Clusters
are candidate families, never asserted graphemes. Source templates are auditable.
"""
from common import OUT,read_json,read_csv,write_json,write_csv,SEED,sha256
import argparse
import functools
import numpy as np
import cv2
from PIL import Image,ImageDraw
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import MiniBatchKMeans
from scipy.special import logsumexp
import joblib

GEOMETRY=['height_ratio','width_ratio','upper_extent_ratio','lower_extent_ratio','ink_area_body2','raster_components','raster_loops','skeleton_endpoint_pixels','skeleton_branch_clusters','column_ink_ridge_count']


def image_feature(shapes):
    return np.stack([cv2.resize(s,(16,16),interpolation=cv2.INTER_AREA).reshape(-1) for s in shapes])


def geom_feature(records):
    rows=[]
    for r in records:
        f=r['features'];v=[f[k] for k in GEOMETRY]
        v[4:]=np.log1p(np.maximum(0,v[4:])).tolist()
        rows.append(v)
    return np.array(rows,np.float32)


def negative_log_density(z,centers,var,weights):
    values=[]
    for start in range(0,len(z),1000):
        d=z[start:start+1000,None,:]-centers[None,:,:]
        ll=-.5*((d*d/var).sum(axis=2)+np.log(2*np.pi*var).sum(axis=1))+np.log(weights)
        values.extend((-logsumexp(ll,axis=1)).tolist())
    return np.array(values)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--model',choices=['fine_components','medium_assemblies','compound_candidates','group_only'],default='medium_assemblies');ap.add_argument('--version',choices=['v3','v4'],default='v4');args=ap.parse_args()
    folder=OUT/f'data/observations/regional_candidates_{args.version}'
    expected=len([r for r in read_csv(OUT/'data/source/all_view_manifest.csv') if r['split']!='excluded_cover'])
    available=[p for p in folder.glob('V_*.json') if p.stem[2:].isdigit()]
    if len(available)!=expected:raise ValueError(f'Incomplete source candidate pass: {len(available)} of {expected}')
    records=[];samples=[];views={};rng=np.random.default_rng(SEED)
    for path in sorted(folder.glob('V_*.json')):
        if not path.stem[2:].isdigit():continue
        obj=read_json(path);view=obj['view'];views[view['view_id']]={'view':view,'native_source':obj['native_source']}
        # Calibration views do not enter formal model training or selection.
        if view['split'] not in ('train','validation'):continue
        candidates=[r for r in obj['instances'] if r['model']==args.model and r['atlas_eligible']]
        if len(candidates)>1000:
            indexes=np.sort(rng.choice(len(candidates),1000,replace=False));candidates=[candidates[i] for i in indexes]
        array=np.load(path.with_name(path.stem+'_shapes.npz'))['shapes']
        records.extend(candidates);samples.extend(cv2.resize(array[r['shape_index']],(16,16),interpolation=cv2.INTER_AREA).reshape(-1) for r in candidates)
    if not records:raise ValueError('No train/validation source instances available')
    images=np.stack(samples);geometry=geom_feature(records)
    train=np.array([r['split']=='train' for r in records]);valid=~train
    if not valid.any():raise ValueError('No independent validation instances')
    train_indexes=np.flatnonzero(train)
    fitting=train_indexes if len(train_indexes)<=16000 else rng.choice(train_indexes,16000,replace=False)
    pca=PCA(n_components=32,whiten=True,svd_solver='randomized',random_state=SEED).fit(images[fitting])
    scaler=StandardScaler().fit(geometry[train])
    z=np.c_[pca.transform(images),scaler.transform(geometry)*.35]
    results=[];fitted={}
    for k in (32,64,128):
        if len(fitting)<k*4:continue
        km=MiniBatchKMeans(n_clusters=k,random_state=SEED,n_init=5,batch_size=1024,max_iter=200,reassignment_ratio=.01).fit(z[fitting])
        labels=km.predict(z[train]);counts=np.bincount(labels,minlength=k)
        var=np.stack([np.var(z[train][labels==i],axis=0)+.05 if (labels==i).sum()>1 else np.ones(z.shape[1]) for i in range(k)])
        weights=(counts+1)/(counts.sum()+k)
        val_loss=negative_log_density(z[valid],km.cluster_centers_,var,weights)
        train_loss=negative_log_density(z[train],km.cluster_centers_,var,weights)
        folios=[len(set(records[j]['folio_component'] for j in train_indexes[labels==i])) for i in range(k)]
        # Equal view weighting in validation selection prevents dense text pages dominating.
        valid_records=[r for r in records if r['split']=='validation'];perview={}
        for r,loss in zip(valid_records,val_loss):perview.setdefault(r['view_id'],[]).append(float(loss))
        meanview=float(np.mean([np.mean(v) for v in perview.values()]))
        result=dict(model=args.model,k=k,training_instances=int(train.sum()),validation_instances=int(valid.sum()),validation_views=len(perview),validation_mean_negative_log_density_nats=meanview,training_mean_negative_log_density_nats=float(train_loss.mean()),recurring_families_three_folios=sum(f>=3 for f in folios),training_quantization_mse=float(np.mean((z[train]-km.cluster_centers_[labels])**2)))
        results.append(result);fitted[k]=dict(kmeans=km,variances=var,weights=weights,training_folio_counts=folios)
        print(result,flush=True)
    best=min(results,key=lambda r:r['validation_mean_negative_log_density_nats']);selected=fitted[best['k']]
    km=selected['kmeans'];assign=km.predict(z);dist=np.linalg.norm(z-km.cluster_centers_[assign],axis=1)
    medoids=[];thresholds=[];family_records=[]
    @functools.lru_cache(maxsize=4)
    def source_image(viewid):return Image.open(OUT/views[viewid]['native_source']).convert('RGB')
    atlas=OUT/f'figures/visual_atlas_{args.version}/{args.model}';atlas.mkdir(parents=True,exist_ok=True)
    cards=[]
    for ci in range(best['k']):
        family_id=f'VF_{args.model}_K{best["k"]:03d}_{ci+1:03d}'
        indexes=train_indexes[assign[train_indexes]==ci]
        if not len(indexes):medoids.append(None);thresholds.append(None);continue
        order=sorted(indexes,key=lambda j:dist[j]);medoid=order[0];medoids.append(records[medoid]['instance_id']);thresholds.append(float(np.percentile(dist[indexes],95)))
        examples=[];seen=set()
        for j in order:
            if records[j]['folio_component'] in seen:continue
            examples.append(j);seen.add(records[j]['folio_component'])
            if len(examples)==6:break
        family=dict(family_id=family_id,model=args.model,cluster_index=ci,training_instances=len(indexes),training_folio_components=len(set(records[j]['folio_component'] for j in indexes)),recurrence_supported=len(seen)>=3,medoid_instance_id=records[medoid]['instance_id'],example_instance_ids=[records[j]['instance_id'] for j in examples],distance_abstention_threshold=thresholds[-1],status='unreviewed candidate visual family',glyph_or_grapheme_claim=False,pen_lift_evidence='unresolved',features_median={key:float(np.median([records[j]['features'][key] for j in indexes])) for key in GEOMETRY})
        family_records.append(family)
        card=Image.new('RGB',(960,185),'white');draw=ImageDraw.Draw(card)
        draw.text((5,5),f'{family_id} train={len(indexes)} folios={family["training_folio_components"]} candidate',fill='black')
        for ei,j in enumerate(examples):
            rec=records[j];crop=source_image(rec['view_id']).crop(rec['bbox_xyxy']);crop.thumbnail((150,125));card.paste(crop,(ei*160+5,35));draw.text((ei*160+5,165),rec['view_id'],fill='black')
        card.save(atlas/f'{family_id}.png');cards.append(card)
    for start in range(0,len(cards),8):
        sheet=Image.new('RGB',(960,1480),'#ddd')
        for i,card in enumerate(cards[start:start+8]):sheet.paste(card,(0,i*185))
        sheet.save(atlas/f'families_{start+1:03d}.png')
    protocol=OUT/f'data/observations/regional_candidate_protocol_snapshot_{args.version}.json'
    if not protocol.exists():protocol=OUT/'data/observations/regional_candidate_protocol_snapshot.json'
    artifact=dict(model_kind=args.model,version=args.version,pca=pca,geometry_scaler=scaler,geometry_feature_names=GEOMETRY,k=best['k'],**selected,medoid_instance_ids=medoids,distance_thresholds=thresholds,source_protocol=sha256(protocol),unit_plan=sha256(OUT/'data/observations/visual_family_analysis_plan.json'),feature_excludes=['line/group rank','pixel position','folio/section/hand labels','conventional transcription identities'])
    modelfolder=OUT/f'data/observations/visual_family_models_{args.version}';modelfolder.mkdir(parents=True,exist_ok=True)
    joblib.dump(artifact,modelfolder/f'{args.model}.joblib')
    write_json(modelfolder/f'{args.model}_families.json',family_records)
    report=dict(status='validation_selected_candidate_model_not_unit_freeze',selection=best,comparisons=results,pca_explained_variance_fraction=float(pca.explained_variance_ratio_.sum()),training_view_count=len(set(r['view_id'] for r in records if r['split']=='train')),validation_view_count=len(set(r['view_id'] for r in records if r['split']=='validation')),test_used=False,limitations=['Training uses unreviewed geometric subdivisions in reviewed approximate writing regions.','Density is a feature-space model comparison, not proof of characters or lossless manuscript compression.','Source quality, unrecognized crossings, faint omissions and incomplete path coverage can bias families.','Validation selection does not establish final held-out performance.'])
    write_json(OUT/f'reports/visual_family_{args.version}_{args.model}.json',report)
    write_csv(OUT/f'reports/visual_family_{args.version}_{args.model}_comparison.csv',results)


if __name__=='__main__':main()
