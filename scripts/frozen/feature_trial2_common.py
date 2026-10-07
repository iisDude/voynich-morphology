"""Trial2 separate namespace; previous packages immutable."""
from common import OUT,read_json,write_json,sha256
from datetime import datetime,timezone
D=OUT/'data/observations/neutral_feature_trial2'
T=OUT/'tests/neutral_feature_trial2'
G=OUT/'figures/neutral_feature_trial2'
P=OUT/'tests/neutral_feature_trial2_postfreeze'
OLD=OUT/'data/observations/structural_inventory_v6_development'
MODEL=OUT/'data/observations/recurrence_v3_structural_candidate/sealed_class_model.pkl'
CAPTIONS=['17','19','22','52','56','100']
def now():return datetime.now(timezone.utc).isoformat()
def guard():
    if (D/'FREEZE_MANIFEST.json').exists():raise RuntimeError('Trial2 frozen; new trial needed')
def save(path,value):guard();write_json(path,value)
def verify_dependencies():
    for p,digest in read_json(D/'PLAN.json')['dependencies'].items():assert sha256(OUT/p)==digest,p
def seal(paths,target):
    save(target,dict(sealed_at_utc=now(),files=[dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p)) for p in paths]))
def verify_seal(path):
    for r in read_json(path)['files']:assert sha256(OUT/r['path'])==r['sha256'],r['path']
