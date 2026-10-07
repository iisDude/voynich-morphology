"""Recover connected ink by source-adjudicated body ownership; never assay effects."""
from common import OUT,read_json,write_json,write_csv,sha256
from visual_extract import ink_mask
from calibrate_assemblies import topology,projection_spans
from regional_extract_v11 import normalise
from discover_visual_families import geom_feature
from PIL import Image,ImageDraw
import numpy as np
import cv2,joblib
from collections import Counter

def main():
    root=OUT/'data/observations/source_adjudication_v2'
    if (OUT/'data/observations/visual_dataset_v2/FREEZE_MANIFEST.json').exists():raise ValueError('v2 frozen; use a new version')
    judgments=read_json(root/'row_judgments.json');q=read_json(root/'queue_plan.json')
    if len(judgments)!=len(q['selected_rows']):raise ValueError('Whole-row queue incomplete')
    dest=root/'reconstructed_core';dest.mkdir(exist_ok=True);gallery=OUT/'figures/source_adjudication_v2/reconstructed_core';gallery.mkdir(parents=True,exist_ok=True)
    model=joblib.load(OUT/'data/observations/visual_family_models_v4/fine_components.joblib')
    reviews={r['cluster_index']:r for r in read_json(OUT/'data/observations/fine_family_source_review_v4.json')['records']}
    config=dict(read_json(OUT/'data/observations/visual_protocol_draft.json'),background_gaussian_sigma_px=25,primary_ink_contrast=6)
    summaries=[]
    for row in judgments:
        vid=row['view_id'];im=Image.open(OUT/row['native_source']).convert('RGB');w,h=im.size;body=row['body'];slope=row.get('seed_slope',0);xref=w/2
        # Process a broad native corridor so connected ascenders/descenders survive.
        x0,x1=row['x_extent'];y0=max(0,int(min([row['seed_y']]+row['other_rows'])-4*body));y1=min(h,int(max([row['seed_y']]+row['other_rows'])+2*body))
        rgb=np.asarray(im.crop((0,y0,w,y1)));blur=cv2.GaussianBlur(rgb,(0,0),.9);raw=ink_mask(blur,config);excluded=np.zeros(raw.shape,np.uint8);uncertain=np.zeros(raw.shape,np.uint8)
        for zones,target in [(row['exclude'],excluded),(row.get('uncertain_zones',[]),uncertain)]:
            for a,b,c,d in zones:target[max(0,b-y0):min(y1-y0,d-y0),max(0,a):min(w,c)]=1
        raw_before=raw.copy();raw[excluded>0]=0
        n,labels,stats,centers=cv2.connectedComponentsWithStats(raw,8)
        baselines=[row['seed_y']]+row['other_rows'];members=[];mask=np.zeros(raw.shape,np.uint8);unknown=np.zeros(raw.shape,np.uint8)
        for ci in range(1,n):
            xx,yy,cw,ch,area=map(int,stats[ci]);cx,cy=centers[ci];cy+=y0
            if area<25 or not x0<=cx<x1 or ch>8*body or cw>20*body:continue
            yy0=yy+y0;component=(labels[yy:yy+ch,xx:xx+cw]==ci).astype(np.uint8);py,px=np.nonzero(component);py=py+yy0;px=px+xx
            supports=[float(np.mean((py>=b+slope*(px-xref)-body)&(py<=b+slope*(px-xref)+.2*body))) for b in baselines]
            winner=int(np.argmax(supports));top=supports[0];rival=max(supports[1:],default=0.)
            # Detached traces near target are preserved as unknown, not assigned atomicity.
            target_center=row['seed_y']+slope*(cx-xref)-body/2
            detached=bool(winner!=0 and top==0 and abs(cy-target_center)<1.7*body and abs(cy-target_center)<min([abs(cy-(b+slope*(cx-xref)-body/2)) for b in row['other_rows']],default=1e9))
            if winner!=0 and top<.1 and not detached:continue
            if top<.1 and not detached:continue
            contact=rival>=.2 or winner!=0;zone=bool(np.any(uncertain[yy:yy+ch,xx:xx+cw]&component));small=area<40;clipped=xx<=x0 or xx+cw>=x1
            # Drawing cuts may sever connected writing; keep any adjacent object unknown.
            nearby=cv2.dilate(component,np.ones((5,5),np.uint8));draw_contact=bool(np.any(excluded[yy:yy+ch,xx:xx+cw]&nearby))
            status='unknown' if contact or zone or small or detached or clipped or draw_contact else 'writing_candidate'
            mask[yy:yy+ch,xx:xx+cw]|=component
            if status=='unknown':unknown[yy:yy+ch,xx:xx+cw]|=component
            features=topology(component,body);base=row['seed_y']+slope*(cx-xref)
            features.update(height_ratio=ch/body,width_ratio=cw/body,ink_area_body2=float(area/body**2),upper_extent_ratio=(base-yy0)/body,lower_extent_ratio=(yy0+ch-1-base)/body)
            members.append(dict(instance_id=f'{vid}_ADJ_CC{ci:05d}',bbox_xyxy=[xx,yy0,xx+cw,yy0+ch],features=features,status=status,ownership=dict(target_band_fraction=top,other_band_fraction=rival,detached=detached),source_local_label=ci,atlas_eligible=bool(area>=40 and ch/body>=.35 and cw/body>=.15),shape=normalise(component,body)))
        if members:
            images=np.stack([cv2.resize(r['shape'],(16,16),interpolation=cv2.INTER_AREA).ravel() for r in members]);z=np.c_[model['pca'].transform(images),model['geometry_scaler'].transform(geom_feature(members))*.35];pred=model['kmeans'].predict(z);dist=np.linalg.norm(z-model['kmeans'].cluster_centers_[pred],axis=1)
            for r,ci,dd in zip(members,pred,dist):
                ci=int(ci);review=reviews[ci];radius=model['distance_thresholds'][ci];admitted=bool(r['status']=='writing_candidate' and r['atlas_eligible'] and radius is not None and dd<=radius and model['training_folio_counts'][ci]>=3 and review['prototype_gate_eligible'])
                r.update(fine_family=f'VF_fine_components_K128_{ci+1:03d}' if admitted else None,broad_family=review.get('visual_structure_merge_hypothesis') if admitted else None,family_distance=float(dd),admitted=admitted);r.pop('shape')
        yy,xx=np.indices(mask.shape);baseline=row['seed_y']+slope*(xx-xref)
        core=mask*((yy+y0>=baseline-body)&(yy+y0<=baseline+.2*body))
        occupied=np.flatnonzero(core.any(axis=0));extent=[int(occupied.min()),int(occupied.max())+1] if len(occupied) else [x0,x1]
        spans=projection_spans(core,max(2,int(np.ceil(.55*body))));groups=[]
        for gi,(a,c) in enumerate(spans):
            mm=mask[:,a:c];ys,xs=np.where(mm);b=int(ys.min())+y0;d=int(ys.max())+y0+1
            parts=[r for r in members if np.any((labels[:,a:c]==r['source_local_label'])&(core[:,a:c]>0))];parts.sort(key=lambda r:(r['bbox_xyxy'][0],r['bbox_xyxy'][1]))
            for r in parts:
                touched=sum(np.any((labels[:,aa:cc]==r['source_local_label'])&(core[:,aa:cc]>0)) for aa,cc in spans)
                if touched>1:r['admitted']=False;r['fine_family']=None;r['broad_family']=None;r['status']='unknown';r['group_boundary_contact']='Connected parent supports multiple body-gap groups; no internal cut forced'
            known=bool(parts and all(r['admitted'] for r in parts));units=[r['fine_family'] for r in parts] if known else None;broad=[r['broad_family'] for r in parts] if known else None
            groups.append(dict(group_id=f'{vid}_ADJ_L001_G{gi+1:03d}',line_id=f'{vid}_ADJ_L001',view_id=vid,split=row['split'],folio_component=row['folio_component'],bbox_xyxy=[a,b,c,d],group_rank=gi,group_count=len(spans),normalized_group_rank=gi/(len(spans)-1) if len(spans)>1 else .5,source_pixel_center_x=(a+c)/2,normalized_pixel_center=((a+c)/2-extent[0])/max(1,extent[1]-extent[0]),line_x_extent_px=extent,member_ids=[r['instance_id'] for r in parts],visual_fine_units=units,visual_merged_units=broad,writing_membership='unknown' if any(r['status']=='unknown' for r in parts) else 'candidate awaiting recomposed source review',boundary_status='pending source gap review',section=None,hand=None,currier=None,conventional_mapping=None))
        # Native RGB, exact mask overlay and native coordinates of proposed gaps.
        crop_y0=max(y0,int(row['seed_y']-3*body));crop_y1=min(y1,int(row['seed_y']+1.5*body));crop=im.crop((max(0,x0-30),crop_y0,min(w,x1+30),crop_y1));origin_x=max(0,x0-30)
        arr=np.asarray(crop).copy();m=mask[crop_y0-y0:crop_y1-y0,origin_x:min(w,x1+30)].astype(bool);u=unknown[crop_y0-y0:crop_y1-y0,origin_x:min(w,x1+30)].astype(bool)
        arr[m]=(.6*arr[m]+.4*np.array([10,150,255])).astype(np.uint8);arr[u]=(.5*arr[u]+.5*np.array([255,60,160])).astype(np.uint8)
        scale=min(1.,2000/crop.width);height=round(crop.height*scale);width=round(crop.width*scale);canvas=Image.new('RGB',(width+20,2*height+95),'white');canvas.paste(crop.resize((width,height)),(10,45));canvas.paste(Image.fromarray(arr).resize((width,height)),(10,60+height));draw=ImageDraw.Draw(canvas);draw.text((10,5),vid+' adjudicated body; blue=assigned; magenta=unknown; all proposed groups numbered',fill='black')
        for gi,(a,c) in enumerate(spans):
            for off in [45,60+height]:
                xx=10+(a-origin_x)*scale;draw.line([xx,off,xx,off+height],fill='red',width=1);draw.text((xx+2,off+3),str(gi+1),fill='red')
        for tick in range((origin_x//100+1)*100,min(w,x1+30),100):
            tx=10+(tick-origin_x)*scale;draw.text((tx,2*height+77),str(tick),fill='black')
        canvas.save(gallery/(vid+'_membership.png'))
        obj=dict(view_id=vid,native_source=row['native_source'],source_sha256=sha256(OUT/row['native_source']),review=row,body_seed=row['seed_y'],body_height=body,source_crop=[0,y0,w,y1],writing_extent=extent,components=members,groups=groups,mask_config=config,status='source-corrected proposal awaiting exact-mask/gap review')
        write_json(dest/(vid+'.json'),obj);np.savez_compressed(dest/(vid+'_masks.npz'),assigned=mask,unknown=unknown,body_core=core,source_before_exclusions=raw_before,drawing_excluded=excluded)
        summaries.append(dict(view_id=vid,groups=len(groups),components=len(members),unknown_components=sum(r['status']=='unknown' for r in members),fully_admitted_groups=sum(bool(g['visual_fine_units']) for g in groups),prior_candidate_groups=row['groups']))
        print(vid,summaries[-1],flush=True)
    write_csv(root/'reconstruction_core_coverage.csv',summaries)
    write_json(root/'reconstruction_core_method.json',dict(source='manual native body seeds/other-body ownership and explicit drawing exclusions',contrast=6,preblur_sigma=.9,minimum_component_area=25,core_band=[-1,.2],rival_unknown_fraction=.2,detached='preserved unknown if nearest target and within 1.7 bodies',contact='Any target core support >=0.1 preserved even if another body wins; multirow ownership unknown',partitions='connected whole primary; existing source-family broad/factor alternatives; no skeleton cut promoted to primary',group_gap=.55,gap_measurement='target body core; whole connected parents retained; parents spanning gaps abstain, not cut',prototype='original frozen source-only image model transferred without refit',no_assay_statistics_inspected=True))

if __name__=='__main__':main()
