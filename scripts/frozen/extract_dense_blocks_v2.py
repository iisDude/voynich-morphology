"""Image-only body-path proposal in source-inspected writing blocks."""
from common import OUT,read_json,write_json,write_csv,sha256
from visual_extract import ink_mask
from calibrate_assemblies import topology,projection_spans
from regional_extract_v11 import normalise
from discover_visual_families import geom_feature
from PIL import Image,ImageDraw
import numpy as np,cv2,joblib
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks

# Coordinates from the native overview. Outside these blocks is unreviewed,
# including marginal signs and short writing fields among illustrations.
BLOCKS={
 'V_196':[[300,200,2270,3320]],'V_138':[[325,350,2360,3010]],
 'V_195':[[585,205,2485,3290]],'V_144':[[450,330,2140,3040]],
 'V_084':[[430,600,1590,1120],[430,1130,1810,1900],[465,1990,1850,2785]],
 'V_190':[[330,205,2410,3290]],
 'V_152':[[425,340,2320,1840],[1280,1820,2300,3230]],
 'V_202':[[230,180,2250,3140]],
}

def classify(members,shapes,model,reviews):
    if not members:return
    images=np.stack([cv2.resize(s,(16,16),interpolation=cv2.INTER_AREA).ravel() for s in shapes]);z=np.c_[model['pca'].transform(images),model['geometry_scaler'].transform(geom_feature(members))*.35];pred=model['kmeans'].predict(z);dist=np.linalg.norm(z-model['kmeans'].cluster_centers_[pred],axis=1)
    for r,ci,dd in zip(members,pred,dist):
        ci=int(ci);rev=reviews[ci];radius=model['distance_thresholds'][ci];admitted=bool(r['status']=='writing_candidate' and r['atlas_eligible'] and radius is not None and dd<=radius and model['training_folio_counts'][ci]>=3 and rev['prototype_gate_eligible'])
        r.update(admitted=admitted,fine_family=f'VF_fine_components_K128_{ci+1:03d}' if admitted else None,broad_family=rev.get('visual_structure_merge_hypothesis') if admitted else None,family_distance=float(dd))

