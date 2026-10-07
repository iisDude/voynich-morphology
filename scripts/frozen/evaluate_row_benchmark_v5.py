"""Separate source extraction diagnostics and frozen-class sequence support."""
from common import OUT,read_json,write_json,SEED
from register_row_benchmark_v5 import D,T,F
from benchmark_membership_v5 import page_features,predict
from seal_membership_rules_v5 import function_hashes
from map_frozen_classes_v5 import verify_source_seal
from collections import Counter,defaultdict
from datetime import datetime,timezone
import numpy as np

def legacy_predictions(rows):
    oldrows=read_json(OUT/'data/observations/sequence_v4_development/source_rows.json')
    # Explicit projection: only source geometry/membership fields, no V3 labels,
    # conventional strings, metadata or positional outcomes used.
    names=['parent_id','view_id','row_number','row_support','native_bbox','writing_membership','row_ownership','small_detached_candidate','field_edge']
    old=[{k:p.get(k) for k in names} for p in read_json(OUT/'data/observations/visual_dataset_v4/source_parent_states.json')]
    byview=defaultdict(list)
    for p in old:byview[p['view_id']].append(p)
    result=[]
    for r in rows:
        choices=[q for q in oldrows if q['view_id']==r['view_id'] and q['status']=='triaged_local_writing_field'];kn=np.array(r['body_path']);grid=np.linspace(r['physical_scope'][0],r['physical_scope'][1],20);body=np.interp(grid,kn[:,0],kn[:,1])
        def loss(q):
            a=np.array(q['body_path_knots']);return float(np.median(abs(np.interp(grid,a[:,0],a[:,1])-body)))
        chosen=min(choices,key=loss) if choices else None;pp={p['parent_id']:p for p in byview[r['view_id']]};objects=[]
        for p in r['objects']:
            suffix='P' if p['raster']=='primary9' else 'F';q=pp.get(f'{r["view_id"]}_{suffix}{p["cc_label"]:06d}')
            strict=bool(q and q['writing_membership']=='source_field_writing_candidate' and not q['small_detached_candidate'] and q['row_ownership']!='unknown' and not q['field_edge']);target=bool(strict and chosen and q['row_number']==chosen['row_number'])
            objects.append(dict(object_id=p['object_id'],state='target_writing_candidate' if target else 'unknown_or_other_row',membership_state='writing_candidate' if strict else 'unknown',candidate_detected=bool(q),legacy_optional=bool(q and (q['small_detached_candidate'] or q['writing_membership']=='unknown')),legacy_native_bbox=q['native_bbox'] if q else None))
        result.append(dict(row_id=r['row_id'],mode='unchanged_V4_source_output',chosen_legacy_row=chosen['row_number'] if chosen else None,median_body_path_error_px=loss(chosen) if chosen else None,predicted_endpoints=[None,None],objects=objects,endpoint_note='V4 did not emit physical row endpoints; not imputed from a field rectangle.'))
    return result

