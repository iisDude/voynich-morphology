from inventory_v6_common import *
from evaluate_source_classes_v3 import transform,assign
from scipy.spatial.distance import cdist
from PIL import Image,ImageDraw
from collections import defaultdict,Counter
import numpy as np,cv2,pickle

def whole_assign(sh,g):
    model=pickle.loads(MODEL.read_bytes());z=transform(sh,g,model);bundle=read_json(D/'sealed_candidate_model.json');embedding=np.load(D/'whole_candidate_embedding.npz')['z'];candidates=[c for c in bundle['whole_candidates'] if c['candidate_id'] in bundle['assignable_candidate_ids']];out=[]
    for i in range(len(z)):
        choices=[]
        for c in candidates:
            if g[i,4]!=c['holes']:continue
            dd=cdist(z[i:i+1],embedding[c['indices']])[0];order=np.argsort(dd);choices.append((float(dd[order[0]]),c,int(c['indices'][order[0]])))
        choices.sort(key=lambda q:q[0])
        if not choices:out.append(dict(candidate=None,accepted=False,nearest=None,distance=None));continue
        dist,c,near=choices[0];nextd=choices[1][0] if len(choices)>1 else float('inf');out.append(dict(candidate=c['candidate_id'],accepted=dist<=c['radius'] and nextd/max(dist,1e-8)>=1.08,nearest=near,distance=dist))
    return out

def inference(records,data):
    sh=data['shapes'];g=data['geometry'];base=whole_assign(sh[:,0],g[:,0]);low=whole_assign(sh[:,1],g[:,1]);high=whole_assign(sh[:,2],g[:,2]);shift=np.array([cv2.warpAffine(s,np.float32([[1,.04,-1],[0,1,1]]),(48,48),flags=cv2.INTER_LINEAR,borderValue=0) for s in sh[:,0]]);nuisance=whole_assign(shift,g[:,0]);model=pickle.loads(MODEL.read_bytes());v3=assign(transform(sh[:,0],g[:,0],model),g[:,0],model)
    # Preserve V5's frozen V3 perturbation procedure: recompute dimensions
    # only, keeping the primary feature vector for the remaining coordinates.
    v3variants=[]
    for j in [1,2]:
        vg=g[:,0].copy();vg[:,:3]=g[:,j,:3];v3variants.append(assign(transform(sh[:,j],vg,model),vg,model))
    v3nu=assign(transform(shift,g[:,0],model),g[:,0],model);out=[]
    for i,r in enumerate(records):
        cid=base[i]['candidate'];ts=bool(base[i]['accepted'] and all(q[i]['accepted'] and q[i]['candidate']==cid for q in [low,high]));ns=bool(base[i]['accepted'] and nuisance[i]['accepted'] and nuisance[i]['candidate']==cid)
        source_ok=(r.get('source_parent_status')=='confirmed_connected_writing_trace' if 'source_parent_status' in r else r.get('parent_boundary_status')=='confirmed_connected_trace' and r['diagnosis_stage']=='stable_source_structure_pending') and r['membership']=='confirmed_writing';geom=r['rasters'][0]['area']>=35 and r['rasters'][0]['connected_components']==1;stable=source_ok and r['photo_raster_stable'] and ts and ns and geom
        old=r.get('structural_class');nom=str(v3['classes'][i]);v3ok=bool(source_ok and r['photo_raster_stable'] and r['native_bbox'][3]-r['native_bbox'][1]>=.32*r['body_proxy'] and r['native_bbox'][3]-r['native_bbox'][1]<=3.8*r['body_proxy'] and r['native_bbox'][2]-r['native_bbox'][0]>=4 and v3['accepted'][i] and all(q['accepted'][i] and q['classes'][i]==nom for q in v3variants+[v3nu]) and nom!='ST09')
        out.append(dict(parent_id=r['parent_id'],caption=r['caption'],source_membership=r['membership'],source_resolved=source_ok,candidate=cid,nominal_candidate_accepted=base[i]['accepted'],threshold_class_stable=ts,alignment_class_stable=ns,source_raster_stable=r['photo_raster_stable'],stable_candidate=cid if stable and old in [None,'UNK'] else None,nearest_training_index=base[i]['nearest'],distance=base[i]['distance'],v3_class=old if old is not None else nom if v3ok else 'UNK',photo_parent_status=r.get('source_parent_status',r.get('parent_boundary_status'))))
    return out

