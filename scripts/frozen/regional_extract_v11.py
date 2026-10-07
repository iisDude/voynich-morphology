"""v11 post-unblinding source-only repair. Frozen v4 remains unchanged.
See extraction_v11_protocol.json for prespecified changes and limitations.
"""
"""Multi-resolution writing-region paths and native raster segmentations.

Layout/localisation uses PDF pixels. Measurements and competing subdivisions
use registered native Yale pixels. Every result is a candidate, not a stroke,
letter, word, or accepted alphabet.
"""
from common import OUT,read_json,read_csv,write_json,write_csv,sha256
from visual_extract import ink_mask
from calibrate_assemblies import projection_spans,topology
import argparse
import numpy as np
import cv2
from PIL import Image,ImageDraw




def track_baseline(eligible,seed,body,pitch):
    from scipy.ndimage import gaussian_filter1d
    height,width=eligible.shape
    grid=np.arange(0,width,96,dtype=int);grid=np.unique(np.r_[grid,width-1])
    radius=max(18,round(.75*pitch));low=max(0,round(seed-radius));high=min(height,round(seed+radius)+1)
    ys=np.arange(low,high);scores=[]
    for x in grid:
        density=gaussian_filter1d(eligible[:,max(0,x-96):min(width,x+96)].sum(axis=1).astype(float),max(3,body*.15))
        density=density/(density.max()+1e-9)
        scores.append(density[ys]-.35*((ys-seed)/max(pitch*.65,1))**2)
    values=scores[0].copy();backs=[]
    shifts=np.arange(-18,19);penalty=.12*(shifts/9)**2
    for score in scores[1:]:
        candidates=np.full((len(shifts),len(ys)),-np.inf)
        for j,shift in enumerate(shifts):
            if shift>=0:candidates[j,shift:]=values[:len(ys)-shift]-penalty[j]
            else:candidates[j,:shift]=values[-shift:]-penalty[j]
        choice=np.argmax(candidates,axis=0);values=candidates[choice,np.arange(len(ys))]+score;backs.append(choice)
    index=int(np.argmax(values));indexes=[index]
    for back in reversed(backs):index-=int(shifts[back[index]]);indexes.append(index)
    centers=ys[np.array(indexes[::-1])]
    return grid.tolist(),(centers+.3*body).tolist()

def baseline_at(line,x):
    if 'native_track_x' in line:return np.interp(x,line['native_track_x'],line['native_track_y'])
    return line['native_baseline']+line['native_slope']*(x-line['native_xref'])


def detect_lines(mask,config):
    from scipy.ndimage import gaussian_filter1d
    from scipy.signal import find_peaks
    if config.get('geometry_scale')!=1.:return [],[],None
    n,labels,stats,centers=cv2.connectedComponentsWithStats(mask,8)
    candidates=[i for i in range(1,n) if stats[i,4]>=60 and 8<=stats[i,3]<=180 and 3<=stats[i,2]<=800]
    eligible=np.isin(labels,candidates)
    heights=[stats[i,3] for i in candidates if stats[i,3]<=80 and stats[i,4]>=100]
    body=float(np.percentile(heights,60)) if heights else 25.
    width=mask.shape[1];tiles=[]
    for x in range(0,width,64):
        # A dense patch cannot dominate the path vote simply through area.
        tiles.append(np.minimum(eligible[:,x:x+64].sum(axis=1),8))
    profile=gaussian_filter1d(np.sum(tiles,axis=0).astype(float),4)
    centered=profile-gaussian_filter1d(profile,40)
    ac=np.correlate(centered,centered,'full')[len(centered)-1:]
    possible,_=find_peaks(ac)
    possible=[p for p in possible if 20<=p<=150]
    pitch=int(max(possible,key=lambda p:ac[p])) if possible else 60
    minimum_distance=max(15,round(.65*pitch))
    peaks,_=find_peaks(profile,distance=minimum_distance,prominence=max(3,float(profile.max())*.12))
    paths=[]
    for peak in peaks:
        track_x,track_y=track_baseline(eligible,int(peak),body,pitch)
        baseline=float(np.interp(width/2,track_x,track_y))
        band=eligible[max(0,round(peak-body*.5)):min(mask.shape[0],round(peak+body*.5))]
        occupied=np.where(band.sum(axis=0)>=2)[0]
        if len(occupied)<100 or not candidates:continue
        x0=int(occupied.min());x1=int(occupied.max())+1
        if x1-x0<config['minimum_line_width_px']:continue
        count=sum(max(0,min(stats[i,1]+stats[i,3],baseline)-max(stats[i,1],baseline-body))>0 for i in candidates)
        if count<6:continue
        paths.append(dict(track_x=track_x,track_y=track_y,x0=x0,x1=x1,baseline=baseline,slope=0.,xref=width/2,body_height=body,component_count=count,
            path_peak_y=int(peak),density_profile_peak=float(profile[peak]),pitch_proxy_px=pitch,baseline_uncertainty='unestimated density-to-baseline offset; no glyph or transcription bottom used'))
    return paths,[],labels


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


