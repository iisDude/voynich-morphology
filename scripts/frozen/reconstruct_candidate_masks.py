"""Recover exact native masks from recorded fine-component source bounds.

Checks every coarser subdivision against the saved normalized shape. This
prevents a prototype gallery from concealing coordinate or membership errors.
"""
from common import OUT,read_json,read_csv,write_json,sha256
from visual_extract import ink_mask
from regional_extract import normalise
import argparse
import numpy as np
import cv2
from PIL import Image


def process(path):
    obj=read_json(path);vid=obj['view']['view_id'];config=obj['native_mask_config']
    rgb=np.asarray(Image.open(OUT/obj['native_source']).convert('RGB'))
    if config.get('preblur_sigma_px',0):rgb=cv2.GaussianBlur(rgb,(0,0),config['preblur_sigma_px'])
    mask=ink_mask(rgb,config)
    fine={};groups={};region_lookup={r['region_id']:r for r in obj['regions']}
    region_labels={};bbox_lookup={}
    for rid,reg in region_lookup.items():
        x0,y0,x1,y1=reg['native_bbox'];n,labels,stats,_=cv2.connectedComponentsWithStats(mask[y0:y1,x0:x1],connectivity=8)
        region_labels[rid]=labels;lookup={}
        for ci in range(1,n):
            x,y,w,h,area=map(int,stats[ci]);bbox=(x+x0,y+y0,x+x0+w,y+y0+h)
            lookup.setdefault(bbox,[]).append(ci)
        bbox_lookup[rid]=lookup
    for rec in obj['instances']:
        if rec['model']!='fine_components':continue
        rid=rec['line_id'].split('_L')[0];reg=region_lookup[rid];rx0,ry0,_,_=reg['native_bbox'];x0,y0,x1,y1=rec['bbox_xyxy']
        candidates=bbox_lookup[rid].get(tuple(rec['bbox_xyxy']),[])
        if len(candidates)!=1:raise ValueError(f'Fine raster identity ambiguous for {rec["instance_id"]}: {len(candidates)}')
        cm=(region_labels[rid][y0-ry0:y1-ry0,x0-rx0:x1-rx0]==candidates[0]).astype(np.uint8)
        fine[rec['instance_id']]=cm;groups.setdefault(rec['group_id'],[]).append(rec)
    shapes=np.load(path.with_name(path.stem+'_shapes.npz'))['shapes'];packed=[];offsets=[0];sizes=[];maximum_error=0.
    for rec in obj['instances']:
        x0,y0,x1,y1=rec['bbox_xyxy']
        if rec['model']=='fine_components':cm=fine[rec['instance_id']]
        else:
            cm=np.zeros((y1-y0,x1-x0),np.uint8)
            for child in groups[rec['group_id']]:
                a,b,c,d=child['bbox_xyxy'];lx0,ly0=max(a,x0),max(b,y0);lx1,ly1=min(c,x1),min(d,y1)
                if lx1<=lx0 or ly1<=ly0:continue
                cm[ly0-y0:ly1-y0,lx0-x0:lx1-x0]|=fine[child['instance_id']][ly0-b:ly1-b,lx0-a:lx1-a]
        expected=shapes[rec['shape_index']];actual=normalise(cm,rec['body_height_proxy_px'])
        error=float(np.max(abs(actual-expected)));maximum_error=max(maximum_error,error)
        if error>1e-6:raise ValueError(f'Native reconstruction differs for {rec["instance_id"]}: {error}')
        bits=np.packbits(cm.ravel(),bitorder='little');packed.append(bits);offsets.append(offsets[-1]+len(bits));sizes.append(cm.shape)
    output=path.with_name(path.stem+'_native_masks.npz')
    np.savez_compressed(output,data=np.concatenate(packed) if packed else np.array([],np.uint8),offsets=np.array(offsets,np.int64),sizes=np.array(sizes,np.int32).reshape(-1,2))
    result=dict(view_id=vid,status='exact_source_mask_reconstruction_verified',instances=len(obj['instances']),max_normalized_pixel_error=maximum_error,source_image_sha256=obj['image_sha256'],source_candidate_json_sha256=sha256(path),native_masks_file=output.relative_to(OUT).as_posix(),native_masks_sha256=sha256(output),limitation='Pixel identity verifies bookkeeping, not writing-versus-texture validity or grapheme boundaries.')
    write_json(path.with_name(path.stem+'_mask_verification.json'),result);print(result,flush=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--scope',choices=['pilot','all'],default='pilot');ap.add_argument('--version',default='v4');ap.add_argument('--resume',action='store_true');args=ap.parse_args()
    pilot={f"V_{int(r['pdf_page']):03d}" for r in read_csv(OUT/'data/source/sample_manifest.csv')}
    for path in sorted((OUT/f'data/observations/regional_candidates_{args.version}').glob('V_*.json')):
        if path.stem.endswith(('_processing','_mask_verification')):continue
        if args.scope=='pilot' and path.stem not in pilot:continue
        if args.resume and path.with_name(path.stem+'_mask_verification.json').exists():continue
        process(path)


if __name__=='__main__':main()
