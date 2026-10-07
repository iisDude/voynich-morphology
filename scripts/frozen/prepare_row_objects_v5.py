"""Native RGB object-location aids; no inherited strings or structural labels."""
from common import OUT,read_json,write_json
from register_row_benchmark_v5 import D,G
from visual_extract import ink_mask
from PIL import Image,ImageDraw
import numpy as np,cv2
from collections import Counter
from datetime import datetime,timezone

# Source-only provisional geometry from full native sweeps; reviewed again in
# object context. These are location aids, not frozen row truth.
GEOMETRY={
'B001':([410,2030],[[410,611],[1000,621],[1600,649],[2030,665]]),
'B002':([400,2030],[[400,755],[950,776],[1500,803],[2030,824]]),
'B005':([730,2770],[[730,524],[1300,547],[1900,540],[2400,534],[2770,514]]),
'B006':([720,2530],[[720,753],[1400,759],[2100,767],[2530,751]]),
'B007':([605,2510],[[605,460],[1000,440],[1700,434],[2510,445]]),
'B008':([625,2540],[[625,587],[1000,570],[1700,570],[2540,575]]),
'B009':([280,2250],[[280,491],[850,500],[1500,493],[2250,536]]),
'B010':([310,2300],[[310,683],[900,690],[1500,700],[2300,726]]),
'B011':([450,1880],[[450,875],[1000,883],[1450,877],[1880,885]]),
'B012':([440,1580],[[440,995],[900,1006],[1300,1030],[1580,1025]]),
'B015':([235,2310],[[235,268],[850,281],[1500,294],[2310,324]]),
'B016':([260,2300],[[260,593],[900,607],[1550,592],[2300,621]])}

def objects(r,geo):
    rgb=np.asarray(Image.open(OUT/r['native_source']).convert('RGB'));smooth=cv2.GaussianBlur(rgb,(0,0),.8)
    cfg=read_json(OUT/'data/observations/visual_protocol_draft.json');cfg['background_gaussian_sigma_px']=25
    masks=[ink_mask(smooth,cfg,c) for c in [9,6,12]];cc=[cv2.connectedComponentsWithStats(m,8) for m in masks]
    scope,knots=geo;body=r['body_proxy'];xx=np.arange(rgb.shape[1]);base=np.interp(xx,np.array(knots)[:,0],np.array(knots)[:,1]);yy=np.arange(rgb.shape[0])[:,None]
    band=(yy>=base[None,:]-1.8*body)&(yy<=base[None,:]+.65*body)&(xx[None,:]>=scope[0]-2*body)&(xx[None,:]<=scope[1]+2*body)
    result=[]
    for vi in [0,1]:
        _,lab,st,centers=cc[vi];ids,counts=np.unique(lab[band],return_counts=True)
        for k,n in zip(ids,counts):
            if not k or n<2 or st[k,4]<8:continue
            x,y,w,h,area=map(int,st[k]);lm=lab[y:y+h,x:x+w]==k
            if vi and np.any(cc[0][1][y:y+h,x:x+w][lm]>0):continue
            result.append(dict(raster='primary9' if vi==0 else 'low_only6',cc_label=int(k),native_bbox=[x,y,x+w,y+h],area=area,centroid=centers[k].tolist(),scope_support=int(n)))
    result.sort(key=lambda p:(p['centroid'][0],p['centroid'][1]))
    for i,p in enumerate(result):p['object_id']=f'{r["row_id"]}_O{i+1:03d}'
    return rgb,cc,result