def count_metrics(r,pr,parents):
    truth={p['object_id']:p for p in r['objects']};pred={p['object_id']:p for p in pr['objects']};target=[p for p in truth.values() if p['membership']=='confirmed_writing' and p['owner']=='target'];nwrite=[p for p in truth.values() if p['membership']=='confirmed_nonwriting'];allwrite=[p for p in truth.values() if p['membership']=='confirmed_writing'];resolved_assigned=[truth[o['object_id']] for o in pr['objects'] if o['state']=='target_writing_candidate' and truth[o['object_id']]['owner'] in ['target','neighbor','margin'] and truth[o['object_id']]['membership']=='confirmed_writing'];all_assigned=[truth[o['object_id']] for o in pr['objects'] if o['state']=='target_writing_candidate'];detached=[p for p in truth.values() if p['source_category']=='detached_mark_uncertain_attachment' and p['membership']=='confirmed_writing'];unresolved=[p for p in truth.values() if p['membership'] in ['unresolved','mixed_writing_and_unresolved']];knownparents=[p for p in parents if p['parent_boundary_status'] in ['confirmed_connected_trace','confirmed_photographic_join']]
    recovered=[p for p in knownparents if len(p['source_objects'])==1 and pred[p['source_objects'][0]]['state']=='target_writing_candidate']
    # Raster location support is shared with the mask-assisted reference. This
    # is whole reviewed-parent support recovery, not independent ink-pixel IoU.
    counts=dict(target_writing_recall=[sum(pred[p['object_id']]['state']=='target_writing_candidate' for p in target),len(target)],all_writing_membership_recall=[sum(pred[p['object_id']]['membership_state']=='writing_candidate' for p in allwrite),len(allwrite)],nonwriting_false_inclusion=[sum(pred[p['object_id']]['state']=='target_writing_candidate' for p in nwrite),len(nwrite)],nonwriting_membership_false_inclusion=[sum(pred[p['object_id']]['membership_state']=='writing_candidate' for p in nwrite),len(nwrite)],resolved_target_ownership_precision=[sum(p['owner']=='target' for p in resolved_assigned),len(resolved_assigned)],ownership_assignment_coverage=[len(resolved_assigned),len(allwrite)],assigned_membership_unresolved_rate=[sum(p['membership'] in ['unresolved','mixed_writing_and_unresolved'] for p in all_assigned),len(all_assigned)],reviewed_parent_recovery=[len(recovered),len(knownparents)],detached_writing_membership_recall=[sum(pred[p['object_id']]['membership_state']=='writing_candidate' for p in detached),len(detached)],detached_target_owner_recovery=[sum(pred[p['object_id']]['state']=='target_writing_candidate' for p in detached if p['owner']=='target'),sum(p['owner']=='target' for p in detached)],unknown_candidate_retention=[sum(pred[p['object_id']]['state']=='unknown_or_other_row' for p in unresolved),len(unresolved)])
    endpoint=[]
    for i,(value,status,interval) in enumerate(zip(pr['predicted_endpoints'],r['endpoint_status'],r['physical_endpoint_x_intervals'])):
        error=None if value is None or status!='resolved' else max(interval[0]-value,value-interval[1],0)
        endpoint.append(dict(side=['start','end'][i],predicted_x=value,reference_interval=interval,reference_status=status,error_px=error,correct=error is not None and error<=.25*r['body_proxy']))
    counts['endpoint_accuracy']=[sum(e['correct'] for e in endpoint),sum(e['reference_status']=='resolved' for e in endpoint)]
    counts['endpoint_prediction_coverage']=[sum(e['predicted_x'] is not None and e['reference_status']=='resolved' for e in endpoint),sum(e['reference_status']=='resolved' for e in endpoint)]
    return dict(row_id=r['row_id'],caption=r['caption'],split=r['split'],counts=counts,endpoint_details=endpoint,missing_confirmed_writing=[p['object_id'] for p in target if pred[p['object_id']]['state']!='target_writing_candidate'],false_included_nonwriting=[p['object_id'] for p in nwrite if pred[p['object_id']]['state']=='target_writing_candidate'],wrong_row_members=[p['object_id'] for p in resolved_assigned if p['owner']!='target'],parent_boundaries_unknown=sum(p['parent_boundary_status'] not in ['confirmed_connected_trace','confirmed_photographic_join'] for p in parents),confirmed_joins_not_recovered=sum(p['parent_boundary_status']=='confirmed_photographic_join' for p in knownparents),membership_mask_dependency='Source candidate masks shared with reference aids; recall is reviewed-object/whole-parent support, not manually painted chemical ink-pixel accuracy.')

def aggregate(records):
    out={};rng=np.random.default_rng(SEED+5);captions=sorted({r['caption'] for r in records});keys=records[0]['counts'].keys()
    for key in keys:
        bycap={c:np.sum([r['counts'][key] for r in records if r['caption']==c],axis=0) for c in captions};num,den=np.sum(list(bycap.values()),axis=0);samples=[]
        for _ in range(2000):
            s=np.sum([bycap[c] for c in rng.choice(captions,len(captions),replace=True)],axis=0)
            if s[1]:samples.append(float(s[0]/s[1]))
        out[key]=dict(numerator=int(num),denominator=int(den),rate=float(num/den) if den else None,caption_bootstrap95=np.percentile(samples,[2.5,97.5]).tolist() if samples else None,caption_clusters=len(captions))
    return out

