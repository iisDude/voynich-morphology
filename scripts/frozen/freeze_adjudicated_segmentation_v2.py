"""Validate and freeze source-only v2 before any new positional assay."""
from common import ROOT,OUT,read_json,read_csv,write_json,sha256
from datetime import datetime,timezone
from collections import Counter
import math

def main():
    root=OUT/'data/observations/source_adjudication_v2';dest=OUT/'data/observations/visual_dataset_v2';freeze=dest/'FREEZE_MANIFEST.json'
    if freeze.exists():raise ValueError('Already frozen; use a new version')
    failures=[];checks=0;groups=read_json(dest/'assay_groups_source_only.json')
    for name,n in [('row_judgments',47),('assembly_judgments',188),('boundary_judgments',47),('curved_judgments',17),('panel_judgments',9)]:
        checks+=1
        if len(read_json(root/(name+'.json')))!=n:failures.append('Incomplete '+name)
    if len(read_json(root/'dense_blocks/source_reviews.json'))!=8:failures.append('Incomplete dense reviews')
    byline={}
    for g in groups:
        checks+=1
        if any(g.get(k) is not None for k in ['currier','section','hand','conventional_mapping']):failures.append('Premature comparison metadata '+g['group_id'])
        byline.setdefault(g['line_id'],[]).append(g)
        a,b,c,d=g['bbox_xyxy'];left,right=g['line_x_extent_px'];expected=((a+c)/2-left)/max(1,right-left)
        if not math.isclose(expected,g['normalized_pixel_center'],abs_tol=1e-12):failures.append('Pixel formula '+g['group_id'])
        if g['primary_eligible'] and not 0<=g['normalized_pixel_center']<=1:failures.append('Pixel extent '+g['group_id'])
        if g['writing_membership']=='unknown' and any(g.get(k) for k in ['visual_fine_units','visual_merged_units','visual_factored_units']):failures.append('Unknown assigned '+g['group_id'])
    for lid,gg in byline.items():
        checks+=1;gg.sort(key=lambda g:g['group_rank']);counts=Counter(i for g in gg if g['visual_fine_units'] for i in g['member_ids'])
        if counts and max(counts.values())>1:failures.append('Known connected parent cut across groups '+lid)
        for i,g in enumerate(gg):
            if g['group_count']!=len(gg) or g['group_rank']!=i or not math.isclose(g['normalized_group_rank'],i/(len(gg)-1) if len(gg)>1 else .5):failures.append('Rank recomputed incorrectly '+lid)
    # Read-only checks of both old freezes and the original user evidence.
    preserved=[]
    for name in ['visual_dataset_v0','visual_dataset_v11']:
        fp=OUT/'data/observations'/name/'FREEZE_MANIFEST.json';old=read_json(fp)
        for r in old['files']:
            checks+=1
            if sha256(OUT/r['path'])!=r['sha256']:failures.append('Old frozen content changed '+r['path'])
        preserved.append(dict(version=name,manifest_sha256=sha256(fp),files_checked=len(old['files'])))
    for r in read_csv(OUT/'data/source/evidence_manifest.csv'):
        p=ROOT/r.get('relative_path',r.get('path',r.get('filename')));checks+=1
        if sha256(p)!=r['sha256']:failures.append('Original evidence changed '+str(p))
    qa=dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),checks=checks,failures=failures,old_freezes=preserved,source_reviews_complete=True,comparison_metadata_attached=False)
    write_json(dest/'pre_freeze_validation.json',qa)
    if failures:raise ValueError(str(failures[:10]))
    paths=set(p for d in [dest,root,OUT/'figures/source_adjudication_v2'] for p in d.rglob('*') if p.is_file())
    paths.update(OUT/'src'/n for n in ['prepare_source_adjudication_v2.py','render_adjudication_evidence_v2.py','record_source_adjudication_v2.py','render_curved_panel_evidence_v2.py','record_curved_panel_adjudication_v2.py','reconstruct_adjudicated_rows_v2.py','record_recomposed_boundary_review_v2.py','prepare_dense_block_extension_v2.py','extract_dense_blocks_v2.py','record_dense_block_reviews_v2.py','assemble_segmentation_v2.py','freeze_adjudicated_segmentation_v2.py','run_adjudicated_currier_B_v2.py','structural_assays.py','common.py','visual_extract.py','calibrate_assemblies.py','regional_extract_v11.py','discover_visual_families.py'])
    paths.update(OUT/n for n in ['data/observations/visual_family_models_v4/fine_components.joblib','data/observations/fine_family_source_review_v4.json','data/source/yale_native_all_manifest.csv','data/source/visual_split_manifest.json','data/observations/visual_protocol_draft.json'])
    if not (OUT/'tests/adjudicated_currier_B_v2/analysis_plan.json').exists():raise ValueError('Assay preregistration missing')
    paths.add(OUT/'tests/adjudicated_currier_B_v2/analysis_plan.json')
    items=[dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p),bytes=p.stat().st_size) for p in sorted(paths)]
    write_json(freeze,dict(snapshot_id='source_adjudicated_segmentation_v2',frozen_at_utc=datetime.now(timezone.utc).isoformat(),status='Frozen source-derived partial segmentation and explicit unknowns; complete manuscript writing-unit system not established',source_inputs='Native Yale photographs only for v2 adjudication; source-trained visual prototype models transferred unchanged',comparison_metadata_read_for_v2=False,v2_effect_statistics_inspected=False,prior_exposure='Prior conventional effects known; this is a post-exposure source repair, not newly blind confirmation',unresolved='Failed row ownership, unrecovered ink, ambiguous contacts, curved internal boundaries and physical panel correspondences remain unknown; no alphabet imposed',files=items,old_freezes=preserved,summary=read_json(dest/'summary.json')))
    print('Frozen v2',len(items),'files',sha256(freeze),'checks',checks,flush=True)
if __name__=='__main__':main()
