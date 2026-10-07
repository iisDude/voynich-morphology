"""Spacing-partition recovery, explicitly distinct from word-boundary truth."""
from common import read_json,write_json
from register_row_benchmark_v5 import T,F
from evaluate_row_benchmark_v5 import aggregate
from collections import defaultdict
import numpy as np

def main():
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen(source_stage=False)
    rows=read_json(F/'source_reference.json')['rows'];classrows={r['row_id']:r['parents'] for r in read_json(F/'parent_class_assignments.json')['rows']};groups=read_json(F/'group_sequences.json');preds=read_json(F/'extraction_predictions.json');result={}
    for gap in [.35,.55,.75]:
        modes={}
        for mode,pr in preds.items():
            records=[]
            for r,pred in zip(rows,pr):
                truth={p['object_id']:p for p in r['objects']};accepted=[truth[p['object_id']] for p in pred['objects'] if p['state']=='target_writing_candidate'];accepted.sort(key=lambda p:(p['native_bbox'][0],p['native_bbox'][2]));pg={};ng=0;right=-np.inf
                for p in accepted:
                    if p['native_bbox'][0]-right>gap*r['body_proxy']:ng+=1
                    pg[p['object_id']]=ng;right=max(p['native_bbox'][2],right) if p['native_bbox'][0]-right<=gap*r['body_proxy'] else p['native_bbox'][2]
                tg={pid:g['group_id'] for g in groups if g['row_id']==r['row_id'] and g['gap']==gap for pid in g['parent_ids']};parents=sorted(classrows[r['row_id']],key=lambda p:p['root_x']);pairs=[]
                for a,b in zip(parents,parents[1:]):
                    eligible=all(p['parent_boundary_status'] in ['confirmed_connected_trace','confirmed_photographic_join'] and p['order_status']=='body_root_supported' for p in [a,b]);gold=tg[a['parent_id']]!=tg[b['parent_id']];seen=eligible and len(a['source_objects'])==len(b['source_objects'])==1 and a['source_objects'][0] in pg and b['source_objects'][0] in pg;value=pg[a['source_objects'][0]]!=pg[b['source_objects'][0]] if seen else None
                    pairs.append(dict(left_parent=a['parent_id'],right_parent=b['parent_id'],source_gap_cut=gold,source_parent_boundary_resolved=eligible,both_parents_recovered=bool(seen),predicted_gap_cut=value))
                sc=[p for p in pairs if p['source_parent_boundary_resolved']];seen=[p for p in sc if p['both_parents_recovered']];tp=sum(p['source_gap_cut'] and p['predicted_gap_cut'] for p in seen);pc=sum(bool(p['predicted_gap_cut']) for p in seen);gold=sum(p['source_gap_cut'] for p in sc)
                records.append(dict(row_id=r['row_id'],caption=r['caption'],split=r['split'],counts=dict(resolved_pair_recovery=[len(seen),len(sc)],conditional_gap_cut_precision=[tp,pc],all_resolved_source_gap_cut_recall=[tp,gold],matched_pair_partition_agreement=[sum(p['source_gap_cut']==p['predicted_gap_cut'] for p in seen),len(seen)]),source_pairs=len(pairs),ambiguous_source_pairs=len(pairs)-len(sc),false_group_splits=sum(not p['source_gap_cut'] and p['predicted_gap_cut'] for p in seen),false_group_merges=sum(p['source_gap_cut'] and p['predicted_gap_cut'] is False for p in seen),pairs=pairs))
            modes[mode]=dict(rows=records,all=aggregate(records),heldout=aggregate([r for r in records if r['split']=='heldout']))
        result[str(gap)]=modes
    write_json(T/'gap_partition_concordance.json',dict(gap_hypotheses=result,scope='Operational source-parent extent spacing partitions, with no-cut-overhang constraint, under fixed benchmark body proxies. Precision/recall here refer to these hypotheses on resolved adjacent parent pairs, not photographed word/grapheme boundaries. Missing parents reduce pair recovery and all-source-cut recall; unknown contacts excluded and counted. Archived V4 membership output is repartitioned for this diagnostic, not changed.'))
    print('Measured3 separate source-gap partition concordances',flush=True)
if __name__=='__main__':main()
