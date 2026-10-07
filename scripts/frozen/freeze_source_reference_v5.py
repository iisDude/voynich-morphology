"""Resolve repeat disagreements conservatively, seal source truth before V3."""
from common import OUT,read_json,write_json,sha256
from register_row_benchmark_v5 import D,T,F
from seal_membership_rules_v5 import function_hashes
from datetime import datetime,timezone
from collections import Counter

def main():
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen(source_stage=True)
    if (F/'SOURCE_REFERENCE_SEAL.json').exists():raise RuntimeError('Source reference already sealed')
    assert function_hashes()==read_json(D/'MEMBERSHIP_RULE_SEAL.json')['function_hashes']
    assert sha256(D/'repeat_blind_decisions.json')==read_json(D/'REPEAT_DECISION_SEAL.json')['sha256']
    rows=read_json(D/'development_source_reference.json')['rows']+read_json(D/'heldout_source_reference.json')['rows'];objs={p['object_id']:p for r in rows for p in r['objects']};repeat={p['anonymous_id']:p for p in read_json(D/'repeat_blind_decisions.json')['objects']};mapping=read_json(D/'repeat_hidden_mapping.json');pairs=[]
    for m in mapping:
        old=objs[m['object_id']];new=repeat[m['anonymous_id']];pair=dict(**m,first_membership=old['membership'],repeat_membership=new['membership'],first_owner=old['owner'],repeat_owner=new['owner'],exact_membership_agreement=old['membership']==new['membership']);pairs.append(pair)
        if old['membership'] in ['confirmed_writing','confirmed_nonwriting'] and old['membership']!=new['membership']:
            old['pre_repeat_membership']=old['membership'];old['membership']='unresolved';old['owner']='unknown';old['repeat_disagreement']=pair;old['physical_parent_status']='unresolved_repeat_disagreement'
        elif old['membership']=='confirmed_writing' and new['membership']=='confirmed_writing' and old['owner']!=new['owner']:
            old['pre_repeat_owner']=old['owner'];old['owner']='unknown';old['repeat_disagreement']=pair;old['physical_parent_status']='unresolved_repeat_ownership'
        # Original unknowns are never promoted because a repeat looked cleaner.
    resolved=[p for p in pairs if p['first_membership'] in ['confirmed_writing','confirmed_nonwriting']];both=[p for p in resolved if p['repeat_membership'] in ['confirmed_writing','confirmed_nonwriting']];wp=sum(p['first_membership']=='confirmed_writing' for p in pairs);wr=sum(p['repeat_membership']=='confirmed_writing' for p in pairs);wa=sum(p['first_membership']==p['repeat_membership']=='confirmed_writing' for p in pairs)
    stats=dict(n=len(pairs),exact_all_state_agreement=sum(p['exact_membership_agreement'] for p in pairs)/len(pairs),prior_resolved_n=len(resolved),prior_resolved_membership_agreement=sum(p['exact_membership_agreement'] for p in resolved)/len(resolved),both_resolved_n=len(both),both_resolved_agreement=sum(p['exact_membership_agreement'] for p in both)/len(both),positive_writing_agreement=2*wa/(wp+wr),first_writing_n=wp,repeat_writing_n=wr,both_writing_n=wa,state_transitions={f'{a} -> {b}':n for (a,b),n in Counter((p['first_membership'],p['repeat_membership']) for p in pairs).items()},source_disagreements_downgraded=sum('repeat_disagreement' in p for p in objs.values()),same_adjudicator_only=True,independent_inter_rater=False,rows=read_json(D/'repeat_blind_decisions.json')['rows'],pairs=pairs)
    write_json(T/'repeatability.json',stats)
    for r in rows:
        r['endpoint_coordinate_precision']='Native source review windows and x intervals; not hand-painted ink-pixel masks'
        r['physical_endpoint_x_intervals']=[r.get('start_alternatives') or [r['physical_scope'][0]-4,r['physical_scope'][0]+4],[r['physical_scope'][1]-4,r['physical_scope'][1]+4]]
        r['boundary_hypotheses']=[.35,.55,.75];r['group_boundary_truth']='Physical source contacts and separate connected parents; three spacing partitions are hypotheses, not word-boundary gold.'
        # Recompute source-geometric admissibility after any conservative repeat downgrade.
        import numpy as np
        for p in r['objects']:
            x,y,c,d=p['native_bbox'];base=float(np.interp((x+c)/2,np.array(r['body_path'])[:,0],np.array(r['body_path'])[:,1]));body=r['body_proxy'];p['possible_target_owner']=bool(p['owner']=='target' or p['owner']=='unknown' and x<r['physical_scope'][1]+.35*body and c>r['physical_scope'][0]-.35*body and y<base+.65*body and d>base-1.8*body)
    F.mkdir(exist_ok=True)
    write_json(F/'source_reference.json',dict(sealed_at_utc=datetime.now(timezone.utc).isoformat(),rows=rows,source_only=True,structural_labels_present=False,reference_scope='Operational full-row photographic object/ownership reference. Mask-assisted coordinate proposals, RGB-reviewed connected structures and explicit unknowns. Does not certify chemical ink or hand-painted pixel masks.',annotation_sources='Native full contexts, every large/small RGB object aid, overlapping coordinate panels, targeted4x contacts, anonymous repeat subset',selection_identity_caveat='Registered geometric proposal anchors are not row truth. Physical row roots were chosen from the native RGB before rule validation; B002/B011/B012/B016 required explicit source identity/context corrections. No row was replaced after observing a heldout rule result. B011 deliberately retains the second source row reviewed before any rule prediction, despite raw anchor ambiguity.',no_conventional_inputs=True))
    paths=[F/'source_reference.json',D/'MEMBERSHIP_RULE_SEAL.json',D/'PLAN.json',D/'development_source_reference.json',D/'heldout_source_reference.json',D/'repeat_blind_decisions.json',D/'REPEAT_REGISTRATION.json',T/'repeatability.json']
    write_json(F/'SOURCE_REFERENCE_SEAL.json',dict(sealed_at_utc=datetime.now(timezone.utc).isoformat(),stage='Source membership, physical row judgments, contacts and repeat handling frozen BEFORE V3 class mapping',files=[dict(path=str(p.relative_to(OUT)),sha256=sha256(p)) for p in paths],structural_suggestion_exposure=False,membership_rule_function_hashes=function_hashes(),ambiguous_membership_retained=True))
    print('Frozen16 source reference rows before any V3 inference',flush=True);print({k:v for k,v in stats.items() if k not in ['pairs','rows','state_transitions']},flush=True)
if __name__=='__main__':main()