def main():
    root=OUT/'data/observations/source_adjudication_v2/dense_blocks';plan=read_json(root/'selection.json');dest=root/'proposals';dest.mkdir(exist_ok=True);gallery=OUT/'figures/source_adjudication_v2/dense_blocks';model=joblib.load(OUT/'data/observations/visual_family_models_v4/fine_components.joblib');reviews={r['cluster_index']:r for r in read_json(OUT/'data/observations/fine_family_source_review_v4.json')['records']};cfg=dict(read_json(OUT/'data/observations/visual_protocol_draft.json'),background_gaussian_sigma_px=25,primary_ink_contrast=6);summary=[]
    if (OUT/'data/observations/visual_dataset_v2/FREEZE_MANIFEST.json').exists():raise ValueError('frozen')
    for src in plan['selected']:
        vid=src['view_id'];im=Image.open(OUT/src['native_source']).convert('RGB');components=[];lines=[];groups=[]
        for bi,(x0,y0,x1,y1) in enumerate(BLOCKS[vid]):
            rgb=np.asarray(im.crop((x0,y0,x1,y1)));mask=ink_mask(cv2.GaussianBlur(rgb,(0,0),.9),cfg);n,labels,stats,centers=cv2.connectedComponentsWithStats(mask,8);bodymask=np.zeros_like(mask);body=28.
            for ci in range(1,n):
                a,b,w,h,area=map(int,stats[ci]);
                if area>=25 and 8<=h<=50 and w<=150:bodymask[b:b+h,a:a+w]|=(labels[b:b+h,a:a+w]==ci)
            profile=gaussian_filter1d(bodymask.sum(axis=1).astype(float),4);peaks,_=find_peaks(profile,distance=38,prominence=max(4,float(profile.max())*.08),height=max(8,float(profile.max())*.12));xs=np.arange(150,mask.shape[1],300);xs=np.r_[0,xs,mask.shape[1]-1];paths=[]
            for peak in peaks:
                ys=[]
                for xx in xs:
                    a=max(0,int(xx)-150);c=min(mask.shape[1],int(xx)+150);prof=gaussian_filter1d(bodymask[:,a:c].sum(axis=1).astype(float),4);lo=max(0,peak-22);hi=min(mask.shape[0],peak+23);ys.append(float(lo+np.argmax(prof[lo:hi])+body*.5))
                paths.append(np.array(ys))
            if not paths:continue
            paths=np.stack(paths);members=[];shapes=[]
            for ci in range(1,n):
                a,b,w,h,area=map(int,stats[ci]);
                if area<25 or w>20*body or h>8*body:continue
                cm=(labels[b:b+h,a:a+w]==ci).astype(np.uint8);py,px=np.nonzero(cm);px=px+a;py=py+b;support=[]
                for path in paths:
                    base=np.interp(px,xs,path);support.append(float(np.mean((py>=base-body)&(py<=base+.2*body))))
                order=np.argsort(support)[::-1];owner=int(order[0]);top=support[owner];rival=support[order[1]] if len(order)>1 else 0.
                if top<.1:continue
                cx,cy=centers[ci];base=float(np.interp(cx,xs,paths[owner]));status='unknown' if rival>=.2 or area<40 or a<=1 or a+w>=mask.shape[1]-1 or b<=1 or b+h>=mask.shape[0]-1 else 'writing_candidate';features=topology(cm,body);features.update(height_ratio=h/body,width_ratio=w/body,ink_area_body2=area/body**2,upper_extent_ratio=(base-b)/body,lower_extent_ratio=(b+h-1-base)/body)
                r=dict(instance_id=f'{vid}_BLOCK{bi+1}_CC{ci:05d}',source_local_label=ci,block_id=bi+1,line_index=owner,bbox_xyxy=[a+x0,b+y0,a+x0+w,b+y0+h],features=features,status=status,ownership=dict(target_band_fraction=top,other_band_fraction=float(rival)),atlas_eligible=bool(area>=40 and h/body>=.35 and w/body>=.15));members.append(r);shapes.append(normalise(cm,body))
            classify(members,shapes,model,reviews);components.extend(members)
            yy,xx=np.indices(mask.shape)
            for li,path in enumerate(paths):
                lid=f'{vid}_BLOCK{bi+1}_L{li+1:03d}';parts=[r for r in members if r['line_index']==li];lm=np.zeros_like(mask)
                for r in parts:
                    ra,rb,rc,rd=r['bbox_xyxy'];ra-=x0;rc-=x0;rb-=y0;rd-=y0;lm[rb:rd,ra:rc]|=(labels[rb:rd,ra:rc]==r['source_local_label'])
                base=np.interp(np.arange(mask.shape[1]),xs,path)[None,:];core=lm*((yy>=base-body)&(yy<=base+.2*body));spans=projection_spans(core,16);ls=[]
                for gi,(a,c) in enumerate(spans):
                    pp=[r for r in parts if np.any((labels[:,a:c]==r['source_local_label'])&(core[:,a:c]>0))];pp.sort(key=lambda r:(r['bbox_xyxy'][0],r['bbox_xyxy'][1]));ls.append(dict(group_id=lid+f'_G{gi+1:03d}',line_id=lid,view_id=vid,split=src['split'],folio_component=src['folio_component'],member_ids=[r['instance_id'] for r in pp],body_gap_span_x=[a+x0,c+x0],boundary_status='pending native source review'))
                # Mark spanning connected parents unknown before deriving any group sequence.
                for r in parts:
                    touched=sum(r['instance_id'] in g['member_ids'] for g in ls)
                    if touched>1:r.update(admitted=False,fine_family=None,broad_family=None,status='unknown',group_boundary_contact='Whole connected assembly supports several body-gap slots; no internal cut')
                if not ls:continue
                occupied=np.flatnonzero(core.any(axis=0));extent=[int(occupied.min())+x0,int(occupied.max())+x0+1];lookup={r['instance_id']:r for r in parts}
                for gi,g in enumerate(ls):
                    pp=[lookup[i] for i in g['member_ids']];a,c=g['body_gap_span_x'];b=min([r['bbox_xyxy'][1] for r in pp],default=int(np.median(path)+y0-body));d=max([r['bbox_xyxy'][3] for r in pp],default=int(np.median(path)+y0));known=bool(pp and all(r['admitted'] for r in pp));g.update(bbox_xyxy=[a,b,c,d],group_rank=gi,group_count=len(ls),normalized_group_rank=gi/(len(ls)-1) if len(ls)>1 else .5,source_pixel_center_x=(a+c)/2,normalized_pixel_center=((a+c)/2-extent[0])/max(1,extent[1]-extent[0]),line_x_extent_px=extent,visual_fine_units=[r['fine_family'] for r in pp] if known else None,visual_merged_units=[r['broad_family'] for r in pp] if known else None,writing_membership='unknown' if any(r['status']=='unknown' for r in pp) else 'block writing candidate',section=None,hand=None,currier=None)
                groups.extend(ls);lines.append(dict(line_id=lid,block_id=bi+1,body_path_knots=[[float(x+x0),float(y+y0)] for x,y in zip(xs,path)],body_height=body,group_ids=[g['group_id'] for g in ls],line_x_extent_px=extent,status='pending source review'))
            np.savez_compressed(dest/f'{vid}_block{bi+1}_masks.npz',source_mask=mask,labels=labels,body_mask=bodymask,paths=paths,x_knots=xs,source_bbox=np.array([x0,y0,x1,y1]))
        obj=dict(**src,source_sha256=sha256(OUT/src['native_source']),source_blocks=BLOCKS[vid],components=components,lines=lines,groups=groups,mask_config=cfg,status='source proposal; no effect inspection');write_json(dest/(vid+'.json'),obj)
        # Four native strips, source RGB plus assigned colored connected components.
        cached_labels={bi+1:np.load(dest/f'{vid}_block{bi+1}_masks.npz')['labels'] for bi in range(len(BLOCKS[vid]))}
        for part in range(4):
            a=min(r[0] for r in BLOCKS[vid]);c=max(r[2] for r in BLOCKS[vid]);top=min(r[1] for r in BLOCKS[vid]);bottom=max(r[3] for r in BLOCKS[vid]);b=int(top+(bottom-top)*part/4);d=int(top+(bottom-top)*(part+1)/4);rgb=np.asarray(im.crop((a,b,c,d))).copy();over=rgb.copy()
            for r in components:
                if not b<=r['bbox_xyxy'][1]<d:continue
                bb=BLOCKS[vid][r['block_id']-1];lab=cached_labels[r['block_id']];xx,yy,ww,hh=r['bbox_xyxy'];l=max(a,xx);right=min(c,ww);up=max(b,yy);down=min(d,hh)
                if right<=l or down<=up:continue
                mm=lab[up-bb[1]:down-bb[1],l-bb[0]:right-bb[0]]==r['source_local_label'];patch=over[up-b:down-b,l-a:right-a];color=np.array([255,50,150]) if r['status']=='unknown' else np.array([30,150,255]);patch[mm]=(.5*patch[mm]+.5*color).astype(np.uint8)
            # Side-by-side source and overlay, unscaled; image viewer may downsample.
            canvas=Image.new('RGB',(c-a,2*(d-b)+50),'white');canvas.paste(Image.fromarray(rgb),(0,30));canvas.paste(Image.fromarray(over),(0,d-b+40));draw=ImageDraw.Draw(canvas);draw.text((5,5),vid+f' native block strip {part+1}; source then assigned/unknown overlay',fill='black')
            for line in lines:
                knots=line['body_path_knots'];my=np.median([v[1] for v in knots]);
                if b<=my<d:
                    draw.line([(x-a,y-b+30) for x,y in knots],fill='cyan',width=1);draw.text((0,int(my-b+30)),str(line['block_id'])+'_'+line['line_id'].split('_')[-1],fill='red')
                    for g in [g for g in groups if g['line_id']==line['line_id']]:
                        x=g['body_gap_span_x'][0]-a;draw.line([x,int(my-b-30)+30,x,int(my-b+10)+30],fill='red',width=1)
            canvas.save(gallery/f'{vid}_strip{part+1}.png')
        summary.append(dict(view_id=vid,lines=len(lines),groups=len(groups),components=len(components),admitted_groups=sum(bool(g['visual_fine_units']) for g in groups)));print(summary[-1],flush=True)
    write_csv(root/'coverage.csv',summary);write_json(root/'method.json',dict(source_blocks=BLOCKS,body_path='Low-height connected-ink projection peaks, then local native stripe peaks interpolated across x; no conventional transcription',frozen_parameters=dict(contrast=6,preblur=.9,body=28,low_height=[8,50],minimum_area=25,peak_distance=38,search_radius=22,group_gap=16,shared_contact=.2),limitations='Paths and exact masks require source inspection; complete field coverage is not presumed. Marginal/illustration-contained writing outside blocks remains unknown.',atlas='Original source-trained frozen prototypes; no refitting or effect optimization'))
if __name__=='__main__':main()
