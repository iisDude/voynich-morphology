"""Read-only V6/V5 application and audit, writing only separate postfreeze."""
from inventory_v6_common import *
import json,copy
def sequence_application():
    assert (F/'FREEZE_MANIFEST.json').exists(),'Inventory must be frozen first'
    verify_dependencies();from evaluate_row_benchmark_v5 import recurrence
    groups=read_json(V5/'group_sequences.json');assignments={p['parent_id']:p for p in read_json(F/'expanded_parent_assignments.json')};expanded=copy.deepcopy(groups)
    for g in expanded:
        tokens=[assignments[p]['expanded_structural_class'] for p in g['parent_ids']];g['ordered_tokens']=tokens;g['class_complete']='UNK' not in tokens;g['exact_sequence_complete']=g['membership_complete'] and g['class_complete'];g['notation']=' '.join(tokens)+(' [UNK_MEMBER]' if g['optional_source_objects'] else '')+(' [UNK_BOUNDARY]' if g['boundary_or_order_ambiguous'] else '')
    before=recurrence(groups);after=recurrence(expanded);assert before==after
    oldrows=read_json(V5/'row_sequences.json');expandedrows=copy.deepcopy(oldrows)
    for r in expandedrows:
        # No validated added class exists; preserve frozen source row/order and
        # all uncertainty states rather than reconstructing unknown membership.
        assert all(assignments[p['parent_id']]['expanded_structural_class']==p['retained_v3_class'] for p in assignments.values() if p['row_id']==r['row_id'])
    support=read_json(OUT/'tests/row_benchmark_v5_postfreeze/downstream_support_assessment.json');plan=read_json(D/'PLAN.json');criteria=plan['downstream'];coverage=read_json(T/'structural_coverage.json');gate=[]
    # Earlier source-rule failures remain necessary, irrespective of inventory.
    sourcepassed=False
    gate.append(dict(gate='V5_source_support_all_required',passed=sourcepassed,note='V5 heldout writing recall, endpoint accuracy and prior-resolved repeatability failed; retained unchanged.'))
    gate.append(dict(gate='unknown_confirmed_rate',observed=coverage['unknown_confirmed_rate'],max=criteria['unknown_confirmed_rate_max'],passed=coverage['unknown_confirmed_rate']<=criteria['unknown_confirmed_rate_max']))
    gate.append(dict(gate='complete_rows',observed=sum(r['exact_complete'] for r in expandedrows),min=criteria['complete_rows_min'],passed=sum(r['exact_complete'] for r in expandedrows)>=criteria['complete_rows_min']))
    for gap,m in after.items():
        for name,value,minimum in [('complete_groups_ge3',m['lengths']['3']['complete_groups'],criteria['complete_groups_ge3_min']),('heldout_groups_ge3',m['lengths']['3']['heldout_complete_groups'],criteria['heldout_groups_ge3_min']),('heldout_recurrence_ge3',m['lengths']['3']['heldout_recurrence'],criteria['heldout_recurrence_min'])]:gate.append(dict(gate=name,gap=gap,observed=value,min=minimum,passed=value is not None and value>=minimum))
    qualified=all(g['passed'] for g in gate)
    write_json(P/'group_sequences_v6_on_v5.json',expanded);write_json(P/'sequence_application.json',dict(applied_at_utc=now(),v6_manifest_sha256=sha256(F/'FREEZE_MANIFEST.json'),v5_manifest_sha256=sha256(V5/'FREEZE_MANIFEST.json'),inventory_frozen_before_application=True,source_rows_groups_memberships_coordinates_and_hypotheses_unchanged=True,baseline=before,v6=after,metrics_identical=True,complete_rows=sum(r['exact_complete'] for r in expandedrows),row_sequences=expandedrows,interpretation='No validated inventory additions means no structural coverage gain. Complete length3+ recurrence remains not estimable; this is not a population absence claim.'))
    write_json(P/'downstream_support_assessment.json',dict(assessed_at_utc=now(),v6_manifest_sha256=sha256(F/'FREEZE_MANIFEST.json'),gates=gate,qualified=qualified,assays_run=[],conventional_inputs_opened=False))
    (P/'SUMMARY.md').write_text('# V6 postfreeze application to unchanged V5\n\nInventory freeze precedes sequence application. No validated added class or composition passed; all638 parent labels, source memberships and three spacing partitions are retained.\n\n| Gap/body | Groups | Membership-complete | Exact structural complete | Complete length≥3 | Heldout length≥3 recurrence |\n|---|---:|---:|---:|---:|---|\n'+''.join(f"| {gap} | {m['groups']} | {m['membership_complete_groups']} | {m['exact_complete_groups']} | {m['lengths']['3']['complete_groups']} | not estimable |\n" for gap,m in after.items())+'\nZero complete rows. Sequence metrics exactly reproduce the frozen V5 baseline; no model was trained on this outcome. **Downstream support remains unqualified.** No Currier, ordinal-rank, native pixel-x, EVA/RF/v101, minimal-pair or decipherment assay was opened.\n',encoding='utf-8');print('Postfreeze V5 sequence application: unchanged; support',qualified,flush=True)

