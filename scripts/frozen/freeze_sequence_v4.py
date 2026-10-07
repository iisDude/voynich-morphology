"""Immutable partial source evidence freeze; failed qualification is retained."""
from common import OUT,read_json,write_json,sha256
from register_sequence_v4 import D,T
from build_sequence_model_v4 import F
from datetime import datetime,timezone
def main():
    manifest=F/'FREEZE_MANIFEST.json'
    if manifest.exists():raise RuntimeError('Already frozen')
    audit=read_json(T/'conservation_and_integrity.json');assert not audit['inference_mismatches'] and audit['strict_finite_json'] and audit['original_root_inputs_checked']==14
    initial=read_json(T/'initial_frozen_integrity.json');assert all(not r['failures'] for r in initial)
    plan=read_json(D/'PLAN.json');assert sha256(OUT/'data/observations/visual_dataset_v3/FREEZE_MANIFEST.json')==plan['v3_manifest_sha256']
    qualification=read_json(T/'qualification.json');files=[]
    for folder in [D,F,T,OUT/'figures/sequence_v4']:
        files.extend(p for p in folder.rglob('*') if p.is_file() and p.name!='FREEZE_MANIFEST.json')
    files+=list((OUT/'src').glob('*_v4.py'));files += [OUT/'reports/13_source_sequence_validation_v4.md',OUT/'reports/14_source_sequence_examples_v4.html']
    records=[dict(path=p.relative_to(OUT).as_posix(),bytes=p.stat().st_size,sha256=sha256(p)) for p in sorted(set(files))]
    write_json(manifest,dict(version='V4 partial source-only sequence model',frozen_at_utc=datetime.now(timezone.utc).isoformat(),v3_immutable_manifest_sha256=plan['v3_manifest_sha256'],source_dependencies='V3 freeze covers maximum-resolution native Yale images, frozen taxonomy, model and imported extraction/inference code; must verify composition with V3 manifest.',source_class_model_sha256=plan['v3_model_sha256'],classes_and_segmentation_frozen_before_any_conventional_comparison=True,qualification_sha256=sha256(T/'qualification.json'),qualified_as_practical_notation=qualification['qualified_as_practical_notation'],scope='100 new captures,1078 proposed/1054 retained local fields; overview triage plus native audit samples; partial sequences and explicit unknown/competing constraints. Complete writing recall and physical row endpoints uncertified.',files=records))
    print('V4 frozen',len(records),'files; qualification',qualification['qualified_as_practical_notation'],'manifest',sha256(manifest),flush=True)
if __name__=='__main__':main()
