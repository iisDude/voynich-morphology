"""Read-only freeze audit, sealed inference replay and postfreeze support."""
from common import ROOT,OUT,read_json,read_csv,write_json,sha256
from register_row_benchmark_v5 import D,T,F
from map_frozen_classes_v5 import verify_source_seal,parent_records,inference
from benchmark_membership_v5 import page_features
from seal_membership_rules_v5 import function_hashes
from datetime import datetime,timezone
from collections import Counter
import pickle,sys
P=OUT/'tests/row_benchmark_v5_postfreeze'

def integrity():
    failures=[];count=0;manifests={}
    for version in ['v0','v11','v2','v3','v4','v5']:
        path=OUT/f'data/observations/visual_dataset_{version}/FREEZE_MANIFEST.json';m=read_json(path);bad=[]
        for e in m['files']:
            p=OUT/e['path'];count+=1
            if not p.exists() or sha256(p)!=e['sha256']:bad.append(e['path'])
        manifests[version]=dict(files=len(m['files']),manifest_sha256=sha256(path),failures=bad);failures.extend(bad);print(version,len(m['files']),len(bad),flush=True)
    evidence=[]
    for r in read_csv(OUT/'data/source/evidence_manifest.csv'):
        path=ROOT/r['path'];ok=path.exists() and sha256(path)==r['sha256'];evidence.append(dict(path=r['path'],unchanged=ok))
    assert not failures,failures[:5];assert all(r['unchanged'] for r in evidence)
    verify_source_seal();assert function_hashes()==read_json(D/'MEMBERSHIP_RULE_SEAL.json')['function_hashes'];assert manifests['v3']['manifest_sha256']==read_json(D/'PLAN.json')['immutable_dependencies']['v3'];assert manifests['v4']['manifest_sha256']==read_json(D/'PLAN.json')['immutable_dependencies']['v4']
    # Writer guards must reject entry without any writes.
    from row_benchmark_guard_v5 import require_unfrozen
    try:require_unfrozen();raise AssertionError('Guard did not reject')
    except RuntimeError:pass
    write_json(P/'integrity.json',dict(verified_at_utc=datetime.now(timezone.utc).isoformat(),frozen_file_checks=count,manifests=manifests,original_evidence=evidence,original_evidence_count=len(evidence),failures=[],source_and_rule_seals_unchanged=True,writer_guard_rejects_v5_overwrite=True))

def replay():
    verify_source_seal();path=OUT/'data/observations/recurrence_v3_structural_candidate/sealed_class_model.pkl';model=pickle.loads(path.read_bytes());stored={r['row_id']:r['parents'] for r in read_json(F/'parent_class_assignments.json')['rows']};mismatch=[];n=0
    for r in read_json(F/'source_reference.json')['rows']:
        rgb,delta,cc=page_features(r);actual=inference(r,parent_records(r),cc,model);before={p['parent_id']:p for p in stored[r['row_id']]}
        for p in actual:
            n+=1;b=before[p['parent_id']]
            for key in ['structural_class','nominal_class','raster_stable','threshold_class_stable','alignment_class_stable','parent_boundary_status','native_bbox','root_x','root_interval','order_status']:
                if p.get(key)!=b.get(key):mismatch.append(dict(parent=p['parent_id'],field=key,before=b.get(key),after=p.get(key)))
        print(r['row_id'],'class replay',len(actual),flush=True)
    assert not mismatch,mismatch[:5];verify_source_seal();write_json(P/'frozen_class_replay.json',dict(verified_at_utc=datetime.now(timezone.utc).isoformat(),parents=n,mismatches=mismatch,v3_model_sha256=sha256(path),no_fit_or_relabeling=True))

