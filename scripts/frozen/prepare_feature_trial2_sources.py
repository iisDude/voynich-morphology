from feature_trial2_common import *
from benchmark_membership_v5 import page_features
from prepare_structural_inventory_v6 import rasters
from PIL import Image,ImageDraw
import numpy as np,cv2

def export(rec,rgb,cc,mask):
    guard();sh,gg,meta=rasters(rgb,cc,mask,rec['native_bbox'],rec['body_proxy']);rec['rasters']=meta;rec['photo_raster_stable']=all(m['iou']>=.5 and not(m['split'] or m['merge']) and m['connected_components']==1 for m in meta) and len({m['holes'] for m in meta})==1
    x,y,c,d=rec['native_bbox'];a=max(0,x-12);b=max(0,y-12);e=min(rgb.shape[1],c+12);f=min(rgb.shape[0],d+12);p=G/'native_parents'/f'{rec["parent_id"]}.png';p.parent.mkdir(exist_ok=True);Image.fromarray(rgb[b:f,a:e]).save(p);rec['native_crop']=p.relative_to(OUT).as_posix();rec['crop_origin']=[a,b]
    q=D/'parent_masks'/f'{rec["parent_id"]}.png';q.parent.mkdir(exist_ok=True);Image.fromarray(mask*255).save(q);rec['mask_path']=q.relative_to(OUT).as_posix();return sh,gg

def gallery(records,name):
    guard()
    for start in range(0,len(records),24):
        rr=records[start:start+24];can=Image.new('RGB',(1440,((len(rr)+5)//6)*195),'#eee');dr=ImageDraw.Draw(can)
        for j,r in enumerate(rr):
            im=Image.open(OUT/r['native_crop']).convert('RGB');sc=min(3,225/im.width,140/im.height);im=im.resize((round(im.width*sc),round(im.height*sc)),Image.Resampling.NEAREST);x=j%6*240;y=j//6*195;can.paste(im,(x+5,y+22));a,b=r['crop_origin'];c,d,e,f=r['native_bbox'];dr.rectangle((x+5+(c-a)*sc,y+22+(d-b)*sc,x+5+(e-a)*sc,y+22+(f-b)*sc),outline='#b35',width=1);dr.text((x+4,y+4),r['audit_id']+' cap'+r['caption'],fill='black');dr.text((x+4,y+169),f'x{c}:{e} y{d}:{f}',fill='black')
        can.save(G/f'{name}_{start//24+1:02d}.png')

def prepare():
    guard();verify_dependencies();verify_seal(D/'SPECIFICATION_SEAL.json')
    if (D/'SOURCE_SEAL.json').exists():raise RuntimeError('Source inputs sealed')
    if (D/'source_location_aids.json').exists():raise RuntimeError('Source aids already prepared')
    raw=read_json(OLD/'discovery_parents.json')+read_json(OLD/'fresh_source_reference.json')['parents'];states={r['parent_id']:r['source_state'] for r in read_json(OUT/'data/observations/visual_dataset_v6/expanded_parent_assignments.json')};eligible=[]
    # Project source evidence only. V3 labels/nominal suggestions are not kept.
    for r in raw:
        ok=states.get(r['parent_id']) in ['source_resolved_existing_V3','source_confirmed_writing_V3_UNK'] if r['split']=='discovery' else r['membership']=='confirmed_writing' and r['source_parent_status']=='confirmed_connected_writing_trace'
        if ok:eligible.append({k:r[k] for k in ['parent_id','caption','native_source','native_bbox','body_proxy','mask_path']})
    rng=np.random.default_rng(20261015);chosen=[]
    for cap in sorted({r['caption'] for r in eligible}):
        rr=[r for r in eligible if r['caption']==cap];idx=rng.choice(len(rr),min(8,len(rr)),replace=False);chosen.extend(rr[int(i)] for i in idx)
    records=[];sh=[];gg=[];cacheview=None;cache=None
    for i,r in enumerate(chosen):
        rec=dict(r,corpus='reference',membership='confirmed_writing_from_sealed_source',source_parent_status='source_resolved_from_sealed_reference',audit_id=f'A{i+1:03d}')
        if cacheview!=r['native_source']:cache=page_features(r);cacheview=r['native_source']
        mask=(np.asarray(Image.open(OUT/r['mask_path']))>0).astype(np.uint8);ss,g=export(rec,cache[0],cache[2],mask);records.append(rec);sh.append(ss);gg.append(g)
    gallery(records,'reference_source')
    contexts=[];fresh=[]
    for field in read_json(D/'PLAN.json')['samples']['fresh_fields']:
        r=dict(field,body_proxy=field['body_height']);rgb,delta,cc=page_features(r);body=r['body_proxy'];kn=np.array(r['body_path_knots']);a,c=r['safe_x'];xx=np.arange(a,c);base=np.interp(xx,kn[:,0],kn[:,1]);yy=np.arange(rgb.shape[0])[:,None];band=(yy>=base[None,:]-.95*body)&(yy<=base[None,:]+.25*body);ids,cnt=np.unique(cc[0][1][:,a:c][band],return_counts=True);ps=[]
        for k,n in zip(ids,cnt):
            if not k or n<8 or cc[0][2][k,4]<35:continue
            x,y,w,h,area=map(int,cc[0][2][k]);mask=(cc[0][1][y:y+h,x:x+w]==k).astype(np.uint8);rec=dict(parent_id=f'T2_{r["view_id"]}_P{k:06d}',caption=r['caption'],view_id=r['view_id'],native_source=r['native_source'],native_bbox=[x,y,x+w,y+h],body_proxy=body,corpus='fresh',membership='unadjudicated',source_parent_status='unadjudicated',audit_id=f'N{len(fresh)+1:03d}',field_edge=x<a or x+w>c,source_core_pixels=int(n));ss,g=export(rec,rgb,cc,mask);records.append(rec);fresh.append(rec);ps.append(rec);sh.append(ss);gg.append(g)
        low=max(0,int(min(kn[:,1])-4*body));high=min(rgb.shape[0],int(max(kn[:,1])+1.8*body));left=max(0,a-100);right=min(rgb.shape[1],c+100);patch=Image.fromarray(rgb[low:high,left:right]);patch.save(G/f'{r["view_id"]}_source_context.png');contexts.append(dict(caption=r['caption'],view_id=r['view_id'],native_bbox=[left,low,right,high],parents=[p['audit_id'] for p in ps]));gallery(ps,r['view_id']+'_source');print(r['caption'],len(ps),'new source candidates',flush=True)
    save(D/'source_location_aids.json',dict(created_at_utc=now(),parents=records,reference_parents=len(chosen),fresh_proposals=len(fresh),no_V3_suggestions=True,source_attributes_pending=True));save(D/'fresh_source_contexts.json',contexts);np.savez_compressed(D/'source_shapes.npz',shapes=np.array(sh),geometry=np.array(gg));print('Source aids',len(chosen),'reference+',len(fresh),'fresh; no feature assignments',flush=True)
if __name__=='__main__':prepare()
