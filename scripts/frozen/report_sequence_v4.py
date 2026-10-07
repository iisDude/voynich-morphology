from common import OUT,read_json,write_json,sha256
from register_sequence_v4 import D,T
from build_sequence_model_v4 import F
from PIL import Image,ImageDraw
from collections import Counter
import numpy as np,html
def pct(v):return 'unavailable' if v is None else f'{v*100:.1f}%'
def main():
    if (F/'FREEZE_MANIFEST.json').exists():raise RuntimeError('Frozen')
    metrics=read_json(T/'sequence_metrics.json');cm=read_json(T/'class_generalization.json');a=read_json(T/'coverage_accounting.json');rp=read_json(T/'repeatability_results.json');qualification=read_json(T/'qualification.json');parents=read_json(F/'source_parent_states.json');rows=read_json(F/'row_sequences.json');plan=read_json(D/'PLAN.json')
    byid={r['parent_id']:r for r in parents};gg=OUT/'figures/sequence_v4/examples';gg.mkdir(exist_ok=True)
    chosen=[]
    for lo,hi in [(4,55),(55,106),(106,157),(157,208)]:
        rr=[r for r in rows if lo<=int(r['view_id'][2:])<hi];used=set()
        for r in rr:
            if r['view_id'] in used:continue
            used.add(r['view_id']);chosen.append(r)
            if len(used)==3:break
    sections=[]
    for i,r in enumerate(chosen):
        xa,xb=r['safe_x'];_,y0,_,y1=r['native_bbox'];box=[xa,y0,xb,y1];im=Image.open(OUT/r['native_source']).convert('RGB').crop(box);dr=ImageDraw.Draw(im)
        for pid in r['parent_ids']:
            p=byid[pid];x,y,x1,y2=p['native_bbox'];dr.rectangle([x-xa,y-y0,x1-xa,y2-y0],outline='#009aaa' if p['structural_class'] else '#ee8b00',width=1)
        im.save(gg/f'field_{i+1:02d}.png');seq=' '.join(r['sequence']);sections.append(f'<article><h2>{r["view_id"]} / proposed field {r["row_number"]}</h2><p>Native bbox {box}. Increasing pixel x; row endpoints unknown.</p><img src="../figures/sequence_v4/examples/field_{i+1:02d}.png" alt="Native source field; cyan class-assigned and orange unknown candidate parents"><pre>{html.escape(seq)}</pre><p>{len(r["optional_parent_ids"])} unresolved optional regions; three gap partitions retained. This is a candidate list, not a complete physical row.</p><details><summary>Traceable parent coordinates and states</summary><pre>{html.escape(chr(10).join(pid+" "+str(byid[pid]["native_bbox"])+" "+(byid[pid]["structural_class"] or "UNK") for pid in r["parent_ids"]))}</pre></details></article>')
    page='<!doctype html><html><head><meta charset="utf-8"><title>V4 partial source sequences</title><style>body{max-width:1300px;margin:30px auto;padding:0 22px;font:17px system-ui;line-height:1.5;background:#faf8f1;color:#242b30}article{margin:30px 0;padding:20px;background:white;border:1px solid #ccc}img{max-width:100%;height:auto}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px monospace}h1,h2{line-height:1.2}</style></head><body><h1>V4 source sequence evidence</h1><p>Frozen V3 class labels plus explicit unknown parents and optional membership constraints. Practical independent notation qualification failed. Cyan and orange boxes refer to whole raster proposals, which may be compounds; no letters or words asserted.</p>'+''.join(sections)+'</body></html>'
    (OUT/'reports/14_source_sequence_examples_v4.html').write_text(page,encoding='utf-8')
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(12,4.5));x=np.arange(3)
    axes[0].bar(x,[r['complete_parent_membership_rate']*100 for r in metrics],color='#447c8a',label='No detected membership ambiguity')
    axes[0].bar(x,[r['fully_identified_group_rate']*100 for r in metrics],color='#c58d36',label='Also all classes known')
    axes[0].set(xticks=x,xticklabels=['0.35','0.55','0.75'],xlabel='Gap / body height',ylabel='Candidate groups (%)',ylim=(0,100),title='Group completeness under each hypothesis');axes[0].legend(fontsize=8)
    axes[1].bar(x,[r['complete_parent_membership_rate']*100 for r in metrics],width=.35,color='#447c8a',label='Optional regions retained')
    axes[1].bar(x+.35,[r['membership_rate_if_detached_faint_ignored']*100 for r in metrics],width=.35,color='#999',label='Optional regions ignored: sensitivity only')
    axes[1].set(xticks=x+.175,xticklabels=['0.35','0.55','0.75'],xlabel='Gap / body height',ylabel='Candidate groups (%)',ylim=(0,100),title='Detached / faint uncertainty contribution');axes[1].legend(fontsize=8)
    fig.tight_layout();fig.savefig(OUT/'figures/sequence_v4/sequence_completeness.png',dpi=160);plt.close(fig)
    table='| Gap/body | Usable ordered membership rows | Complete detected membership groups | Unknown primary proposals | Boundary ambiguous groups | Fully identified groups | Complete lists ≥3 | Cross-caption repeat ≥3 | Fresh held-out repeat ≥3 |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|\n'
    for r in metrics:table+=f'| {r["gap_body"]:.2f} | {pct(r["usable_ordered_membership_row_rate"])} | {pct(r["complete_parent_membership_rate"])} | {pct(r["unknown_primary_parent_rate"])} | {pct(r["boundary_ambiguity_rate"])} | {pct(r["fully_identified_group_rate"])} | {r["complete_sequences_ge3"]} | {pct(r["cross_caption_repeated_complete_sequence_coverage_ge3"])} | {pct(r["heldout_recurrence_ge3"])} ({r["heldout_complete_sequences_ge3"]} lists) |\n'
    sensitivity='| Gap/body | Membership with optional regions retained | If detached/faint regions ignored | If row-ownership uncertainty ignored | Repeated complete lists / all candidate groups |\n|---|---:|---:|---:|---:|\n'
    for r in metrics:sensitivity+=f'| {r["gap_body"]:.2f} | {pct(r["complete_parent_membership_rate"])} | {pct(r["membership_rate_if_detached_faint_ignored"])} | {pct(r["membership_rate_if_row_ownership_ignored"])} | {pct(r["repeated_complete_sequence_share_of_all_groups"])} |\n'
    nulltable='| Gap/body | Actual cross-caption repeat ≥3 | Conditional row-order shuffle mean | 95% null interval | Upper-tail fraction |\n|---|---:|---:|---|---:|\n'
    for r in metrics:
        n=r['order_shuffle_null_ge3'];nulltable+=f'| {r["gap_body"]:.2f} | {pct(r["cross_caption_repeated_complete_sequence_coverage_ge3"])} | {pct(n["mean"])} | {n["interval"]} | {n["p_upper"]} |\n'
    report=f'''# V4 source-only sequence evidence and support assessment

V4 preserves source-traceable candidate sequences of the frozen V3 structural classes, with `UNK`, optional membership states, alternative row ownership, possible connected compounds and all three gap partitions. **This V4 does not qualify as a practical independent manuscript notation.** V3 was neither altered nor retuned. No Currier, conventional strings, positional outcomes or minimal-pair support entered selection, ownership or class assignment.

## Source expansion and preregistration

The protocol selected **{a['new_views']} additional native Yale captures and {a['proposed_fields']} proposed row fields** using source geometry. {a['triaged_retained_fields']} local fields remained after {a['excluded_fields']} drawing/empty-field exclusions. Together with the 61 V3-triaged captures this reaches 161 of the 204 cached manuscript captures, as overview coverage only. Caption groups {', '.join(plan['fresh_caption_reserve'])} were held out from V4 development and excluded from all V3 selected captions. Some inherited split names were reassigned for V4 holdout because the entire caption had been outside V3; the class fit was never updated. These are fresh caption groups relative to that corpus, not globally unseen photographs or certified bifolio/panel identities.

Every selected view received source-overview triage. Native RGB inspection comprised 24 preregistered row contexts twice, 60 prioritized membership cases, 80 source structural pairs, 12 repeated structural pairs and 23 local adjacency contexts twice. The missing 24th adjacency case had fewer than two eligible primary proposals; it was not replaced. This scope does **not** certify every physical line or every ink region on 100 pages. The maximum advertised Yale images were already cached and frozen in V3; no source image was replaced or modified.

The plan and source-field rules were sealed before new class results were computed. A registered review-detail addendum, after inference had started but before sequence results or pair judgments, added local continuity and class-pair repeats because coarse context descriptors could not establish exact sequence stability. This procedural timing is retained. No support threshold or V3 class parameter changed after results. The within-row null implementation was corrected before freezing to keep UNK slots and original incomplete flags fixed; otherwise shuffling would change the eligible sequence denominator.

## Observed source evidence and representation

The expanded extraction contains {a['candidate_regions']:,} candidate raster regions. {a['body_parent_proposals']:,} enter the primary parent-order hypotheses; {a['optional_detached_faint_regions']:,} remain explicit optional regions and {a['source_adjudicated_nonwriting']} individually reviewed proposals were classified as drawing/substrate. Optional regions include tiny marks, faint threshold-only regions, show-through and possible extraction artifacts. They are **not counted as established writing units**. Their include/exclude/neighbor-attachment and row alternatives remain constraints with no canonical choice.

The 60-case queue resolved {a['source_adjudicated_nonwriting']} nonwriting proposals, retained one writing/contact proposal with unknown row ownership, and retained 22 undecidable proposals. The queue prioritized large drawing contacts, cross-row parents, field edges, detached fragments and faint-only regions. These are risk cases, not a random accuracy sample. The writing/contact example spans several apparent writing rows and cannot responsibly be split from a bounding box alone.

Primary candidates are ordered by native x. A connected parent is kept whole even if a conventional character interpretation would divide it. Low/high contrast joins across a proposed gap produce explicit `UNK_COMPOUND` alternatives, with the original competing rasters retained. A tall trace attached to lower traces, a bench/frame with an insertion or a connected repetition is classified only when the whole parent reliably fits frozen V3; otherwise it stays unknown. Atomicity, stroke order, pen lifts and detached attachments remain unknown. The taxonomy was not enlarged, merged or split to make sequences recur.

All retained fields have a source-coordinate candidate list. **Candidate list availability is 100%; usable complete row membership is 0%.** Every retained field still has optional or other membership uncertainty under the conservative protocol. This zero describes the present evidence/annotation pipeline; it does not establish that the manuscript itself has no stable writing units. Local field limits are not physical row endpoints. Complete physical row and group recall remains uncertified throughout.

## Class generalization, separate from sequences

The frozen model assigned {cm['reliable_assigned']:,} of {cm['clear_test_parents']:,} clear held-out proposed parents after corroboration and case-specific audit abstention: {pct(cm['clear_test_assignment_coverage'])}. All fourteen validated structural classes recur in at least three fresh caption groups with at least five instances. Threshold class stability is {pct(cm['threshold_assignment_stability'])}; alignment/slant stability is {pct(cm['alignment_assignment_stability'])}.

Source positive agreement is 36/40 = {pct(cm['source_positive_agreement'])}. Four proposed positives were judged incompatible and those individual left parents remain UNK; the classifier and class definitions were unchanged. Among 28 source-judged different pairs, 4 had been proposed positives: false grouping {pct(cm['source_different_pair_false_grouping'])}. The other-class nearest pairs included 14 source-compatible pairs and two unknowns, so proposed negatives were not treated as source truth. Caption-bootstrap intervals are {cm['source_positive_caption_interval']} for positive agreement and {cm['source_false_grouping_caption_interval']} for false grouping. The registered point gates passed, but interval width and a single adjudicator limit the accuracy claim. Class recurrence has generalized; full sequence membership has not.

## Completeness and recurrence for each partition

{table}

“Complete detected membership” means no retained optional, row, edge or oversize ambiguity in that group under that partition. It is a **model completeness ceiling**, not certification of all actual ink. Source-certified full membership is unavailable (0% certified). “Fully identified” additionally requires every primary class to be known. The primary unknown rate refers to proposed body parents, including possible nonwriting/extraction errors; it is not an estimate of the fraction of actual writing that is unrecognizable. All-candidate abstention is {pct(metrics[0]['unknown_all_candidate_rate'])}, with optional regions deliberately retained.

Cross-caption recurrence excludes duplicates from the same caption. Held-out recurrence matches fresh complete test lists against development lists only. Lists of at least three parents are reported separately from short lists. At 0.75, 50% held-out recurrence is only 1 of 2 complete lists of length ≥3; its caption interval is [0,1]. At 0.55 it is 1 of 8; at 0.35, 1 of 12. These counts cannot establish broad sequence coverage.

For all lengths, conditional repeated coverage is {', '.join(pct(r['cross_caption_repeated_complete_sequence_coverage']) for r in metrics)} and held-out recurrence is {', '.join(pct(r['heldout_recurrence']) for r in metrics)}. These large percentages are driven by short lists in a small complete subset. Repeated complete lists occupy only {', '.join(pct(r['repeated_complete_sequence_share_of_all_groups']) for r in metrics)} of all proposed groups. No gap setting was selected as the winner.

## Uncertainty contribution and sensitivity

{sensitivity}

Ignoring detached/faint candidate regions raises apparent membership coverage by roughly 52–60 percentage points. Ignoring row ownership changes it by roughly 1–2 points. These are fixed-corpus pipeline sensitivities, not independent causal effects or permission to discard uncertain ink. Raster/connectivity instability affects 7,420 unknown primary proposals; field limits affect 1,628 and row ownership 696. Reasons overlap. There are 10,146 reliably assigned primary proposals of 25,750; enlarging source coverage has not eliminated class abstention or created certified sequence membership.

The optional detector is deliberately permissive and retains candidate paper texture, show-through and fragmentary threshold evidence. This produces a substantial unresolved-region burden. The result localizes the next evidence problem: source adjudication of actual writing membership and whole-row recall, rather than class merging or changing gap thresholds to produce repetition. The current data cannot quantify a manuscript-wide writing recall rate because complete source reference rows are absent.

## Repeatability and nulls

Repeated structural pair judgment agreement is {pct(rp['class_pair_agreement'])} over 12 pairs. Local gap-visibility judgment agreement is {pct(rp['local_gap_visibility_agreement'])} over 23 pairs. Both passes retained unknown actual group boundaries and detached ownership. Coarse context agreement by field is {rp['coarse_context_agreement']}. Exact full sequence re-adjudication agreement is **not established**. These results concern repeated judgments by the same adjudicator with prior exposure and memory; they are neither independent human-rater results nor a blinded palaeographic accuracy estimate. No algorithm class suggestion or prior decision file was displayed in the repeat images.

The source order null shuffles known class labels within each proposed row while preserving group sizes, UNK slots, incomplete flags and class frequencies. It uses 200 replicates, cross-caption recurrence and the same complete-list denominator.

{nulltable}

These conditional order controls address whether the small complete subset carries order information. They do not resolve membership, drawing contamination or physical group boundaries, and do not qualify V4 as a notation system. Dependence-aware caption intervals are included in the machine-readable metrics. Natural-language controls and Currier positional nulls are not applicable to the present source membership question and were not substituted for missing source completeness.

## Freeze and downstream support

V4 freezes a **partial evidence representation**, including failures and alternatives. It does not claim a validated functional notation. Registered support requires ≥40 new captures, ≥600 new retained fields, ≥6 fresh captions, ≥80% usable row/group membership, ≤20% unknown parents and boundary ambiguity, ≥50% identified groups, ≥20% held-out recurrence of complete lists of length ≥3, repeatability and certified physical endpoints. The source/class count gates pass; row membership, group completeness, unknown coverage, boundary ambiguity, identified-group coverage and endpoints fail. The 0.35/0.55 held-out long-list gates also fail. Additional exact sequence-repeatability evidence remains absent.

The segmentation, class states, acceptance criteria and source evidence are sealed before downstream support assessment. The post-freeze assessment may only read that freeze. Because support fails, **no Currier-B rank assay, native pixel-x assay or EVA/RF/v101 crosswalk is run**. No conventional outcome was inspected to improve these results. A valid next version would need source-certified complete rows and adjudication of uncertain fragments; V3 and V4 should remain immutable.

Artifacts: `data/observations/visual_dataset_v4/`, `data/observations/sequence_v4_development/`, `tests/sequence_v4/`, the source example atlas and frozen scripts ending `_v4.py`. Source coordinates, competing threshold rasters, optional parent IDs, alternate row ownership and all three partitions are retained. The atlas notation is an observational candidate notation only.
'''
    (OUT/'reports/13_source_sequence_validation_v4.md').write_text(report,encoding='utf-8')
    (T/'README.md').write_text('# V4 source sequence validation\n\nRead config.json and reports/13_source_sequence_validation_v4.md. Frozen V3 source inference only; explicit unknown and competing membership states. Run scripts in order: register_sequence_v4, prepare_sequence_source_v4, record_sequence_reviews_v4, extract_sequence_v4, prepare_sequence_audits_v4; native judgments are saved separately; build_sequence_model_v4, audit_sequence_v4, report_sequence_v4, freeze_sequence_v4. Do not rerun mutations after freeze. Post-freeze audit writes into tests/sequence_v4_postfreeze.\n\nSeed 20261009. Null: known-class order shuffle within source row, UNK and incomplete flags fixed. Conditional recurrence only, no conventional assay. Source judgments by one adjudicator, repeatability only.\n',encoding='utf-8')
    write_json(T/'input_manifest.json',dict(plan_sha256=sha256(D/'PLAN.json'),protocol_seal_sha256=sha256(D/'SOURCE_PROTOCOL_SEAL.json'),audit_sample_seal_sha256=sha256(D/'AUDIT_SAMPLE_SEAL.json'),v3_manifest_sha256=plan['v3_manifest_sha256'],v3_model_sha256=plan['v3_model_sha256'],source_rows_sha256=sha256(D/'source_rows.json'),source_parent_candidates_sha256=sha256(D/'source_parents.json'),maximum_yale_native_sources=[dict(view_id=v['view_id'],path=v['native_source'],sha256=sha256(OUT/v['native_source'])) for v in plan['selected_views']]))
    print('Report, source examples, completeness figure and input manifest written',flush=True)
if __name__=='__main__':main()