def support():
    m=read_json(F/'FREEZE_MANIFEST.json');cfg=read_json(D/'PLAN.json');s=read_json(T/'sequence_completeness.json');a=read_json(T/'extraction_accuracy.json')['V5_automatic']['heldout'];repeat=read_json(T/'repeatability.json');rules=cfg['rule_validation_gates'];down=cfg['downstream_support'];gates=[]
    def add(name,value,limit,relation):gates.append(dict(name=name,observed=value,required=limit,relation=relation,passed=value is not None and (value>=limit if relation=='min' else value<=limit)))
    add('heldout_target_writing_recall',a['target_writing_recall']['rate'],rules['heldout_writing_recall_min'],'min');add('heldout_nonwriting_false_inclusion',a['nonwriting_false_inclusion']['rate'],rules['heldout_nonwriting_false_inclusion_max'],'max');add('heldout_resolved_target_owner_precision',a['resolved_target_ownership_precision']['rate'],rules['heldout_resolved_owner_accuracy_min'],'min');add('heldout_reviewed_parent_support_recovery',a['reviewed_parent_recovery']['rate'],rules['heldout_exact_parent_recovery_min'],'min');add('heldout_endpoint_x_accuracy',a['endpoint_accuracy']['rate'],rules['heldout_endpoint_accuracy_min'],'min');add('repeat_prior_resolved_membership_agreement',repeat['prior_resolved_membership_agreement'],rules['repeatability_resolved_membership_min'],'min');sourcepass=all(g['passed'] for g in gates)
    add('complete_reference_structural_rows',s['complete_structural_rows'],down['complete_reference_rows_min'],'min');add('unknown_confirmed_parent_rate',s['unknown_v3_rate'],down['unknown_confirmed_parent_rate_max'],'max');add('resolved_source_endpoint_fraction',s['resolved_endpoint_fraction'],down['resolved_row_endpoint_fraction_min'],'min')
    for gap,metrics in s['gap_hypotheses'].items():
        l=metrics['lengths']['3'];add('complete_groups_length3_gap'+gap,l['complete_groups'],down['complete_identified_groups_ge3_min'],'min');add('heldout_complete_groups_length3_gap'+gap,l['heldout_complete_groups'],down['heldout_complete_identified_groups_ge3_min'],'min');add('heldout_recurrence_length3_gap'+gap,l['heldout_recurrence'],down['heldout_recurrence_ge3_min'],'min')
    accepted=all(g['passed'] for g in gates);assert not accepted
    write_json(P/'downstream_support_assessment.json',dict(evaluated_after_freeze_at_utc=datetime.now(timezone.utc).isoformat(),v5_manifest_sha256=sha256(F/'FREEZE_MANIFEST.json'),source_rule_validation_passed=sourcepass,qualified_for_downstream_assays=accepted,gates=gates,decision='Do not reopen ordinal-rank/pixel-x assays, conventional crosswalks or minimal-pair support. V5 is a partial source benchmark; no complete length3+ sequence or complete row meets the registered support threshold.',metric_limitations='Writing recovery is object-level; parent support shares raster aids; owner precision is conditional; two heldout caption clusters and one source adjudicator. These do not become independent ground truth by passing point gates.',conventional_data_loaded=False,currier_loaded=False,positional_outcomes_loaded=False,assays_run=[]))
    lines=['# V5 postfreeze support assessment','',f'Frozen manifest SHA-256: `{sha256(F/"FREEZE_MANIFEST.json")}`','',f'**Downstream support: {"qualified" if accepted else "not qualified"}.** No rank/pixel-x assay, EVA/RF/v101 crosswalk, Currier metadata or minimal-pair support was opened.','', '| Gate | Observed | Required | Result |','|---|---:|---:|---|']
    for g in gates:lines.append(f'| {g["name"]} | {g["observed"] if g["observed"] is not None else "not estimable"} | {g["relation"]} {g["required"]} | {"pass" if g["passed"] else "fail"} |')
    P.mkdir(exist_ok=True);(P/'SUMMARY.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');print('Postfreeze downstream support',accepted,flush=True)

if __name__=='__main__':
    P.mkdir(exist_ok=True)
    mode=sys.argv[1] if len(sys.argv)>1 else 'all'
    if mode in ['integrity','all']:integrity()
    if mode in ['replay','all']:replay()
    if mode in ['support','all']:support()
