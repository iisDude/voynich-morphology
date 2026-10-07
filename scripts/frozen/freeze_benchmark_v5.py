"""Seal the partial V5 reference and diagnostics before support assessment."""
from common import OUT,read_json,write_json,sha256
from register_row_benchmark_v5 import D,T,F,G
from map_frozen_classes_v5 import verify_source_seal
from seal_membership_rules_v5 import function_hashes
from datetime import datetime,timezone

def main():
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen();verify_source_seal();assert function_hashes()==read_json(D/'MEMBERSHIP_RULE_SEAL.json')['function_hashes']
    paths=[]
    for root in [D,T,F,G]:paths.extend(p for p in root.rglob('*') if p.is_file())
    paths.extend(OUT.glob('src/*v5*.py'));paths.extend(OUT/'reports'/p for p in ['15_source_adjudicated_row_benchmark_v5.md','16_source_row_reference_atlas_v5.html']);paths=sorted(set(paths))
    write_json(F/'FREEZE_MANIFEST.json',dict(version='V5 source-adjudicated ordinary-row reference benchmark',frozen_at_utc=datetime.now(timezone.utc).isoformat(),source_reference_seal_sha256=sha256(F/'SOURCE_REFERENCE_SEAL.json'),membership_rules_seal_sha256=sha256(D/'MEMBERSHIP_RULE_SEAL.json'),sequence_protocol_seal_sha256=sha256(F/'SEQUENCE_PROTOCOL_SEAL.json'),immutable_dependencies=read_json(D/'PLAN.json')['immutable_dependencies'],v3_class_model_sha256=read_json(D/'PLAN.json')['v3_model_sha256'],scope='16 source-adjudicated row targets, native object/member/owner/contact judgments, explicit unknowns, frozen V3 assignment, competing spacing partitions, extraction diagnosis, development-sealed rules and heldout validation, same-adjudicator repeatability. Partial photographic reference; no complete notation certification.',source_and_class_judgments_frozen_before_conventional_inputs=True,qualification_decision='Pending separate postfreeze support assessment',no_downstream_assay_performed=True,files=[dict(path=str(p.relative_to(OUT)),bytes=p.stat().st_size,sha256=sha256(p)) for p in paths]))
    print('Froze V5',len(paths),'artifacts SHA',sha256(F/'FREEZE_MANIFEST.json'),flush=True)
if __name__=='__main__':main()
