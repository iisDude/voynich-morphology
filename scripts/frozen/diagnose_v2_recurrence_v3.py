"""Coverage/classification bottlenecks in V2. No comparison/position outcomes."""
from common import OUT,read_json,write_json,write_csv
from collections import Counter,defaultdict

def support(sequences):
    freq=Counter(tuple(s) for s in sequences if s);n=sum(freq.values());repeated=sum(v for v in freq.values() if v>=2)
    return dict(occurrences=n,distinct_sequences=len(freq),singleton_sequences=sum(v==1 for v in freq.values()),repeated_occurrence_fraction=repeated/max(1,n),maximum_frequency=max(freq.values(),default=0))

def main():
    from recurrence_guard_v3 import require_unfrozen
    require_unfrozen(OUT/'data/observations/recurrence_v3_development')
    root=OUT/'data/observations/visual_dataset_v2';dest=OUT/'tests/recurrence_v3_development';groups=read_json(root/'assay_groups_source_only.json');components={}
    for path in root.glob('V_*.json'):
        obj=read_json(path)
        for field in obj['writing_fields']:
            for r in field['components']:components[r['instance_id']]=r
    count=Counter();class_unknown=Counter();matched=[];local=[];source_rows=set();reviewed_captures=set();counts_by_capture=[]
    for g in groups:
        count['proposed_groups']+=1;source_rows.add(g['line_id']);reviewed_captures.add(g['view_id']);parts=[components[i] for i in g['member_ids']];clean=bool(parts and all(r['status']=='writing_candidate' for r in parts));admit=bool(parts and all(r.get('admitted') for r in parts));source_gate=g['writing_membership']!='unknown'
        count['local_components_clean_groups']+=clean;count['source_membership_accepted_groups']+=source_gate;count['full_row_extent_eligible_slots']+=g['primary_eligible'];count['source_accepted_with_all_old_families']+=bool(source_gate and admit);count['old_final_fine_sequence_groups']+=bool(g['visual_fine_units']);count['old_final_eligible_fine_groups']+=bool(g['primary_eligible'] and g['visual_fine_units'])
        if clean:
            local.append(dict(group_id=g['group_id'],view_id=g['view_id'],folio_component=g['folio_component'],component_count=len(parts),fine=[r.get('fine_family') for r in parts] if admit else None,broad=[r.get('broad_family') for r in parts] if admit and all(r.get('broad_family') for r in parts) else None,complete_source_membership=source_gate))
        if source_gate and admit:matched.append(g)
        for r in parts:
            if r['status']=='writing_candidate' and not r.get('admitted'):class_unknown['clear_candidate_component_rejected_by_family_gate']+=1
            elif r['status']=='unknown':class_unknown['unknown_component_ownership_or_contact']+=1
    seqfine=[g['visual_fine_units'] for g in matched];seqbroad=[g['visual_merged_units'] for g in matched];seqfact=[g['visual_factored_units'] for g in matched]
    bycap=defaultdict(list)
    for g in groups:bycap[g['view_id']].append(g)
    for v,gg in sorted(bycap.items()):counts_by_capture.append(dict(view_id=v,proposed=len(gg),source_accepted=sum(g['writing_membership']!='unknown' for g in gg),fine_complete=sum(bool(g['visual_fine_units']) for g in gg)))
    result=dict(counts=dict(count),unique_proposed_rows=len(source_rows),captures_with_reviewed_group_proposals=len(reviewed_captures),total_source_captures=204,source_review_capture_fraction=len(reviewed_captures)/204,component_occurrence_losses=dict(class_unknown),matched_membership_cohort=dict(groups=len(matched),fine=support(seqfine),broad=support(seqbroad),factored=support(seqfact)),all_local_clean_proposals=dict(groups=len(local),fine=support([r['fine'] for r in local]),broad=support([r['broad'] for r in local])),attribution='Direct observable sequential gate accounting; local clean mask is not certified recall. Coverage outside reviewed fields and recovered source writing cannot be estimated from accepted identities. Coarse relabeling on a fixed cohort isolates classifier-specific sequence distinctions but is not an accuracy-validated merge.',causal_limit='Nonrandom uncertainty samples, interacting membership/classification losses, and no ground-truth inventory prevent a manuscript-wide percentage causally attributable to coverage versus classification. Expanded ordinary corpus and matched-size curves are required.',no_forbidden_inputs_read=True)
    write_json(dest/'v2_bottleneck_diagnosis.json',result);write_json(dest/'v2_local_component_cohort.json',local);write_csv(dest/'v2_coverage_by_capture.csv',counts_by_capture);print(result,flush=True)
if __name__=='__main__':main()