def source_sequences(rows,classrows,predictions):
    byrow={r['row_id']:r for r in classrows};out=[]
    for gap in [.35,.55,.75]:
        for r in rows:
            parents=sorted(byrow[r['row_id']]['parents'],key=lambda p:(p['root_x'],p['native_bbox'][0],p['parent_id']));groups=[];current=[];right=-np.inf
            for p in parents:
                if current and p['native_bbox'][0]-right>gap*r['body_proxy']:groups.append(current);current=[];right=-np.inf
                current.append(p);right=max(right,p['native_bbox'][2])
            if current:groups.append(current)
            unknown=[p for p in r['objects'] if p['possible_target_owner'] and p['owner']=='unknown']
            for gi,ps in enumerate(groups):
                left=min(p['native_bbox'][0] for p in ps);right=max(p['native_bbox'][2] for p in ps);optional=[p for p in unknown if p['native_bbox'][0]<=right+.35*r['body_proxy'] and p['native_bbox'][2]>=left-.35*r['body_proxy']];ambiguous=any(p['parent_boundary_status'] not in ['confirmed_connected_trace','confirmed_photographic_join'] or p['order_status']!='body_root_supported' for p in ps);membership_complete=not optional and not ambiguous;tokens=[p['structural_class'] for p in ps];complete=membership_complete and 'UNK' not in tokens;mode_recovery={}
                for mode,prs in predictions.items():
                    pred={o['object_id']:o for o in next(q for q in prs if q['row_id']==r['row_id'])['objects']};mode_recovery[mode]=bool(complete and all(len(p['source_objects'])==1 and pred[p['source_objects'][0]]['state']=='target_writing_candidate' for p in ps))
                alternatives=[]
                ids={int(i[-3:]) for p in ps for i in p['source_objects'] if '_O' in i}
                for j in r['possible_joins']:
                    if ids.intersection(j):alternatives.append(dict(source_object_numbers=j,hypotheses=['separate_source_traces_if_gap_real','one_connected_parent_if_faint_contact_real'],joined_notation='UNK_COMPOUND',status='not_resolved_or_used_to_choose_a_class'))
                out.append(dict(row_id=r['row_id'],caption=r['caption'],split=r['split'],gap=gap,group_id=f'{r["row_id"]}_G{str(gap).replace(".","")}_{gi+1:03d}',native_x_extent=[left,right],parent_ids=[p['parent_id'] for p in ps],ordered_tokens=tokens,notation=' '.join(tokens)+(' [UNK_MEMBER]' if optional else '')+(' [UNK_BOUNDARY]' if ambiguous else ''),optional_source_objects=[p['object_id'] for p in optional],optional_types=[p['source_category'] for p in optional],membership_complete=membership_complete,class_complete='UNK' not in tokens,exact_sequence_complete=complete,boundary_or_order_ambiguous=ambiguous,competing_parent_hypotheses=alternatives,recovered_complete_sequence=mode_recovery,counterfactual_membership_complete_ignore_all_optional=not ambiguous,counterfactual_membership_complete_ignore_detached=not ambiguous and not [p for p in optional if p['source_category']=='possible_showthrough_or_extraction_artifact' or p['source_category']!='detached_mark_uncertain_attachment'],counterfactual_membership_complete_ignore_owner_uncertainty=not ambiguous and not [p for p in optional if p['membership']!='confirmed_writing']))
    return out

def recurrence(groups):
    out={}
    for gap in [.35,.55,.75]:
        rr=[g for g in groups if g['gap']==gap];complete=[g for g in rr if g['exact_sequence_complete']];dev={tuple(g['ordered_tokens']) for g in complete if g['split']=='development'};lex=defaultdict(set)
        for g in complete:lex[tuple(g['ordered_tokens'])].add(g['caption'])
        counters={}
        for length in [1,3]:
            cc=[g for g in complete if len(g['ordered_tokens'])>=length];held=[g for g in cc if g['split']=='heldout'];repeat=[g for g in cc if len(lex[tuple(g['ordered_tokens'])])>=2];matched=[g for g in held if tuple(g['ordered_tokens']) in dev];counters[str(length)]=dict(complete_groups=len(cc),repeated_cross_caption_groups=len(repeat),repeated_coverage=len(repeat)/len(cc) if cc else None,heldout_complete_groups=len(held),heldout_matches=len(matched),heldout_recurrence=len(matched)/len(held) if held else None)
        out[str(gap)]=dict(groups=len(rr),membership_complete_groups=sum(g['membership_complete'] for g in rr),class_complete_groups=sum(g['class_complete'] for g in rr),exact_complete_groups=len(complete),membership_complete_rate=sum(g['membership_complete'] for g in rr)/len(rr),exact_complete_rate=len(complete)/len(rr),boundary_or_order_ambiguity_rate=sum(g['boundary_or_order_ambiguous'] for g in rr)/len(rr),optional_membership_ambiguity_rate=sum(bool(g['optional_source_objects']) for g in rr)/len(rr),sensitivity={k:sum(g[k] for g in rr)/len(rr) for k in ['counterfactual_membership_complete_ignore_all_optional','counterfactual_membership_complete_ignore_detached','counterfactual_membership_complete_ignore_owner_uncertainty']},lengths=counters)
    return out

