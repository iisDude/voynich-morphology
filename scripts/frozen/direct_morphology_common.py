from common import OUT,ROOT,read_json,write_json,sha256
from datetime import datetime,timezone
D=OUT/'data/observations/direct_morphology_trial1'
T=OUT/'tests/direct_morphology_trial1'
G=OUT/'figures/direct_morphology_trial1'
P=OUT/'tests/direct_morphology_trial1_postfreeze'
SOURCE=OUT/'data/observations/neutral_feature_trial2'
def now():return datetime.now(timezone.utc).isoformat()
def guard():
    if (D/'FREEZE_MANIFEST.json').exists():raise RuntimeError('Direct morphology Trial1 immutable; use a separately registered trial')
def save(path,value):guard();write_json(path,value)
def seal(paths,target):save(target,dict(sealed_at_utc=now(),files=[dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p)) for p in paths]))
def verify_seal(path):
    for r in read_json(path)['files']:assert sha256(OUT/r['path'])==r['sha256'],r['path']
def verify():
    for p,digest in read_json(D/'PLAN.json')['dependencies'].items():assert sha256(OUT/p)==digest,p
