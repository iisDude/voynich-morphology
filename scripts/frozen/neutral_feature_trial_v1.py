"""Neutral continuous source-feature trial, independent of class fitting."""
from common import OUT,read_json,write_json,sha256
from datetime import datetime,timezone
from pathlib import Path
import numpy as np,cv2
from PIL import Image
from collections import Counter,defaultdict
from calibrate_assemblies import topology
from benchmark_membership_v5 import page_features
from measure_inventory_factors_v6 import variants

D=OUT/'data/observations/neutral_feature_trial_v1'
T=OUT/'tests/neutral_feature_trial_v1'
G=OUT/'figures/neutral_feature_trial_v1'
V6=OUT/'data/observations/visual_dataset_v6'
OLD=OUT/'data/observations/structural_inventory_v6_development'
DEFS={
 'log_height_body':('geometry',.18,'log native ink-envelope height/body proxy'),
 'log_width_body':('geometry',.18,'log native ink-envelope width/body proxy'),
 'log_aspect':('geometry',.18,'log native width/height'),
 'ink_density':('geometry',.10,'ink pixel fraction of tight parent envelope'),
 'ink_centroid_x':('distribution',.10,'ink centroid relative to own envelope width'),
 'ink_centroid_y':('distribution',.10,'ink centroid relative to own envelope height'),
 'ink_spread_x':('distribution',.08,'ink x standard deviation/envelope width'),
 'ink_spread_y':('distribution',.08,'ink y standard deviation/envelope height'),
 'raster_components':('connectivity',0,'eight-connected raster components, not pen lifts'),
 'significant_cavity_count':('cavity',0,'enclosed background regions, area>=max(8px,1.2%ink)'),
 'cavity_area_fraction':('cavity',.08,'significant enclosed background area/envelope area'),
 'cavity_centroid_x':('cavity',.10,'area-weighted cavity centroid relative width; absent if no cavity'),
 'cavity_centroid_y':('cavity',.10,'area-weighted cavity centroid relative height; absent if no cavity'),
 'cavity_upper_count':('cavity',0,'significant cavity centroids above parent mid-height'),
 'cavity_lower_count':('cavity',0,'significant cavity centroids at/below parent mid-height'),
 'skeleton_endpoint_count':('graph',0,'skeleton endpoint pixels; nuisance-sensitive, not stroke ends'),
 'skeleton_branch_cluster_count':('graph',0,'connected clusters of skeleton pixels with>=3 neighbors'),
 'horizontal_run_fraction':('run',.12,'longest horizontal contiguous ink run/envelope width'),
 'vertical_run_fraction':('run',.12,'longest vertical contiguous ink run/envelope height')}
for i in range(3):
    DEFS[f'ink_row_band_{i}']=('distribution',.10,'fraction of ink in vertical third'+str(i))
    DEFS[f'ink_col_band_{i}']=('distribution',.10,'fraction of ink in horizontal third'+str(i))
for y in range(3):
    for x in range(3):DEFS[f'ink_grid_{y}{x}']=('distribution',.08,'fraction of ink in3x3 cell, top-left origin')

def now():return datetime.now(timezone.utc).isoformat()
def guard():
    if (D/'EVIDENCE_SEAL.json').exists():raise RuntimeError('Feature trial sealed; new trial required')
def verify():
    for p,digest in read_json(D/'PLAN.json')['dependencies'].items():assert sha256(OUT/p)==digest,p
def register():
    guard()
    if (D/'PLAN.json').exists():raise RuntimeError('Already registered')
    for p in [D,T,G]:p.mkdir(parents=True,exist_ok=True)
    dependencies={f'data/observations/visual_dataset_{v}/FREEZE_MANIFEST.json':sha256(OUT/f'data/observations/visual_dataset_{v}/FREEZE_MANIFEST.json') for v in ['v3','v4','v5','v6']}
    for p in [OLD/'discovery_parents.json',OLD/'fresh_source_reference.json',V6/'expanded_parent_assignments.json',OUT/'src/neutral_feature_trial_v1.py']:dependencies[p.relative_to(OUT).as_posix()]=sha256(p)
    write_json(D/'PLAN.json',dict(registered_at_utc=now(),question='Can confirmed-writing parents support reproducible neutral partial feature profiles without discrete class assignment?',dependencies=dependencies,features={k:dict(family=v[0],max_variant_range=v[1],definition=v[2]) for k,v in DEFS.items()},source='All638 V5 confirmed target parents plus66 V6 source-confirmed parents from three captions. Existing source/raster exposure; reused validation corpus, not globally fresh or independent adjudicators.',inputs='Native source masks and RGB, physical relative geometry only; old class labels used for reporting strata after measurement, never for defining features/tolerances or fitting.',variants=['native contrasts9/6/12 matched whole parents','native+0.04 and-0.04 slant without clipping, nearest raster interpolation','body proxy0.90 and1.10'],stability='Descriptor robust if full range over all variants<=fixed tolerance. Counts require exact agreement. Cavity centroids absent when no cavity; mixed presence is unknown. Output primary value and full range plus stable/unknown/not_applicable, never substitute a guessed value.',source_uncertainty='All contact and insufficient-photo states retained. A stable numeric descriptor cannot resolve source ownership or source parent ambiguity. Split/merge or IoU<0.5 across thresholds blocks a usable whole-parent profile but per-feature measurements remain diagnostic.',usable_profile='Source-resolved parent, matched whole-parent correspondence, >=8 stable applicable descriptors in>=3 families, requiring geometry+distribution+at least one of cavity/run/graph. Connectivity count alone cannot meet the third-family gate. Correlated descriptors are not independent evidence.',support_gates=dict(resolved_discovery_usable_min=.80,resolved_validation_usable_min=.80,each_validation_caption_usable_min=.70),statistics='Caption bootstrap, not iid parent CI. Contrast/slant robustness is operational repeatability, not independent source-feature annotation accuracy.',reproducibility='Deterministic re-execution required; no post-result feature/tolerance edits',prohibited=['new classes','V3/V4/V5/V6 retuning','EVA/RF/v101','Currier','global pixel-x or ordinal outcomes','sequence reconstruction','decipherment'],scope='Partial descriptor feasibility study, not V7 segmentation/model freeze or validated compositional writing alphabet.'))
    print('Registered34 neutral descriptors; tolerances fixed before measurements',flush=True)

