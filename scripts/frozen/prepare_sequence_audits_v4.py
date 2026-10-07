from common import OUT,read_json,write_json,sha256
from register_sequence_v4 import D,T
from prepare_sequence_source_v4 import G,sheet
from PIL import Image,ImageDraw
from collections import Counter,defaultdict
import numpy as np
def crop(r,pad=4):
    a,b,c,d=r['native_bbox'];return Image.open(OUT/r['native_source']).convert('RGB').crop((max(0,a-pad),max(0,b-pad),c+pad,d+pad))
def pair_sheets(pairs,name):
    for start in range(0,len(pairs),10):
        can=Image.new('RGB',(1400,1800),'white');dr=ImageDraw.Draw(can)
        for j,p in enumerate(pairs[start:start+10]):
            yy=j*180;dr.text((5,yy+4),p['id']+' source RGB, class hypothesis hidden',fill='black')
            for x,key in [(5,'left'),(705,'right')]:
                im=Image.open(OUT/p[key]);im=im.convert('RGB');scale=min(3.,675/im.width,145/im.height);im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.NEAREST);can.paste(im,(x,yy+28))
        can.save(G/f'{name}_{start+1:03d}.png')
def main():
    if (D/'class_pair_key.json').exists():raise RuntimeError('Prepared already')
    rec=read_json(D/'source_parents.json');lookup={r['parent_id']:r for r in rec};rows=read_json(D/'source_rows.json');rl={(r['view_id'],r['row_number']):r for r in rows};plan=read_json(D/'PLAN.json');rng=np.random.default_rng(plan['seed'])
    native=D/'audit_crops';native.mkdir(exist_ok=True)
    eligible=[r for r in rec if r['split']=='test' and r['structural_class'] and r.get('nearest_training_crop') and r.get('negative_training_crop')];rng.shuffle(eligible);chosen=[];counts=Counter()
    for r in eligible:
        cid=r['structural_class']
        if counts[cid]>=3:continue
        counts[cid]+=1;chosen.append(r)
        if len(chosen)==40:break
    pairs=[]
    for r in chosen:
        path=native/(r['parent_id']+'.png');crop(r).save(path)
        for kind,key in [('positive','nearest_training_crop'),('hard_negative','negative_training_crop')]:pairs.append(dict(kind=kind,parent_id=r['parent_id'],proposed_class=r['structural_class'],left=path.relative_to(OUT).as_posix(),right=r[key],folio_component=r['folio_component']))
    rng.shuffle(pairs)
    for i,p in enumerate(pairs):p['id']=f'C{i+1:03d}'
    pair_sheets(pairs,'class_pairs');write_json(D/'class_pair_key.json',pairs)
    repeatidx=rng.choice(len(pairs),min(12,len(pairs)),replace=False);rep=[]
    for j,i in enumerate(rng.permutation(repeatidx)):
        p=dict(pairs[i]);p['original_id']=p['id'];p['id']=f'R{j+1:03d}';rep.append(p)
    pair_sheets(rep,'class_repeat');write_json(D/'class_repeat_key.json',rep)
    byrow=defaultdict(list)
    for r in rec:
        if '_P' in r['parent_id'] and not r['small_detached_candidate'] and max(p['core_pixels'] for p in r['row_support'])>=8:byrow[(r['view_id'],r['row_number'])].append(r)
    boundary=[]
    for k in plan['review_repeatability']['sample']:
        rr=sorted(byrow[tuple(k)],key=lambda r:r['native_bbox'][0]);body=rl[tuple(k)]['body_height']
        if len(rr)<2:continue
        options=[(abs((b['native_bbox'][0]-a['native_bbox'][2])/body-.55),a,b) for a,b in zip(rr,rr[1:])];_,a,b=min(options,key=lambda t:(t[0],t[1]['native_bbox'][0]));x=(a['native_bbox'][2]+b['native_bbox'][0])/2;y=(max(a['native_bbox'][1],b['native_bbox'][1])+min(a['native_bbox'][3],b['native_bbox'][3]))/2
        row=rl[tuple(k)];box=[max(0,int(x-3*body)),max(0,int(y-1.8*body)),int(x+3*body),int(y+1.8*body)];im=Image.open(OUT/a['native_source']).convert('RGB').crop(box);dr=ImageDraw.Draw(im);dr.line([(x-box[0],0),(x-box[0],6)],fill='red',width=2);path=native/f'boundary_{len(boundary)+1:03d}.png';im.save(path)
        boundary.append(dict(view_id=k[0],row_number=k[1],parent_ids=[a['parent_id'],b['parent_id']],native_bbox=box,midpoint_x=x,native_crop=path.relative_to(OUT).as_posix()))
    bk=[]
    for passid in ['L','M']:
        tiles=[]
        for j,i in enumerate(rng.permutation(len(boundary))):
            r=boundary[i];ident=f'{passid}{j+1:03d}';tiles.append((ident+' inspect ink continuity below red midpoint tick',Image.open(OUT/r['native_crop']).resize((720,432),Image.Resampling.NEAREST)));bk.append(dict(id=ident,case_index=int(i),**r))
        for start in range(0,len(tiles),6):sheet(tiles[start:start+6],G/f'boundary_{passid}_{start+1:03d}.png',width=900)
    write_json(D/'boundary_repeat_key.json',bk)
    # Registered source-only priority queue. Class labels do not choose cases.
    queue=[];seen=set()
    for kind in ['oversize_compound_or_drawing','row_ownership','field_edge','detached_small_mark','faint_contrast6_only_region']:
        pool=sorted([r for r in rec if kind in r['unknown_reasons']],key=lambda r:(-r['area'],r['parent_id']));caps=set();n=0
        for r in pool:
            if r['view_id'] in caps or r['parent_id'] in seen:continue
            caps.add(r['view_id']);seen.add(r['parent_id']);n+=1;body=r['body_height_proxy'];a,b,c,d=r['native_bbox'];x=(a+c)/2;y=(b+d)/2
            box=[max(0,int(x-max(3*body,(c-a)/2+body))),max(0,int(y-max(1.8*body,(d-b)/2+body))),int(x+max(3*body,(c-a)/2+body)),int(y+max(1.8*body,(d-b)/2+body))]
            im=Image.open(OUT/r['native_source']).convert('RGB').crop(box);ImageDraw.Draw(im).rectangle([a-box[0],b-box[1],c-box[0],d-box[1]],outline='red',width=1);path=native/f'queue_{len(queue)+1:03d}.png';im.save(path)
            queue.append(dict(id=f'Q{len(queue)+1:03d}',parent_id=r['parent_id'],risk=kind,native_context_bbox=box,native_crop=path.relative_to(OUT).as_posix()))
            if n==12:break
    for start in range(0,len(queue),6):
        can=Image.new('RGB',(1800,1000),'white');dr=ImageDraw.Draw(can)
        for j,r in enumerate(queue[start:start+6]):
            im=Image.open(OUT/r['native_crop']);im.thumbnail((590,450));x=(j%3)*600;y=(j//3)*500;can.paste(im,(x,y+30));dr.text((x+4,y+4),r['id']+' red box: source membership only',fill='black')
        can.save(G/f'queue_{start+1:03d}.png')
    write_json(D/'membership_queue.json',queue)
    write_json(D/'AUDIT_SAMPLE_SEAL.json',dict(plan_sha256=sha256(D/'PLAN.json'),pair_key_sha256=sha256(D/'class_pair_key.json'),repeat_key_sha256=sha256(D/'class_repeat_key.json'),boundary_key_sha256=sha256(D/'boundary_repeat_key.json'),queue_sha256=sha256(D/'membership_queue.json'),prior_class_pair_and_local_boundary_judgments=None))
    print(len(pairs),'pairs',len(boundary),'boundary cases',len(queue),'source queue cases',flush=True)
if __name__=='__main__':main()
