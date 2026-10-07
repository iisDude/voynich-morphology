from feature_trial2_common import *
from neutral_feature_trial_v1 import describe,slant,tight
from measure_inventory_factors_v6 import variants
from benchmark_membership_v5 import page_features
from PIL import Image,ImageDraw
import numpy as np,cv2
from collections import defaultdict,Counter

def measure(r,masks,spec,source):
    body=r['body_proxy'];mm=masks+[slant(masks[0],a) for a in [.04,-.04]]+[masks[0],masks[0]];bb=[body]*5+[body*.9,body*1.1];vv=[]
    for m,b in zip(mm,bb):
        f=describe(m,b);tt=tight(m);f.update(log_height_native=float(np.log(tt.shape[0])) if tt is not None else None,log_width_native=float(np.log(tt.shape[1])) if tt is not None else None);vv.append(f)
    ff={}
    cavity_ok=source['source_cavity_count'] is not None and source['source_cavity_count']==vv[0]['significant_cavity_count']
    up=vv[0]['cavity_upper_count'];lo=vv[0]['cavity_lower_count'];place='both' if up and lo else 'upper' if up else 'lower' if lo else 'none'
    position_ok=cavity_ok and source['source_cavity_placement']==place
    for k,d in spec['features'].items():
        values=[v[k] for v in vv];present=[v for v in values if v is not None];extent=[min(present),max(present)] if present else None
        status='not_applicable' if not present else 'unknown_presence' if len(present)!=len(values) else 'stable' if extent[1]-extent[0]<=d['range_tolerance']+1e-9 else 'unknown_variant_sensitive'
        qualified=status
        if d['family']=='cavity':
            if not cavity_ok:qualified='unknown_source_cavity'
            elif k not in ['significant_cavity_count','cavity_area_fraction'] and not position_ok:qualified='unknown_source_placement'
        ff[k]=dict(primary=values[0],range=extent,values=values,raster_status=status,source_qualified_status=qualified,family=d['family'],core=d['core'])
    stable=[k for k in spec['core_features'] if ff[k]['source_qualified_status']=='stable'];families={ff[k]['family'] for k in stable}
    correspondence=all(z['iou']>=.5 and not(z['split'] or z['merge']) and z['connected_components']==1 for z in r['rasters']);resolved=source['membership']=='confirmed_writing' and source['source_parent_status']=='resolved_whole_parent'
    usable=resolved and correspondence and len(stable)>=8 and {'geometry','distribution'}<=families and bool(families&{'run','cavity'})
    return dict(parent_id=r['parent_id'],audit_id=r['audit_id'],caption=r['caption'],corpus=r['corpus'],membership=source['membership'],source_parent_status=source['source_parent_status'],source_resolved=resolved,whole_parent_correspondence=correspondence,usable_partial_profile=usable,stable_core_count=len(stable),stable_families=sorted(families),features=ff,source_cavity_compatible=cavity_ok,source_cavity_placement_compatible=position_ok,native_bbox=r['native_bbox'],native_source=r['native_source'])

def distances(rows,spec):
    n=len(rows);acc=np.zeros((n,n));nf=np.zeros((n,n));shared=np.zeros((n,n));present_fam={}
    for fam in ['geometry','distribution','run','cavity']:
        fs=[k for k in spec['core_features'] if spec['features'][k]['family']==fam];total=np.zeros((n,n));cnt=np.zeros((n,n))
        for k in fs:
            val=np.array([np.mean(r['features'][k]['range']) if r['features'][k]['source_qualified_status']=='stable' else np.nan for r in rows]);ok=np.isfinite(val);good=ok[:,None]&ok[None,:];den=spec['features'][k]['range_tolerance'] or 1;total+=np.where(good,np.minimum(3,np.abs(val[:,None]-val[None,:])/den),0);cnt+=good
        shared+=cnt;exist=cnt>0;present_fam[fam]=exist;acc+=np.divide(total,cnt,out=np.zeros_like(cnt),where=exist);nf+=exist
    dist=np.divide(acc,nf,out=np.full_like(acc,np.inf),where=nf>0)+.1*(1-shared/25)
    ok=(shared>=8)&present_fam['geometry']&present_fam['distribution']&(present_fam['run']|present_fam['cavity']);dist[~ok]=np.inf
    return dist,shared

def baselines(shapes,rows):
    # Frozen aspect-preserving normalized shapes;24px outline distances.
    small=np.array([cv2.resize(s,(24,24),interpolation=cv2.INTER_AREA)>.25 for s in shapes]);contours=[];maps=[]
    for s in small:
        edge=s&~cv2.erode(s.astype(np.uint8),np.ones((3,3),np.uint8)).astype(bool);contours.append(edge);maps.append(cv2.distanceTransform((~edge).astype(np.uint8),cv2.DIST_L2,3))
    n=len(rows);ch=np.zeros((n,n));asp=np.array([r['features']['log_aspect']['primary'] for r in rows]);ad=np.abs(asp[:,None]-asp[None,:])
    for i in range(n):
        for j in range(i+1,n):ch[i,j]=ch[j,i]=(float(maps[i][contours[j]].mean())+float(maps[j][contours[i]].mean()))/2
    ref=np.array([r['corpus']=='reference' for r in rows]);caps=np.array([r['caption'] for r in rows]);sel=ref[:,None]&ref[None,:]&(caps[:,None]!=caps[None,:]);scale=[float(np.percentile(m[sel],95)) for m in [ad,ch]];combo=.5*np.minimum(1,ad/scale[0])+.5*np.minimum(1,ch/scale[1]);return ad,ch,combo,scale

