"""Read-only verification of original evidence and the full first freeze."""
from common import ROOT,OUT,read_csv,read_json,write_json,sha256
from datetime import datetime,timezone

freeze=OUT/'data/observations/visual_dataset_v0/FREEZE_MANIFEST.json'
manifest=read_json(freeze);failures=[]
for r in manifest['files']:
    p=OUT/r['path'];actual=sha256(p) if p.exists() else None
    if actual!=r['sha256']:failures.append(dict(path=r['path'],expected=r['sha256'],actual=actual))
original=read_csv(OUT/'data/source/evidence_manifest.csv');of=[]
for r in original:
    name=r.get('relative_path',r.get('path',r.get('filename')))
    p=ROOT/name;actual=sha256(p) if p.exists() else None
    if actual!=r['sha256']:of.append(dict(path=name,expected=r['sha256'],actual=actual))
destination=OUT/'reports/integrity_verification_v1.json'
if destination.exists():destination=OUT/'reports/integrity_verification_v2.json'
write_json(destination,dict(time_utc=datetime.now(timezone.utc).isoformat(),freeze_sha256=sha256(freeze),freeze_files_checked=len(manifest['files']),freeze_failures=failures,original_files_checked=len(original),original_failures=of,previous_pass='An initial read reported one mismatch; a subsequent in-memory reconstruction, direct byte hash and three independent streaming reads matched the original V_038 hash without changing that file. Cause of transient first read unresolved.'))
print('Freeze',len(manifest['files']),'failures',len(failures),'Original',len(original),'failures',len(of),flush=True)
if failures or of:raise RuntimeError('Integrity failure; see report')
