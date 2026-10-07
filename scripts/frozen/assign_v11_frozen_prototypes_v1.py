"""Transfer original image-only prototypes to source-tracked rows; no refit."""
from common import OUT,read_json,write_json,write_csv,sha256,SEED
from discover_visual_families import geom_feature
from analyse_native_structure import unpack
from collections import Counter
from PIL import Image,ImageDraw
import numpy as np
import cv2,joblib,argparse

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--resume',action='store_true');args=ap.parse_args()
    source=OUT/'data/observations/regional_candidates_v11';paths=[p for p in sorted(source.glob('V_*.json')) if p.stem[2:].isdigit()]
    if len(paths)!=204:raise ValueError('Full candidate pass incomplete')
    folder=OUT/'data/observations/assigned_visual_candidates_v11';folder.mkdir(parents=True,exist_ok=True)
    models={m:joblib.load(OUT/f'data/observations/visual_family_models_v4/{m}.joblib') for m in ['fine_components','medium_assemblies']}
    reviews={}
    for m,filename in [('fine_components','fine_family_source_review_v4.json'),('medium_assemblies','medium_family_source_review_v4.json')]:
        reviews[m]={r['cluster_index']:r for r in read_json(OUT/'data/observations'/filename)['records']}
    summaries=[];rows=[];pool=[]
    for path in paths:
        obj=read_json(path);dest=folder/path.name
        if args.resume and dest.exists():assigned=read_json(dest)
        else:
            array=np.load(path.with_name(path.stem+'_shapes.npz'))['shapes'];assignments={}
            for m,model in models.items():
                records=[r for r in obj['instances'] if r['model']==m]
                if not records:continue
                images=np.stack([cv2.resize(array[r['shape_index']],(16,16),interpolation=cv2.INTER_AREA).ravel() for r in records]);z=np.c_[model['pca'].transform(images),model['geometry_scaler'].transform(geom_feature(records))*.35];labels=model['kmeans'].predict(z);distances=np.linalg.norm(z-model['kmeans'].cluster_centers_[labels],axis=1)
                for r,ci,d in zip(records,labels,distances):
                    ci=int(ci);review=reviews[m][ci];radius=model['distance_thresholds'][ci];eligible=review['prototype_gate_eligible'] if m=='fine_components' else review['review_category']=='writing_consistent'
                    admitted=bool(r['atlas_eligible'] and radius is not None and d<=radius and model['training_folio_counts'][ci]>=3 and eligible)
                    assignments[r['instance_id']]=dict(family=f'VF_{m}_K{model["k"]:03d}_{ci+1:03d}',broad_structure=review.get('visual_structure_merge_hypothesis'),admitted=admitted,distance=float(d),review_category=review['review_category'])
            groups=[]
            for g in obj['groups']:
                fg=[assignments[i] for i in g['models']['fine_components']];mg=[assignments[i] for i in g['models']['medium_assemblies']]
                fine=[r['family'] for r in fg] if fg and all(r['admitted'] for r in fg) else None
                merged=[r['broad_structure'] for r in fg] if fine else None;factors={'VS12':['VS04','VS01'],'VS16':['VS13','VS07'],'VS17':['VS08','VS15'],'VS18':['VS08','VS04'],'VS19':['VS04','VS11'],'VS21':['VS01','VS10']}
                groups.append(dict(**g,visual_fine_units=fine,visual_merged_units=merged,visual_factored_units=[v for u in merged for v in factors.get(u,[u])] if merged else None,primary_candidate_units=[r['family'] for r in mg] if mg and all(r['admitted'] for r in mg) else None,source_pixel_x_page_fraction=g['source_pixel_center_x']/g['native_image_width_px'],section=None,hand=None,currier=None,conventional_mapping=None,
                    source_quality='Candidate tracked row and gray-gap boundary; complete-writing membership unvalidated',row_multiline_components=next(l['multiline_component_count'] for l in obj['lines'] if l['line_id']==g['line_id'])))
            assigned=dict(view=obj['view'],groups=groups,units=assignments,source_candidate_sha256=sha256(path),status='Frozen v4 image prototypes transferred without refitting; source geometry v11; not a recovered alphabet');write_json(dest,assigned)
        rows.extend(assigned['groups']);summaries.append(dict(view_id=path.stem,split=obj['view']['split'],candidate_lines=len(obj['lines']),candidate_groups=len(obj['groups']),admitted_fine_groups=sum(bool(g['visual_fine_units']) for g in assigned['groups']),admitted_medium_groups=sum(bool(g['primary_candidate_units']) for g in assigned['groups'])))
        if obj['view']['split']=='test' and len(obj['lines'])>=4:pool.append((obj['view'],obj['native_source'],obj['lines']))
        print(path.stem,summaries[-1],flush=True)
    write_json(folder/'assay_groups.json',rows);write_csv(OUT/'reports/assigned_visual_candidate_coverage_v11.csv',summaries)
    # Whole-row source audit chosen without cluster admissions/count agreements.
    rng=np.random.default_rng(SEED);audit=[];selected=[]
    for lo,hi in [(4,54),(54,104),(104,154),(154,208)]:
        candidates=[p for p in pool if lo<=int(p[0]['pdf_page'])<hi];rng.shuffle(candidates);seen=set()
        for item in candidates:
            if item[0]['folio_component'] in seen:continue
            selected.append(item);seen.add(item[0]['folio_component'])
            if len(seen)==2:break
    gallery=OUT/'figures/tracked_row_source_audit_v11';gallery.mkdir(parents=True,exist_ok=True)
    for view,source_path,lines in selected:
        vid=view['view_id'];obj=read_json(source/f'{vid}.json');instances={r['instance_id']:r for r in obj['instances']};packed=np.load(source/f'{vid}_native_masks.npz');rgb=Image.open(OUT/source_path).convert('RGB');tiles=[]
        for index in rng.choice(len(lines),4,replace=False):
            line=lines[index];bbox=line['bbox_xyxy'];x0,y0,x1,y1=bbox;mask=np.zeros((y1-y0,x1-x0),np.uint8)
            for group in obj['groups']:
                if group['line_id']!=line['line_id']:continue
                for iid in group['models']['group_only']:
                    r=instances[iid];a,b,c,d=r['bbox_xyxy'];mask[b-y0:d-y0,a-x0:c-x0]|=unpack(packed,r['shape_index'])
            patch=rgb.crop((max(0,x0-10),max(0,y0-20),min(rgb.width,x1+10),min(rgb.height,y1+20)));binary=Image.fromarray(255-mask*255).convert('RGB')
            patch.thumbnail((1600,240));binary.thumbnail((1600,240));tile=Image.new('RGB',(1620,patch.height+binary.height+45),'white');tile.paste(patch,(10,30));tile.paste(binary,(10,35+patch.height));ImageDraw.Draw(tile).text((10,5),line['line_id']+' RGB context / EXACT assigned mask',fill='black');tiles.append(tile)
            audit.append(dict(view_id=vid,folio_component=view['folio_component'],line_id=line['line_id'],bbox_xyxy=bbox,native_source=source_path,groups=sum(g['line_id']==line['line_id'] for g in obj['groups']),outcome='unreviewed',gallery=(gallery/f'{vid}.png').relative_to(OUT).as_posix()))
        canvas=Image.new('RGB',(1620,sum(t.height for t in tiles)),'#ddd');y=0
        for tile in tiles:canvas.paste(tile,(0,y));y+=tile.height
        canvas.save(gallery/f'{vid}.png')
    write_json(folder/'tracked_row_source_audit_plan.json',dict(seed=SEED,rows=audit,selection='Two test caption components per fixed manuscript quartile, four uniform entire candidate rows per view; no unit admissions or conventional alignment used',limitation='Post-exposure diagnostic, not a fresh blind study; only writing flow and assignment coverage reviewed.'))

if __name__=='__main__':main()
