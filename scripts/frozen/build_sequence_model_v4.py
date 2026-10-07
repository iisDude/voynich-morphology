"""Compile source-traceable partial sequences and evaluate registered support."""
from common import OUT,read_json,write_json,sha256
from register_sequence_v4 import D,T
from collections import Counter,defaultdict
from datetime import datetime,timezone
import numpy as np
F=OUT/'data/observations/visual_dataset_v4'
def fraction(n,d):return n/d if d else None
def block_interval(records,num,den,seed=20261009):
    caps=sorted({r['folio_component'] for r in records});rng=np.random.default_rng(seed)
    tallies=np.array([[sum(num(r) for r in records if r['folio_component']==c),sum(den(r) for r in records if r['folio_component']==c)] for c in caps],float)
    if not len(caps) or not tallies[:,1].sum():return None
    draws=rng.integers(0,len(caps),(1000,len(caps)));tot=tallies[draws].sum(axis=1);ok=tot[:,1]>0
    return np.quantile(tot[ok,0]/tot[ok,1],[.025,.975]).tolist()
def main():
    if (F/'FREEZE_MANIFEST.json').exists():raise RuntimeError('V4 immutable')
    F.mkdir(exist_ok=True);plan=read_json(D/'PLAN.json');rec=read_json(D/'source_parents.json');rows=read_json(D/'source_rows.json')
    pk={p['id']:p for p in read_json(D/'class_pair_key.json')};pj=read_json(D/'class_pair_judgments_before_key.json')['judgments']
    joined=[dict(**pk[j['id']],source_judgment=j['judgment']) for j in pj];pos=[p for p in joined if p['kind']=='positive'];different=[p for p in joined if p['source_judgment']=='different'];bad={p['parent_id'] for p in pos if p['source_judgment']!='same'}
    qk={r['id']:r for r in read_json(D/'membership_queue.json')};qj=read_json(D/'membership_queue_judgments_before_key.json')['judgments'];nonwriting={qk[j['id']]['parent_id'] for j in qj if j['membership']=='nonwriting'}
    for r in rec:
        r['source_adjudication']='nonwriting' if r['parent_id'] in nonwriting else 'writing_ownership_unknown' if any(qk[j['id']]['parent_id']==r['parent_id'] and j['membership']=='writing_ownership_unknown' for j in qj) else 'unknown' if any(qk[j['id']]['parent_id']==r['parent_id'] for j in qj) else 'not_individually_reviewed'
        if r['parent_id'] in bad:r['structural_class']=None;r['unknown_reasons'].append('audited_source_class_compatibility_unknown_or_failed')
        if r['parent_id'] in nonwriting:r['structural_class']=None;r['writing_membership']='nonwriting'
    write_json(F/'source_parent_states.json',rec)
    repeatkey=read_json(D/'class_repeat_key.json');repeatj={r['id']:r['judgment'] for r in read_json(D/'class_repeat_judgments_before_key.json')['judgments']};pjmap={r['id']:r['judgment'] for r in pj};rep= [dict(id=k['id'],original_id=k['original_id'],first=pjmap[k['original_id']],second=repeatj[k['id']]) for k in repeatkey]
    bkey=read_json(D/'boundary_repeat_key.json');l={r['id']:r for r in read_json(D/'boundary_judgments_L_before_key.json')['judgments']};m={r['id']:r for r in read_json(D/'boundary_judgments_M_before_key.json')['judgments']};bl={k['case_index']:l[k['id']] for k in bkey if k['id'].startswith('L')};bm={k['case_index']:m[k['id']] for k in bkey if k['id'].startswith('M')}
    contextkey=read_json(D/'repeatability_mask_key.json');ca={r['id']:r for r in read_json(D/'masked_context_judgments_A.json')['judgments']};cb={r['id']:r for r in read_json(D/'masked_context_judgments_B.json')['judgments']};first={k['sample_index']:ca[k['id']] for k in contextkey if k['id'].startswith('A')};second={k['sample_index']:cb[k['id']] for k in contextkey if k['id'].startswith('B')}
    fields=['drawing_contact_region','visible_body_rows','boundary_interpretation','detached_ownership','connected_parent_splitting','faint_ink'];ctx={f:sum(first[i][f]==second[i][f] for i in first)/len(first) for f in fields}
    repeat=dict(class_pair_count=len(rep),class_pair_agreement=sum(r['first']==r['second'] for r in rep)/len(rep),class_pairs=rep,local_gap_cases=len(bl),local_gap_visibility_agreement=sum(bl[i]['judgment']==bm[i]['judgment'] for i in bl)/len(bl),group_boundary_decision='unknown in both passes; no forced partition agreement claimed',context_count=len(first),coarse_context_agreement=ctx,not_independent_human_rater=True,previous_exposure_and_memory=True,exact_sequence_re_adjudication_agreement=None,limit='Local gap and structural compatibility judgments; exact full membership/partition repeatability not established.')
    write_json(T/'repeatability_results.json',repeat)
    clear=[r for r in rec if r['split']=='test' and r['class_eligible']];nom=[r for r in clear if r.get('nominal_accepted')];accepted=[r for r in clear if r['structural_class']];cc=defaultdict(list)
    for r in accepted:cc[r['structural_class']].append(r)
    cores={c:dict(test_instances=len(rr),test_captions=len({r['folio_component'] for r in rr})) for c,rr in cc.items()};corecount=sum(v['test_instances']>=5 and v['test_captions']>=3 for v in cores.values())
    cm=dict(test_caption_groups=len({r['folio_component'] for r in clear}),clear_test_parents=len(clear),nominal_accepted=len(nom),reliable_assigned=len(accepted),clear_test_assignment_coverage=fraction(len(accepted),len(clear)),threshold_assignment_stability=fraction(sum(r['threshold_stable'] for r in nom),len(nom)),alignment_assignment_stability=fraction(sum(r['alignment_stable'] for r in nom),len(nom)),source_positive_agreement=fraction(sum(p['source_judgment']=='same' for p in pos),len(pos)),source_different_pair_false_grouping=fraction(sum(p['kind']=='positive' for p in different),len(different)),source_pair_counts=dict(positive=Counter(p['source_judgment'] for p in pos),hard_negative=Counter(p['source_judgment'] for p in joined if p['kind']=='hard_negative')),source_positive_caption_interval=block_interval(pos,lambda p:p['source_judgment']=='same',lambda p:1),source_false_grouping_caption_interval=block_interval(different,lambda p:p['kind']=='positive',lambda p:1),recurring_core_class_count=corecount,classes=cores,audited_parents_abstained=len(bad),class_model_unchanged=True)
    cg=plan['class_generalization_gates'];classgates=dict(test_captions=cm['test_caption_groups']>=cg['test_captions_min'],recurring_classes=corecount>=cg['recurring_classes_min'],positive_agreement=cm['source_positive_agreement']>=cg['positive_pair_agreement_min'],false_grouping=cm['source_different_pair_false_grouping']<=cg['source_different_pair_false_grouping_max'],threshold_stability=cm['threshold_assignment_stability']>=cg['threshold_assignment_stability_min'],clear_test_coverage=cm['clear_test_assignment_coverage']>=cg['clear_test_class_coverage_min'])
    cm['gates']=classgates;write_json(T/'class_generalization.json',cm);write_json(T/'source_pair_results.json',joined)
    primary=defaultdict(list);optional=defaultdict(list);allrow=defaultdict(list)
    for r in rec:
        if r['writing_membership']=='nonwriting':continue
        k=(r['view_id'],r['row_number']);allrow[k].append(r)
        isprimary='_P' in r['parent_id'] and not r['small_detached_candidate'] and max(p['core_pixels'] for p in r['row_support'])>=8
        (primary if isprimary else optional)[k].append(r)
    rseq=[];groups=[];links=[];optgraph=[]
    for row in rows:
        if row['status']!='triaged_local_writing_field':continue
        k=(row['view_id'],row['row_number']);rr=sorted(primary[k],key=lambda r:(r['native_bbox'][0],r['native_bbox'][1],r['parent_id']));oo=optional[k];body=row['body_height'];tokens=[r['structural_class'] or 'UNK' for r in rr];adj=[]
        for a,b in zip(rr,rr[1:]):
            gap=(b['native_bbox'][0]-a['native_bbox'][2])/body
            possible_join=any(v['merge'] and v['native_bbox'][0]<=other['native_bbox'][0] and v['native_bbox'][2]>=other['native_bbox'][2] for this,other in [(a,b),(b,a)] for v in this.get('competing_rasters',[]))
            ambig=.35<gap<=.75 or possible_join or a['row_ownership']=='unknown' or b['row_ownership']=='unknown'
            adj.append(dict(parent_ids=[a['parent_id'],b['parent_id']],native_gap_pixels=b['native_bbox'][0]-a['native_bbox'][2],gap_body=gap,boundary_by_hypothesis={str(t):gap>t for t in [.35,.55,.75]},ambiguous=ambig,possible_connected_parent_across_gap=bool(possible_join),alternative_joined_state='UNK_COMPOUND' if possible_join else None,source_boundary='unknown',connected_parent_split=False))
        links.extend(dict(view_id=row['view_id'],row_number=row['row_number'],**a) for a in adj)
        for o in oo:
            x=(o['native_bbox'][0]+o['native_bbox'][2])/2;neighbors=sorted(rr,key=lambda p:min(abs(x-p['native_bbox'][0]),abs(x-p['native_bbox'][2])))[:2]
            optgraph.append(dict(parent_id=o['parent_id'],view_id=o['view_id'],default_row_number=o['row_number'],native_bbox=o['native_bbox'],state='UNK_OPTIONAL',alternatives=['nonwriting','independent_unknown_parent']+[f'attachment_to:{p["parent_id"]}' for p in neighbors],row_ownership_alternatives=[p['row_number'] for p in o['row_support']],canonical_choice=None))
        ordered=bool(rr) and all(r['row_ownership']!='unknown' and not r['field_edge'] and r['writing_membership']!='unknown' for r in rr) and not oo
        rseq.append(dict(**row,parent_ids=[r['parent_id'] for r in rr],sequence=tokens,optional_parent_ids=[o['parent_id'] for o in oo],ordered_candidate_sequence=bool(rr),model_membership_complete=ordered,source_membership_certified=False,fully_identified=ordered and 'UNK' not in tokens,ordering='Increasing native x; not inferred linguistic reading direction',alternative_row_ownership=[dict(parent_id=r['parent_id'],row_candidates=[p['row_number'] for p in r['row_support']]) for r in rr if r['row_ownership']=='unknown'],boundary_hypotheses=[.35,.55,.75]))
        for threshold in [.35,.55,.75]:
            partition=[]
            for i,r in enumerate(rr):
                if i==0 or adj[i-1]['gap_body']>threshold:partition.append([])
                partition[-1].append(r)
            for gi,gg in enumerate(partition):
                x0=min(r['native_bbox'][0] for r in gg);x1=max(r['native_bbox'][2] for r in gg);unc=[o for o in oo if o['native_bbox'][0]<=x1+.35*body and o['native_bbox'][2]>=x0-.35*body]
                membership=all(r['row_ownership']!='unknown' and not r['field_edge'] and r['writing_membership']!='unknown' for r in gg) and not unc
                membership_ignore_optional=all(r['row_ownership']!='unknown' and not r['field_edge'] and r['writing_membership']!='unknown' for r in gg)
                membership_ignore_row=all(not r['field_edge'] and 'oversize_compound_or_drawing' not in r['unknown_reasons'] for r in gg) and not unc
                gs=[r['structural_class'] or 'UNK' for r in gg];inside={r['parent_id'] for r in gg};boundaryamb=any(a['ambiguous'] and any(p in inside for p in a['parent_ids']) for a in adj)
                groups.append(dict(group_id=f'{row["view_id"]}_R{row["row_number"]:02d}_H{threshold}_G{gi+1:03d}',view_id=row['view_id'],row_number=row['row_number'],folio_component=row['folio_component'],split=row['split'],gap_body=threshold,parent_ids=[r['parent_id'] for r in gg],sequence=gs,native_bbox=[x0,min(r['native_bbox'][1] for r in gg),x1,max(r['native_bbox'][3] for r in gg)],optional_parent_ids=[o['parent_id'] for o in unc],model_membership_complete=membership,source_membership_certified=False,complete_sequence=membership and 'UNK' not in gs,boundary_ambiguity=bool(boundaryamb),membership_if_optional_ignored=membership_ignore_optional,membership_if_row_uncertainty_ignored=membership_ignore_row,observed_parent_count=len(gg),physical_group_status='competing source partition, not word',native_row_endpoints=None))
    write_json(F/'row_sequences.json',rseq);write_json(F/'competing_group_sequences.json',groups);write_json(F/'boundary_constraints.json',links);write_json(F/'optional_membership_constraints.json',optgraph)
    results=[];rng=np.random.default_rng(plan['seed'])
    for threshold in [.35,.55,.75]:
        gg=[g for g in groups if g['gap_body']==threshold];complete=[g for g in gg if g['complete_sequence']];caps_by_seq=defaultdict(set);devseq=set()
        for g in complete:
            caps_by_seq[tuple(g['sequence'])].add(g['folio_component'])
            if g['split']=='development':devseq.add(tuple(g['sequence']))
        long=[g for g in complete if len(g['sequence'])>=3];test=[g for g in complete if g['split']=='test'];testlong=[g for g in test if len(g['sequence'])>=3]
        for g in complete:g['cross_caption_repeat']=len(caps_by_seq[tuple(g['sequence'])])>1;g['heldout_seen_in_development']=tuple(g['sequence']) in devseq if g['split']=='test' else None
        # Conditional order null, preserves incomplete positions and group sizes; no shuffled UNK becomes observed ink.
        byline=defaultdict(list)
        for g in gg:byline[(g['view_id'],g['row_number'])].append(g)
        null=[]
        for iteration in range(200):
            ns=[]
            for line in byline.values():
                # Preserve UNK locations and each original group's completeness flag.
                flat=[s for g in line for s in g['sequence'] if s!='UNK'];rng.shuffle(flat);offset=0
                for g in line:
                    n=len(g['sequence']);seq=[]
                    for s in g['sequence']:
                        if s=='UNK':seq.append('UNK')
                        else:seq.append(flat[offset]);offset+=1
                    seq=tuple(seq)
                    if g['complete_sequence'] and n>=3:ns.append((seq,g['folio_component']))
            c=defaultdict(set)
            for s,cap in ns:c[s].add(cap)
            null.append(sum(len(c[s])>1 for s,cap in ns)/len(ns) if ns else None)
        nv=[x for x in null if x is not None];actual=fraction(sum(g['cross_caption_repeat'] for g in long),len(long))
        result=dict(gap_body=threshold,reviewed_rows=len(rseq),ordered_candidate_rows=sum(r['ordered_candidate_sequence'] for r in rseq),ordered_candidate_row_rate=fraction(sum(r['ordered_candidate_sequence'] for r in rseq),len(rseq)),usable_ordered_membership_row_rate=fraction(sum(r['model_membership_complete'] for r in rseq),len(rseq)),source_certified_row_rate=0.,groups=len(gg),model_complete_parent_membership_groups=sum(g['model_membership_complete'] for g in gg),complete_parent_membership_rate=fraction(sum(g['model_membership_complete'] for g in gg),len(gg)),source_certified_group_rate=0.,unknown_primary_parent_rate=fraction(sum(s=='UNK' for g in gg for s in g['sequence']),sum(len(g['sequence']) for g in gg)),unknown_all_candidate_rate=fraction(sum(r['structural_class'] is None for rr in allrow.values() for r in rr),sum(len(rr) for rr in allrow.values())),boundary_ambiguity_rate=fraction(sum(g['boundary_ambiguity'] for g in gg),len(gg)),complete_sequences=len(complete),fully_identified_group_rate=fraction(len(complete),len(gg)),complete_sequences_ge3=len(long),cross_caption_repeated_complete_sequence_coverage=fraction(sum(g['cross_caption_repeat'] for g in complete),len(complete)),cross_caption_repeated_complete_sequence_coverage_ge3=actual,repeated_complete_sequence_share_of_all_groups=fraction(sum(g['cross_caption_repeat'] for g in complete),len(gg)),heldout_complete_sequences=len(test),heldout_complete_sequences_ge3=len(testlong),heldout_recurrence=fraction(sum(g['heldout_seen_in_development'] for g in test),len(test)),heldout_recurrence_ge3=fraction(sum(g['heldout_seen_in_development'] for g in testlong),len(testlong)),heldout_ge3_caption_interval=block_interval(testlong,lambda g:g['heldout_seen_in_development'],lambda g:1),membership_rate_if_detached_faint_ignored=fraction(sum(g['membership_if_optional_ignored'] for g in gg),len(gg)),membership_rate_if_row_ownership_ignored=fraction(sum(g['membership_if_row_uncertainty_ignored'] for g in gg),len(gg)),order_shuffle_null_ge3=dict(iterations=200,mean=float(np.mean(nv)) if nv else None,interval=np.quantile(nv,[.025,.975]).tolist() if nv else None,p_upper=(1+sum(x>=actual for x in nv))/(1+len(nv)) if nv and actual is not None else None),limit='Model-complete means no retained detected membership ambiguity under this hypothesis. Photograph recall, row endpoints and exact physical group boundaries remain uncertified. Conditional recurrence is not notation qualification.')
        result['membership_caption_interval']=block_interval(gg,lambda g:g['model_membership_complete'],lambda g:1)
        results.append(result)
    write_json(F/'competing_group_sequences.json',groups);write_json(T/'sequence_metrics.json',results)
    primarylist=[r for rr in primary.values() for r in rr];optionallist=[r for rr in optional.values() for r in rr]
    accounting=dict(new_views=len(plan['selected_views']),proposed_fields=len(rows),triaged_retained_fields=len(rseq),excluded_fields=len(rows)-len(rseq),candidate_regions=len(rec),body_parent_proposals=len(primarylist),optional_detached_faint_regions=len(optionallist),source_adjudicated_nonwriting=len(nonwriting),primary_class_assigned=sum(r['structural_class'] is not None for r in primarylist),optional_regions_are_not_assumed_writing_units=True,primary_unknown_reasons=dict(Counter(z for r in primarylist if r['structural_class'] is None for z in r['unknown_reasons'])),coverage_limit='No denominator estimates unreviewed physical writing or all manuscript rows. 100 new captures overview-triaged; native audit samples only.',v3_immutable=True)
    write_json(T/'coverage_accounting.json',accounting)
    sg=plan['sequence_support_gates'];gates=dict(new_views=len(plan['selected_views'])>=sg['new_views_min'],new_row_fields=len(rseq)>=sg['new_row_fields_min'],fresh_test_captions=cm['test_caption_groups']>=sg['fresh_test_captions_min'],class_generalization=all(classgates.values()),repeatability=repeat['class_pair_agreement']>=sg['repeatability_min'] and repeat['local_gap_visibility_agreement']>=sg['repeatability_min'],exact_sequence_repeatability_established=False,native_row_endpoint_certification=False)
    pergap={str(r['gap_body']):dict(ordered_membership_rows=r['usable_ordered_membership_row_rate']>=sg['ordered_membership_rows_min'],complete_parent_membership=r['complete_parent_membership_rate']>=sg['complete_parent_membership_groups_min'],unknown_parent_rate=r['unknown_primary_parent_rate']<=sg['unknown_parent_rate_max'],boundary_ambiguity=r['boundary_ambiguity_rate']<=sg['boundary_ambiguity_rate_max'],fully_identified_groups=r['fully_identified_group_rate']>=sg['fully_identified_groups_min'],heldout_ge3_recurrence=r['heldout_recurrence_ge3'] is not None and r['heldout_recurrence_ge3']>=sg['heldout_complete_sequence_recurrence_ge3_min']) for r in results}
    qualified=all(gates.values()) and all(all(g.values()) for g in pergap.values())
    qualification=dict(evaluated_at_utc=datetime.now(timezone.utc).isoformat(),global_gates=gates,per_gap_gates=pergap,qualified_as_practical_notation=qualified,downstream_support=qualified,freeze_status='Partial source sequence evidence freeze; practical notation qualification failed' if not qualified else 'Qualified source sequence notation',no_conventional_inputs_inspected=True,preregistered_support_sha256=sha256(D/'PLAN.json'),interpretation='Frozen V3 classes can label some source parents, but this V4 does not establish complete, stable manuscript sequences. A partial observational representation with coordinates and unknown constraints is supported; an independent functional notation is not yet established.' if not qualified else 'Support gates passed')
    write_json(T/'qualification.json',qualification);write_json(F/'model_contract.json',dict(version='V4',v3_immutable_manifest_sha256=plan['v3_manifest_sha256'],v3_class_model_sha256=plan['v3_model_sha256'],taxonomy='Frozen14 V3 core classes; ST09 experimental/UNK',notation='STnn or UNK in a candidate native-x parent order; optional UNK states and alternative ownership/partitions are separate constraint graphs. Not letters, words or graphemes.',boundary_hypotheses=[.35,.55,.75],parent_atomicity='unknown',native_row_endpoints='unknown; local field is not line',qualification=qualification,observed='Native pixel regions, geometry, connected threshold parents and visibility judgments',hypothesized='Parent-to-writing membership, structural compatibility, optional ownership and gap partition',forbidden_inputs=plan['prohibited_inputs']))
    print(accounting,flush=True);print(cm,flush=True);print(results,flush=True);print(qualification,flush=True)
if __name__=='__main__':main()