def tight(mask):
    ys,xs=np.where(mask)
    if not len(xs):return None
    return mask[ys.min():ys.max()+1,xs.min():xs.max()+1]
def longest(mask):
    best=0
    for row in mask:
        d=np.diff(np.r_[0,row,0].astype(int));a=np.where(d==1)[0];b=np.where(d==-1)[0]
        if len(a):best=max(best,int((b-a).max()))
    return best
def describe(mask,body):
    mask=tight(mask)
    if mask is None:return {k:None for k in DEFS}
    h,w=mask.shape;yy,xx=np.where(mask);x=(xx+.5)/w;y=(yy+.5)/h;n=len(x);t=topology(mask.astype(bool),body);padded=np.pad(mask,1);nn,ll,st,cent=cv2.connectedComponentsWithStats(1-padded,8);cut=max(8,n*.012);holes=[i for i in range(2,nn) if st[i,4]>=cut];area=sum(int(st[i,4]) for i in holes)
    hc=np.array([cent[i]-1 for i in holes]);weights=np.array([st[i,4] for i in holes]);cx=float(np.average((hc[:,0]+.5)/w,weights=weights)) if holes else None;cy=float(np.average((hc[:,1]+.5)/h,weights=weights)) if holes else None
    f=dict(log_height_body=float(np.log(h/body)),log_width_body=float(np.log(w/body)),log_aspect=float(np.log(w/h)),ink_density=n/(h*w),ink_centroid_x=float(x.mean()),ink_centroid_y=float(y.mean()),ink_spread_x=float(x.std()),ink_spread_y=float(y.std()),raster_components=t['raster_components'],significant_cavity_count=len(holes),cavity_area_fraction=area/(h*w),cavity_centroid_x=cx,cavity_centroid_y=cy,cavity_upper_count=sum((hc[:,1]+.5)/h<.5) if holes else 0,cavity_lower_count=sum((hc[:,1]+.5)/h>=.5) if holes else 0,skeleton_endpoint_count=t['skeleton_endpoint_pixels'],skeleton_branch_cluster_count=t['skeleton_branch_clusters'],horizontal_run_fraction=longest(mask)/w,vertical_run_fraction=longest(mask.T)/h)
    for i in range(3):f[f'ink_row_band_{i}']=float(((y>=i/3)&(y<(i+1)/3)).mean());f[f'ink_col_band_{i}']=float(((x>=i/3)&(x<(i+1)/3)).mean())
    for a in range(3):
        for b in range(3):f[f'ink_grid_{a}{b}']=float(((y>=a/3)&(y<(a+1)/3)&(x>=b/3)&(x<(b+1)/3)).mean())
    return {k:float(v) if v is not None else None for k,v in f.items()}
def slant(mask,shear):
    padded=np.pad(mask,12);h,w=padded.shape;matrix=np.float32([[1,shear,-shear*h/2],[0,1,0]]);output=cv2.warpAffine(padded,matrix,(w,h),flags=cv2.INTER_NEAREST,borderValue=0)
    assert output.sum()>0
    return output
