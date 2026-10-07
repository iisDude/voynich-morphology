"""Native RGB pair judgments, recorded before reading the audit key."""
from common import OUT,read_json,write_json
from collections import Counter
ROOT=OUT/'data/observations/recurrence_v3_development'
# Visual structural sameness is a grouping hypothesis, not linguistic equivalence.
DIFFERENT={9:'Lower connected construction differs or parent ownership is not interchangeable',19:'Lower branches/repeated trough structure differs',35:'Compact two-arch parent versus longer assembly',40:'Tall upper assembly and lower attachment differ',65:'Open curved parent with extra connected descending trace',77:'Open frame/terminal versus upward/downward curl assembly'}
UNKNOWN={7:'Faint leading contour and trough contacts cannot be decided',21:'Lower contour ownership/contact uncertain',30:'Pale contour cannot certify branches',37:'Filled upper region prevents loop comparison',43:'Faint narrow trace versus background/adjacent mark unresolved',46:'Horizontal bridge versus sloping terminal contact ambiguous',48:'Filled left region hides possible loop',54:'Lower-loop closure ambiguous',60:'Faint small trace does not establish connectivity',61:'Pale source cannot decide leading contour',62:'Upper loop closure unclear',67:'Faint narrow trace is insufficient',72:'Neighboring repeated arch/loop ownership unclear',76:'Filled upper region hides loop closure'}

def main():
    from recurrence_guard_v3 import require_unfrozen
    require_unfrozen(ROOT)
    judgments=[dict(pair_id=f'A{i:03d}',judgment='different' if i in DIFFERENT else 'unknown' if i in UNKNOWN else 'same_structural_hypothesis',reason=DIFFERENT.get(i,UNKNOWN.get(i,'Same visible contour/connectivity organization with width, slant, ink density or relative proportion variation')),basis='Direct native RGB pair gallery, candidate class/positive-negative labels hidden; no transcription, Currier, group recurrence or position',confidence='tentative' if i in UNKNOWN else 'source-supported local hypothesis') for i in range(1,81)]
    write_json(ROOT/'pair_source_judgments_before_key.json',judgments)
    pairs=read_json(ROOT/'pair_audit_key.json');lookup={r['pair_id']:r for r in judgments};table=Counter((p['kind'],lookup[p['pair_id']]['judgment']) for p in pairs)
    pos=sum(v for (k,j),v in table.items() if k=='positive');neg=sum(v for (k,j),v in table.items() if k=='hard_negative');true_diff=sum(v for (k,j),v in table.items() if j=='different')
    result=dict(counts={f'{k}:{j}':v for (k,j),v in table.items()},positive_agreement=table['positive','same_structural_hypothesis']/pos,apparent_hard_negative_same_structure_fraction=table['hard_negative','same_structural_hypothesis']/neg,
      false_acceptance_among_source_judged_different_pairs=table['positive','different']/max(1,true_diff),definition='Model-class-different nearest neighbors are proposed hard negatives, not ground truth. Same-structure judgment on a proposed negative measures false separation. Actual false acceptance uses source-judged different pairs. Unknowns are not positive agreement.',independent_raters=1,limitation='Single-agent source judgments, not independent inter-rater reproducibility. Native crops can include adjacent ink; uncertain parent ownership remains unknown.',freeze_allowed=False,freeze_failure='Threshold assignment stability below registered minimum; pair audit may also expose over-specific partitions/false acceptance.')
    write_json(ROOT/'pair_audit_results.json',result);print(result,flush=True)

if __name__=='__main__':main()
