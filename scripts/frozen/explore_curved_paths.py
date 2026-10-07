"""Reversible elliptical-coordinate proposals, isolated from horizontal assays."""
from common import OUT,read_json,read_csv,write_json
from visual_extract import ink_mask,detect_lines
from calibrate_assemblies import projection_spans
import numpy as np
import cv2
from PIL import Image,ImageDraw


def main():
    plan=read_json(OUT/'data/observations/curved_region_candidates.json')
    registrations={r['view_id']:r for r in read_json(OUT/'data/source/yale_registration_all.json')}
    folder=OUT/'data/observations/curved_path_candidates_v2';folder.mkdir(parents=True,exist_ok=True)
    audit=OUT/'figures/curved_path_audit_v2';audit.mkdir(parents=True,exist_ok=True)
    summary=[]
    for vid,boxes in plan['elliptical_boxes'].items():
        reg=registrations[vid];rgb=np.asarray(Image.open(OUT/reg['native_path']).convert('RGB'))
        h,w=rgb.shape[:2];config=read_json(OUT/'data/observations/visual_protocol_draft.json')
        config.update(background_gaussian_sigma_px=25,primary_ink_contrast=8)
        mask=ink_mask(rgb,config);paths=[]
        for ri,(a,b,c,d) in enumerate(boxes):
            cx=(a+c)*w/2;cy=(b+d)*h/2;rx=(c-a)*w/2;ry=(d-b)*h/2
            radial_scale=np.sqrt(rx*ry);angular_count=min(10000,max(720,round(2*np.pi*radial_scale)))
            radial_count=max(120,round(.85*radial_scale))
            # Clockwise tangent + inward radial y is orientation preserving.
            # Clockwise tangent + outward radial y would reflect local glyphs.
            rho=np.linspace(1.05,.20,radial_count,dtype=np.float32);theta=np.linspace(0,2*np.pi,angular_count,endpoint=False,dtype=np.float32)
            mx=(cx+rx*rho[:,None]*np.cos(theta)[None,:]).astype(np.float32);my=(cy+ry*rho[:,None]*np.sin(theta)[None,:]).astype(np.float32)
            polar=cv2.remap(mask,mx,my,cv2.INTER_NEAREST,borderMode=cv2.BORDER_CONSTANT)
            color=cv2.remap(rgb,mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
            pathconfig=dict(config);pathconfig.update(geometry_scale=1.,page_margin_fraction=0,component_area_px=[12,16000],component_height_px=[4,240],component_width_px=[2,600],baseline_vote_sigma_px=4,baseline_peak_min_distance_px=24,baseline_assignment_tolerance_px=12,minimum_line_width_px=150,minimum_line_component_count=6,line_horizontal_break_px=250,recovery_height_px=240,recovery_width_px=600,recovery_area_px=20000)
            lines,cc,labels=detect_lines(polar,pathconfig)
            record=dict(region_id=f'{vid}_ARC{ri+1:02d}',native_ellipse_center=[cx,cy],native_ellipse_radii=[rx,ry],rho_range=[1.05,.2],angular_samples=angular_count,radial_samples=radial_count,seam_radians=0,direction='increasing native image clockwise angle with inward radial y; logical direction unassigned',orientation_alternative='180-degree rotation gives counterclockwise tangent with outward radial y, without reflection',paths=[])
            for li,line in enumerate(lines):
                x0,y0,x1,y1=[line[k] for k in ('x0','y0','x1','y1')]
                assigned=np.isin(labels[y0:y1,x0:x1],line['component_labels']).astype(np.uint8)
                spans=projection_spans(assigned,max(2,round(.55*line['body_height'])))
                source_boxes=[]
                for ga,gb in spans:
                    yy,xx=np.where(assigned[:,ga:gb]);yy+=y0;xx+=x0+ga
                    if not len(xx):continue
                    sx=mx[yy,xx];sy=my[yy,xx]
                    source_boxes.append([float(sx.min()),float(sy.min()),float(sx.max()),float(sy.max())])
                record['paths'].append(dict(path_id=f'{record["region_id"]}_P{li+1:03d}',unwrapped_bbox=[x0,y0,x1,y1],angular_interval_radians=[x0/angular_count*2*np.pi,x1/angular_count*2*np.pi],native_source_group_bbox_candidates=source_boxes,body_height_unwrapped_proxy_px=line['body_height'],status='unreviewed curved-coordinate proposal',horizontal_position_eligible=False,pen_lift_evidence='unresolved',limitations=['Curve geometry approximate.','Unwrapped raster is an aid, not native physical stroke evidence.','Seam-spanning groups and radial labels unresolved.']))
            paths.append(record)
            preview=Image.fromarray(color)
            # Preview rescaling is for audit only, never measurement.
            preview.thumbnail((1600,600));preview.save(audit/f'{vid}_ARC{ri+1:02d}.png')
            preview.rotate(180).save(audit/f'{vid}_ARC{ri+1:02d}_orientation_alternative.png')
        write_json(folder/f'{vid}.json',dict(view_id=vid,image_sha256=reg['image_sha256'],native_source=reg['native_path'],regions=paths,status='unreviewed path hypotheses',unit_family_training_eligible=False))
        summary.append(dict(view_id=vid,ellipse_regions=len(paths),proposed_arc_paths=sum(len(r['paths']) for r in paths),status='needs source path audit',horizontal_assay_inclusion=False));print(summary[-1],flush=True)
    write_json(OUT/'reports/curved_path_processing_v2.json',summary)


if __name__=='__main__':main()