def pair_gallery(pairs,rec):
    guard()
    lookup={r['parent_id']:r for r in rec};fresh={r['parent_id']:r for r in read_json(D/'fresh_source_reference.json')['parents']};lookup.update(fresh)
    for start in range(0,len(pairs),10):
        can=Image.new('RGB',(1250,1800),'#eee');dr=ImageDraw.Draw(can)
        for j,p in enumerate(pairs[start:start+10]):
            y=j*180;dr.text((5,y+3),p['pair_id']+' native RGB, suggestion hidden',fill='black')
            for x,key in [(5,'left'),(630,'right')]:
                r=lookup[p[key]];im=Image.open(OUT/r['native_crop']).convert('RGB');sc=min(3,600/im.width,145/im.height);im=im.resize((round(im.width*sc),round(im.height*sc)),Image.Resampling.NEAREST);can.paste(im,(x,y+25))
        can.save(G/f'heldout_pairs_{start//10+1:02d}.png')

def main():
    guard();verify_dependencies();verify_seal(D/'CANDIDATE_MODEL_SEAL.json');verify_seal(D/'FRESH_SOURCE_SEAL.json');rec=read_json(D/'fresh_source_reference.json')['parents'];data=np.load(D/'fresh_shapes.npz');result=inference(rec,data);save(D/'fresh_assignments.json',result);train=read_json(D/'discovery_parents.json');td=np.load(D/'discovery_shapes.npz');save(D/'discovery_candidate_assignments.json',inference(train,td));pairs=[];bundle=read_json(D/'sealed_candidate_model.json');rng=np.random.default_rng(20261011);g=data['geometry'][:,0];tg=td['geometry'][:,0];zz=np.load(D/'whole_candidate_embedding.npz')['z'];model=pickle.loads(MODEL.read_bytes());z=transform(data['shapes'][:,0],g,model)
    for c in bundle['whole_candidates']:
        if c['candidate_id'] not in bundle['assignable_candidate_ids']:continue
        positives=[i for i,r in enumerate(result) if r['source_resolved'] and r['candidate']==c['candidate_id'] and r['nominal_candidate_accepted']];pp=[]
        for i in positives:
            order=np.argsort(cdist(z[i:i+1],zz[c['indices']])[0])
            for j in order[:4]:pp.append(dict(kind='positive',candidate=c['candidate_id'],left=rec[i]['parent_id'],right=train[c['indices'][j]]['parent_id']))
        rng.shuffle(pp);pairs.extend(pp[:10]);neg=[]
        for i,r in enumerate(rec):
            if r['membership']!='confirmed_writing' or not result[i]['source_resolved']:continue
            pool=[j for j in range(len(train)) if tg[j,4]==g[i,4] and j not in c['indices']]
            order=np.argsort(cdist(z[i:i+1],zz[pool])[0])[:3] if pool else []
            for k in order:neg.append(dict(kind='negative',candidate=c['candidate_id'],left=r['parent_id'],right=train[pool[k]]['parent_id']))
        rng.shuffle(neg);pairs.extend(neg[:20])
    rng.shuffle(pairs)
    for i,p in enumerate(pairs):p['pair_id']=f'Q{i+1:03d}'
    save(D/'pair_audit_hidden_key.json',pairs);pair_gallery(pairs,train)
    counts=Counter(r['stable_candidate'] for r in result if r['source_membership']=='confirmed_writing');print('Fresh confirmed66, stable candidates',dict(counts),'native pair audit',len(pairs),flush=True)
if __name__=='__main__':main()
