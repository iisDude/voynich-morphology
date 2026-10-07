from feature_trial2_common import *
import ast
def main():
    guard();verify_dependencies()
    for name in ['SPECIFICATION_SEAL','SOURCE_SEAL','METRIC_SEAL','RATING_SEAL','REPEAT_SEAL']:verify_seal(D/(name+'.json'))
    spec=read_json(D/'PLAN.json');rows=read_json(D/'feature_profiles.json')['parents'];assert len(rows)==221 and len({r['parent_id'] for r in rows})==221
    assert all(set(r['features'])==set(spec['features']) for r in rows)
    assert all(not r['usable_partial_profile'] or r['source_resolved'] and r['whole_parent_correspondence'] for r in rows)
    assert all(v['primary'] is None or v['range'][0]<=v['primary']<=v['range'][1] for r in rows for v in r['features'].values())
    replay=read_json(T/'deterministic_replay.json');assert replay['feature_profiles_exact'] and replay['five_distance_matrices_exact'] and replay['source_uncertainty_preserved']
    scripts=list((OUT/'src').glob('*feature_trial2*.py'))
    for p in scripts:ast.parse(p.read_text(encoding='utf-8'))
    dependencies=[OUT/p for p in spec['dependencies']]+[OUT/r['native_source'] for r in rows]
    helpers=['common.py','neutral_feature_trial_v1.py','measure_inventory_factors_v6.py','benchmark_membership_v5.py','prepare_structural_inventory_v6.py','calibrate_assemblies.py','regional_extract_v11.py','extract_recurrence_units_v3.py','evaluate_source_classes_v3.py','fit_source_classes_v3.py','inventory_v6_common.py','register_row_benchmark_v5.py']
    dependencies+=[OUT/'src'/p for p in helpers]+[OLD/'discovery_parents.json',OLD/'fresh_source_reference.json',OLD/'fresh_assignments.json',OUT/'data/observations/visual_dataset_v6/expanded_parent_assignments.json',OUT/'data/observations/neutral_feature_trial_v1/parent_feature_profiles.json']
    paths=[p for folder in [D,T,G] for p in folder.rglob('*') if p.is_file()]+scripts+dependencies+[OUT/'reports/21_neutral_structural_feature_profiles_trial2.md',OUT/'reports/22_neutral_feature_profiles_trial2.html'];paths=sorted(set(paths));assert all(p.is_file() for p in paths)
    acceptance=read_json(T/'acceptance_summary.json');save(D/'FREEZE_MANIFEST.json',dict(frozen_at_utc=now(),status='Neutral Structural Feature Profiles Trial2 frozen evidence; coverage/source and similarity superiority gates fail. Not new segmentation/classes/notation.',files=[dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p)) for p in paths],file_count=len(paths),specification_sha256=sha256(D/'SPECIFICATION_SEAL.json'),coverage_source_support=acceptance['coverage_source_pass'],similarity_superiority_support=acceptance['similarity_superiority_pass'],earlier_freezes_unchanged=True,downstream_correlations_opened=False,new_classes=False,source_semantics_separate_from_raster_repeatability=True))
    print('Trial2 frozen',len(paths),'files',sha256(D/'FREEZE_MANIFEST.json'),flush=True)
if __name__=='__main__':main()