def process(view,registration,version='v11'):
    vid=view['view_id'];folder=OUT/f'data/observations/regional_candidates_{version}';folder.mkdir(parents=True,exist_ok=True)
    pdf=np.asarray(Image.open(OUT/view['image_path']).convert('RGB'));h,w=pdf.shape[:2]
    config=read_json(OUT/'data/observations/visual_protocol_draft.json')
    pdfmask=ink_mask(pdf,config)
    rgb=np.asarray(Image.open(OUT/registration['native_path']).convert('RGB'));nh,nw=rgb.shape[:2]
    matrix=np.array(registration['pdf_to_native_matrix']);scale=np.sqrt(np.linalg.det(matrix[:2,:2]))
    nativeconfig=dict(config);nativeconfig['background_gaussian_sigma_px']=25 if version!='v1' else 12
    nativeconfig['primary_ink_contrast']=12 if version=='v11' else 8 if version!='v1' else 12
    nativeconfig['preblur_sigma_px']=1.2 if version=='v11' else 0.
    native_mask_path=OUT/f'data/observations/all_native_global_proposals/{vid}_mask.png'
    detection_rgb=cv2.GaussianBlur(rgb,(0,0),1.2) if version=='v11' else rgb
    native= (np.asarray(Image.open(native_mask_path))>0).astype(np.uint8) if version=='v1' and native_mask_path.exists() else ink_mask(detection_rgb,nativeconfig)
    all_lines=[];records=[];groups=[];shapes=[];native_bytes=[];native_offsets=[0];native_sizes=[];path_tiles=[];region_records=[]
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
        if version=='v11':
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
            if 'track_x' in line:
                line['native_track_x']=[v+nx0 for v in line['track_x']]
                line['native_track_y']=[v+ny0 for v in line['track_y']]
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
            if not kept:continue
            py,px=np.nonzero(labels[y-ny0:y-ny0+ch,x-nx0:x-nx0+cw]==ci)
            py=py+y;px=px+x
            supports=[];bottom_distances=[];ownership_scores=[]
            for line in kept:
                body=max(12.,line['native_body'])
                baseline=baseline_at(line,px)
                support=float(np.mean((py>=baseline-body)&(py<=baseline+.25*body)))
                bottom=float(abs(y+ch-1-baseline_at(line,cx))/body)
                supports.append(support);bottom_distances.append(bottom)
                ownership_scores.append(support-.25*min(bottom,4.))
            winner=int(np.argmax(ownership_scores));line=kept[winner];body=max(12.,line['native_body'])
            if supports[winner]<.12 or ch>5*body or cw>20*body:continue
            rival_support=max([s for i,s in enumerate(supports) if i!=winner],default=0.)
            memberships[winner].append(dict(label=ci,x0=x,y0=y,x1=x+cw,y1=y+ch,width=cw,height=ch,area=area,cx=float(cx),cy=float(cy),
                baseline_distance_body=float(bottom_distances[winner]),core_band_ink_fraction=float(supports[winner]),
                other_row_core_support_fraction=float(rival_support),multiline_contact=bool(rival_support>=.3)))
        region_records.append(dict(region_id=regionid,pdf_bbox=[rx0,ry0,rx1,ry1],native_bbox=[nx0,ny0,nx1,ny1],path_detection_frame=path_frame,path_proposal_count=len(proposed),retained_path_candidates=len(kept),quality='layout_reviewed; path and membership unreviewed'))
        for li,(line,members) in enumerate(zip(kept,memberships)):
            if len(members)<6:continue
            lineid=f'{regionid}_L{li+1:03d}';body=max(1.,line['native_body'])
            x0,x1=min(c['x0'] for c in members),max(c['x1'] for c in members);y0,y1=min(c['y0'] for c in members),max(c['y1'] for c in members)
            if x1-x0<3*body:continue
            if sum(c['area'] for c in members)/max(1,(x1-x0)*body)<.05:continue
            local=labels[y0-ny0:y1-ny0,x0-nx0:x1-nx0]
            assigned=np.isin(local,[c['label'] for c in members]).astype(np.uint8)
            line_record=dict(line_id=lineid,view_id=vid,region_id=regionid,bbox_xyxy=[x0,y0,x1,y1],coordinate_frame='native_yale_image',body_height_proxy_px=body,baseline_y_at_xref=line['native_baseline'],baseline_xref=line['native_xref'],baseline_slope=line['native_slope'],baseline_polyline_xy=list(zip(line['native_track_x'],line['native_track_y'])),membership_rule='maximum core-band ink fraction minus 0.25 bottom-distance/body; ambiguous row contacts retained',multiline_component_count=sum(c['multiline_contact'] for c in members),core_band_component_ink_fraction_mean=float(np.mean([c['core_band_ink_fraction'] for c in members])),component_count=len(members),segmentation_status='unreviewed candidate',groups_by_gap={},missing_ink_risk='Detached upper ink and descenders may be omitted; crossing drawings can be retained.')
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
                        features.update(height_ratio=(by1-by0)/body,width_ratio=(bx1-bx0)/body,ink_area_body2=float(cm.sum()/body**2),upper_extent_ratio=(baseline_at(line,(bx0+bx1)/2)-by0)/body,lower_extent_ratio=(by1-1-baseline_at(line,(bx0+bx1)/2))/body)
                        record=dict(instance_id=aid,group_id=groupid,line_id=lineid,view_id=vid,split=view['split'],folio_component=view['folio_component'],model=model,bbox_xyxy=[bx0,by0,bx1,by1],image_sha256=registration['image_sha256'],coordinate_frame='native_yale_image',body_height_proxy_px=body,features=features,tall_candidate=features['height_ratio']>=1.8,horizontal_connector_candidate=features['longest_horizontal_ink_run_px']>=.8*body,repetition_candidate=features['column_ink_ridge_count']>=3,pen_lift_evidence='unresolved',stroke_order='unresolved',unit_identity='unassigned',status='raster subdivision proposal',shape_index=len(shapes))
                        # Sparse or very small fragments remain records but cannot define atlas families.
                        record['atlas_eligible']=bool(cm.sum()>=40 and features['height_ratio']>=.35 and features['width_ratio']>=.15)
                        shapes.append(normalise(cm,body));packed=np.packbits(cm.reshape(-1),bitorder='little');native_bytes.append(packed);native_offsets.append(native_offsets[-1]+len(packed));native_sizes.append(cm.shape);records.append(record);grecord['models'][model].append(aid)
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
    np.savez_compressed(folder/f'{vid}_native_masks.npz',data=np.concatenate(native_bytes) if native_bytes else np.empty(0,np.uint8),offsets=np.array(native_offsets,np.int64),sizes=np.array(native_sizes,np.int32).reshape(-1,2))
    write_json(folder/f'{vid}.json',dict(view=view,native_source=registration['native_path'],image_sha256=registration['image_sha256'],native_mask_config=nativeconfig,regions=region_records,lines=all_lines,groups=groups,instances=records,status='unreviewed regional candidates',limitations=['Source masks threshold-sensitive.','Rows, group gaps and assemblies are reversible geometric proposals, not canonical units.','Detached upper ink, descenders, faint marks and crossings need manual alternatives.']))
    print(f'{vid}: {len(all_lines)} paths, {len(groups)} groups, {len(records)} subdivisions',flush=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--scope',choices=['pilot','all'],default='pilot');ap.add_argument('--view-id');ap.add_argument('--resume',action='store_true');ap.add_argument('--version',choices=['v11'],default='v11');args=ap.parse_args()
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
