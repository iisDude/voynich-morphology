from inventory_v6_common import *
import ast
def main():
    guard();verify_dependencies()
    for n in ['DIAGNOSIS_SEAL.json','DEVELOPMENT_AMENDMENT_SEAL.json','CANDIDATE_MODEL_SEAL.json','FRESH_SOURCE_SEAL.json','PAIR_DECISION_SEAL.json']:verify_seal(D/n)
    reference=read_json(V5/'source_reference.json')['rows'];parents=read_json(F/'expanded_parent_assignments.json');lookup={p['parent_id']:p for p in parents};confirmed={p['object_id'] for r in reference for p in r['objects'] if p['membership']=='confirmed_writing' and p['owner']=='target'};members=[p for r in parents for p in r['source_objects']];assert set(members)==confirmed and len(members)==len(confirmed)==639
    old={p['parent_id']:p for r in read_json(V5/'parent_class_assignments.json')['rows'] for p in r['parents']};assert len(parents)==638 and len(lookup)==638
    for pid,p in lookup.items():
        q=old[pid];assert p['native_bbox']==q['native_bbox'] and p['retained_v3_class']==q['structural_class'] and p['expanded_structural_class']==q['structural_class'] and p['new_validated_class'] is None
    scripts=sorted(p for p in (OUT/'src').glob('*v6*.py') if 'inventory' in p.name or 'factor_source' in p.name)
    for p in scripts:ast.parse(p.read_text(encoding='utf-8'))
    save(T/'conservation_checks.json',dict(checked_at_utc=now(),source_confirmed_object_memberships=639,whole_parent_records=638,unique_parent_ids=638,previous_v3_labels_preserved=311,unknown_labels_preserved=327,no_new_model_tokens_unsupported=True,all_previous_dependency_identities_unchanged=True,stage_seals_pass=True,scripts_ast_parsed=len(scripts),no_sequences_constructed_yet=True))
    paths=[]
    for folder in [D,F,T,G]:paths.extend(p for p in folder.rglob('*') if p.is_file())
    paths.extend(scripts);paths.extend([OUT/'reports/17_confirmed_unknown_structures_v6.md',OUT/'reports/18_confirmed_unknown_source_atlas_v6.html']);paths=sorted(set(paths))
    sources={r['native_source'] for r in read_json(D/'discovery_parents.json')+read_json(D/'fresh_source_reference.json')['parents']}
    manifest=dict(frozen_at_utc=now(),version='V6 confirmed-writing source structural inventory assessment',files=[dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p),bytes=p.stat().st_size) for p in paths],file_count=len(paths),source_image_dependencies=[dict(path=p,sha256=sha256(OUT/p)) for p in sorted(sources)],prior_dependencies=read_json(D/'PLAN.json')['dependencies'],validated_new_classes=[],validated_compositional_classes=[],status='Frozen negative inventory result. Failed candidates and diagnostic factors retained; no validated coverage expansion. Existing V3 classes and V5 judgments unchanged.',sequence_stage='Not constructed or evaluated before this inventory freeze; must write separate postfreeze outputs.',conventional_inputs_opened=False)
    save(F/'FREEZE_MANIFEST.json',manifest);print('FROZEN V6',len(paths),'artifacts',sha256(F/'FREEZE_MANIFEST.json'),flush=True)
if __name__=='__main__':main()
