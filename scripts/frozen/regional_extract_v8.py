"""v8 post-unblinding source-only repair. Frozen v4 remains unchanged.
See extraction_v8_protocol.json for prespecified changes and limitations.
"""
"""Multi-resolution writing-region paths and native raster segmentations.

Layout/localisation uses PDF pixels. Measurements and competing subdivisions
use registered native Yale pixels. Every result is a candidate, not a stroke,
letter, word, or accepted alphabet.
"""
from common import OUT,read_json,read_csv,write_json,write_csv,sha256
from visual_extract import detect_lines
from calibrate_assemblies import projection_spans,topology
import argparse
import numpy as np
import cv2
from PIL import Image,ImageDraw



def ink_mask(rgb,config,contrast=None):
    gray=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY).astype(np.float32)
    response=np.zeros_like(gray)
    for sigma in (1.5,2.5):
        smoothed=cv2.GaussianBlur(gray,(0,0),sigma)
        dxx=cv2.Sobel(smoothed,cv2.CV_32F,2,0,ksize=3,scale=.25)*sigma*sigma
        dyy=cv2.Sobel(smoothed,cv2.CV_32F,0,2,ksize=3,scale=.25)*sigma*sigma
        dxy=cv2.Sobel(smoothed,cv2.CV_32F,1,1,ksize=3,scale=.25)*sigma*sigma
        radius=np.sqrt((dxx-dyy)**2+4*dxy*dxy)
        low=(dxx+dyy-radius)/2;high=(dxx+dyy+radius)/2
        value=np.maximum(high,0)*np.exp(-.5*(low/np.maximum(high,1e-4)/.5)**2)
        response=np.maximum(response,value)
    ridges=(response>=8).astype(np.uint8)
    paper=cv2.morphologyEx(gray,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(51,51)))
    dark=(paper-gray)>=8
    nearby=cv2.dilate(ridges,np.ones((5,5),np.uint8))>0
    r,g,b=[rgb[:,:,i].astype(np.int16) for i in range(3)]
    limits=config['color_limits']
    color=(r-g>=limits['r_minus_g_min'])&(r-g<=limits['r_minus_g_max'])&(b-r<=limits['b_minus_r_max'])
    return (dark&nearby&color).astype(np.uint8)


def boxes_for(view,pdf_width,pdf_height):
    exact=read_json(OUT/'data/observations/calibration_regions.json')['regions']
    fractional=read_json(OUT/'data/observations/layout_regions_fractional.json')['regions']
    if view in exact:return exact[view]
    return [[round(a*pdf_width),round(b*pdf_height),round(c*pdf_width),round(d*pdf_height)] for a,b,c,d in fractional[view]]


def normalise(mask,body):
    # Aspect-preserving shape sample; geometry stays in separate features.
    h,w=mask.shape;scale=44/max(h,w,1)
    resized=cv2.resize(mask.astype(np.float32),(max(1,round(w*scale)),max(1,round(h*scale))),interpolation=cv2.INTER_AREA)
    output=np.zeros((48,48),np.float32);y=(48-resized.shape[0])//2;x=(48-resized.shape[1])//2
    output[y:y+resized.shape[0],x:x+resized.shape[1]]=resized
    return output