def profile(r,masks,state):
    body=r['body_proxy'];vals=[describe(m,body) for m in masks];vals.extend(describe(slant(masks[0],s),body) for s in [.04,-.04]);vals.extend(describe(masks[0],body*s) for s in [.9,1.1]);features={}
    for name,(family,tol,definition) in DEFS.items():
        values=[q[name] for q in vals];present=[v for v in values if v is not None]
        status='not_applicable' if not present else 'unknown_presence' if len(present)!=len(values) else 'stable' if max(present)-min(present)<=tol+1e-9 else 'unknown_variant_sensitive'
        features[name]=dict(primary=values[0],range=[min(present),max(present)] if present else None,status=status,family=family,values=values)
    stable=[k for k,v in features.items() if v['status']=='stable'];families={DEFS[k][0] for k in stable};correspond=all(q['iou']>=.5 and not(q['split'] or q['merge']) and q['connected_components']==1 for q in r['rasters'])
    source_resolved=state in ['source_resolved_existing_V3','source_confirmed_writing_V3_UNK','confirmed_connected_writing_trace'];usable=source_resolved and correspond and len(stable)>=8 and {'geometry','distribution'}.issubset(families) and bool(families.intersection({'cavity','run','graph'}))
    return dict(parent_id=r['parent_id'],caption=r['caption'],native_source=r['native_source'],native_bbox=r['native_bbox'],native_crop=r['native_crop'],source_state=state,source_resolved=source_resolved,old_class_reporting_only=r.get('structural_class','not_V5'),features=features,stable_descriptor_count=len(stable),stable_families=sorted(families),whole_parent_variant_correspondence=correspond,usable_partial_profile=usable,whole_parent_primary=True,components_are_measurements_not_writing_units=True)

def run():
    guard();verify();rec=read_json(OLD/'discovery_parents.json');fresh=[r for r in read_json(OLD/'fresh_source_reference.json')['parents'] if r['membership']=='confirmed_writing'];states={r['parent_id']:r['source_state'] for r in read_json(V6/'expanded_parent_assignments.json')};out=[];cacheview=None;cache=None
    for i,r in enumerate(rec+fresh):
        if cacheview!=r['native_source']:cache=page_features(r);cacheview=r['native_source']
        masks=variants(r,cache[2]);state=states[r['parent_id']] if i<len(rec) else r['source_parent_status'];out.append(profile(r,masks,state))
        if i%100==0:print('Feature profiles',i,'/',len(rec+fresh),flush=True)
    write_json(D/'parent_feature_profiles.json',dict(created_at_utc=now(),protocol_sha256=sha256(D/'PLAN.json'),variant_labels=read_json(D/'PLAN.json')['variants'],parents=out,training_or_class_assignment=False));summarize(out)

def summarize(rows):
    def stats(rr):
        resolved=[r for r in rr if r['source_resolved']];return dict(parents=len(rr),source_resolved=len(resolved),usable_profiles=sum(r['usable_partial_profile'] for r in rr),usable_among_resolved=sum(r['usable_partial_profile'] for r in resolved)/len(resolved) if resolved else None,corresponding_whole_parent=sum(r['whole_parent_variant_correspondence'] for r in rr),median_stable_descriptors=float(np.median([r['stable_descriptor_count'] for r in rr])),by_feature={k:dict(stable=sum(r['features'][k]['status']=='stable' for r in rr),unknown=sum(r['features'][k]['status'].startswith('unknown') for r in rr),not_applicable=sum(r['features'][k]['status']=='not_applicable' for r in rr)) for k in DEFS})
    trial=[r for r in rows if r['old_class_reporting_only']=='not_V5'];discovery=[r for r in rows if r not in trial];results=dict(discovery=stats(discovery),V5_existing_class=stats([r for r in discovery if r['old_class_reporting_only']!='UNK']),V5_UNK=stats([r for r in discovery if r['old_class_reporting_only']=='UNK']),validation=stats(trial));bycap={c:stats([r for r in trial if r['caption']==c]) for c in sorted({r['caption'] for r in trial})};plan=read_json(D/'PLAN.json');g=plan['support_gates'];gates=dict(discovery=results['discovery']['usable_among_resolved']>=g['resolved_discovery_usable_min'],validation=results['validation']['usable_among_resolved']>=g['resolved_validation_usable_min'],every_validation_caption=all(s['usable_among_resolved'] is not None and s['usable_among_resolved']>=g['each_validation_caption_usable_min'] for s in bycap.values()));confidence={};rng=np.random.default_rng(20261013)
    for label,rr in [('discovery',discovery),('validation',trial)]:
        caps=sorted({r['caption'] for r in rr});rates=[]
        for _ in range(2000):
            selected=[r for cap in rng.choice(caps,len(caps),replace=True) for r in rr if r['caption']==cap and r['source_resolved']]
            if selected:rates.append(sum(r['usable_partial_profile'] for r in selected)/len(selected))
        confidence[label]=dict(caption_clusters=len(caps),usable_resolved_bootstrap95=np.percentile(rates,[2.5,97.5]).tolist())
    write_json(T/'feature_repeatability.json',dict(created_at_utc=now(),strata=results,validation_captions=bycap,gates=gates,all_support_gates_pass=all(gates.values()),caption_intervals=confidence,interpretation='Robust numeric partial profiles only. Descriptor redundancy and deterministic masks are not independent annotation validation. A profile is not a compositional writing unit, a class, or an ordered sequence.'))
    print('Usable discovery',results['discovery']['usable_profiles'],'/',results['discovery']['source_resolved'],'UNK',results['V5_UNK']['usable_profiles'],'/',results['V5_UNK']['source_resolved'],'validation',results['validation']['usable_profiles'],'/',results['validation']['source_resolved'],'gates',gates,flush=True)

if __name__=='__main__':
    import sys
    {'register':register,'run':run}[sys.argv[1]]()