def main():
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen(source_stage=False)
    verify_source_seal();assert function_hashes()==read_json(D/'MEMBERSHIP_RULE_SEAL.json')['function_hashes'];rows=read_json(F/'source_reference.json')['rows'];classes=read_json(F/'parent_class_assignments.json')['rows'];byclass={r['row_id']:r['parents'] for r in classes};preds={'V4':legacy_predictions(rows),'V5_automatic':[],'V5_layout_assisted':[]}
    for r in rows:
        rgb,delta,cc=page_features(r);preds['V5_automatic'].append(predict(r,delta,cc));preds['V5_layout_assisted'].append(predict(r,delta,cc,True));print(r['row_id'],'sealed rules evaluated, no retuning',flush=True)
    write_json(F/'extraction_predictions.json',preds);results={}
    for mode,pr in preds.items():
        records=[count_metrics(r,p,byclass[r['row_id']]) for r,p in zip(rows,pr)];results[mode]=dict(rows=records,all=aggregate(records),development=aggregate([q for q in records if q['split']=='development']),heldout=aggregate([q for q in records if q['split']=='heldout']))
    write_json(T/'extraction_accuracy.json',results)
    groups=source_sequences(rows,classes,preds);write_json(F/'group_sequences.json',groups);metrics=recurrence(groups)
    rowmetrics=[]
    for r in rows:
        ps=byclass[r['row_id']];unk=[p for p in r['objects'] if p['possible_target_owner'] and p['owner']=='unknown'];rowmetrics.append(dict(row_id=r['row_id'],caption=r['caption'],split=r['split'],confirmed_parents=len(ps),assigned_v3_parents=sum(p['structural_class']!='UNK' for p in ps),unknown_class_parents=sum(p['structural_class']=='UNK' for p in ps),unknown_membership_spans=len(unk),membership_complete=not unk and all(p['parent_boundary_status'] in ['confirmed_connected_trace','confirmed_photographic_join'] and p['order_status']=='body_root_supported' for p in ps) and all(x=='resolved' for x in r['endpoint_status']),exact_complete=not unk and all(p['structural_class']!='UNK' and p['parent_boundary_status'] in ['confirmed_connected_trace','confirmed_photographic_join'] and p['order_status']=='body_root_supported' for p in ps) and all(x=='resolved' for x in r['endpoint_status']),ordered_tokens=[p['structural_class'] for p in sorted(ps,key=lambda p:p['root_x'])]))
    write_json(F/'row_sequences.json',rowmetrics);ps=[p for r in classes for p in r['parents']];tot=Counter(p['membership'] for r in rows for p in r['objects']);summary=dict(created_at_utc=datetime.now(timezone.utc).isoformat(),rows=16,captions=8,heldout_rows=4,heldout_captions=2,source_objects=sum(tot.values()),membership_states=dict(tot),confirmed_target_parents=len(ps),assigned_v3=sum(p['structural_class']!='UNK' for p in ps),unknown_v3_rate=sum(p['structural_class']=='UNK' for p in ps)/len(ps),classes=dict(Counter(p['structural_class'] for p in ps)),class_abstention_reasons=dict(Counter(reason for p in ps for reason in p['unknown_reasons'])),complete_membership_rows=sum(r['membership_complete'] for r in rowmetrics),complete_structural_rows=sum(r['exact_complete'] for r in rowmetrics),resolved_endpoint_fraction=sum(x=='resolved' for r in rows for x in r['endpoint_status'])/32,gap_hypotheses=metrics,source_group_boundary_accuracy='Spacing-hypothesis concordance and contact constraints only; no semantic group-boundary gold. All partitions prevent cuts through included whole parents; unresolved contacts/joins retained. Precision/recall of true word boundaries is unavailable.',reference_pixel_iou='Not asserted. Shared raster location aids make same-mask IoU non-independent; scored source-reviewed membership, ownership, confirmed joins, parent support, endpoint x intervals and exact sequences separately.',notation_practical=False)
    write_json(T/'sequence_completeness.json',summary);verify_source_seal();print('Summary',summary['confirmed_target_parents'],summary['assigned_v3'],summary['complete_structural_rows'],flush=True)
if __name__=='__main__':main()
