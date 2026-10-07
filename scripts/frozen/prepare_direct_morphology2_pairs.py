from direct_morphology2_common import *
from PIL import Image,ImageDraw
from itertools import combinations
from collections import Counter
import numpy as np
def gallery(pairs,rec,name):
    for start in range(0,len(pairs),12):
        rr=pairs[start:start+12];can=Image.new('RGB',(1440,940),'#eee');dr=ImageDraw.Draw(can)
        for j,p in enumerate(rr):
            x=j%3*480;y=j//3*235;dr.text((x+5,y+4),p['pair_id'],fill='black')
            for side,i in enumerate(p['display_indices']):
                r=rec[i];im=Image.open(OUT/r['native_crop']).convert('RGB');scale=min(4,225/im.width,185/im.height);im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.NEAREST);xx=x+5+side*235;yy=y+27;can.paste(im,(xx,yy));a,b=r['crop_origin'];c,d,e,f=r['native_bbox'];dr.rectangle((xx+(c-a)*scale,yy+(d-b)*scale,xx+(e-a)*scale,yy+(f-b)*scale),outline='#b35')
        can.save(G/f'{name}_{start//12+1:02d}.png')
def main():
    guard();verify();verify_seal(D/'SOURCE_SEAL.json');assert not (D/'PAIR_POOL_SEAL.json').exists();plan=read_json(D/'PLAN.json');rec=read_json(D/'source_location_aids.json')['parents'];src={r['parent_id']:r for r in read_json(D/'source_decisions.json')['parents']};ids=[i for i,r in enumerate(rec) if src[r['parent_id']]['membership']=='confirmed_writing' and src[r['parent_id']]['source_extent_resolved']];caps=sorted({rec[i]['caption'] for i in ids},key=int);dyads=list(combinations(caps,2));rng=np.random.default_rng(plan['seed']);rng.shuffle(dyads);area=np.array([(r['native_bbox'][2]-r['native_bbox'][0])*(r['native_bbox'][3]-r['native_bbox'][1]) for r in rec]);asp=np.array([np.log((r['native_bbox'][2]-r['native_bbox'][0])/(r['native_bbox'][3]-r['native_bbox'][1])) for r in rec]);cuts=np.quantile(area[ids],[.25,.5,.75]);quartile=np.searchsorted(cuts,area,side='right');degree=Counter();used=set();pairs=[];short=[]
    for k in range(600):
        method='broad_random' if k%2==0 else 'aspect_matched';target=k//2%4;found=None
        for step in range(len(dyads)):
            a,b=dyads[(k//2+step)%len(dyads)];aa=[i for i in ids if rec[i]['caption']==a and degree[i]<12];bb=[j for j in ids if rec[j]['caption']==b and degree[j]<12];choices=[(i,j) for i in aa for j in bb if (i,j) not in used and (method=='broad_random' or abs(asp[i]-asp[j])<=.35)];stratum=[p for p in choices if quartile[p[0]]==target]
            if choices:found=(stratum or choices)[int(rng.integers(len(stratum or choices)))];break
        if found is None:short.append(dict(slot=k,method=method));continue
        i,j=found;used.add((i,j));degree[i]+=1;degree[j]+=1;p=dict(pair_id=f'Q{len(pairs)+1:03d}',left_index=i,right_index=j,display_indices=[i,j] if rng.random()<.5 else [j,i],caption_left=rec[i]['caption'],caption_right=rec[j]['caption'],sampling_method=method,area_quartile_left=int(quartile[i]),native_aspect_difference=float(abs(asp[i]-asp[j])));pairs.append(p)
    save(D/'PAIR_PROTOCOL.json',dict(sealed_before_source_similarity=True,protocol=plan['pair_sampling'],pool_n=len(pairs),eligible_parent_n=len(ids),caption_groups=caps,degree_limit=12,actual_max_degree=max(degree.values()),sampling_method_counts=dict(Counter(r['sampling_method'] for r in pairs)),unfilled_slots=short,source_unknowns_excluded_from_primary_pool_but_retained_in_representation=True,contour_distances_not_used=True));save(D/'pair_pool_hidden_key.json',dict(prepared_at_utc=now(),pairs=pairs,eligible_parent_indices=ids,source_parent_ids=[r['parent_id'] for r in rec]));gallery(pairs,rec,'blind_pairs');save(D/'OPENED_PAIRS.json',dict(initial_n=min(240,len(pairs)),used_n=min(240,len(pairs)),extensions=[],prediction_metrics_unopened=True));seal([D/'PAIR_PROTOCOL.json',D/'pair_pool_hidden_key.json',OUT/'src/prepare_direct_morphology2_pairs.py']+list(G.glob('blind_pairs_*.png')),D/'PAIR_POOL_SEAL.json');print('Blind deterministic pool',len(pairs),'initial opened',min(240,len(pairs)),'from',len(ids),'resolved parents; no contour selection',flush=True)
if __name__=='__main__':main()