def process(view,registration,version='v8'):
    vid=view['view_id'];folder=OUT/f'data/observations/regional_candidates_{version}';folder.mkdir(parents=True,exist_ok=True)
    pdf=np.asarray(Image.open(OUT/view['image_path']).convert('RGB'));h,w=pdf.shape[:2]
    config=read_json(OUT/'data/observations/visual_protocol_draft.json')
    pdfmask=ink_mask(pdf,config)
    rgb=np.asarray(Image.open(OUT/registration['native_path']).convert('RGB'));nh,nw=rgb.shape[:2]
    matrix=np.array(registration['pdf_to_native_matrix']);scale=np.sqrt(np.linalg.det(matrix[:2,:2]))
    nativeconfig=dict(config);nativeconfig['background_gaussian_sigma_px']=25 if version!='v1' else 12
    nativeconfig['primary_ink_contrast']=6 if version=='v8' else 8 if version!='v1' else 12
    nativeconfig['preblur_sigma_px']=1.2 if version=='v8' else 0.
    native_mask_path=OUT/f'data/observations/all_native_global_proposals/{vid}_mask.png'
    detection_rgb=cv2.GaussianBlur(rgb,(0,0),1.2) if version=='v8' else rgb
    native= (np.asarray(Image.open(native_mask_path))>0).astype(np.uint8) if version=='v1' and native_mask_path.exists() else ink_mask(detection_rgb,nativeconfig)
    all_lines=[];records=[];groups=[];shapes=[];path_tiles=[];region_records=[]
    for ri,(rx0,ry0,rx1,ry1) in enumerate(boxes_for(vid,w,h)):
        rx0,ry0=max(0,rx0),max(0,ry0);rx1,ry1=min(w,rx1),min(h,ry1)
        if rx1<=rx0 or ry1<=ry0:continue
        regionid=f'{vid}_R{ri+1:02d}'
        localconfig=dict(config);localconfig.update(page_margin_fraction=0,minimum_line_width_px=min(100,(rx1-rx0)*.4),minimum_line_component_count=6)
        proposed,_,_=detect_lines(pdfmask[ry0:ry1,rx0:rx1],localconfig)
        points=cv2.perspectiveTransform(np.array([[[rx0,ry0],[rx1,ry1]]],np.float32),matrix)[0]
        nx0,ny0=points[0].round().astype(int);nx1,ny1=points[1].round().astype(int)
        nx0,ny0=max(0,int(nx0)),max(0,int(ny0));nx1,ny1=min(nw,int(nx1)),min(nh,int(ny1))
        roi=native[ny0:ny1,nx0:nx1]
        n,labels,stats,centers=cv2.connectedComponentsWithStats(roi,connectivity=8)
        path_frame='native_embedded_image'
        if version=='v8':
            path_config=dict(config)
            path_config.update(geometry_scale=1.,page_margin_fraction=0,
                component_area_px=[60,16000],component_height_px=[8,240],component_width_px=[3,600],
                baseline_vote_sigma_px=4,baseline_peak_min_distance_px=40,baseline_assignment_tolerance_px=12,
                minimum_line_width_px=min(150,(nx1-nx0)*.4),minimum_line_component_count=6,
                line_horizontal_break_px=250,recovery_height_px=240,recovery_width_px=600,recovery_area_px=20000)
            proposed,_,_=detect_lines(roi,path_config)
            path_frame='native_yale_image'
        candidates=[]
        for line in proposed:
            if path_frame=='native_embedded_image':
                px=(line['x0']+line['x1'])/2+rx0
                py=line['baseline']+line['slope']*((line['x0']+line['x1'])/2-line['xref'])+ry0
                center=cv2.perspectiveTransform(np.array([[[px,py]]],np.float32),matrix)[0,0]
                path_body=line['body_height']*scale
            else:
                px=(line['x0']+line['x1'])/2+nx0
                py=line['baseline']+line['slope']*((line['x0']+line['x1'])/2-line['xref'])+ny0
                center=np.array([px,py]);path_body=line['body_height']
            line=dict(line,native_baseline=float(center[1]),native_xref=float(center[0]),native_body=float(path_body),native_slope=float(line['slope']),region_id=regionid)
            candidates.append(line)
        # Reject near-duplicate proposals only by geometry; keep ambiguity flags.
        kept=[]
        for line in sorted(candidates,key=lambda l:-l['component_count']):
            if any(abs(line['native_baseline']-other['native_baseline'])<.65*min(line['native_body'],other['native_body']) for other in kept):continue
            kept.append(line)
        kept.sort(key=lambda l:l['native_baseline'])
        memberships=[[] for l in kept]
        for ci in range(1,n):
            x,y,cw,ch,area=map(int,stats[ci]);cx,cy=centers[ci];x+=nx0;y+=ny0;cx+=nx0;cy+=ny0
            if area<60 or cw<3 or ch<8:continue
            distances=np.array([abs(y+ch-1-l['native_baseline']-l['native_slope']*(cx-l['native_xref']))/max(1,l['native_body']) for l in kept])
            if not len(distances):continue
            winner=int(distances.argmin());line=kept[winner];body=line['native_body']
            if distances[winner]>.65 or ch>3.5*body or cw>8*body:continue
            memberships[winner].append(dict(label=ci,x0=x,y0=y,x1=x+cw,y1=y+ch,width=cw,height=ch,area=area,cx=float(cx),cy=float(cy),baseline_distance_body=float(distances[winner])))
        region_records.append(dict(region_id=regionid,pdf_bbox=[rx0,ry0,rx1,ry1],native_bbox=[nx0,ny0,nx1,ny1],path_detection_frame=path_frame,path_proposal_count=len(proposed),retained_path_candidates=len(kept),quality='layout_reviewed; path and membership unreviewed'))
        for li,(line,members) in enumerate(zip(kept,memberships)):
            if len(members)<6:continue
            lineid=f'{regionid}_L{li+1:03d}';body=max(1.,line['native_body'])
            x0,x1=min(c['x0'] for c in members),max(c['x1'] for c in members);y0,y1=min(c['y0'] for c in members),max(c['y1'] for c in members)
            if x1-x0<3*body:continue
            local=labels[y0-ny0:y1-ny0,x0-nx0:x1-nx0]
            assigned=np.isin(local,[c['label'] for c in members]).astype(np.uint8)
            line_record=dict(line_id=lineid,view_id=vid,region_id=regionid,bbox_xyxy=[x0,y0,x1,y1],coordinate_frame='native_yale_image',body_height_proxy_px=body,baseline_y_at_xref=line['native_baseline'],baseline_xref=line['native_xref'],baseline_slope=line['native_slope'],membership_rule='raster-component lowest pixel within 0.65 local-body height of closest proposed baseline',component_count=len(members),segmentation_status='unreviewed candidate',groups_by_gap={},missing_ink_risk='Detached upper ink and descenders may be omitted; crossing drawings can be retained.')
            for ratio in config['group_gap_body_ratios']:
                line_record['groups_by_gap'][str(ratio)]=[[x0+a,x0+b] for a,b in projection_spans(assigned,max(2,int(np.ceil(ratio*body))))]
            all_lines.append(line_record)
            spans=projection_spans(assigned,max(2,int(np.ceil(config['primary_group_gap_body_ratio']*body))))
            for gi,(ga,gb) in enumerate(spans):
                groupid=f'{lineid}_G{gi+1:03d}';gm=assigned[:,ga:gb]
                ys,xs=np.where(gm)
                if not len(ys):continue
                gy0,gy1=int(ys.min()),int(ys.max())+1
                grecord=dict(group_id=groupid,line_id=lineid,view_id=vid,split=view['split'],folio_component=view['folio_component'],bbox_xyxy=[x0+ga,y0+gy0,x0+gb,y0+gy1],coordinate_frame='native_yale_image',group_rank=gi,group_count=len(spans),normalized_group_rank=gi/(len(spans)-1) if len(spans)>1 else .5,normalized_pixel_center=((ga+gb)/2)/(x1-x0),source_pixel_center_x=x0+(ga+gb)/2,source_pixel_center_y=y0+(gy0+gy1)/2,native_image_width_px=nw,native_image_height_px=nh,line_x_extent_px=[x0,x1],body_height_proxy_px=body,models={'fine_components':[],'medium_assemblies':[],'compound_candidates':[],'group_only':[]},status='space-gap candidate; not assumed word')
                for model,parts in [('fine_components',None),('medium_assemblies',projection_spans(gm,max(1,int(np.ceil(.1*body))))),('compound_candidates',projection_spans(gm,max(2,int(np.ceil(.25*body))))),('group_only',[(0,gb-ga)])]:
                    pieces=[]
                    if parts is None:
                        for c in members:
                            if x0+ga<=c['cx']<x0+gb:
                                bx0,by0,bx1,by1=[c[k] for k in ('x0','y0','x1','y1')]
                                cm=(labels[by0-ny0:by1-ny0,bx0-nx0:bx1-nx0]==c['label']).astype(np.uint8)
                                pieces.append((bx0,by0,bx1,by1,cm))
                    else:
                        for a,b in parts:
                            part=gm[:,a:b];ys,xs=np.where(part)
                            if not len(ys):continue
                            a0,a1=int(ys.min()),int(ys.max())+1
                            pieces.append((x0+ga+a,y0+a0,x0+ga+b,y0+a1,part[a0:a1]))
                    pieces.sort(key=lambda p: (p[0],p[1]))
                    for ai,(bx0,by0,bx1,by1,cm) in enumerate(pieces):
                        aid=f'{groupid}_{model[:1].upper()}{ai+1:03d}'
                        features=topology(cm,body)
                        features.update(height_ratio=(by1-by0)/body,width_ratio=(bx1-bx0)/body,ink_area_body2=float(cm.sum()/body**2),upper_extent_ratio=(line['native_baseline']+line['native_slope']*((bx0+bx1)/2-line['native_xref'])-by0)/body,lower_extent_ratio=(by1-1-line['native_baseline']-line['native_slope']*((bx0+bx1)/2-line['native_xref']))/body)
                        record=dict(instance_id=aid,group_id=groupid,line_id=lineid,view_id=vid,split=view['split'],folio_component=view['folio_component'],model=model,bbox_xyxy=[bx0,by0,bx1,by1],image_sha256=registration['image_sha256'],coordinate_frame='native_yale_image',body_height_proxy_px=body,features=features,tall_candidate=features['height_ratio']>=1.8,horizontal_connector_candidate=features['longest_horizontal_ink_run_px']>=.8*body,repetition_candidate=features['column_ink_ridge_count']>=3,pen_lift_evidence='unresolved',stroke_order='unresolved',unit_identity='unassigned',status='raster subdivision proposal',shape_index=len(shapes))
                        # Sparse or very small fragments remain records but cannot define atlas families.
                        record['atlas_eligible']=bool(cm.sum()>=40 and features['height_ratio']>=.35 and features['width_ratio']>=.15)
                        shapes.append(normalise(cm,body));records.append(record);grecord['models'][model].append(aid)
                groups.append(grecord)
            if True:
                patch=Image.fromarray(rgb[y0:y1,x0:x1]);patch.thumbnail((1260,180))
                binpatch=Image.fromarray((255-assigned*255).astype(np.uint8)).convert('RGB');binpatch.thumbnail((1260,180))
                tile=Image.new('RGB',(1280,patch.height+binpatch.height+35),'white');tile.paste(patch,(10,25));tile.paste(binpatch,(10,30+patch.height));ImageDraw.Draw(tile).text((10,5),f'{lineid} body_proxy={body:.1f}px unreviewed',fill='black');path_tiles.append(tile)
    if path_tiles:
        indexes=sorted(set(np.linspace(0,len(path_tiles)-1,min(4,len(path_tiles))).round().astype(int)))
        path_tiles=[path_tiles[i] for i in indexes]
        sheet=Image.new('RGB',(1280,sum(t.height for t in path_tiles)),'#ddd');yy=0
        for tile in path_tiles:sheet.paste(tile,(0,yy));yy+=tile.height
        audit=OUT/f'figures/regional_audit_{version}';audit.mkdir(parents=True,exist_ok=True);sheet.save(audit/f'{vid}.png')
    np.savez_compressed(folder/f'{vid}_shapes.npz',shapes=np.stack(shapes) if shapes else np.empty((0,48,48),np.float32))
    write_json(folder/f'{vid}.json',dict(view=view,native_source=registration['native_path'],image_sha256=registration['image_sha256'],native_mask_config=nativeconfig,regions=region_records,lines=all_lines,groups=groups,instances=records,status='unreviewed regional candidates',limitations=['Source masks threshold-sensitive.','Rows, group gaps and assemblies are reversible geometric proposals, not canonical units.','Detached upper ink, descenders, faint marks and crossings need manual alternatives.']))
    print(f'{vid}: {len(all_lines)} paths, {len(groups)} groups, {len(records)} subdivisions',flush=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--scope',choices=['pilot','all'],default='pilot');ap.add_argument('--view-id');ap.add_argument('--resume',action='store_true');ap.add_argument('--version',choices=['v8'],default='v8');args=ap.parse_args()
    rows=[r for r in read_csv(OUT/'data/source/all_view_manifest.csv') if r['split']!='excluded_cover']
    pilot={f"V_{int(r['pdf_page']):03d}" for r in read_csv(OUT/'data/source/sample_manifest.csv')}
    if args.scope=='pilot':rows=[r for r in rows if r['view_id'] in pilot]
    if args.view_id:rows=[r for r in rows if r['view_id']==args.view_id]
    registrations={r['view_id']:r for r in read_json(OUT/'data/source/yale_registration_all.json')}
    for row in rows:
        path=OUT/f'data/observations/regional_candidates_{args.version}/{row["view_id"]}.json'
        if args.resume and path.exists():continue
        process(row,registrations[row['view_id']],args.version)


if __name__=='__main__':main()
