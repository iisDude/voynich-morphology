"""Apply training-only prototypes without refitting, retaining abstentions."""
from common import OUT,read_json,write_json,write_csv,sha256,SEED
from discover_visual_families import geom_feature
import numpy as np
import cv2
import joblib
from PIL import Image,ImageDraw

MODELS=['fine_components','medium_assemblies','compound_candidates','group_only']

def main():
    modeldir=OUT/'data/observations/visual_family_models_v4'
    models={m:joblib.load(modeldir/f'{m}.joblib') for m in MODELS}
    review=read_json(OUT/'data/observations/medium_family_source_review_v4.json')
    quality={r['cluster_index']:r['review_category'] for r in review['records']}
    write_json(OUT/'data/observations/heldout_source_audit_plan.json',dict(seed=SEED,
        frozen_model_hashes={m:sha256(modeldir/f'{m}.joblib') for m in MODELS},
        source_review_hash=sha256(OUT/'data/observations/medium_family_source_review_v4.json'),
        gate='atlas eligible; training radius <= training 95th percentile; at least three training folio components; primary medium family reviewed writing_consistent',
        sample='up to 20 admitted medium instances per selected view; 4 validation and 6 test views chosen by fixed RNG; uniform within each view',
        outcome='writing visible / non-writing or incompatible row / ambiguous; source quality only, atomic identity remains unproven',
        rule='no refitting or source-quality threshold changes using test crops; failure is retained as a failure of v4'))
    folder=OUT/'data/observations/assigned_visual_candidates_v4';folder.mkdir(parents=True,exist_ok=True)
    summaries=[];auditviews=[]
    for path in sorted((OUT/'data/observations/regional_candidates_v4').glob('V_*.json')):
        if not path.stem[2:].isdigit():continue
        obj=read_json(path);shapes=np.load(path.with_name(path.stem+'_shapes.npz'))['shapes'];units={}
        for model in MODELS:
            recs=[r for r in obj['instances'] if r['model']==model];artifact=models[model]
            if not recs:continue
            images=np.stack([cv2.resize(shapes[r['shape_index']],(16,16),interpolation=cv2.INTER_AREA).ravel() for r in recs])
            z=np.c_[artifact['pca'].transform(images),artifact['geometry_scaler'].transform(geom_feature(recs))*.35]
            labels=artifact['kmeans'].predict(z);dist=np.linalg.norm(z-artifact['kmeans'].cluster_centers_[labels],axis=1)
            for r,ci,d in zip(recs,labels,dist):
                ci=int(ci);radius=artifact['distance_thresholds'][ci]
                recognized=bool(r['atlas_eligible'] and radius is not None and d<=radius and artifact['training_folio_counts'][ci]>=3)
                cat=quality[ci] if model=='medium_assemblies' else 'source_quality_unreviewed'
                admitted=recognized and cat=='writing_consistent'
                units[r['instance_id']]=dict(instance_id=r['instance_id'],bbox_xyxy=r['bbox_xyxy'],model=model,
                    nearest_family_id=f'VF_{model}_K{artifact["k"]:03d}_{ci+1:03d}',prototype_distance=float(d),
                    training_distance_threshold=radius,recognized_within_training_radius=recognized,
                    source_quality_category=cat,admitted_to_primary_candidate_assay=admitted,
                    unit_identity=f'VF_{model}_K{artifact["k"]:03d}_{ci+1:03d}' if admitted else None,
                    abstention_reason=None if admitted else 'fragment, distance outlier, or source family not consistently writing',
                    atomic_unit_status='unresolved',pen_lift_evidence='unresolved')
        groups=[]
        for g in obj['groups']:
            medium=[units[i] for i in g['models']['medium_assemblies']]
            approved=bool(medium and all(r['admitted_to_primary_candidate_assay'] for r in medium))
            groups.append(dict(**g,primary_candidate_units=[r['unit_identity'] for r in medium] if approved else None,
                primary_assay_eligible=approved,assay_exclusion=None if approved else 'one or more medium subdivisions unresolved',
                neighboring_groups_unresolved=True))
        write_json(folder/path.name,dict(view=obj['view'],source_image_sha256=obj['image_sha256'],
            source_candidate_sha256=sha256(path),units=units,groups=groups,
            status='training-only family assignments; primary source gate candidate; no atomic alphabet claim'))
        summaries.append(dict(view_id=path.stem,split=obj['view']['split'],candidate_groups=len(groups),
            admitted_groups=sum(g['primary_assay_eligible'] for g in groups),
            medium_instances=sum(u['model']=='medium_assemblies' for u in units.values()),
            admitted_medium_instances=sum(u['admitted_to_primary_candidate_assay'] for u in units.values())))
        if obj['view']['split'] in ('validation','test'):
            admitted=[u for u in units.values() if u['admitted_to_primary_candidate_assay']]
            if len(admitted)>=20:auditviews.append((obj['view']['split'],path,admitted,obj['native_source']))
        print(path.stem,summaries[-1]['admitted_groups'],flush=True)
    write_csv(OUT/'reports/assigned_visual_candidate_coverage_v4.csv',summaries)
    rng=np.random.default_rng(SEED);audit=[];auditfolder=OUT/'figures/heldout_source_audit_v4';auditfolder.mkdir(parents=True,exist_ok=True)
    number=0
    for split,count in [('validation',4),('test',6)]:
        pool=[v for v in auditviews if v[0]==split]
        for vi in rng.choice(len(pool),min(count,len(pool)),replace=False):
            _,path,admitted,source=pool[vi];rgb=Image.open(OUT/source).convert('RGB')
            chosen=rng.choice(len(admitted),20,replace=False);sheet=Image.new('RGB',(800,1000),'white');draw=ImageDraw.Draw(sheet)
            for cell,j in enumerate(chosen):
                u=admitted[j];number+=1;x=(cell%4)*200;y=(cell//4)*200
                crop=rgb.crop(u['bbox_xyxy']);crop.thumbnail((190,150));sheet.paste(crop,(x+5,y+30))
                draw.text((x+5,y+4),f'A{number:03d} {path.stem} {split}',fill='black')
                draw.text((x+5,y+180),u['nearest_family_id'].split('_')[-1],fill='black')
                audit.append(dict(audit_id=f'A{number:03d}',view_id=path.stem,split=split,instance_id=u['instance_id'],
                    family_id=u['nearest_family_id'],bbox_xyxy=u['bbox_xyxy'],source_path=source,
                    outcome='unreviewed',gallery=f'figures/heldout_source_audit_v4/{path.stem}.png'))
            sheet.save(auditfolder/f'{path.stem}.png')
    write_json(OUT/'data/observations/heldout_source_audit_v4.json',audit)
    print('Audit',len(audit),flush=True)

if __name__=='__main__':main()
