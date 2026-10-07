"""Native source rasters and atlas; no sequence reconstruction."""
from inventory_v6_common import *
from benchmark_membership_v5 import page_features
from regional_extract_v11 import normalise
from extract_recurrence_units_v3 import feature,holes
from PIL import Image,ImageDraw
from collections import Counter
import numpy as np,cv2

def rasters(rgb,cc,mask,bbox,body):
    x,y,c,d=bbox;pack=[];geo=[];meta=[];base_lab,base_st=cc[0][1:3];n=int(mask.sum())
    for vi in range(3):
        if vi==0:am=mask;box=bbox;info=dict(contrast=9,iou=1.,split=False,merge=False)
        else:
            al,st=cc[vi][1:3];ids,cnt=np.unique(al[y:d,x:c][mask>0],return_counts=True);valid=sorted([(int(i),int(k)) for i,k in zip(ids,cnt) if i],key=lambda z:-z[1])
            if not valid:am=mask;box=bbox;info=dict(contrast=[9,6,12][vi],iou=0.,split=True,merge=False)
            else:
                k,inter=valid[0];a,b,w,h,area=map(int,st[k]);am=(al[b:b+h,a:a+w]==k).astype(np.uint8);box=[a,b,a+w,b+h]
                ids2,cnt2=np.unique(base_lab[b:b+h,a:a+w][am>0],return_counts=True)
                info=dict(contrast=[9,6,12][vi],iou=float(inter/(n+area-inter)),split=sum(z>=n*.05 for i,z in valid)>1,merge=sum(i!=0 and base_st[i,4]>=35 and z>=base_st[i,4]*.2 for i,z in zip(ids2,cnt2))>1)
        info['split']=bool(info['split']);info['merge']=bool(info['merge'])
        info.update(native_bbox=box,holes=holes(am),connected_components=cv2.connectedComponents(am,8)[0]-1,area=int(am.sum()))
        pack.append(normalise(am,body));geo.append(feature(am,body));meta.append(info)
    return pack,geo,meta

def export_parent(rec,rgb,cc,mask):
    guard()
    x,y,c,d=rec['native_bbox'];body=rec['body_proxy'];sh,gg,meta=rasters(rgb,cc,mask,rec['native_bbox'],body)
    rec['rasters']=meta;rec['photo_raster_stable']=bool(all(m['iou']>=.5 and not(m['split'] or m['merge']) and m['connected_components']==1 for m in meta) and len({m['holes'] for m in meta})==1)
    crop=G/'native_parents'/f'{rec["parent_id"]}.png';crop.parent.mkdir(exist_ok=True)
    Image.fromarray(rgb[max(0,y-10):min(rgb.shape[0],d+10),max(0,x-10):min(rgb.shape[1],c+10)]).save(crop)
    maskpath=D/'parent_masks'/f'{rec["parent_id"]}.png';maskpath.parent.mkdir(exist_ok=True);Image.fromarray(mask*255).save(maskpath)
    rec['native_crop']=crop.relative_to(OUT).as_posix();rec['mask_path']=maskpath.relative_to(OUT).as_posix()
    return sh,gg

