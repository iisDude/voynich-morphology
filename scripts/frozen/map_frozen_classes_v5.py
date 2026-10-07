"""Apply immutable V3 to source-frozen V5 parents; never refit classes."""
from common import OUT,read_json,write_json,sha256
from register_row_benchmark_v5 import D,T,F
from benchmark_membership_v5 import page_features
from regional_extract_v11 import normalise
from extract_recurrence_units_v3 import feature,holes
from evaluate_source_classes_v3 import transform,assign
from datetime import datetime,timezone
import numpy as np,cv2,pickle

def verify_source_seal():
    for p in read_json(F/'SOURCE_REFERENCE_SEAL.json')['files']:assert sha256(OUT/p['path'])==p['sha256'],p['path']

def prepare_protocol():
    p=F/'SEQUENCE_PROTOCOL_SEAL.json'
    if p.exists():return
    write_json(p,dict(sealed_at_utc=datetime.now(timezone.utc).isoformat(),source_seal_sha256=sha256(F/'SOURCE_REFERENCE_SEAL.json'),before_v3_inference=True,
       taxonomy='Frozen V3 model/radii/features/core exclusions, primary contrast9 with6/12 and fixed slant perturbation. No fitting, merging or splitting structural classes.',
       parent_membership='Confirmed target writing only forms definite parents. Confirmed photographic joins form one parent; disconnected primary raster keeps class UNK. Possible joins remain separate/combined alternatives, neither is privileged by class recurrence. Mixed/unknown target-admissible source spans become explicit unknown membership states.',
       order='Median x of primary pixels in the source-reviewed body core(-.95,+.25 body), centroid fallback for detached structures, flagged order-unknown when no core support. Native whole-parent extent retained. Ordering ambiguity is not optimized by recurrence.',
       partition='Three separate0.35/0.55/0.75 body-height gap hypotheses. Running maximum right extent prevents a cut through any already included connected parent or upper overhang. No claim of words or semantic group boundaries.',
       completeness='Exact complete source group requires all writing membership/owner/parent/order resolved and every parent assigned a stable core V3 class. UNK retained; unknown/mixed source spans and possible joins prevent exact-complete qualification. Report membership completeness and class completeness separately.',
       recurrence='Complete class sequences only, with length1+ and length3+ separately. Repeated coverage requires occurrence in another caption. Heldout lexicon uses development-caption sequences only. Unknown strings do not count as repeated complete sequences.',
       sensitivity='Report source membership with all optional spans, with detached uncertainty removed, with owner uncertainty removed, and all optional spans removed. These are counterfactual bounds, not reference corrections.',
       statistics='Caption-cluster bootstrap intervals; two heldout captions cannot establish a broad population error rate. Source class-frequency/UNK-location/group-size preserving row shuffle null,200 draws. No natural-language/positional claim is tested.',
       downstream='Only after final V5 freeze and only registered support gates. No conventional labels, Currier metadata, positional outcomes or minimal-pair support have been opened.'))

def parent_records(r):
    target=[p for p in r['objects'] if p['membership']=='confirmed_writing' and p['owner']=='target'];lookup={int(p['object_id'][-3:]):p for p in target};joined=set();ps=[]
    for j in r['confirmed_joins']:
        members=[lookup[n] for n in j if n in lookup]
        if len(members)!=len(j):continue
        joined.update(j);ps.append(dict(parent_id=r['row_id']+'_J'+'_'.join(map(str,j)),source_objects=[p['object_id'] for p in members],members=members,parent_boundary_status='confirmed_photographic_join'))
    for p in target:
        n=int(p['object_id'][-3:])
        if n in joined:continue
        ps.append(dict(parent_id=p['object_id'],source_objects=[p['object_id']],members=[p],parent_boundary_status=p['physical_parent_status']))
    for p in ps:
        b=np.array([q['native_bbox'] for q in p['members']]);p['native_bbox']=[int(b[:,0].min()),int(b[:,1].min()),int(b[:,2].max()),int(b[:,3].max())]
    return ps

