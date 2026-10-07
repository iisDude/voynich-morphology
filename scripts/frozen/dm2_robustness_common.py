from common import OUT,ROOT,read_json,write_json,sha256
from datetime import datetime,timezone
B=OUT/'data/observations/direct_morphology_trial2'
BT=OUT/'tests/direct_morphology_trial2'
D=OUT/'data/observations/direct_morphology_trial2_robustness_v1'
T=OUT/'tests/direct_morphology_trial2_robustness_v1'
G=OUT/'figures/direct_morphology_trial2_robustness_v1'
P=OUT/'tests/direct_morphology_trial2_robustness_v1_postfreeze'
def now():return datetime.now(timezone.utc).isoformat()
def guard():
    if (D/'FREEZE_MANIFEST.json').exists():raise RuntimeError('Robustness package frozen')
def save(path,value):guard();write_json(path,value)
def seal(paths,target):save(target,dict(sealed_at_utc=now(),files=[dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p)) for p in sorted(set(paths))]))
def verify_seal(path):
    for r in read_json(path)['files']:assert sha256(OUT/r['path'])==r['sha256'],r['path']
def verify_base():
    assert sha256(B/'FREEZE_MANIFEST.json')=='82eb82441addc43067e678ae987147b4e8de08e845cdc04141c5230dc70e9836';verify_seal(B/'FREEZE_MANIFEST.json')
    if (D/'PRIOR_POSTFREEZE_SNAPSHOT.json').exists():verify_seal(D/'PRIOR_POSTFREEZE_SNAPSHOT.json')