def gallery(records,name,cols=6,per=48):
    guard()
    for start in range(0,len(records),per):
        subset=records[start:start+per];can=Image.new('RGB',(cols*220,((len(subset)+cols-1)//cols)*185),'#eee');dr=ImageDraw.Draw(can)
        for j,r in enumerate(subset):
            x=(j%cols)*220;y=(j//cols)*185;im=Image.open(OUT/r['native_crop']).convert('RGB');sc=min(3,205/im.width,140/im.height);im=im.resize((max(1,round(im.width*sc)),max(1,round(im.height*sc))),Image.Resampling.NEAREST);can.paste(im,(x+5,y+20));dr.text((x+4,y+3),r['parent_id'],fill='black');dr.text((x+4,y+164),'cap'+r['caption']+' '+r.get('diagnosis_stage','source confirmation'),fill='black')
        can.save(G/f'{name}_{start//per+1:02d}.png')

def discovery():
    if (D/'DIAGNOSIS_SEAL.json').exists():raise RuntimeError('Discovery source inputs sealed')
    guard();verify_dependencies();rows=read_json(V5/'source_reference.json')['rows'];cr={r['row_id']:r for r in read_json(V5/'parent_class_assignments.json')['rows']};records=[];sh=[];gg=[];cache={}
    for row in rows:
        if row['view_id'] not in cache:cache[row['view_id']]=page_features(row)
        rgb,delta,cc=cache[row['view_id']];obj={p['object_id']:p for p in row['objects']}
        for p in cr[row['row_id']]['parents']:
            rec=dict(p,row_id=row['row_id'],caption=row['caption'],native_source=row['native_source'],membership='confirmed_writing',split='discovery');x,y,c,d=p['native_bbox'];mask=np.zeros((d-y,c-x),np.uint8)
            for oid in p['source_objects']:
                q=obj[oid]
                if q['raster']=='primary9':mask|=(cc[0][1][y:d,x:c]==q['cc_label']).astype(np.uint8)
            if not mask.any():raise ValueError('No primary source support')
            ss,g=export_parent(rec,rgb,cc,mask);sh.append(ss);gg.append(g)
            if p['structural_class']!='UNK':stage='existing_V3'
            elif p['parent_boundary_status']=='competing_join':stage='unresolved_parent_contact'
            elif cc[0][1][y:d,x:c].shape!=mask.shape or rec['rasters'][0]['connected_components']!=1 or mask.sum()<35:stage='insufficient_photo_or_disconnected'
            elif len({m['holes'] for m in rec['rasters']})>1 or any(m['split'] or m['merge'] for m in rec['rasters'][1:]):stage='topology_connectivity_instability'
            elif not rec['photo_raster_stable']:stage='threshold_coverage_instability'
            else:stage='stable_source_structure_pending'
            rec['diagnosis_stage']=stage;records.append(rec)
        print(row['row_id'],'exported',flush=True)
    save(D/'discovery_parents.json',records);np.savez_compressed(D/'discovery_shapes.npz',shapes=np.array(sh),geometry=np.array(gg));gallery([r for r in records if r['structural_class']=='UNK'],'unknown_source')
    counts=Counter(r['diagnosis_stage'] for r in records);save(T/'preclass_diagnosis.json',dict(created_at_utc=now(),exclusive_raster_source_categories=dict(counts),unknown_total=327,source_hypotheses_not_yet_classes=True,semantic_diagnosis_pending_native_RGB=True));print(dict(counts),flush=True)

def fresh():
    if (D/'FRESH_SOURCE_SEAL.json').exists():raise RuntimeError('Fresh source inputs sealed')
    guard();plan=read_json(D/'PLAN.json');rows=read_json(OUT/'data/observations/sequence_v4_development/source_rows.json');records=[];sh=[];gg=[];contexts=[]
    for view in plan['fresh_validation']['views']:
        r=next(q for q in rows if q['view_id']==view and q['status']=='triaged_local_writing_field');r=dict(r,body_proxy=r['body_height'],caption=r['folio_component']);rgb,delta,cc=page_features(r);body=r['body_proxy'];kn=np.array(r['body_path_knots']);xa,xb=r['safe_x'];xx=np.arange(xa,xb);base=np.interp(xx,kn[:,0],kn[:,1]);yy=np.arange(rgb.shape[0])[:,None];band=(yy>=base[None,:]-.95*body)&(yy<=base[None,:]+.25*body);ids,cnt=np.unique(cc[0][1][:,xa:xb][band],return_counts=True)
        ps=[]
        for k,n in zip(ids,cnt):
            if not k or n<8 or cc[0][2][k,4]<35:continue
            x,y,w,h,a=map(int,cc[0][2][k]);mask=(cc[0][1][y:y+h,x:x+w]==k).astype(np.uint8)
            rec=dict(parent_id=f'{view}_P{k:06d}',view_id=view,caption=r['caption'],native_source=r['native_source'],native_bbox=[x,y,x+w,y+h],body_proxy=body,split='fresh_validation',field_edge=x<xa or x+w>xb,source_field=[xa,xb],membership='unadjudicated',parent_boundary_status='unadjudicated',source_core_pixels=int(n))
            ss,g=export_parent(rec,rgb,cc,mask);sh.append(ss);gg.append(g);records.append(rec);ps.append(rec)
        y1=max(0,int(min(kn[:,1])-4*body));y2=min(rgb.shape[0],int(max(kn[:,1])+1.5*body));patch=Image.fromarray(rgb[y1:y2,max(0,xa-70):min(rgb.shape[1],xb+70)]);patch.save(G/f'{view}_fresh_context.png');contexts.append(dict(view_id=view,caption=r['caption'],native_source=r['native_source'],native_context_bbox=[max(0,xa-70),y1,min(rgb.shape[1],xb+70),y2],safe_x=[xa,xb],body_path=r['body_path_knots'],parents=len(ps)));gallery(ps,view+'_fresh_source');print(view,len(ps),'unadjudicated',flush=True)
    save(D/'fresh_parent_location_aids.json',records);save(D/'fresh_contexts.json',contexts);np.savez_compressed(D/'fresh_shapes.npz',shapes=np.array(sh),geometry=np.array(gg))

if __name__=='__main__':
    import sys
    discovery() if sys.argv[1]=='discovery' else fresh()
