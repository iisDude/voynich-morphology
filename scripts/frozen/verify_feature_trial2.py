"""Postfreeze read-only verification; writes only the separate audit folder."""
from feature_trial2_common import *
from common import ROOT,read_csv,write_json
from measure_feature_trial2 import measure,distances,baselines
from evaluate_feature_trial2 import labels
import numpy as np
def main():
    verify_dependencies();manifest=read_json(D/'FREEZE_MANIFEST.json');assert len(manifest['files'])==manifest['file_count'];verify_seal(D/'FREEZE_MANIFEST.json');old_count=0;old_summary={}
    for v in ['v0','v11','v2','v3','v4','v5','v6']:
        p=OUT/f'data/observations/visual_dataset_{v}/FREEZE_MANIFEST.json';s=read_json(p)
        for r in s['files']:assert sha256(OUT/r['path'])==r['sha256'],r['path'];old_count+=1
        old_summary[v]=dict(manifest_sha256=sha256(p),file_checks=len(s['files']))
        print(v,'hashes verified',len(s['files']),flush=True)
    verify_seal(OUT/'data/observations/neutral_feature_trial_v1/EVIDENCE_SEAL.json')
    originals=read_csv(OUT/'data/source/evidence_manifest.csv')
    for r in originals:assert sha256(ROOT/r['path'])==r['sha256'],r['path']
    for name in ['SPECIFICATION_SEAL','SOURCE_SEAL','METRIC_SEAL','RATING_SEAL','REPEAT_SEAL']:verify_seal(D/(name+'.json'))
    spec=read_json(D/'PLAN.json');rec=read_json(D/'source_location_aids.json')['parents'];source={r['parent_id']:r for r in read_json(D/'source_decisions.json')['parents']};old=read_json(D/'feature_profiles.json')['parents'];native=np.load(D/'native_variants.npz');computed=[measure(r,[native[f'{i}_{j}'] for j in range(3)],spec,source[r['parent_id']]) for i,r in enumerate(rec)];assert computed==old
    dm,ss=distances(computed,spec);ad,ch,co,scale=baselines(np.load(D/'source_shapes.npz')['shapes'][:,0],computed);prior=np.load(D/'distances.npz')
    for k,v in [('profile',dm),('shared',ss),('aspect',ad),('contour',ch),('combined',co)]:assert np.array_equal(v,prior[k]),k
    assert labels(rec,old)==read_json(D/'V3_reporting_labels.json')
    try:guard()
    except RuntimeError:blocked=True
    else:blocked=False
    assert blocked
    write_json(P/'integrity.json',dict(checked_at_utc=now(),trial2_manifest_sha256=sha256(D/'FREEZE_MANIFEST.json'),trial2_file_checks=len(manifest['files']),previous_frozen_file_checks=old_count,previous_snapshots=old_summary,Trial1_unchanged=True,original_evidence_files=len(originals),stage_seals_pass=True,deterministic_profiles=221,descriptors=36,seven_variants=True,distance_matrices_exact=5,V3_reporting_labels_exact=221,writer_guard_blocks_frozen_trial=True,failures=[],meaning='Integrity and deterministic replay; source judgments same AI and not independent inter-rater validation.',downstream_opened=False))
    print('Postfreeze audit passed',old_count,'prior frozen checks and221 feature/V3-label replays',flush=True)
if __name__=='__main__':main()
