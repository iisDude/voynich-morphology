"""Native morphology sensitivity and destructive geometric null probes."""
from common import OUT,read_json,write_json,write_csv,sha256,SEED
from analyse_native_structure import unpack,measure
from visual_extract import ink_mask
import numpy as np
import cv2
from PIL import Image
from sklearn.mixture import GaussianMixture


def main():
    rng=np.random.default_rng(SEED);rows=[];heights=[];inputs=[]
    for path in sorted((OUT/'data/observations/assigned_visual_candidates_v4').glob('V_*.json')):
        if not path.stem[2:].isdigit():continue
        obj=read_json(OUT/f'data/observations/regional_candidates_v4/{path.name}');a=read_json(path)
        eligible=[r for r in obj['instances'] if r['model']=='medium_assemblies' and a['units'][r['instance_id']]['admitted_to_primary_candidate_assay']]
        heights.extend(dict(view_id=path.stem,split=r['split'],folio_component=r['folio_component'],height=r['features']['height_ratio']) for r in eligible)
        if not eligible:continue
        selected=[eligible[i] for i in rng.choice(len(eligible),min(8,len(eligible)),replace=False)]
        packed=np.load(OUT/f'data/observations/regional_candidates_v4/{path.stem}_native_masks.npz')
        rgb=np.asarray(Image.open(OUT/obj['native_source']).convert('RGB'));blur=cv2.GaussianBlur(rgb,(0,0),.9)
        masks={}
        for contrast in (4,6,8):
            config=dict(obj['native_mask_config'],primary_ink_contrast=contrast);masks[contrast]=ink_mask(blur,config)
        for rec in selected:
            cm=unpack(packed,rec['shape_index']);body=rec['body_height_proxy_px'];m=measure(cm,body)
            # Each row permutation preserves the silhouette's row ink count and
            # bounding rectangle, but intentionally destroys writing geometry.
            null=np.stack([rng.permutation(row) for row in cm]);nm=measure(null,body)
            x,y,c,d=rec['bbox_xyxy'];counts={};ious={}
            for contrast in (4,6,8):
                local=masks[contrast][y:d,x:c];n,lab,stats,_=cv2.connectedComponentsWithStats(local,connectivity=8)
                counts[str(contrast)]=int(sum(s[cv2.CC_STAT_AREA]>=12 for s in stats[1:]))
                full=masks[6][y:d,x:c];union=np.logical_or(local,full).sum();ious[str(contrast)]=float(np.logical_and(local,full).sum()/union) if union else 1.
            rows.append(dict(instance_id=rec['instance_id'],view_id=path.stem,folio_component=rec['folio_component'],split=rec['split'],
                frame_observed=bool(m['frame_candidates']),frame_row_permutation=bool(nm['frame_candidates']),
                insertion_above_bar_candidate=any(f['above_bar_ink_pixels']>0 for f in m['frame_candidates']),
                regular_repetition_observed=m['regular_repetition_candidate'],regular_repetition_row_permutation=nm['regular_repetition_candidate'],
                sparse_cut_observed=bool(m['sparse_skeleton_cut_columns']),erosion_connectivity_sensitive=m['connectivity_erosion_sensitive'],
                threshold_component_count_4=counts['4'],threshold_component_count_6=counts['6'],threshold_component_count_8=counts['8'],
                threshold_component_count_changes=len(set(counts.values()))>1,threshold_mask_iou_4=ious['4'],threshold_mask_iou_8=ious['8']))
        inputs.append(dict(path=path.relative_to(OUT).as_posix(),sha256=sha256(path)))
        print(path.stem,flush=True)
    out=OUT/'tests/visual_structure';out.mkdir(parents=True,exist_ok=True);write_csv(out/'results.csv',rows)
    mixture=[];train=np.log(np.array([r['height'] for r in heights if r['split']=='train'])).reshape(-1,1)
    for k in (1,2,3):
        gm=GaussianMixture(n_components=k,random_state=SEED,n_init=3,reg_covar=.005).fit(train)
        for split in ('validation','test'):
            rr=[r for r in heights if r['split']==split];vals=gm.score_samples(np.log(np.array([r['height'] for r in rr])).reshape(-1,1))
            perfolio={}
            for r,v in zip(rr,vals):perfolio.setdefault(r['folio_component'],[]).append(v)
            mixture.append(dict(components=k,split=split,instances=len(rr),folio_components=len(perfolio),
                equal_folio_log_density=float(np.mean([np.mean(v) for v in perfolio.values()])),
                component_height_centres=np.exp(gm.means_[:,0]).tolist(),component_weights=gm.weights_.tolist()))
    write_json(out/'height_mixture_results.json',mixture)
    summary=[]
    for split in ('calibration','train','validation','test'):
        rr=[r for r in rows if r['split']==split];folios=sorted(set(r['folio_component'] for r in rr))
        for metric in ['frame_observed','insertion_above_bar_candidate','regular_repetition_observed','sparse_cut_observed','erosion_connectivity_sensitive','threshold_component_count_changes']:
            perfolio=[np.mean([r[metric] for r in rr if r['folio_component']==f]) for f in folios]
            boot=rng.choice(perfolio,(2000,len(perfolio)),replace=True).mean(axis=1) if perfolio else [np.nan]
            summary.append(dict(split=split,metric=metric,sampled_instances=len(rr),folio_components=len(folios),
                equal_folio_fraction=float(np.mean(perfolio)),bootstrap_lower=float(np.quantile(boot,.025)),bootstrap_upper=float(np.quantile(boot,.975))))
    write_csv(out/'summary.csv',summary)
    write_json(out/'config.json',dict(seed=SEED,sampling='8 uniform admitted medium instances per view; every populated view included',
        thresholds=[4,6,8],erosion='2 by 2 pixel square; raster sensitivity only',
        geometric_null='independent column permutation within each native mask row, preserving row ink counts',
        height_models='training log-height Gaussian mixtures with 1,2,3 components; held-out equal-folio log density',
        interpretation=['Morphology proxies do not establish frames, insertions, minims, ligatures, strokes or pen lifts.',
            'A shape-aware null is destructive and does not establish linguistic or cryptographic significance.',
            'Threshold probe uses full crop mask; crossings/background not assigned to the component can influence counts.',
            'Body/baseline are provisional estimates, not gold-standard physical measurements.',
            'Height mixture can reflect different assemblies and detector truncation; no discrete sign inventory is inferred.',
            'Gate source errors persist and folio caption groups are not verified independent bifolios.']))
    write_json(out/'input_manifest.json',inputs)
    (out/'README.md').write_text('# Visual geometry probes\n\nRun `run.py`. Every populated manuscript view contributes a reproducible native-mask sample. See configuration for proxy definitions and limitations. No result licenses pen-lift or stroke-order assertions.\n',encoding='utf-8')
    (out/'run.py').write_text('from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]/"src"))\nfrom test_visual_structure import main\nmain()\n',encoding='utf-8')
    (out/'summary.md').write_text('# Morphology and ambiguity\n\n`summary.csv` reports per-folio proportions and descriptive bootstrap intervals. `height_mixture_results.json` preserves continuous-height model comparisons; apparent mixtures do not settle units. Full instance results include threshold connectivity changes and the row-permutation null. The manuscript photographs do not resolve pen lifts or stroke order for these masks.\n',encoding='utf-8')
    print('samples',len(rows),'height_models',mixture)

if __name__=='__main__':main()
