"""Optional-region decomposition, failure attribution and conditional nulls."""
from common import OUT,read_json,write_json,SEED
from register_row_benchmark_v5 import T,F,G
from map_frozen_classes_v5 import verify_source_seal
from collections import Counter,defaultdict
import numpy as np

def main():
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen(source_stage=False)
    verify_source_seal();rows=read_json(F/'source_reference.json')['rows'];pred=read_json(F/'extraction_predictions.json');classes=read_json(F/'parent_class_assignments.json')['rows'];groups=read_json(F/'group_sequences.json');lookup={r['row_id']:r for r in rows};optional=[]
    for r,pr in zip(rows,pred['V4']):
        byid={p['object_id']:p for p in r['objects']}
        for o in pr['objects']:
            if not o['legacy_optional']:continue
            p=byid[o['object_id']];optional.append(dict(row_id=r['row_id'],caption=r['caption'],split=r['split'],object_id=p['object_id'],native_bbox=p['native_bbox'],raster=p['raster'],reference_membership=p['membership'],reference_owner=p['owner'],source_category=p['source_category'],possible_target_owner=p['possible_target_owner']))
    write_json(T/'optional_region_source_adjudication.json',dict(objects=optional,counts=dict(Counter(p['reference_membership'] for p in optional)),writing_owners=dict(Counter(p['reference_owner'] for p in optional if p['reference_membership']=='confirmed_writing')),source_types=dict(Counter(p['source_category'] for p in optional)),interpretation='Optional means detector/extraction uncertainty, not automatically writing. Confirmed surface/drawing and actual writing both occur. Diffuse masks may combine real writing and substrate/row contacts. Show-through cannot generally be identified chemically from these photographs; unresolved remains unresolved.'))
    reasons=Counter();bycaption={};allparents=[]
    for r in classes:
        ps=r['parents'];allparents.extend(ps);bycaption[r['row_id']]=dict(caption=r['caption'],split=r['split'],confirmed_source_parents=len(ps),stable_v3_assigned=sum(p['structural_class']!='UNK' for p in ps),nominal_fit=sum(p.get('nominal_accepted',False) for p in ps),raster_stable=sum(p.get('raster_stable',False) for p in ps),threshold_class_stable=sum(p.get('threshold_class_stable',False) for p in ps),alignment_class_stable=sum(p.get('alignment_class_stable',False) for p in ps))
        for p in ps:
            if p['structural_class']!='UNK':continue
            for condition,name in [('nominal_accepted','frozen_radius_margin_or_topology_fit_abstention'),('raster_stable','threshold_connectivity_or_topology_instability'),('threshold_class_stable','class_changes_or_abstains_under_threshold'),('alignment_class_stable','class_changes_or_abstains_under_fixed_slant')]:
                if condition not in p:continue
                if not p[condition]:reasons[name]+=1
            if 'frozen_v3_geometry_or_primary_connectivity' in p['unknown_reasons']:reasons['frozen_geometry_or_disconnected_source_join']+=1
    write_json(T/'class_abstention_diagnosis.json',dict(rows=bycaption,overlapping_failure_counts=dict(reasons),reason_counts_not_additive=True,v3_unchanged=True,interpretation='Source confirmation improves membership confidence but does not force V3 assignment. Whole connected compounds, faint connectivity, radius/margin rejection and perturbation instability retain UNK. Class coverage here is in-domain use of a frozen model on previously source-covered captures, not a fresh independent class validation.'))
    rng=np.random.default_rng(SEED+5);nulls={};byrow={r['row_id']:r['parents'] for r in classes}
    for gap in [.35,.55,.75]:
        gg=[g for g in groups if g['gap']==gap];draws=[]
        for _ in range(200):
            shuffled={}
            for rid,ps in byrow.items():
                known=[p for p in ps if p['structural_class']!='UNK'];values=[p['structural_class'] for p in known];rng.shuffle(values);shuffled.update({p['parent_id']:v for p,v in zip(known,values)})
            complete=[(g,tuple(shuffled.get(p,'UNK') for p in g['parent_ids'])) for g in gg if g['exact_sequence_complete']];lex=defaultdict(set);dev=set()
            for g,t in complete:lex[t].add(g['caption']);dev.update([t] if g['split']=='development' else [])
            for length in [1,3]:
                cc=[(g,t) for g,t in complete if len(t)>=length];held=[(g,t) for g,t in cc if g['split']=='heldout'];draws.append(dict(length=length,complete_n=len(cc),repeated=sum(len(lex[t])>=2 for g,t in cc),heldout_n=len(held),heldout_matches=sum(t in dev for g,t in held)))
        nulls[str(gap)]={str(length):dict(draws=200,complete_groups=next(q['complete_n'] for q in draws if q['length']==length),repeated_counts=np.percentile([q['repeated'] for q in draws if q['length']==length],[2.5,50,97.5]).tolist(),heldout_n=next(q['heldout_n'] for q in draws if q['length']==length),heldout_match_counts=np.percentile([q['heldout_matches'] for q in draws if q['length']==length],[2.5,50,97.5]).tolist(),informative=any(q['length']==length and q['complete_n']>0 for q in draws)) for length in [1,3]}
    write_json(T/'conditional_source_sequence_null.json',dict(nulls=nulls,method='200 within-row permutations of known V3 labels; preserves class frequencies by row, native geometry/group sizes, UNK locations and source completeness flags. No resegmentation or class fitting.',interpretation='No complete length3+ group exists; its null is degenerate and supplies no evidence for notation/language. Single-unit repetitions are structural-class recurrence, not usable multi-unit sequence recurrence.'))
    # Traceability and conservation checks with explicit scope limits.
    ids=[p['object_id'] for r in rows for p in r['objects']];assert len(ids)==len(set(ids));assert all(p['membership'] in ['confirmed_writing','confirmed_nonwriting','unresolved','mixed_writing_and_unresolved'] for r in rows for p in r['objects'])
    core={f'ST{i:02d}' for i in range(1,16)}-{'ST09'};assert all(p['structural_class']=='UNK' or p['structural_class'] in core for p in allparents)
    for r in rows:
        ps=byrow[r['row_id']];assigned=[q for p in ps for q in p['source_objects']];confirmed=[p['object_id'] for p in r['objects'] if p['membership']=='confirmed_writing' and p['owner']=='target'];assert sorted(assigned)==sorted(confirmed),r['row_id']
        for gap in [.35,.55,.75]:assert sorted(p for g in groups if g['row_id']==r['row_id'] and g['gap']==gap for p in g['parent_ids'])==sorted(p['parent_id'] for p in ps)
    stale=[]
    for r in read_json(OUT/'data/observations/row_benchmark_v5_development/development_object_location_aids.json')['rows']:
        maxpage=(len(r['objects'])+47)//48
        for f in G.glob(r['row_id']+'_objects_*.png'):
            if int(f.stem.split('_')[-1])>maxpage:stale.append(str(f.relative_to(OUT)))
    write_json(T/'artifact_roles.json',dict(superseded_provisional_object_atlases=stale,reason='Earlier B002 provisional band followed another physical row; superseded before source annotation. These are historical aids, not source reference or class evidence.',active='Current large/small mosaics, source locators, raw contexts, contact crops and repeat RGB aids; frozen source_reference.json defines the reference.'))
    write_json(T/'conservation_checks.json',dict(source_objects=len(ids),unique_source_objects=len(set(ids)),confirmed_target_parent_objects=sum(len(p['source_objects']) for p in allparents),connected_parents=len(allparents),three_partitions_conserve_all_confirmed_parent_ids=True,source_reference_hashes_unchanged=True,all_assigned_classes_frozen_core=True,confirmed_parent_recall_not_ink_pixel_truth=True,semantic_word_boundary_ground_truth=False))
    verify_source_seal();print('Optional cases',Counter(p['reference_membership'] for p in optional),'abstentions',dict(reasons),flush=True)
if __name__=='__main__':main()
