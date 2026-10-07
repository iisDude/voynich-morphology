"""Evaluate sealed source classes; never updates their fit or thresholds."""
from common import OUT,read_json,write_json,sha256,SEED
from fit_source_classes_v3 import pixels
import numpy as np,cv2,pickle
from sklearn.neighbors import NearestNeighbors
from collections import Counter,defaultdict
from PIL import Image,ImageDraw
ROOT=OUT/'data/observations/recurrence_v3_development'

def transform(sh,g,model):
    p=model['pca'].transform(pixels(sh));geo=np.clip(model['geometry_scaler'].transform(g),-4,4);geo[:,4]=g[:,4]*2
    return np.c_[p/model['pca_scale']/np.sqrt(model.get('pca_components',32)),geo*model.get('geometry_weight',.65)/np.sqrt(g.shape[1])]

def assign(z,g,model):
    ids=sorted(set(model['class_ids']));d=np.full((len(z),len(ids)),np.inf);near=np.full((len(z),len(ids)),-1,int)
    for j,cid in enumerate(ids):
        idx=np.where(model['class_ids']==cid)[0]
        topology=[b for (a,b),c in model['keys'].items() if c==cid][0];q=np.where(g[:,4]==topology)[0]
        if not len(q):continue
        nn=NearestNeighbors(n_neighbors=1).fit(model['z_train'][idx]);dd,jj=nn.kneighbors(z[q]);d[q,j]=dd[:,0];near[q,j]=model['train_indices'][idx[jj[:,0]]]
    order=np.argsort(d,axis=1);first=order[:,0];second=order[:,1];best=d[np.arange(len(z)),first];nextd=d[np.arange(len(z)),second]
    classes=np.array(ids)[first];alternatives=np.array(ids)[second];r=np.array([model['radii'][c] for c in classes]);ratio=np.zeros(len(best));finite=np.isfinite(best);ratio[finite]=nextd[finite]/np.maximum(best[finite],1e-8)
    accepted=(best<=r)&(ratio>=1.08)&np.isfinite(best)&np.array([model['core'][c]['training_captions']>=3 for c in classes])
    return dict(classes=classes,alternatives=alternatives,distance=best,alternative_distance=nextd,accepted=accepted,nearest=near[np.arange(len(z)),first],negative=near[np.arange(len(z)),second])

def chamfer(a,b):
    aa=(cv2.resize(a,(24,24))>.25).astype(np.uint8);bb=(cv2.resize(b,(24,24))>.25).astype(np.uint8)
    da=cv2.distanceTransform(1-aa,cv2.DIST_L2,3);db=cv2.distanceTransform(1-bb,cv2.DIST_L2,3)
    return float((db[aa>0].mean()+da[bb>0].mean())/48)