def inference(r,ps,cc,model):
    sh=[];gg=[];low=[];high=[];vg=[];base_lab,base_st=cc[0][1:3];body=r['body_proxy'];kn=np.array(r['body_path'])
    for rec in ps:
        x,y,c,d=rec['native_bbox'];mask=np.zeros((d-y,c-x),np.uint8)
        for p in rec['members']:
            if p['raster']!='primary9':continue
            mask|=(base_lab[y:d,x:c]==p['cc_label']).astype(np.uint8)
        ys,xs=np.where(mask);core=(ys+y>=np.interp(xs+x,kn[:,0],kn[:,1])-.95*body)&(ys+y<=np.interp(xs+x,kn[:,0],kn[:,1])+.25*body)
        rec['body_core_support']=int(core.sum());rec['root_x']=float(np.median(xs[core]+x)) if core.sum() else float((x+c)/2);rec['root_interval']=[int((xs[core]+x).min()),int((xs[core]+x).max())+1] if core.sum() else [x,c];rec['order_status']='body_root_supported' if core.sum()>=8 else 'unknown_detached_order';rec['structural_class']='UNK';rec['unknown_reasons']=[];rec['body_proxy']=body
        n=mask.sum();connected=cv2.connectedComponents(mask,8)[0]-1
        eligible=n>=35 and d-y>=.32*body and c-x>=4 and d-y<=3.8*body and c-x<=12*body and connected==1
        if not eligible:rec['unknown_reasons'].append('frozen_v3_geometry_or_primary_connectivity');continue
        vv=[];boxes=[];ious=[];same=[];top=[holes(mask)];variants=[]
        for contrast,alt in zip([6,12],cc[1:]):
            al,st=alt[1:3];ids,cnt=np.unique(al[y:d,x:c][mask>0],return_counts=True);valid=sorted([(int(i),int(k)) for i,k in zip(ids,cnt) if i],key=lambda z:-z[1])
            if not valid:
                vv.append(normalise(mask,body));boxes.append([x,y,c,d]);ious.append(0);same.append(False);top.append(top[0]);variants.append(dict(contrast=contrast,status='absent'));continue
            k,inter=valid[0];a,b,w,h,area=map(int,st[k]);am=(al[b:b+h,a:a+w]==k).astype(np.uint8);iou=inter/(n+area-inter);split=sum(z>=n*.05 for i,z in valid)>1
            others,counts=np.unique(base_lab[b:b+h,a:a+w][am>0],return_counts=True);merge=sum(i!=0 and base_st[i,4]>=35 and z>=base_st[i,4]*.2 for i,z in zip(others,counts))>1
            vv.append(normalise(am,body));boxes.append([a,b,a+w,b+h]);ious.append(float(iou));same.append(not(split or merge));top.append(holes(am));variants.append(dict(contrast=contrast,native_bbox=boxes[-1],iou=float(iou),split=bool(split),merge=bool(merge)))
        rec['raster_stable']=bool(all(same) and min(ious)>=.5 and len(set(top))==1);rec['competing_rasters']=variants;rec['holes_across_thresholds']=list(map(int,top));rec['feature_index']=len(sh);sh.append(normalise(mask,body));gg.append(feature(mask,body));low.append(vv[0]);high.append(vv[1]);vg.append(boxes)
    if sh:
        sh=np.array(sh);gg=np.array(gg);base=assign(transform(sh,gg,model),gg,model);variants=[]
        for j,ss in enumerate([low,high]):
            g=gg.copy()
            for i,box in enumerate(vg):a,b,c,d=box[j];g[i,:3]=[np.log((d-b)/body),np.log((c-a)/body),np.log((c-a)/(d-b))]
            variants.append(assign(transform(np.array(ss),g,model),g,model))
        nuisance=np.array([cv2.warpAffine(s,np.float32([[1,.04,-1],[0,1,1]]),(48,48),flags=cv2.INTER_LINEAR,borderValue=0) for s in sh]);nu=assign(transform(nuisance,gg,model),gg,model)
        for rec in ps:
            if 'feature_index' not in rec:continue
            i=rec['feature_index'];cid=str(base['classes'][i]);nom=bool(base['accepted'][i]);ts=bool(nom and all(v['accepted'][i] and v['classes'][i]==cid for v in variants));ns=bool(nom and nu['accepted'][i] and nu['classes'][i]==cid)
            reliable=rec['raster_stable'] and nom and ts and ns and cid!='ST09'
            rec.update(structural_class=cid if reliable else 'UNK',nominal_class=cid if np.isfinite(base['distance'][i]) else None,competing_class=str(base['alternatives'][i]) if np.isfinite(base['alternative_distance'][i]) else None,nominal_accepted=nom,threshold_class_stable=ts,alignment_class_stable=ns,distance=float(base['distance'][i]) if np.isfinite(base['distance'][i]) else None)
            if not reliable:rec['unknown_reasons'].append('unchanged_v3_abstention_or_perturbation')
    for p in ps:p.pop('members')
    return ps

def main():
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen(source_stage=False)
    verify_source_seal();prepare_protocol()
    if (F/'parent_class_assignments.json').exists():raise RuntimeError('Already mapped')
    path=OUT/'data/observations/recurrence_v3_structural_candidate/sealed_class_model.pkl';assert sha256(path)==read_json(D/'PLAN.json')['v3_model_sha256'];model=pickle.loads(path.read_bytes());out=[]
    for r in read_json(F/'source_reference.json')['rows']:
        rgb,delta,cc=page_features(r);ps=inference(r,parent_records(r),cc,model);out.append(dict(row_id=r['row_id'],caption=r['caption'],split=r['split'],parents=ps));print(r['row_id'],len(ps),'parents',sum(p['structural_class']!='UNK' for p in ps),'assigned unchanged V3',flush=True)
    write_json(F/'parent_class_assignments.json',dict(created_at_utc=datetime.now(timezone.utc).isoformat(),v3_model_sha256=sha256(path),source_reference_seal_sha256=sha256(F/'SOURCE_REFERENCE_SEAL.json'),sequence_protocol_sha256=sha256(F/'SEQUENCE_PROTOCOL_SEAL.json'),rows=out,classes_refitted=False,source_judgments_changed=False))
    verify_source_seal()
if __name__=='__main__':main()
