"""Realize the internal-cut alternative recorded before conventional exposure.

The cut coordinates and uncut alternative already exist in the frozen native
structure records. This does not choose cuts from a transcription or position
effect, and never certifies that a cut is a sign or pen boundary.
"""
from common import OUT,read_json,read_csv,write_json,sha256
from regional_extract import normalise
from calibrate_assemblies import topology
from analyse_native_structure import unpack
import argparse,copy
import numpy as np
from PIL import Image,ImageDraw

def process(path):
    vid=path.stem;obj=read_json(path);structure_path=OUT/f'data/observations/native_structure_v4/{vid}.json'
    observed={r['instance_id']:r for r in read_json(structure_path)['observations']};packed=np.load(path.with_name(vid+'_native_masks.npz'))
    lines={r['line_id']:r for r in obj['lines']};records=[];shapes=[];groups=[];tiles=[]
    instances={r['instance_id']:r for r in obj['instances']};rgb=Image.open(OUT/obj['native_source']).convert('RGB')
    for group in obj['groups']:
        g=copy.deepcopy(group);g['models']={'bridge_segments':[]}
        for instanceid in group['models']['medium_assemblies']:
            rec=instances[instanceid];measure=observed[instanceid];mask=unpack(packed,rec['shape_index']);h,w=mask.shape
            cuts=measure['sparse_skeleton_cut_columns'];boundaries=[0]+cuts+[w];x0,y0,x1,y1=rec['bbox_xyxy'];body=rec['body_height_proxy_px'];line=lines[rec['line_id']]
            for start,end in zip(boundaries,boundaries[1:]):
                piece=mask[:,start:end];ys,xs=np.nonzero(piece)
                if not len(ys):continue
                low,high=int(ys.min()),int(ys.max())+1;left,right=int(xs.min()),int(xs.max())+1;piece=piece[low:high,left:right]
                bbox=[x0+start+left,y0+low,x0+start+right,y0+high];baseline=line['baseline_y_at_xref']+line['baseline_slope']*((bbox[0]+bbox[2])/2-line['baseline_xref'])
                f=topology(piece,body);f.update(height_ratio=piece.shape[0]/body,width_ratio=piece.shape[1]/body,ink_area_body2=float(piece.sum()/body**2),upper_extent_ratio=(baseline-bbox[1])/body,lower_extent_ratio=(bbox[3]-1-baseline)/body)
                aid=f"{group['group_id']}_B{len(g['models']['bridge_segments'])+1:03d}"
                record=dict(instance_id=aid,group_id=group['group_id'],line_id=rec['line_id'],view_id=vid,split=rec['split'],folio_component=rec['folio_component'],model='bridge_segments',
                    bbox_xyxy=bbox,image_sha256=obj['image_sha256'],coordinate_frame='native_yale_image',body_height_proxy_px=body,features=f,
                    original_assembly_id=instanceid,frozen_cut_columns=cuts,cut_span=[start,end],shape_index=len(shapes),
                    atlas_eligible=bool(piece.sum()>=40 and f['height_ratio']>=.35 and f['width_ratio']>=.15),
                    segmentation_status='alternative cut through <=2 skeleton pixels; uncut source assembly remains equally available',
                    boundary_claim='No pen-lift, grapheme or canonical boundary inferred',pen_lift_evidence='unresolved')
                shapes.append(normalise(piece,body));records.append(record);g['models']['bridge_segments'].append(aid)
            if cuts and obj['view']['split']=='calibration' and rec['atlas_eligible'] and len(tiles)<8:
                source=rgb.crop(rec['bbox_xyxy']);source=source.resize((max(1,source.width*2),max(1,source.height*2)));draw=ImageDraw.Draw(source)
                for cut in cuts:draw.line((cut*2,0,cut*2,source.height-1),fill='red',width=1)
                source.thumbnail((310,230));tile=Image.new('RGB',(320,280),'white');tile.paste(source,(5,25));draw=ImageDraw.Draw(tile);draw.text((5,5),rec['instance_id'].split('_R')[-1],fill='black');draw.text((5,260),f'{len(cuts)} frozen cuts / uncut retained',fill='black');tiles.append(tile)
        groups.append(g)
    folder=OUT/'data/observations/regional_candidates_bridge_v0';folder.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(folder/f'{vid}_shapes.npz',shapes=np.stack(shapes) if shapes else np.empty((0,48,48),np.float32))
    write_json(folder/f'{vid}.json',dict(view=obj['view'],native_source=obj['native_source'],image_sha256=obj['image_sha256'],native_mask_config=obj['native_mask_config'],
        regions=obj['regions'],lines=obj['lines'],groups=groups,instances=records,status='realization of previously frozen competing cuts, not accepted segmentation',
        original_candidate_sha256=sha256(path),frozen_structure_sha256=sha256(structure_path),
        limitations=['All original v4 row, mask and source-quality failures persist.','A thin skeleton neck can lie inside one shape or between connected shapes.','Unit-model fitting occurs after conventional exposure; no renewed blind claim.']))
    if tiles:
        canvas=Image.new('RGB',(1280,560),'white')
        for i,tile in enumerate(tiles):canvas.paste(tile,((i%4)*320,(i//4)*280))
        destination=OUT/'figures/frozen_bridge_calibration';destination.mkdir(parents=True,exist_ok=True);canvas.save(destination/f'{vid}.png')
    print(vid,len(records),'bridge alternatives',flush=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--scope',choices=['pilot','all'],default='pilot');ap.add_argument('--resume',action='store_true');args=ap.parse_args()
    freeze=OUT/'data/observations/visual_dataset_v0/FREEZE_MANIFEST.json';manifest=read_json(freeze);inputs={r['path']:r['sha256'] for r in manifest['files']}
    pilot={f"V_{int(r['pdf_page']):03d}" for r in read_csv(OUT/'data/source/sample_manifest.csv')}
    for path in sorted((OUT/'data/observations/regional_candidates_v4').glob('V_*.json')):
        if not path.stem[2:].isdigit() or (args.scope=='pilot' and path.stem not in pilot):continue
        structure=OUT/f'data/observations/native_structure_v4/{path.name}'
        for inputpath in (path,structure):
            key=inputpath.relative_to(OUT).as_posix()
            if sha256(inputpath)!=inputs[key]:raise ValueError('Frozen input changed: '+key)
        if args.resume and (OUT/'data/observations/regional_candidates_bridge_v0'/path.name).exists():continue
        process(path)
    write_json(OUT/'data/observations/regional_candidate_protocol_snapshot_bridge_v0.json',dict(hypothesis='split source assemblies at every internal sparse skeleton cut recorded in the first visual freeze, with the uncut alternatives retained',
        original_freeze_sha256=sha256(freeze),geometry='Original pre-exposure cut coordinates, no new cut threshold, source group/line geometry unchanged',
        unit_model_status='post-exposure realization and statistical binding; not an independent blind confirmation',
        prohibition='No conventional strings, alphabet, rank or pixel-position effect used to generate cuts or shape features',
        failures='Inherited v4 row/group failure remains; this tests a missing within-connectivity alternative, not a repair of writing-group correspondence.'))

if __name__=='__main__':main()
