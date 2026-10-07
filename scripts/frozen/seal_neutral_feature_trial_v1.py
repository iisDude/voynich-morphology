from common import OUT,read_json,write_json,sha256
from neutral_feature_trial_v1 import D,T,G,DEFS,verify
from datetime import datetime,timezone
import ast
def main():
    if (D/'EVIDENCE_SEAL.json').exists():raise RuntimeError('Trial already sealed')
    verify()
    for r in read_json(D/'RGB_DECISION_SEAL.json')['files']:assert sha256(OUT/r['path'])==r['sha256'],r['path']
    rows=read_json(D/'parent_feature_profiles.json')['parents'];assert len(rows)==704 and len({r['parent_id'] for r in rows})==704
    assert all(set(r['features'])==set(DEFS) for r in rows)
    assert all(r['features'][k]['primary'] is None or r['features'][k]['range'][0]<=r['features'][k]['primary']<=r['features'][k]['range'][1] for r in rows for k in DEFS)
    assert all(not r['usable_partial_profile'] or r['source_resolved'] and r['whole_parent_variant_correspondence'] for r in rows)
    paths=[p for folder in [D,T,G] for p in folder.rglob('*') if p.is_file()];scripts=sorted((OUT/'src').glob('*neutral*features*v1.py'))+sorted((OUT/'src').glob('*neutral*feature*v1.py'));scripts=sorted(set(scripts))
    for p in scripts:ast.parse(p.read_text(encoding='utf-8'))
    paths.extend(scripts);paths.extend([OUT/'reports/19_neutral_structural_feature_profiles_trial1.md',OUT/'reports/20_neutral_feature_profile_examples_trial1.html']);paths=sorted(set(paths))
    write_json(D/'EVIDENCE_SEAL.json',dict(sealed_at_utc=datetime.now(timezone.utc).isoformat(),status='Neutral feature feasibility trial evidence. Not V7 segmentation or discrete structural-class inventory.',files=[dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p)) for p in paths],file_count=len(paths),support_gate_pass=read_json(T/'feature_repeatability.json')['all_support_gates_pass'],previous_freezes_unchanged=True,no_downstream_assays=True));print('Sealed feature trial',len(paths),'artifacts',sha256(D/'EVIDENCE_SEAL.json'),flush=True)
if __name__=='__main__':main()
