"""Separate observable coverage/ownership/classification gates without outcome fitting."""
from common import OUT,read_json,write_json,write_csv,SEED
from collections import Counter,defaultdict
import numpy as np
from validate_recurrence_structure_v3 import recurrence
ROOT=OUT/'data/observations/recurrence_v3_structural_candidate';TEST=OUT/'tests/recurrence_v3_development'

def main():
    from recurrence_guard_v3 import require_unfrozen
    require_unfrozen(ROOT)
    old=read_json(TEST/'v2_bottleneck_diagnosis.json');c=old['counts'];n=c['proposed_groups'];source=c['source_membership_accepted_groups'];family=c['source_accepted_with_all_old_families'];retained=c['old_final_eligible_fine_groups']
    ledger=[dict(gate='source_membership_or_boundary',lost=n-source,denominator=n),dict(gate='old_visual_family_gate_after_source_acceptance',lost=source-family,denominator=n),dict(gate='whole_row_extent_after_local_fine_completion',lost=family-retained,denominator=n),dict(gate='retained',lost=retained,denominator=n)]
    for r in ledger:r['fraction_of_proposals']=r['lost']/n
    rec=read_json(ROOT/'corroborated_parent_assignments.json');lookup={r['parent_id']:r for r in rec};groups=[r for r in read_json(ROOT/'competing_group_hypotheses.json') if r['gap_body']==.55];counts=Counter();bylength=defaultdict(list)
    for g in groups:
        ps=[lookup[i] for i in g['parent_ids']];raster=any(not p['class_eligible'] for p in ps);row_unknown=any(p['row_ownership']=='unknown' for p in ps);classes=any(not p['structural_class'] for p in ps)
        if raster:reason='unstable_or_unresolved_parent_raster'
        elif row_unknown:reason='competing_row_ownership'
        elif classes:reason='structural_class_or_perturbation_unknown'
        elif not g['structural_units']:reason='local_field_edge'
        else:reason='complete_retained_parent_list'
        counts[reason]+=1;bylength[len(ps)].append(bool(g['structural_units']))
    lengthrows=[dict(parent_count=k,candidates=len(v),complete_retained_lists=sum(v),completion_fraction=sum(v)/len(v)) for k,v in sorted(bylength.items())]
    # Pair audit confidence is blocked by held-out source caption, not independent pair.
    pairs=read_json(ROOT/'pair_audit_key.json');jj={r['pair_id']:r['judgment'] for r in read_json(ROOT/'pair_source_judgments_before_key.json')};bycap=defaultdict(list)
    for p in pairs:bycap[lookup[p['left_parent']]['folio_component']].append(p)
    rng=np.random.default_rng(SEED);caps=list(bycap);boot=[]
    for _ in range(3000):
        sample=[p for cap in rng.choice(caps,len(caps),replace=True) for p in bycap[cap]];pos=[p for p in sample if p['kind']=='positive'];diff=[p for p in sample if jj[p['pair_id']]=='different'];boot.append([sum(jj[p['pair_id']]=='same_structural_hypothesis' for p in pos)/len(pos),sum(p['kind']=='positive' for p in diff)/max(1,len(diff))])
    audit_ci=np.quantile(np.array(boot),[.025,.975],axis=0).tolist()
    result=dict(v2_observable_disjoint_gate_ledger=ledger,expanded_group_gate_ledger=dict(counts),expanded_parent_counts=dict(total=len(rec),raster_stable=sum(r['class_eligible'] for r in rec),corroborated_structural_class=sum(bool(r['structural_class']) for r in rec),unknown_class=sum(not r['structural_class'] for r in rec),row_ownership_unknown=sum(r['row_ownership']=='unknown' for r in rec)),completion_by_parent_count=lengthrows,
      source_pair_caption_bootstrap=dict(caption_groups=len(caps),columns=['positive_agreement','false_acceptance_among_source_different'],interval95=audit_ci,interpretation='Point-estimate freeze thresholds are preregistered; confidence intervals are descriptive and broad. This is one source adjudicator, not inter-rater validation.'),
      coverage_interpretation='Source review outside selected fields, small omitted detached ink, physical panel identity and true writing recall remain unknown. The direct disjoint ledger measures pipeline exclusions, not a causal manuscript-wide coverage percentage.',
      specificity_interpretation='Old fine-to-broad relabeling changes recurrence on identical old groups. New contour-subclass-to-structural grouping changes recurrence on identical new pixels and candidate boundaries. Neither comparison uses minimal pairs or positional outcomes.',
      main_diagnosis='The sparse downstream object was a complete assembled group sequence, not merely a recurring parent form. Source omissions/ownership uncertainty, conjunctive class admission over longer lists, overly fine type distinctions and competing boundaries each reduce sequence recurrence. Reusable parents do recur on held-out imagery, but whole retained group strings remain sparse and uncertified as words.')
    write_json(TEST/'bottleneck_accounting.json',result);write_csv(TEST/'completion_by_parent_count.csv',lengthrows);print(result['expanded_parent_counts'],counts,'pair caption intervals',audit_ci,flush=True)
    # Static scientific figure, no position or conventional findings.
    import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
    new=read_json(TEST/'expanded_coverage_specificity.json');fig,ax=plt.subplots(1,3,figsize=(14,4.7))
    names=['Source/\nboundary','Family\ngate','Whole-row\nextent','Retained'];ax[0].bar(names,[r['fraction_of_proposals']*100 for r in ledger],color=['#767b86','#6684a5','#aaa37b','#507467']);ax[0].set_ylabel('% of V2 proposed groups');ax[0].set_title('Observable V2 gate accounting')
    aa=new['matched_class_comparison']['0.55']['groups_at_least_three_parents'];ax[1].bar(['Contour\nsubclasses','Structural\nclasses'],[aa['premerge']['repeated_occurrence_fraction']*100,aa['structural']['repeated_occurrence_fraction']*100],color=['#6684a5','#507467']);ax[1].set_ylim(0,35);ax[1].set_ylabel('% occurrences in repeated lists');ax[1].set_title('Same 237 parent lists, ≥3 parents')
    cc=new['caption_subsampling_without_replacement'];ax[2].plot([r['captions'] for r in cc],[r['mean_premerge_repeated_fraction']*100 for r in cc],marker='o',label='Contour subclasses');ax[2].plot([r['captions'] for r in cc],[r['mean_structural_repeated_fraction']*100 for r in cc],marker='o',label='Structural classes');ax[2].set_xlabel('Source caption groups sampled');ax[2].set_ylabel('% occurrences in repeated lists');ax[2].legend();ax[2].set_title('Coverage growth, fixed taxonomy')
    fig.suptitle('Recurrence diagnosis: observed exclusions and matched source hypotheses');fig.tight_layout();fig.savefig(OUT/'figures/recurrence_v3/bottleneck_accounting.png',dpi=160);plt.close(fig)

if __name__=='__main__':main()
