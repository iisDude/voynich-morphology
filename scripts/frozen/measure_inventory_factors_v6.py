"""Quantify base-removal promiscuity and threshold robustness; no tokens."""
from inventory_v6_common import *
from discover_inventory_candidates_v6 import factor_arrays
from evaluate_source_classes_v3 import transform,assign
from benchmark_membership_v5 import page_features
from PIL import Image
from collections import Counter
import numpy as np,cv2,pickle

def explanations(mask,body,model):
    items,sh,g=factor_arrays(mask,body);out=[]
    if not sh:return out
    sh=np.array(sh);g=np.array(g);base=assign(transform(sh,g,model),g,model);shift=np.array([cv2.warpAffine(s,np.float32([[1,.04,-1],[0,1,1]]),(48,48),flags=cv2.INTER_LINEAR,borderValue=0) for s in sh]);nu=assign(transform(shift,g,model),g,model)
    for i,q in enumerate(items):
        if base['accepted'][i] and nu['accepted'][i] and base['classes'][i]==nu['classes'][i] and base['classes'][i]!='ST09':out.append(dict(q,base_class=str(base['classes'][i]),description=str(base['classes'][i])+'+outside_'+q['side']+'_residual'))
    return out

def variants(r,cc):
    mask=(np.asarray(Image.open(OUT/r['mask_path']))>0).astype(np.uint8);x,y,c,d=r['native_bbox'];out=[mask]
    for vi in [1,2]:
        ids,cnt=np.unique(cc[vi][1][y:d,x:c][mask>0],return_counts=True);valid=sorted([(int(i),int(k)) for i,k in zip(ids,cnt) if i],key=lambda q:-q[1])
        if not valid:out.append(mask*0);continue
        k=valid[0][0];a,b,w,h,area=map(int,cc[vi][2][k]);out.append((cc[vi][1][b:b+h,a:a+w]==k).astype(np.uint8))
    return out

def main():
    guard();verify_seal(D/'CANDIDATE_MODEL_SEAL.json');model=pickle.loads(MODEL.read_bytes());disc=read_json(D/'discovery_parents.json');fresh=read_json(D/'fresh_source_reference.json')['parents'];allrec=disc+[r for r in fresh if r['membership']=='confirmed_writing'];out=[];cacheview=None;cache=None
    for i,r in enumerate(allrec):
        native=r['native_source']
        if cacheview!=native:cache=page_features(r);cacheview=native
        masks=variants(r,cache[2]);ex=[explanations(m,r['body_proxy'],model) if m.any() else [] for m in masks];keys=[{(q['description'],q['fraction']) for q in qs} for qs in ex];stable=set.intersection(*keys)
        # Matched transform controls keep each source silhouette's connectivity,
        # loop count and scale but reverse its relative orientation.
        control=explanations(np.ascontiguousarray(np.rot90(masks[0],2)),r['body_proxy'],model)
        source_ok=(r.get('source_parent_status')=='confirmed_connected_writing_trace' if 'source_parent_status' in r else r['parent_boundary_status']=='confirmed_connected_trace' and r['diagnosis_stage']!='insufficient_photo_or_disconnected')
        out.append(dict(parent_id=r['parent_id'],caption=r['caption'],corpus='discovery_known_V3' if r.get('structural_class') not in [None,'UNK'] else 'discovery_UNK' if r['split']=='discovery' else 'fresh_writing',source_resolved=source_ok,primary_explanations=ex[0],threshold_stable_measurements=[dict(description=a,fraction=b) for a,b in sorted(stable)],rotated_control_explanations=len(control),validated_compositional_class=None,whole_source_parent_unchanged=True))
        if i%50==0:print('Factor diagnostic',i,'/',len(allrec),flush=True)
    summary={}
    for kind in ['discovery_known_V3','discovery_UNK','fresh_writing']:
        rr=[r for r in out if r['corpus']==kind];summary[kind]=dict(parents=len(rr),primary_factor_fits=sum(bool(r['primary_explanations']) for r in rr),threshold_stable_factor_measurements=sum(bool(r['threshold_stable_measurements']) for r in rr),rotated_control_factor_fits=sum(r['rotated_control_explanations']>0 for r in rr),validated_composition_assignments=0)
    save(T/'composition_robustness_and_controls.json',dict(created_at_utc=now(),parents=out,summary=summary,source_classification='Three recurrent generic cut families rejected by pretest native review. Primary/threshold-stable fits here are descriptive measurements, not validated coverage or sequence notation.',null='180degree orientation reversal retains parent shape topology/ink/scale but not manuscript orientation. Diagnostic promiscuity control, not proof the rotated source is writing; no independence claim.',selection='Includes unstable confirmed parents to quantify raw fits; resolved-only denominator separately available, never counted as accepted.'))
    print(summary,flush=True)
if __name__=='__main__':main()
