"""Train-only whole-parent and base/residual descriptions; no sequences."""
from inventory_v6_common import *
from evaluate_source_classes_v3 import transform,assign
from extract_recurrence_units_v3 import feature
from regional_extract_v11 import normalise
from prepare_structural_inventory_v6 import gallery
from sklearn.cluster import AgglomerativeClustering
from scipy.spatial.distance import cdist
from PIL import Image
from collections import Counter,defaultdict
import numpy as np,cv2,pickle

def candidate_fit():
    if (D/'CANDIDATE_MODEL_SEAL.json').exists():raise RuntimeError('Candidate model sealed')
    guard();verify_seal(D/'DIAGNOSIS_SEAL.json');plan=read_json(D/'PLAN.json');rec=read_json(D/'discovery_parents.json');data=np.load(D/'discovery_shapes.npz');g=data['geometry'][:,0];model=pickle.loads(MODEL.read_bytes());z=transform(data['shapes'][:,0],g,model);groups=[]
    amended=(D/'DEVELOPMENT_AMENDMENT.json').exists();diameter=read_json(D/'DEVELOPMENT_AMENDMENT.json')['grouping_diameter'] if amended else .35
    pool=[i for i,r in enumerate(rec) if r['structural_class']=='UNK' and r['diagnosis_stage']=='stable_source_structure_pending'];faint={r['parent_id'] for r in read_json(D/'source_unknown_diagnosis.json')['parents'] if 'insufficient_photographic_morphology' in r['overlapping_hypotheses']};pool=[i for i in pool if rec[i]['parent_id'] not in faint]
    for h in sorted(set(g[pool,4])):
        ii=np.array([i for i in pool if g[i,4]==h]);labels=AgglomerativeClustering(n_clusters=None,distance_threshold=diameter,linkage='complete').fit_predict(z[ii]) if len(ii)>1 else [0]
        for l in sorted(set(labels)):
            idx=ii[np.array(labels)==l];caps={rec[i]['caption'] for i in idx};groups.append(dict(indices=idx.tolist(),parents=[rec[i]['parent_id'] for i in idx],holes=int(h),n=len(idx),captions=sorted(caps),qualifies_train=len(idx)>=8 and len(caps)>=3))
    groups.sort(key=lambda a:(-a['n'],a['parents'][0]));qualified=[r for r in groups if r['qualifies_train']][:12];bundle=[]
    for j,q in enumerate(qualified):
        cid=f'NC{j+1:02d}';q['candidate_id']=cid;ii=np.array(q['indices']);dd=cdist(z[ii],z[ii]);mins=[]
        for a,i in enumerate(ii):
            vals=[dd[a,b] for b,k in enumerate(ii) if rec[k]['caption']!=rec[i]['caption']]
            if vals:mins.append(min(vals))
        radius=min(diameter,float(np.quantile(mins,.9)));bundle.append(dict(candidate_id=cid,indices=q['indices'],parent_ids=q['parents'],holes=q['holes'],radius=radius,source_structure='pending native whole-parent group review',training_instances=q['n'],training_captions=len(q['captions'])))
        gallery([rec[i] for i in ii],cid+'_candidate')
    target=D/('calibrated_whole_candidate_discovery.json' if amended else 'whole_candidate_discovery.json')
    save(target,dict(created_at_utc=now(),pool=len(pool),all_clusters=groups,candidates=bundle,diameter=diameter,metric='Frozen V3 embedding, exact significant hole count, complete-link; no test data or sequence objective',candidate_grouping_prespecified=True));
    if not amended:np.savez_compressed(D/'whole_candidate_embedding.npz',z=z,g=g)
    print('Stable eligible',len(pool),'clusters',len(groups),'qualified',[(c['candidate_id'],c['training_instances'],c['training_captions']) for c in bundle],flush=True)

def factor_arrays(mask,body):
    h,w=mask.shape;items=[];sh=[];gg=[]
    for side in ['left','right','top','bottom']:
        for fraction in [.2,.3,.4]:
            base=mask.copy();cut=round((w if side in ['left','right'] else h)*fraction)
            if side=='left':base[:,:cut]=0
            elif side=='right':base[:,w-cut:]=0
            elif side=='top':base[:cut,:]=0
            else:base[h-cut:,:]=0
            residual=mask-base;ratio=residual.sum()/max(mask.sum(),1)
            if not .15<=ratio<=.45 or cv2.connectedComponents(base,8)[0]-1!=1:continue
            ys,xs=np.where(base);a,b,c,d=int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1);bm=base[b:d,a:c]
            if bm.sum()<35 or d-b<.32*body or d-b>3.8*body or c-a<4:continue
            # A boundary of the hypothetical removal must actually touch ink.
            contact=int((cv2.dilate(base,np.ones((3,3),np.uint8))&residual).sum())
            if not contact:continue
            items.append(dict(side=side,fraction=fraction,base_local_bbox=[a,b,c,d],residual_ink_fraction=float(ratio),contact_pixels=contact));sh.append(normalise(bm,body));gg.append(feature(bm,body))
    return items,sh,gg

def composition_fit():
    if (D/'CANDIDATE_MODEL_SEAL.json').exists():raise RuntimeError('Candidate factors sealed')
    guard();rec=read_json(D/'discovery_parents.json');model=pickle.loads(MODEL.read_bytes());records=[]
    for r in rec:
        if r['structural_class']!='UNK' or r['diagnosis_stage']!='stable_source_structure_pending':continue
        mask=(np.asarray(Image.open(OUT/r['mask_path']))>0).astype(np.uint8);items,sh,gg=factor_arrays(mask,r['body_proxy'])
        explanations=[]
        if sh:
            sh=np.array(sh);gg=np.array(gg);base=assign(transform(sh,gg,model),gg,model);shift=np.array([cv2.warpAffine(s,np.float32([[1,.04,-1],[0,1,1]]),(48,48),flags=cv2.INTER_LINEAR,borderValue=0) for s in sh]);alt=assign(transform(shift,gg,model),gg,model)
            for i,q in enumerate(items):
                if base['accepted'][i] and alt['accepted'][i] and base['classes'][i]==alt['classes'][i] and base['classes'][i]!='ST09':explanations.append(dict(q,base_class=str(base['classes'][i]),description=str(base['classes'][i])+'+outside_'+q['side']+'_residual',distance=float(base['distance'][i]),threshold_validation='pending: primary-mask factor only, not a valid composite assignment'))
        records.append(dict(parent_id=r['parent_id'],caption=r['caption'],explanations=explanations,whole_parent_retained=True))
    by=defaultdict(list)
    for r in records:
        for key in set(q['description'] for q in r['explanations']):by[key].append(r)
    candidates={k:dict(training_instances=len(v),training_captions=len({r['caption'] for r in v}),parents=[r['parent_id'] for r in v],eligible=len(v)>=8 and len({r['caption'] for r in v})>=3) for k,v in by.items()}
    save(D/'composition_discovery.json',dict(created_at_utc=now(),parents=records,candidates=candidates,primary_factor_coverage=sum(bool(r['explanations']) for r in records),interpretation='Outside-band removal supports competing morphology measurements only. A successful truncated-base fit does not prove an inserted unit; residual geometry/contact and source agreement still require validation.'))
    print('Primary factor explanations',sum(bool(r['explanations']) for r in records),'candidate families',[(k,v['training_instances']) for k,v in candidates.items() if v['eligible']],flush=True)

if __name__=='__main__':
    import sys
    candidate_fit() if sys.argv[1]=='whole' else composition_fit()
