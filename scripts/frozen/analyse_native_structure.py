"""Geometry and competing internal cuts, using exact native candidate masks.

No inherited signs, positions, sections or hands determine the structures.
Skeleton endpoints and junctions are raster observations, not pen movements.
"""
from common import OUT, read_json, write_json, write_csv, sha256
import argparse
import numpy as np
import cv2
from scipy.signal import find_peaks
from skimage.morphology import skeletonize
from PIL import Image, ImageDraw


def unpack(data, index):
    a, b = data['offsets'][index:index+2]; h, w = data['sizes'][index]
    return np.unpackbits(data['data'][a:b], bitorder='little', count=int(h*w)).reshape(h,w).astype(np.uint8)


def measure(cm, body):
    h,w=cm.shape; sk=skeletonize(cm.astype(bool)).astype(np.uint8)
    # Hough fragments are evidence of approximately straight ink, not strokes.
    segments=cv2.HoughLinesP(sk,1,np.pi/180,threshold=max(6,round(body*.25)),
        minLineLength=max(6,round(body*.35)),maxLineGap=max(1,round(body*.08)))
    horizontal=[];vertical=[]
    if segments is not None:
        for a,b,c,d in segments[:,0]:
            dx,dy=int(c-a),int(d-b);angle=abs(np.degrees(np.arctan2(dy,dx)))%180
            if min(angle,180-angle)<=15:horizontal.append([int(a),int(b),int(c),int(d)])
            if abs(angle-90)<=20:vertical.append([int(a),int(b),int(c),int(d)])
    upper_bars=[s for s in horizontal if (s[1]+s[3])/2<h*.6 and abs(s[2]-s[0])>=.6*body]
    frames=[]
    for bar in upper_bars:
        xa,xb=sorted([bar[0],bar[2]]);yy=round((bar[1]+bar[3])/2)
        sides=[]
        for xx in (xa,xb):
            strip=sk[max(0,yy-2):min(h,yy+round(body)),max(0,xx-round(body*.15)):min(w,xx+round(body*.15)+1)]
            sides.append(int((strip.sum(axis=1)>0).sum()))
        if min(sides)>=.35*body:
            above=sk[:max(0,yy-2),xa:xb+1]
            frames.append(dict(bar=bar,downward_support_rows=sides,above_bar_ink_pixels=int(above.sum()),
                insertion_status='above-bar raster ink; insertion and stroke order unresolved' if above.sum() else 'no above-bar ink in assigned mask'))
    # Connected alternatives: cuts through few skeleton pixels can sever a ligature
    # or a single shape. Both hypotheses remain; no cut is accepted as graphemic.
    occupancy=sk.sum(axis=0).astype(float)
    smooth=cv2.GaussianBlur(occupancy.reshape(1,-1),(0,0),max(.6,body*.035)).ravel()
    valleys,_=find_peaks(-smooth,distance=max(2,round(body*.25)))
    cuts=[int(x) for x in valleys if x>=.3*body and w-x>=.3*body and occupancy[x]<=2
          and cm[:,x].sum()>0 and smooth[x]<np.percentile(smooth,50)]
    ridges,_=find_peaks(cm.sum(axis=0).astype(float),prominence=max(2,body*.12),distance=max(2,round(body*.15)))
    spacings=np.diff(ridges)/body
    repeated=len(spacings)>=2 and np.std(spacings)/max(np.mean(spacings),1e-6)<.4
    n0=cv2.connectedComponents(cm,connectivity=8)[0]-1
    eroded=cv2.erode(cm,np.ones((2,2),np.uint8))
    ne=cv2.connectedComponents(eroded,connectivity=8)[0]-1
    return dict(native_height_px=h,native_width_px=w,body_height_proxy_px=body,
        horizontal_segment_count=len(horizontal),vertical_segment_count=len(vertical),
        maximum_vertical_segment_body=max([abs(s[3]-s[1])/body for s in vertical] or [0.]),
        upper_bar_candidates=upper_bars,frame_candidates=frames,
        sparse_skeleton_cut_columns=cuts,cut_hypothesis='uncut connected assembly versus connected subdivisions at listed columns',
        ridge_columns=ridges.tolist(),ridge_spacings_body=spacings.tolist(),regular_repetition_candidate=bool(repeated),
        raster_components=n0,eroded_components_2px=ne,connectivity_erosion_sensitive=ne>n0,
        pen_lift_evidence='unresolved from assigned raster; no positive pen-lift assertion',stroke_order='unresolved')


