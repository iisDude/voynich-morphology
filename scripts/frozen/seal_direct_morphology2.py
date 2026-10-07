from direct_morphology2_common import *
from common import read_csv
import ast,platform,numpy,cv2,scipy,sklearn
def prior_integrity():
    checks={}
    paths=[OUT/f'data/observations/visual_dataset_{v}/FREEZE_MANIFEST.json' for v in ['v0','v11','v2','v3','v4','v5','v6']]+[OUT/'data/observations/neutral_feature_trial_v1/EVIDENCE_SEAL.json',OUT/'data/observations/neutral_feature_trial2/FREEZE_MANIFEST.json',OLD/'FREEZE_MANIFEST.json']
    for p in paths:
        verify_seal(p);checks[p.relative_to(OUT).as_posix()]=dict(sha256=sha256(p),file_checks=len(read_json(p)['files']))
    originals=read_csv(OUT/'data/source/evidence_manifest.csv')
    for r in originals:assert sha256(ROOT/r['path'])==r['sha256'],r['path']
    return dict(previous_packages=checks,original_evidence_files=len(originals),earlier_visual_frozen_file_checks=sum(v['file_checks'] for k,v in checks.items() if 'visual_dataset_' in k),failures=[])
def main():
    guard();verify()
    for p in D.glob('*SEAL.json'):verify_seal(p)
    replay=read_json(T/'DETERMINISTIC_REPLAY.json');assert replay['candidate_n']==1437 and replay['parent_n']==280 and len(replay['exact_distance_matrices'])==10 and replay['source_unknowns_preserved'];assert not read_json(T/'SOURCE_REPLAY.json')['failures'];assert not read_json(T/'METRIC_REPLAY.json')['failures']
    save(T/'PRIOR_INTEGRITY.json',dict(checked_at_utc=now(),**prior_integrity()))
    save(D/'ENVIRONMENT.json',dict(python=platform.python_version(),numpy=numpy.__version__,opencv=cv2.__version__,scipy=scipy.__version__,sklearn=sklearn.__version__,scope='Exact array/matrix/native/metric replay on this workstation; no platform-independent bitwise guarantee'))
    scripts=list((OUT/'src').glob('*direct_morphology2*.py'))
    for p in scripts:ast.parse(p.read_text(encoding='utf-8-sig'))
    parents=read_json(D/'source_parent_ensembles.json')['parents'];audit=read_json(D/'CAPTION_ELIGIBILITY.json');dependencies=[OUT/p for p in read_json(D/'PLAN.json')['dependencies']]+[OUT/r[k] for r in parents for k in ['native_source','native_crop']]+[OUT/r['path'] for r in audit['evidence']]+[OUT/'src/common.py']
    paths=sorted(set([p for folder in [D,T,G] for p in folder.rglob('*') if p.is_file()]+scripts+dependencies+[OUT/'reports/25_direct_contour_morphology_trial2.md',OUT/'reports/26_direct_contour_morphology_atlas_trial2.html']))
    save(D/'FREEZE_MANIFEST.json',dict(frozen_at_utc=now(),trial='Direct Continuous Contour/Morphology Trial2 fresh caption validation',file_count=len(paths),files=[dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p)) for p in paths],freshness_qualified_not_global_image_blindness=True,Trial1_unchanged=True,earlier_freezes_unchanged=True,source_unknowns_preserved=True,deterministic_replay=True,interpretation_deferred_to_postfreeze=True,no_downstream_assays=True))
    print('Trial2 freeze sealed',len(paths),sha256(D/'FREEZE_MANIFEST.json'),flush=True)
if __name__=='__main__':main()
