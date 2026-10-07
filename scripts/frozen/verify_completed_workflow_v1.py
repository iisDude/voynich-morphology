"""Read-only freeze/data invariance and completed artifact-contract audit."""
from common import ROOT,OUT,read_json,read_csv,write_json,write_csv,sha256,SEED
from datetime import datetime,timezone
import numpy as np

def main():
    checks=[];failures=[]
    def check(kind,target,passed,detail=None):
        row=dict(check=kind,target=target,passed=bool(passed),detail=detail);checks.append(row)
        if not passed:failures.append(row)
    for version in ['v0','v11']:
        freeze=OUT/f'data/observations/visual_dataset_{version}/FREEZE_MANIFEST.json';manifest=read_json(freeze)
        for r in manifest['files']:
            path=OUT/r['path'];actual=sha256(path) if path.exists() else None;check('frozen_file_hash',version+':'+r['path'],actual==r['sha256'],None if actual==r['sha256'] else dict(expected=r['sha256'],actual=actual))
        source=read_json(OUT/f'data/observations/visual_dataset_{version}/assay_groups.json');copy=read_json(OUT/f'data/comparisons/{"v2" if version=="v0" else "v11"}/visual_groups_with_metadata.json');index={r['group_id']:r for r in copy}
        protected=['visual_fine_units','visual_merged_units','visual_factored_units','primary_candidate_units','bbox_xyxy','normalized_group_rank','normalized_pixel_center','source_pixel_center_x','source_pixel_center_y','group_rank','group_count']
        check('postfreeze_group_count',version,len(source)==len(copy))
        check('postfreeze_unit_and_position_invariance',version,all(r['group_id'] in index and all(r.get(k)==index[r['group_id']].get(k) for k in protected) for r in source))
        check('no_prefreeze_context_or_conventional_mapping',version,all(all(r.get(k) is None for k in ['section','hand','currier','conventional_mapping']) for r in source))
        check('all_204_canonical_views',version,len([p for p in freeze.parent.glob('V_*.json') if p.stem[2:].isdigit()])==204)
    original=read_csv(OUT/'data/source/evidence_manifest.csv')
    for r in original:
        name=r.get('relative_path',r.get('path',r.get('filename')));check('original_evidence_hash',name,sha256(ROOT/name)==r['sha256'])
    datasets=['ZL_EVA','RF','v101','visual_fine','visual_merged','visual_factored','visual_medium','Finnish','Turkish','Latin','visual_v11_fine','visual_v11_merged','visual_v11_factored','visual_v11_medium']
    roots=[]
    for category in ['structural','context','depth_order_repetition','hmm_transfer']:
        for name in datasets:
            root=OUT/'tests'/category/name;roots.append(root);check('registered_dataset_suite',category+':'+name,root.exists())
    for name in ['visual_geometry','visual_reconstruction','visual_structure','candidate_integrity_v1','conventional_crossgraph','compound_stress_v1','dependence_boundaries','literal_e_repetition_v1','mechanics_v1','physical_overlap_v1','visual_family_stability_v1']:
        roots.append(OUT/'tests'/name)
    roots.append(OUT/'tests/hmm_transfer/ZL_EVA_all_hands')
    contract=['README.md','run.py','config.json','input_manifest.json','results.csv','summary.md']
    artifacts=[]
    for root in roots:
        for name in contract:check('empirical_artifact_contract',root.relative_to(OUT).as_posix()+'/'+name,(root/name).is_file())
        check('empirical_figure_contract',root.relative_to(OUT).as_posix(),bool(list((root/'figures').glob('*.png'))))
        for path in root.rglob('*'):
            if path.is_file() and path.suffix in ['.json','.csv','.md','.py','.png']:artifacts.append(dict(path=path.relative_to(OUT).as_posix(),sha256=sha256(path),bytes=path.stat().st_size))
    for name in ['ZL_EVA','RF','v101']:
        rows=read_json(OUT/f'data/comparisons/v2/{name}_groups_with_metadata.json');check('no_conventional_pixel_fabrication',name,all(r.get('source_pixel_center_x') is None and r.get('normalized_pixel_center') is None for r in rows))
    check('all_32_tracked_whole_row_reviews','v11',len(read_json(OUT/'data/observations/assigned_visual_candidates_v11/tracked_row_source_audit_reviewed.json')['rows'])==32)
    check('all_22_tracked_alignment_reviews','v11',len(read_json(OUT/'data/comparisons/v11/visual_row_alignment_source_audit.json'))==22)
    check('all_nine_caption_pair_source_reviews','physical',len(read_json(OUT/'tests/physical_overlap_v1/source_reviewed.json'))==9)
    check('all_12_mechanics_fixtures','mechanics',len(read_json(OUT/'tests/mechanics_v1/results.json')['checks'])==12 and all(r['passed'] for r in read_json(OUT/'tests/mechanics_v1/results.json')['checks']))
    reports=['06_manuscript_derived_model_v1.md','03_transcription_crosswalk.md','04_positional_replication.md','07_full_test_ledger_results.md','04_prior_art_collisions_v1.md']
    for name in reports:check('research_deliverable',name,(OUT/'reports'/name).is_file())
    root=OUT/'tests/workflow_audit_v1';root.mkdir(parents=True,exist_ok=True);write_csv(root/'results.csv',checks);write_json(root/'results.json',dict(time_utc=datetime.now(timezone.utc).isoformat(),status='passed' if not failures else 'failed',checks=len(checks),failures=failures,empirical_result_directories=len(roots),original_evidence_files=len(original),frozen_manifest_sha256={v:sha256(OUT/f'data/observations/visual_dataset_{v}/FREEZE_MANIFEST.json') for v in ['v0','v11']},interpretation='Artifact completeness and immutable data bookkeeping are verified; manuscript writing-unit validity is not.'))
    write_json(OUT/'reports/research_artifact_index_v1.json',dict(status='Completed current empirical pass; recovered complete writing-unit system not established',artifacts=artifacts,source_sha256=sha256(OUT/'src/verify_completed_workflow_v1.py')))
    print('Workflow audit',len(checks),'checks',len(failures),'failures',len(roots),'empirical directories',flush=True)
    if failures:
        print(failures[:25],flush=True);raise ValueError('Workflow audit failures')

if __name__=='__main__':main()
