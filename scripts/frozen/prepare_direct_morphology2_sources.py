from direct_morphology2_common import *
from benchmark_membership_v5 import page_features
from PIL import Image,ImageDraw
import numpy as np
def main():
    guard();verify();verify_seal(D/'SELECTION_SEAL.json');verify_seal(D/'SPECIFICATION_SEAL.json');assert not (D/'source_location_aids.json').exists();plan=read_json(D/'PLAN.json');fields=read_json(D/'SELECTED_FIELDS.json')['fields'];rng=np.random.default_rng(plan['seed']);records=[];contexts=[];(D/'parent_masks').mkdir(exist_ok=True);(G/'native_parents').mkdir(exist_ok=True)
    for cap in plan['caption_groups']:
        rr=[r for r in fields if r['caption']==cap];rgb,delta,cc=page_features(rr[0]);pool={}
        for field in rr:
            a,c=field['safe_x'];body=field['body_height'];kn=np.array(field['body_path_knots']);xx=np.arange(a,c);base=np.interp(xx,kn[:,0],kn[:,1]);yy=np.arange(rgb.shape[0])[:,None];band=(yy>=base[None,:]-.95*body)&(yy<=base[None,:]+.25*body);ids,cnt=np.unique(cc[0][1][:,a:c][band],return_counts=True)
            for k,n in zip(ids,cnt):
                if not k or n<8 or cc[0][2][k,4]<35:continue
                x,y,w,h,area=map(int,cc[0][2][k]);key=int(k)
                if key not in pool:pool[key]=dict(cc_label=key,caption=cap,view_id=field['view_id'],native_source=field['native_source'],native_bbox=[x,y,x+w,y+h],body_proxy=body,field_rows=[field['row_number']],field_edge=x<a or x+w>c,source_core_pixels=int(n))
                else:pool[key]['field_rows'].append(field['row_number'])
        candidates=list(pool.values());groups=[[r for r in candidates if min(r['field_rows'])==q['row_number']] for q in rr];selected=[];seen=set()
        for gg in groups:
            rng.shuffle(gg)
        while len(selected)<24 and any(groups):
            for gg in groups:
                if gg and len(selected)<24:
                    r=gg.pop();selected.append(r);seen.add(r['cc_label'])
        selected.sort(key=lambda r:(min(r['field_rows']),r['native_bbox'][0]))
        for r in selected:
            x,y,c,d=r['native_bbox'];mask=(cc[0][1][y:d,x:c]==r['cc_label']).astype(np.uint8);r.update(parent_id=f"DM2_{r['view_id']}_P{r['cc_label']:06d}",audit_id=f'S{len(records)+1:03d}',source_membership='unadjudicated',source_parent_status='unadjudicated');p=D/'parent_masks'/(r['parent_id']+'.png');Image.fromarray(mask*255).save(p);r['mask_path']=p.relative_to(OUT).as_posix();box=[max(0,x-12),max(0,y-12),min(rgb.shape[1],c+12),min(rgb.shape[0],d+12)];p=G/'native_parents'/(r['parent_id']+'.png');Image.fromarray(rgb[box[1]:box[3],box[0]:box[2]]).save(p);r['native_crop']=p.relative_to(OUT).as_posix();r['crop_origin']=box[:2];records.append(r)
        can=Image.new('RGB',(1440,4*230),'#eee');dr=ImageDraw.Draw(can)
        for j,r in enumerate(selected):
            x=j%6*240;y=j//6*230;im=Image.open(OUT/r['native_crop']).convert('RGB');sc=min(4,225/im.width,175/im.height);im=im.resize((max(1,round(im.width*sc)),max(1,round(im.height*sc))),Image.Resampling.NEAREST);can.paste(im,(x+5,y+25));a,b=r['crop_origin'];c,d,e,f=r['native_bbox'];dr.rectangle((x+5+(c-a)*sc,y+25+(d-b)*sc,x+5+(e-a)*sc,y+25+(f-b)*sc),outline='#b35');dr.text((x+5,y+4),r['audit_id']+' cap'+cap+' row'+str(r['field_rows']),fill='black');dr.text((x+4,y+204),f'x{c}:{e} y{d}:{f}',fill='black')
        can.save(G/f'source_cap{cap}.png');contexts.append(dict(caption=cap,primary_proposal_pool=len(pool),selected=len(selected),field_rows=[r['row_number'] for r in rr],no_contour_features_computed=True));print('Source proposal cap',cap,len(selected),'/',len(pool),flush=True)
    save(D/'source_location_aids.json',dict(prepared_at_utc=now(),parents=records,contexts=contexts,source_membership_pending=True,no_morphology_distances=True));print('192-or-fewer nativeRGB parent proposals; judgments pending',flush=True)
if __name__=='__main__':main()
