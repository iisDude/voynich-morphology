"""Read-only postseal verification, outside sealed artifact paths."""
from common import OUT,read_json,write_json,sha256
from neutral_feature_trial_v1 import D,profile,verify
from benchmark_membership_v5 import page_features
from measure_inventory_factors_v6 import variants
from datetime import datetime,timezone
P=OUT/'tests/neutral_feature_trial_v1_postseal'
def integrity():
    seal=read_json(D/'EVIDENCE_SEAL.json');failures=[]
    for r in seal['files']:
        if sha256(OUT/r['path'])!=r['sha256']:failures.append(r['path'])
    assert not failures;verify();count=0
    for version in ['v3','v4','v5','v6']:
        for r in read_json(OUT/f'data/observations/visual_dataset_{version}/FREEZE_MANIFEST.json')['files']:
            assert sha256(OUT/r['path'])==r['sha256'],r['path'];count+=1
    write_json(P/'integrity.json',dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),feature_trial_files=len(seal['files']),previous_frozen_file_checks=count,failures=[],trial_seal_sha256=sha256(D/'EVIDENCE_SEAL.json')));print('Trial and V3–V6 integrity pass',count,flush=True)
def replay():
    verify();old=read_json(D/'parent_feature_profiles.json')['parents'];lookup={r['parent_id']:r for r in old};states={r['parent_id']:r['source_state'] for r in read_json(OUT/'data/observations/visual_dataset_v6/expanded_parent_assignments.json')};source=OUT/'data/observations/structural_inventory_v6_development';rec=read_json(source/'discovery_parents.json')+[r for r in read_json(source/'fresh_source_reference.json')['parents'] if r['membership']=='confirmed_writing'];cacheview=None;cache=None;failures=[]
    for i,r in enumerate(rec):
        if cacheview!=r['native_source']:cache=page_features(r);cacheview=r['native_source']
        state=states.get(r['parent_id'],r.get('source_parent_status'));computed=profile(r,variants(r,cache[2]),state)
        if computed!=lookup[r['parent_id']]:failures.append(r['parent_id'])
        if i%200==0:print('Replay',i,'/',len(rec),flush=True)
    assert not failures;write_json(P/'deterministic_replay.json',dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),parents=len(rec),descriptors=34,variant_measurements=7,mismatches=[],scope='Deterministic measurement replay, not independent annotation or source-semantic validation.'));print('704 profiles reproduced exactly',flush=True)
if __name__=='__main__':
    import sys
    {'integrity':integrity,'replay':replay}[sys.argv[1]]()