def main():
    from recurrence_guard_v3 import require_unfrozen
    require_unfrozen(ROOT)
    seal=read_json(ROOT/'MODEL_SEAL.json');assert sha256(ROOT/'sealed_class_model.pkl')==seal['model_sha256']
    model=pickle.loads((ROOT/'sealed_class_model.pkl').read_bytes());rec=read_json(ROOT/'source_parents.json');data=np.load(ROOT/'source_shapes.npz');sh=data['shapes'];g=data['geometry']
    idx=np.array([i for i,r in enumerate(rec) if r['class_eligible'] and r['split'] in ['validation','test']]);z=transform(sh[idx],g[idx],model);base=assign(z,g[idx],model);variants=[]
    for name in ['low','high']:
        vg=g[idx].copy()
        for ii,global_i in enumerate(idx):
            r=rec[global_i];alt=r['competing_rasters'][0 if name=='low' else 1]['native_bbox'];a,b,c,d=alt;body=r['body_height_proxy'];vg[ii,0]=np.log((d-b)/body);vg[ii,1]=np.log((c-a)/body);vg[ii,2]=np.log((c-a)/(d-b))
        variants.append(assign(transform(data[name][idx],vg,model),vg,model))
    nuisance=sh[idx].copy()
    for i,s in enumerate(nuisance):nuisance[i]=cv2.warpAffine(s,np.float32([[1,.04,-1],[0,1,1]]),(48,48),flags=cv2.INTER_LINEAR,borderValue=0)
    nuisance_assign=assign(transform(nuisance,g[idx],model),g[idx],model)
    records=[];core=defaultdict(list);captions={}
    for local,global_i in enumerate(idx):
        r=rec[global_i];cid=str(base['classes'][local]);accepted=bool(base['accepted'][local]);stable=all(v['classes'][local]==cid and v['accepted'][local] for v in variants)
        if r['split']=='test' and accepted:core[cid].append(global_i)
        records.append(dict(parent_id=r['parent_id'],index=int(global_i),split=r['split'],view_id=r['view_id'],folio_component=r['folio_component'],class_id=cid if accepted else None,proposed_class=cid if np.isfinite(base['distance'][local]) else None,competing_class=str(base['alternatives'][local]) if np.isfinite(base['alternative_distance'][local]) else None,distance=float(base['distance'][local]) if np.isfinite(base['distance'][local]) else None,alternative_distance=float(base['alternative_distance'][local]) if np.isfinite(base['alternative_distance'][local]) else None,nearest_training_parent=rec[base['nearest'][local]]['parent_id'] if base['nearest'][local]>=0 else None,
          status='accepted_candidate' if accepted else 'unknown_class',threshold_class_stable=bool(stable),alignment_slant_stable=bool(nuisance_assign['classes'][local]==cid and nuisance_assign['accepted'][local]),native_chamfer=chamfer(sh[global_i],sh[base['nearest'][local]]) if base['nearest'][local]>=0 else None))
    coreclasses={c:dict(training_captions=model['core'][c]['training_captions'],test_instances=len(ii),test_captions=len(set(rec[i]['folio_component'] for i in ii))) for c,ii in core.items() if len(ii)>=5 and len(set(rec[i]['folio_component'] for i in ii))>=3 and model['core'][c]['training_captions']>=3}
    summary={}
    for split in ['validation','test']:
        rr=[r for r in records if r['split']==split];aa=[r for r in rr if r['class_id']];summary[split]=dict(clear_components=len(rr),accepted=len(aa),assignment_coverage=len(aa)/max(1,len(rr)),caption_groups=len(set(r['folio_component'] for r in rr)),threshold_assignment_stability=sum(r['threshold_class_stable'] for r in aa)/max(1,len(aa)),alignment_slant_stability=sum(r['alignment_slant_stable'] for r in aa)/max(1,len(aa)),median_chamfer=float(np.median([r['native_chamfer'] for r in aa])))
    write_json(ROOT/'heldout_class_assignments.json',records);write_json(ROOT/'heldout_class_metrics.json',dict(model_seal_sha256=sha256(ROOT/'MODEL_SEAL.json'),metrics=summary,recurring_core_classes=coreclasses,recurring_core_count=len(coreclasses),note='Unsupervised source candidates only. Native pair adjudication still required; no new freeze.'))
    # Balanced deterministic source pair audit. Labels for predicted same/different withheld in gallery.
    rng=np.random.default_rng(SEED);eligible=[i for i,r in enumerate(records) if r['split']=='test' and r['class_id'] in coreclasses];rng.shuffle(eligible);chosen=[];seen=Counter()
    for j in eligible:
        cid=records[j]['class_id']
        if seen[cid]>=model.get('audit_pairs_per_class',2):continue
        chosen.append(j);seen[cid]+=1
        if len(chosen)==40:break
    pairs=[]
    for j in chosen:
        local=j;global_i=int(idx[local])
        for kind,near in [('positive',base['nearest'][local]),('hard_negative',base['negative'][local])]:
            if near<0:continue
            pairs.append(dict(kind=kind,left_parent=rec[global_i]['parent_id'],right_parent=rec[near]['parent_id'],left_index=global_i,right_index=int(near),proposed_class=records[j]['class_id'],left_crop=rec[global_i]['native_crop'],right_crop=rec[near]['native_crop'],chamfer=chamfer(sh[global_i],sh[near])))
    rng.shuffle(pairs);gallery=OUT/'figures/recurrence_v3'/('structural_pair_audit' if model.get('pca_components')==24 else 'pair_audit');gallery.mkdir(parents=True,exist_ok=True)
    for i,p in enumerate(pairs):p['pair_id']=f'A{i+1:03d}'
    for start in range(0,len(pairs),10):
        canvas=Image.new('RGB',(1250,1900),'white');draw=ImageDraw.Draw(canvas)
        for j,p in enumerate(pairs[start:start+10]):
            yy=j*190;draw.text((8,yy+5),p['pair_id']+' source RGB; class suggestion hidden',fill='black')
            for xx,key in [(10,'left_crop'),(640,'right_crop')]:
                im=Image.open(OUT/p[key]).convert('RGB');scale=min(3.,600/im.width,145/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);canvas.paste(im,(xx,yy+30))
        canvas.save(gallery/f'pairs_{start+1:03d}_{min(start+10,len(pairs)):03d}.png')
    write_json(ROOT/'pair_audit_key.json',pairs);print(summary,'recurring core',len(coreclasses),'audit pairs',len(pairs),flush=True)

if __name__=='__main__':main()