def integrity():
    manifest=read_json(F/'FREEZE_MANIFEST.json');failures=[];checks={}
    for version in ['v0','v11','v2','v3','v4','v5','v6']:
        path=OUT/f'data/observations/visual_dataset_{version}/FREEZE_MANIFEST.json';m=read_json(path);ff=[]
        for row in m['files']:
            p=OUT/row['path']
            if not p.exists() or sha256(p)!=row['sha256']:ff.append(row['path'])
        checks[version]=dict(files=len(m['files']),failures=ff,manifest_sha256=sha256(path));failures.extend(ff);print(version,len(m['files']),'failures',len(ff),flush=True)
    for d in manifest['source_image_dependencies']:
        if sha256(OUT/d['path'])!=d['sha256']:failures.append(d['path'])
    verify_dependencies()
    for n in ['DIAGNOSIS_SEAL.json','DEVELOPMENT_AMENDMENT_SEAL.json','CANDIDATE_MODEL_SEAL.json','FRESH_SOURCE_SEAL.json','PAIR_DECISION_SEAL.json']:verify_seal(D/n)
    guard_refusal=False
    try:guard()
    except RuntimeError:guard_refusal=True
    assert guard_refusal and not failures
    from common import read_csv,ROOT
    originals=[]
    for r in read_csv(OUT/'data/source/evidence_manifest.csv'):
        p=ROOT/r['path'];ok=sha256(p)==r['sha256'];originals.append(dict(path=r['path'],unchanged=ok));assert ok,p
    write_json(P/'integrity.json',dict(checked_at_utc=now(),manifests=checks,file_checks=sum(q['files'] for q in checks.values()),source_images_checked=len(manifest['source_image_dependencies']),originals=originals,failures=failures,stage_seals_unchanged=True,writer_refuses_v6_overwrite=guard_refusal))

def replay():
    from validate_inventory_candidates_v6 import inference
    import numpy as np
    failures=[];counts={}
    for inputfile,datafile,outputfile,label in [('discovery_parents.json','discovery_shapes.npz','discovery_candidate_assignments.json','discovery'),('fresh_source_reference.json','fresh_shapes.npz','fresh_assignments.json','fresh')]:
        r=read_json(D/inputfile);r=r['parents'] if isinstance(r,dict) else r;result=inference(r,np.load(D/datafile));old=read_json(D/outputfile);counts[label]=len(result)
        for a,b in zip(result,old):
            if a!=b:failures.append(a['parent_id'])
        assert len(result)==len(old)
    assert not failures;write_json(P/'model_replay.json',dict(checked_at_utc=now(),parents=counts,mismatches=failures,v3_model_sha256=sha256(MODEL),no_fitting_or_retuning=True));print('Model replay638 discovery+70 fresh: identical',flush=True)
if __name__=='__main__':
    import sys
    {'sequences':sequence_application,'integrity':integrity,'replay':replay}[sys.argv[1]]()