def process(path, resume):
    vid=path.stem;dest=OUT/f'data/observations/native_structure_v4/{vid}.json'
    if resume and dest.exists():return
    obj=read_json(path);packed_path=path.with_name(vid+'_native_masks.npz')
    if not packed_path.exists():return
    packed=np.load(packed_path);rgb=Image.open(OUT/obj['native_source']).convert('RGB')
    rows=[];examples={'tall':[],'frame':[],'cuts':[],'repetition':[]};records={}
    for rec in obj['instances']:
        if rec['model']!='medium_assemblies':continue
        cm=unpack(packed,rec['shape_index']);m=measure(cm,rec['body_height_proxy_px'])
        row=dict(instance_id=rec['instance_id'],group_id=rec['group_id'],line_id=rec['line_id'],view_id=vid,
            split=rec['split'],folio_component=rec['folio_component'],bbox_xyxy=rec['bbox_xyxy'],
            atlas_eligible=rec['atlas_eligible'],height_ratio=rec['features']['height_ratio'],**m)
        rows.append(row);records[rec['instance_id']]=rec
        if rec['atlas_eligible']:
            for name,yes in [('tall',row['height_ratio']>=1.8),('frame',bool(m['frame_candidates'])),
                ('cuts',bool(m['sparse_skeleton_cut_columns'])),('repetition',m['regular_repetition_candidate'])]:
                if yes and len(examples[name])<8:examples[name].append(row)
    # Calibration/train source galleries only; held-out inspection is reserved.
    if obj['view']['split'] in ('train','calibration'):
        card=Image.new('RGB',(1280,720),'white');draw=ImageDraw.Draw(card)
        for yi,(name,exampleset) in enumerate(examples.items()):
            draw.text((5,yi*180+3),f'{vid} {name}: geometric candidates, no stroke-order claim',fill='black')
            for xi,r in enumerate(exampleset):
                crop=rgb.crop(r['bbox_xyxy']);crop.thumbnail((150,125));card.paste(crop,(xi*160+5,yi*180+25))
                draw.text((xi*160+5,yi*180+155),r['instance_id'].split('_G')[-1],fill='black')
        folder=OUT/'figures/native_structure_v4';folder.mkdir(parents=True,exist_ok=True);card.save(folder/f'{vid}.png')
    write_json(dest,dict(view=obj['view'],source_image_sha256=obj['image_sha256'],
        candidate_json_sha256=sha256(path),native_masks_sha256=sha256(packed_path),
        observations=rows,status='geometric observations with competing cuts; unreviewed instances',
        limitations=['Assigned masks can omit faint and detached ink.',
            'Straight segments, frames and repetition are geometric proxies requiring source review.',
            'Two-pixel erosion is a sensitivity probe, not evidence that the pen lifted.']))
    print(vid,len(rows),flush=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--resume',action='store_true');args=ap.parse_args()
    for p in sorted((OUT/'data/observations/regional_candidates_v4').glob('V_*.json')):
        if p.stem[2:].isdigit():process(p,args.resume)
    paths=list((OUT/'data/observations/native_structure_v4').glob('V_*.json'));summaries=[]
    for p in paths:
        obj=read_json(p);rr=obj['observations'];summaries.append(dict(view_id=p.stem,split=obj['view']['split'],
            assemblies=len(rr),tall_candidates=sum(r['height_ratio']>=1.8 for r in rr),
            frame_candidates=sum(bool(r['frame_candidates']) for r in rr),
            connected_cut_candidates=sum(bool(r['sparse_skeleton_cut_columns']) for r in rr),
            regular_repetition_candidates=sum(r['regular_repetition_candidate'] for r in rr),
            erosion_sensitive=sum(r['connectivity_erosion_sensitive'] for r in rr)))
    if summaries:write_csv(OUT/'reports/native_structure_v4_summary.csv',summaries)


if __name__=='__main__':main()