def atlas(r,rgb,cc,result):
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen()
    # Individual source RGB + three masks locate threshold fragility without
    # suggesting ownership, membership, or V3 classes.
    for start in range(0,len(result),48):
        canvas=Image.new('RGB',(1440,8*210),'#eee');draw=ImageDraw.Draw(canvas)
        for j,p in enumerate(result[start:start+48]):
            x,y,c,d=p['native_bbox'];cx=(j%6)*240;cy=(j//6)*210
            a=max(0,x-12);b=max(0,y-12);e=min(rgb.shape[1],c+12);f=min(rgb.shape[0],d+12)
            patch=Image.fromarray(rgb[b:f,a:e]);scale=min(2,224/patch.width,132/patch.height)
            patch=patch.resize((max(1,round(patch.width*scale)),max(1,round(patch.height*scale))),Image.Resampling.NEAREST);canvas.paste(patch,(cx+8,cy+22))
            dr=ImageDraw.Draw(canvas);dr.rectangle((cx+8+(x-a)*scale,cy+22+(y-b)*scale,cx+8+(c-a)*scale,cy+22+(d-b)*scale),outline='#bd3b75',width=1)
            dr.text((cx+4,cy+3),p['object_id']+' '+p['raster'],fill='black');dr.text((cx+4,cy+157),f'x{x}:{c} y{y}:{d} A{p["area"]}',fill='black')
            for t,(n,lab,st,cent) in enumerate(cc):
                ma=(lab[y:d,x:c]>0).astype(np.uint8)*255;im=Image.fromarray(255-ma).convert('RGB');im.thumbnail((65,32));canvas.paste(im,(cx+5+t*77,cy+174));dr.text((cx+5+t*77,cy+198),str([9,6,12][t]),fill='black')
        canvas.save(G/f'{r["row_id"]}_objects_{start//48+1:02d}.png')

def compact(r,rgb,result):
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen()
    for name,ps in [('large',[p for p in result if p['area']>=35 or p['native_bbox'][3]-p['native_bbox'][1]>=10]),('small',[p for p in result if p['area']<35 and p['native_bbox'][3]-p['native_bbox'][1]<10])]:
        cw,ch,cols=(210,160,8) if name=='large' else (100,96,16)
        canvas=Image.new('RGB',(cw*cols,ch*max(1,(len(ps)+cols-1)//cols)),'#eee');dr=ImageDraw.Draw(canvas)
        for i,p in enumerate(ps):
            x,y,c,d=p['native_bbox'];cx=(i%cols)*cw;cy=(i//cols)*ch;a=max(0,x-9);b=max(0,y-9);e=min(rgb.shape[1],c+9);f=min(rgb.shape[0],d+9)
            im=Image.fromarray(rgb[b:f,a:e]);sc=min(2,(cw-10)/im.width,(ch-45)/im.height);im=im.resize((max(1,round(im.width*sc)),max(1,round(im.height*sc))),Image.Resampling.NEAREST);canvas.paste(im,(cx+4,cy+16));dr.rectangle((cx+4+(x-a)*sc,cy+16+(y-b)*sc,cx+4+(c-a)*sc,cy+16+(d-b)*sc),outline='#be2b66')
            dr.text((cx+3,cy+2),p['object_id'].split('_')[-1]+(' F' if p['raster']=='low_only6' else ''),fill='black');dr.text((cx+3,cy+ch-25),f'x{x} y{y}',fill='black');dr.text((cx+3,cy+ch-13),f'{c-x}x{d-y} A{p["area"]}',fill='black')
        canvas.save(G/f'{r["row_id"]}_{name}.png')

def locator(r,rgb,result):
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen()
    import math
    knots=r['provisional_body_path'];scope=r['provisional_scope'];body=r['body_proxy'];low=max(0,math.floor(min(y for x,y in knots)-3*body));high=min(rgb.shape[0],math.ceil(max(y for x,y in knots)+1.9*body))
    ps=[]
    for x in range(max(0,scope[0]-60),min(rgb.shape[1],scope[1]+80),500):
        right=min(rgb.shape[1],x+520);p=Image.fromarray(rgb[low:high,x:right]).resize(((right-x)*2,(high-low)*2),Image.Resampling.NEAREST);can=Image.new('RGB',(1100,p.height+35),'white');can.paste(p,(50,35));dr=ImageDraw.Draw(can)
        dr.text((50,4),f'{r["row_id"]} native x{x}:{right} y{low}:{high}; location labels only',fill='black')
        for y in range(int(math.ceil(low/25)*25),high,25):dr.text((0,35+(y-low)*2),str(y),fill='red');dr.line((45,35+(y-low)*2,52,35+(y-low)*2),fill='red')
        for ob in result:
            a,b,c,d=ob['native_bbox']
            if x<=ob['centroid'][0]<right and ob['area']>=35 and b<high and d>low:
                dr.text((50+(a-x)*2,35+(b-low)*2-12),ob['object_id'].split('_')[-1],fill='#ae0a72')
        ps.append(can)
    for i,p in enumerate(ps):p.save(G/f'{r["row_id"]}_locator_{i+1:02d}.png')

def prepare():
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen(source_stage=True)
    rows=read_json(D/'PLAN.json')['rows'];index=[]
    for r in rows:
        if r['row_id'] not in GEOMETRY:continue
        geo=GEOMETRY[r['row_id']];rgb,cc,result=objects(r,geo);atlas(r,rgb,cc,result);compact(r,rgb,result)
        index.append(dict(**r,provisional_scope=geo[0],provisional_body_path=geo[1],objects=result))
        print(r['row_id'],len(result),'primary',sum(p['raster']=='primary9' for p in result),flush=True)
    write_json(D/'development_object_location_aids.json',dict(created_at_utc=datetime.now(timezone.utc).isoformat(),status='Unadjudicated source-only object proposals',rows=index))

def main():
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen(source_stage=True)
    plan=read_json(D/'PLAN.json');cfg=read_json(OUT/'data/observations/visual_protocol_draft.json');cfg['background_gaussian_sigma_px']=25
    for r in plan['rows']:
        if r['split']!='development':continue
        rgb=np.asarray(Image.open(OUT/r['native_source']).convert('RGB'));smooth=cv2.GaussianBlur(rgb,(0,0),.8)
        mask=ink_mask(smooth,cfg,9);_,lab,st,centers=cv2.connectedComponentsWithStats(mask,8)
        anchor=r['source_anchor_y'];body=r['body_proxy'];lines=[]
        for a,b in [(350,850),(1100,1600),(1800,2400)]:
            points=[]
            for k in range(1,len(st)):
                x,y,w,h,area=map(int,st[k]);cx=centers[k,0]
                if area>=60 and .4*body<h<1.7*body and a<cx<b and anchor-100<y+h<anchor+100:points.append(round((y+h)/5)*5)
            lines.append(Counter(points).most_common(12))
        print(r['row_id'],lines,flush=True)
if __name__=='__main__':
    import sys
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen(source_stage=True)
    if '--compact' in sys.argv:
        for r in read_json(D/'development_object_location_aids.json')['rows']:
            rgb=np.asarray(Image.open(OUT/r['native_source']).convert('RGB'));compact(r,rgb,r['objects']);locator(r,rgb,r['objects'])
    else:prepare() if '--objects' in sys.argv else main()
