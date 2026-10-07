"""Separate V6 structural discovery; all preceding datasets read-only."""
from common import OUT,read_json,write_json,sha256
from datetime import datetime,timezone
from pathlib import Path
D=OUT/'data/observations/structural_inventory_v6_development'
F=OUT/'data/observations/visual_dataset_v6'
T=OUT/'tests/structural_inventory_v6'
G=OUT/'figures/structural_inventory_v6'
P=OUT/'tests/structural_inventory_v6_postfreeze'
V5=OUT/'data/observations/visual_dataset_v5'
MODEL=OUT/'data/observations/recurrence_v3_structural_candidate/sealed_class_model.pkl'
def now():return datetime.now(timezone.utc).isoformat()
def guard():
    if (F/'FREEZE_MANIFEST.json').exists():raise RuntimeError('V6 immutable: write a new version')
def save(path,value):
    guard();write_json(path,value)
def verify_dependencies():
    plan=read_json(D/'PLAN.json')
    for name,digest in plan['dependencies'].items():
        assert sha256(OUT/name)==digest,name
def seal(paths,target):
    save(target,dict(sealed_at_utc=now(),files=[dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p)) for p in paths]))
def verify_seal(path):
    for f in read_json(path)['files']:assert sha256(OUT/f['path'])==f['sha256'],f['path']
