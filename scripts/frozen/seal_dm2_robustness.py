from dm2_robustness_common import *
from seal_direct_morphology2 import prior_integrity
import ast,platform,numpy,scipy,sklearn
def main():
    guard();verify_base()
    for p in D.glob('*SEAL.json'):verify_seal(p)
    replay=read_json(T/'DETERMINISTIC_REPLAY.json');assert replay['analysis_conditions_replayed']==108 and not replay['failures'];assert not read_json(T/'REPEAT_REPLAY.json')['failures']
    save(T/'PRIOR_INTEGRITY.json',dict(checked_at_utc=now(),**prior_integrity(),direct_Trial2_file_checks=len(read_json(B/'FREEZE_MANIFEST.json')['files']),direct_Trial2_manifest_sha256=sha256(B/'FREEZE_MANIFEST.json'),prior_Trial2_postfreeze_files=len(read_json(D/'PRIOR_POSTFREEZE_SNAPSHOT.json')['files']),prior_Trial2_postfreeze_unchanged=True))
    save(D/'ENVIRONMENT.json',dict(python=platform.python_version(),numpy=numpy.__version__,scipy=scipy.__version__,sklearn=sklearn.__version__,maximum_cardinality_solver='scipy.optimize.milp, deterministic same-workstation replay; HiGHS secondary optimum may not be unique on another environment',exact_replay_scope='Frozen scores, graph selections,5000 caption resamples, all108 conditions and repeat analyses on this workstation'))
    scripts=list((OUT/'src').glob('*dm2_robustness*.py'))
    for p in scripts:ast.parse(p.read_text(encoding='utf-8-sig'))
    dependencies=[B/'FREEZE_MANIFEST.json',B/'PLAN.json',B/'source_decisions.json',B/'source_parent_ensembles.json',B/'source_location_aids.json',B/'pair_pool_hidden_key.json',B/'source_similarity_decisions.json',B/'direct_distance_matrices.npz',BT/'primary_and_secondary_metrics.json',OUT/'src/common.py',OUT/'src/seal_direct_morphology2.py']
    loc=read_json(B/'source_location_aids.json')['parents'];dependencies += [OUT/r['native_crop'] for r in loc]+[OUT/r['native_source'] for r in loc]
    paths=sorted(set([p for folder in [D,T,G] for p in folder.rglob('*') if p.is_file()]+scripts+dependencies+[OUT/'reports/27_direct_morphology_trial2_robustness.md',OUT/'reports/28_direct_morphology_trial2_robustness_dashboard.html']))
    save(D/'FREEZE_MANIFEST.json',dict(frozen_at_utc=now(),study='Postfreeze Direct Morphology Trial2 robustness v1',file_count=len(paths),files=[dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p)) for p in paths],classification=read_json(T/'DISPOSITION.json')['classification'],not_a_new_validation_pass=True,frozen_Trial2_manifest_sha256=sha256(B/'FREEZE_MANIFEST.json'),frozen_Trial2_status_unchanged=True,previous_freezes_and_prior_postfreeze_evidence_unchanged=True,contour64_only=True,no_downstream_assays=True))
    print('Separate robustness freeze sealed',len(paths),sha256(D/'FREEZE_MANIFEST.json'),flush=True)
if __name__=='__main__':main()
