from common import OUT,ROOT,read_json,write_json,sha256
from datetime import datetime,timezone
D=OUT/'data/observations/direct_morphology_trial2'
T=OUT/'tests/direct_morphology_trial2'
G=OUT/'figures/direct_morphology_trial2'
P=OUT/'tests/direct_morphology_trial2_postfreeze'
OLD=OUT/'data/observations/direct_morphology_trial1'
def now():return datetime.now(timezone.utc).isoformat()
def guard():
    if (D/'FREEZE_MANIFEST.json').exists():raise RuntimeError('Direct Morphology Trial2 frozen; do not overwrite')
def save(path,value):guard();write_json(path,value)
def seal(paths,target):save(target,dict(sealed_at_utc=now(),files=[dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p)) for p in sorted(set(paths))]))
def verify_seal(path):
    for r in read_json(path)['files']:assert sha256(OUT/r['path'])==r['sha256'],r['path']
def verify():
    for p,digest in read_json(D/'PLAN.json')['dependencies'].items():assert sha256(OUT/p)==digest,p
