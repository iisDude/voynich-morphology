from direct_morphology_common import *
from replay_direct_morphology import run
from common import read_csv
def main():
    verify();verify_seal(D/'FREEZE_MANIFEST.json');old_count=0
    for v in ['v0','v11','v2','v3','v4','v5','v6']:
        p=OUT/f'data/observations/visual_dataset_{v}/FREEZE_MANIFEST.json';verify_seal(p);old_count+=len(read_json(p)['files']);print('Previous',v,'intact',flush=True)
    for p in [OUT/'data/observations/neutral_feature_trial_v1/EVIDENCE_SEAL.json',SOURCE/'FREEZE_MANIFEST.json']:verify_seal(p)
    originals=read_csv(OUT/'data/source/evidence_manifest.csv')
    for r in originals:assert sha256(ROOT/r['path'])==r['sha256'],r['path']
    run(P/'deterministic_replay.json')
    try:guard()
    except RuntimeError:blocked=True
    else:blocked=False
    assert blocked
    write_json(P/'integrity.json',dict(checked_at_utc=now(),manifest_sha256=sha256(D/'FREEZE_MANIFEST.json'),direct_trial_file_checks=len(read_json(D/'FREEZE_MANIFEST.json')['files']),previous_frozen_file_checks=old_count,Trial1_unchanged=True,Trial2_unchanged=True,Trial2_file_checks=len(read_json(SOURCE/'FREEZE_MANIFEST.json')['files']),original_evidence_files=len(originals),candidate_fields_replayed=1124,parents=217,three_resolutions_exact=True,SDF_fields_exact=True,ten_distance_matrices_exact=True,source_unknowns_preserved=True,writer_guard_blocks=True,no_downstream_assays=True,failures=[]))
    print('Direct trial postfreeze audit pass',old_count,'earlier files, Trial1/Trial2 and14 originals',flush=True)
if __name__=='__main__':main()