def galleries(pairs,records):
    for start in range(0,len(pairs),12):
        pp=pairs[start:start+12];can=Image.new('RGB',(1440,((len(pp)+2)//3)*235),'#eee');dr=ImageDraw.Draw(can)
        for j,p in enumerate(pp):
            x=j%3*480;y=j//3*235;dr.text((x+5,y+4),p['pair_id'],fill='black')
            for side,idx in enumerate(p['display_indices']):
                im=Image.open(OUT/records[idx]['native_crop']).convert('RGB');sc=min(3,225/im.width,195/im.height);im=im.resize((max(1,round(im.width*sc)),max(1,round(im.height*sc))),Image.Resampling.NEAREST);can.paste(im,(x+5+side*235,y+27))
        can.save(G/f'similarity_{start//12+1:02d}.png')

def main():
    guard();verify_dependencies();verify_seal(D/'SOURCE_SEAL.json');assert not (D/'METRIC_SEAL.json').exists();spec=read_json(D/'PLAN.json');rec=read_json(D/'source_location_aids.json')['parents'];sources={r['parent_id']:r for r in read_json(D/'source_decisions.json')['parents']};out=[];view=None;cache=None;native={}
    for i,r in enumerate(rec):
        if view!=r['native_source']:cache=page_features(r);view=r['native_source']
        masks=variants(r,cache[2]);native.update({f'{i}_{j}':m for j,m in enumerate(masks)});out.append(measure(r,masks,spec,sources[r['parent_id']]))
        if i%25==0:print('Trial2 features',i,'/',len(rec),flush=True)
    np.savez_compressed(D/'native_variants.npz',**native);save(D/'feature_profiles.json',dict(created_at_utc=now(),parents=out,protocol_sha256=sha256(D/'PLAN.json')))
    dist,shared=distances(out,spec);sh=np.load(D/'source_shapes.npz')['shapes'][:,0];asp,contour,combo,scale=baselines(sh,out);np.savez_compressed(D/'distances.npz',profile=dist,shared=shared,aspect=asp,contour=contour,combined=combo)
    rng=np.random.default_rng(spec['seed']);ref=np.array([i for i,r in enumerate(out) if r['corpus']=='reference' and r['source_resolved']]);pairs={};anchors=[]
    for cap in CAPTIONS:
        ids=[i for i,r in enumerate(out) if r['caption']==cap and r['corpus']=='fresh' and r['source_resolved']];chosen=rng.choice(ids,min(12,len(ids)),replace=False);anchors.extend(map(int,chosen))
        for i in chosen:
            eligible=ref[np.isfinite(dist[i,ref])];choices=[]
            if len(eligible):choices.append(('profile_nearest',int(eligible[np.argmin(dist[i,eligible])])) )
            choices.append(('contour_nearest',int(ref[np.argmin(contour[i,ref])])))
            match=ref[asp[i,ref]<=.35]
            if len(match):choices.append(('aspect_matched_random',int(rng.choice(match))))
            for method,j in choices:pairs.setdefault((int(i),j),[]).append(method)
    keys=list(pairs);rng.shuffle(keys);pp=[]
    for k,(i,j) in enumerate(keys):pp.append(dict(pair_id=f'Q{k+1:03d}',anchor_index=i,reference_index=j,display_indices=[i,j] if rng.random()<.5 else [j,i],selectors=pairs[(i,j)],caption=out[i]['caption'],profile_distance=float(dist[i,j]) if np.isfinite(dist[i,j]) else None,aspect_distance=float(asp[i,j]),contour_distance=float(contour[i,j]),combined_distance=float(combo[i,j])))
    save(D/'similarity_hidden_key.json',dict(pairs=pp,anchors=anchors,reference_baseline95_scales=scale,predictions_hidden_during_source_rating=True));galleries(pp,rec)
    save(T/'coverage_prelabels.json',dict(by_corpus={c:dict(proposals=sum(r['corpus']==c for r in out),confirmed=sum(r['corpus']==c and r['membership']=='confirmed_writing' for r in out),resolved=sum(r['corpus']==c and r['source_resolved'] for r in out),usable=sum(r['corpus']==c and r['usable_partial_profile'] for r in out)) for c in ['reference','fresh']},similarity_pairs=len(pp),fresh_anchors=len(anchors)))
    seal([D/'feature_profiles.json',D/'native_variants.npz',D/'distances.npz',D/'similarity_hidden_key.json',T/'coverage_prelabels.json',OUT/'src/measure_feature_trial2.py']+list(G.glob('similarity_*.png')),D/'METRIC_SEAL.json')
    print(read_json(T/'coverage_prelabels.json'),flush=True)
if __name__=='__main__':main()
