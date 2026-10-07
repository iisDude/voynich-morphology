"""Native source reference atlas and separate diagnostic reporting."""
from common import OUT,read_json,write_json
from register_row_benchmark_v5 import D,T,F,G
from map_frozen_classes_v5 import verify_source_seal
from collections import Counter
from PIL import Image,ImageDraw
import html,json

def fraction(m):return f'{m["numerator"]}/{m["denominator"]} ({m["rate"]*100:.1f}%)' if m['rate'] is not None else 'Not estimable'

def main():
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen(source_stage=False)
    verify_source_seal();stats=read_json(T/'sequence_completeness.json');acc=read_json(T/'extraction_accuracy.json');rep=read_json(T/'repeatability.json');opt=read_json(T/'optional_region_source_adjudication.json');ab=read_json(T/'class_abstention_diagnosis.json');gaps=read_json(T/'gap_partition_concordance.json');rows=read_json(F/'source_reference.json')['rows'];classes={r['row_id']:r['parents'] for r in read_json(F/'parent_class_assignments.json')['rows']}
    metricnames=[('target_writing_recall','Confirmed target-writing object recovery'),('all_writing_membership_recall','Writing recognition across reviewed context'),('nonwriting_false_inclusion','Nonwriting falsely included in target row'),('resolved_target_ownership_precision','Target-owner precision among resolved assignments'),('ownership_assignment_coverage','Resolved target-owner assignment coverage'),('reviewed_parent_recovery','Whole reviewed-parent support recovery'),('detached_writing_membership_recall','Detached writing recognition'),('endpoint_accuracy','Physical endpoint x recovery')]
    table='\n'.join('| '+name+' | '+fraction(acc['V4']['heldout'][k])+' | '+fraction(acc['V5_automatic']['heldout'][k])+' | '+fraction(acc['V5_layout_assisted']['heldout'][k])+' |' for k,name in metricnames)
    seqtable='\n'.join(f'| {gap} | {m["groups"]} | {m["membership_complete_groups"]} ({100*m["membership_complete_rate"]:.1f}%) | {m["exact_complete_groups"]} ({100*m["exact_complete_rate"]:.1f}%) | {m["lengths"]["3"]["complete_groups"]} | {m["lengths"]["3"]["heldout_complete_groups"]} |' for gap,m in stats['gap_hypotheses'].items())
    gtable='\n'.join('| '+gap+' | '+fraction(m['V5_automatic']['heldout']['resolved_pair_recovery'])+' | '+fraction(m['V5_automatic']['heldout']['conditional_gap_cut_precision'])+' | '+fraction(m['V5_automatic']['heldout']['all_resolved_source_gap_cut_recall'])+' |' for gap,m in gaps['gap_hypotheses'].items())
    text=f'''# V5 source-adjudicated ordinary-row benchmark

The small benchmark establishes many reliable source-writing judgments, but **complete source-only structural sequence recovery remains unestablished**. Sixteen row targets in eight existing Yale caption groups were inspected at native resolution. V3 and V4 were reused unchanged. No manuscript-wide source expansion occurred.

The reference contains **2,616 source object-location records**: 1,051 confirmed writing objects across the reviewed contexts, 1,117 confirmed nonwriting detections, 419 unresolved objects and 29 mixed writing/contact/artifact structures. Of the confirmed writing objects, 639 belong to the selected rows; one confirmed photographic join gives **638 connected-parent records**. These counts are photographic object judgments, not letters, words or hand-painted ink-pixel masks.

## Source selection and review

The [registration](../data/observations/row_benchmark_v5_development/PLAN.json) selected 16 clear ordinary horizontal targets in captions 5, 10, 34, 39, 55, 81, 106 and 115 using image contrast, layout, minimal drawing intrusion and visible margins. Captions 10 and 106 supplied four heldout rows for new membership-rule validation. Caption grouping does not establish physical-bifolio or independent-hand sampling. All captures were already available in the project; prior overview/source-model exposure remains.

Every large and small location-aid record was reviewed against native RGB, alongside full-width contexts, overlapping coordinate-labeled source panels and selected 4× contact crops. Primary/low threshold masks locate objects; they do not define writing truth. Full RGB sweeps checked for separate visible target traces outside the ledger. Source coordinates, neighbor/marginal ownership, detached alternatives, mixed structures, connected parents and all three gap hypotheses are retained in the [sealed source reference](../data/observations/visual_dataset_v5/source_reference.json).

The raw geometric anchors sometimes straddle physical rows. B002 and B016 initially had provisional aids following another row on the left; their continuous physical paths were corrected before source annotation/validation. B011 retains the second source row chosen during RGB adjudication before any rule result, despite raw-anchor ambiguity. B012 has a leading loop/contact whose ownership leaves start alternatives x455–501. No row was replaced after observing a heldout result. Historical superseded B002 object mosaics are listed explicitly in [artifact roles](../tests/row_benchmark_v5/artifact_roles.json).

Source row starts/ends are native coordinate review windows and x intervals. They do not claim chemically exact fringe pixels. The reference has 31 resolved endpoint judgments of 32; every row retains at least one possible member, contact, parent or ordering ambiguity. The row benchmark is therefore useful for **resolved-object error assessment**, while remaining incomplete as exhaustive row truth.

## Rules and heldout extraction

Source membership/row judgments were concealed from V3 suggestions. Development RGB errors motivated a source-only contrast/coherence triage, shorter minim eligibility for membership, explicit long-descender abstention, and a density-based row track. The [rule seal](../data/observations/row_benchmark_v5_development/MEMBERSHIP_RULE_SEAL.json) predates heldout object adjudication. Heldout rows were then annotated without rule predictions or class suggestions, evaluated once, and not used to retune the rule.

The strong writing-candidate rule requires area≥35 px, height≥0.20 body, width≥0.075 body, height≤4.5 body, width≤12 body, native gray contrast90≥50 and median≥25 against a sigma25 background. The relaxed membership height **does not relax V3 class eligibility**. Small weak regions are texture predictions; other faint/mixed evidence stays unknown. Reference-unknown cases remain unknown even when a rule predicts texture. No faint bridge is automatically joined into a parent.

The automatic mode tracks source density from the registered anchor. The second diagnostic supplies the adjudicated body path, but no object labels or endpoint boxes. It is **layout-assisted**, not automatic row recovery. Both modes work within source-localized contexts, so neither certifies full-page row discovery.

Heldout results (four rows, two caption clusters):

| Metric | Unchanged V4 output | Sealed V5 automatic rule | V5 with source body path |
|---|---:|---:|---:|
{table}

V4 had no physical endpoint output; its zero recovered endpoints mean **no endpoint predictions**, not measured zero-accuracy endpoint guesses. Source-writing recognition across all reviewed context includes neighboring writing; it differs from complete target-row membership recovery. Ownership precision is conditional on resolved assignments and must be read with assignment coverage.

The remaining automatic misses include detached upper curves, small/faint fragments and long descenders. B014_O002, adjudicated substrate contrast before rule evaluation, is the single false target inclusion on heldout data; it shifts the predicted start 72 px left of the source interval. The rule recovers 168/178 confirmed target-writing objects and 7/8 resolved endpoints, rather than perfect extraction. These failures are preserved.

Whole reviewed-parent support recovery is proposal-conditioned: the location aids and tested raster share source masks. Its one-to-one support/confirmed-join checks are useful diagnostics, but **independent photographic ink-pixel IoU is not available**. Source-confirmed joined traces can still be split by the raster; unknown contacts are excluded from asserted boundary truth and explicitly counted. No independent human paleographer or chemical ink test is represented by this benchmark.

All numerators, missing-object IDs, false inclusions, endpoint errors and caption-cluster intervals appear in [extraction accuracy](../tests/row_benchmark_v5/extraction_accuracy.json). With only two heldout caption clusters, the intervals do not establish manuscript-wide population error rates.

## What the optional regions were

The unchanged V4 pipeline supplies 706 optional detections within these reviewed contexts:

| Source adjudication | Count |
|---|---:|
| Confirmed writing | {opt['counts'].get('confirmed_writing',0)} |
| Confirmed nonwriting texture/drawing detections | {opt['counts'].get('confirmed_nonwriting',0)} |
| Unresolved | {opt['counts'].get('unresolved',0)} |
| Mixed writing/contact/artifact | {opt['counts'].get('mixed_writing_and_unresolved',0)} |

Of the optional writing objects, 53 belong to the target row, 138 belong to neighboring rows and two have uncertain ownership. Thus removing optional detections indiscriminately removes real target writing and hides ownership failures. Clear surface ridges, drawing contours/stars and irregular substrate patches can be excluded by source judgment; faint coherent curves remain writing, while diffuse connections or undecidable marks retain alternatives. Photograph-only identification of actual show-through is generally unavailable, so possible show-through stays a hypothesis.

B001_O015 and B005_O189 illustrate diffuse raster contamination; B015 separates ordinary writing from drawn stars and detached marginal writing. Connected upper frames and low traces retain whole-parent extents and possible compounds. No letters, pen lifts or stroke order are inferred. The complete [optional-region ledger](../tests/row_benchmark_v5/optional_region_source_adjudication.json) distinguishes these cases.

## Frozen V3 assignments and sequence completeness

Source judgments and conservative repeat handling were [sealed before V3 inference](../data/observations/visual_dataset_v5/SOURCE_REFERENCE_SEAL.json). A separate [sequence protocol seal](../data/observations/visual_dataset_v5/SEQUENCE_PROTOCOL_SEAL.json) fixed ordering, gap handling, completeness and recurrence criteria before class mapping. Frozen V3 radii, topology, features, core exclusions and perturbation tests were unchanged.

V3 assigns **311/638 parents (48.7%)** to its 14 frozen core classes; **327 (51.3%) remain UNK**. Eleven fail frozen geometry/primary-connectivity eligibility; the others fail one or more existing class-fit/perturbation criteria. Among overlapping abstention reasons: 207 nominal fit/radius/margin/topology rejections, 139 raster connectivity/topology failures, 274 threshold-class failures and 234 fixed-slant failures. These counts overlap and are not an additive decomposition. Source confirmation therefore does not itself produce a reusable V3 assignment. Coverage here is in-domain frozen-model use on previously source-covered captures, not new independent class validation.

Parents are ordered by source body-core x support, with explicit detached/order uncertainty. Gap partitions use running whole-parent right extent, preventing a cut through an included upper overhang. Possible joins preserve separate/combined alternatives; combined unresolved forms are `UNK_COMPOUND`, never selected because a class sequence repeats. Neutral sequences retain `UNK`, `[UNK_MEMBER]` and `[UNK_BOUNDARY]` with source IDs and coordinates.

| Gap/body hypothesis | Groups | Complete source membership | Exact complete V3 sequences | Complete length≥3 | Heldout complete length≥3 |
|---|---:|---:|---:|---:|---:|
{seqtable}

There are **zero fully complete source-membership rows and zero fully complete structural rows**. All reviewed rows have a traceable partial ordered representation, but none qualifies as a complete independent notation row. Exact completeness is stricter than having a list of known classes: parent membership, row ownership, connectivity/order and class assignment must all be resolved.

At gap0.35, four of six complete short groups repeat a class sequence in another caption; the sole heldout complete group does not match the development lexicon. Gaps0.55 and0.75 have two and one complete short groups, with no cross-caption repeated coverage. **No complete length≥3 sequence exists under any hypothesis**, so heldout recurrence at that length is not estimable—not an observed zero population recurrence rate. The 200 within-row label-shuffle null preserves group geometry, class frequency, unknown locations and completeness; its length≥3 result is degenerate. Single-unit repetition supplies no evidence for a practical multi-unit notation.

Ignoring all optional source spans would raise membership completeness from 18.0/12.9/10.9% to 81.4/77.3/73.6% across the three hypotheses. That counterfactual is not a permitted correction. Removing only detached or confirmed-writing ownership uncertainty does not remove the remaining mixed/faint ambiguity burden. Exact source sequences and alternatives are in [group sequences](../data/observations/visual_dataset_v5/group_sequences.json); [completeness](../tests/row_benchmark_v5/sequence_completeness.json) records all denominators and sensitivities.

Source spacing-partition recovery is reported separately:

| Gap/body hypothesis | Resolved adjacent-pair recovery | Conditional cut precision | Recall of all resolved source cuts |
|---|---:|---:|---:|
{gtable}

These are **three operational source-spacing hypotheses**, not photographed word or grapheme boundary truth. Missing parents reduce pair/cut recall; ambiguous contacts are retained. Semantic group-boundary precision/recall cannot be supplied from this reference. [Detailed gap concordance](../tests/row_benchmark_v5/gap_partition_concordance.json) keeps every hypothesis separate.

## Same-adjudicator repeatability

The originally registered rows B002/B005/B010/B014 were revisited after development diagnosis and heldout annotation. A preregistered-before-repeat uniform source-coordinate sample supplied 32 objects per row, in anonymous random order, with prior source/class suggestions absent. Full unlabeled contexts were provided. Familiarity and visual memory remain; this is **same-adjudicator repeatability only**.

Exact all-state agreement is 104/128 (81.3%). Of 107 initially resolved membership decisions, 93 remain the same resolved decision (86.9%); 14 become unresolved on repeat. Agreement conditional on both judgments being resolved is 93/93, which would overstate repeatability if reported alone. Positive writing agreement is 94/95 (98.9%). Original unknowns were not promoted; all resolved-to-unknown disagreements were conservatively downgraded before source freeze. The four repeated endpoint intervals agree with the original source x judgments, without implying precise ink-pixel endpoints. [Repeat records](../tests/row_benchmark_v5/repeatability.json) preserve every transition and timestamped protocol.

The repeated object locations use the same source coordinate aids. Exact parent/group-boundary segmentation was not independently redrawn on the repeat pass, so no independent boundary-repeatability rate is asserted. Crop connectivity descriptors, ownership decisions and source endpoint intervals are retained alongside membership agreement.

## Snapshot and scope

The [native reference atlas](16_source_row_reference_atlas_v5.html) exposes source coordinates, membership, classes and uncertainty. The final V5 manifest records this partial benchmark, extraction rules, alternatives and diagnostics. Formal downstream support assessment occurs **after the final freeze**, in `tests/row_benchmark_v5_postfreeze`.

No EVA/RF/v101 data, Currier metadata, new positional outcomes or minimal-pair support were used to choose this benchmark, adjudicate source membership, fit membership rules or assign V3. Historical findings were already disclosed in the handoff/project overview, so this is not global researcher blinding. No downstream positional or transcription assay was performed in V5. Natural-language controls are not relevant to these photographic extraction diagnostics; any later linguistic assay would require its own controls and support.

The practical result is a source-traceable **partial photographic reference**, with improved writing recognition and explicit failure evidence. It is not a recovered alphabet, fully resolved segmentation, independent-rater consensus or complete manuscript notation.
'''
    (OUT/'reports/15_source_adjudicated_row_benchmark_v5.md').write_text(text,encoding='utf-8')
    parts=[]
    contexts={r['row_id']:r for r in read_json(D/'CONTEXT_EXTENSION.json')['rows']}
    colors={'confirmed_writing':'#087c3d','confirmed_nonwriting':'#788488','unresolved':'#e13c8b','mixed_writing_and_unresolved':'#d57a00'}
    for r in rows:
        a,b,c,d=contexts[r['row_id']]['review_context_bbox'];rects=[];labels=[]
        for p in r['objects']:
            x,y,e,f=p['native_bbox'];title=html.escape(f'{p["object_id"]} {p["membership"]}; owner={p["owner"]}; source={p["native_bbox"]}; {p["physical_parent_status"]}')
            kind='writing' if p['membership']=='confirmed_writing' else 'nonwriting' if p['membership']=='confirmed_nonwriting' else 'unknown';rects.append(f'<rect class="{kind}" x="{x}" y="{y}" width="{e-x}" height="{f-y}" fill="none" stroke="{colors[p["membership"]]}" stroke-width="1.2"><title>{title}</title></rect>')
        for p in classes[r['row_id']]:
            x,y,e,f=p['native_bbox'];labels.append(f'<text class="classlabel" x="{p["root_x"]}" y="{f+10}" font-size="11" fill="#053ca5">{p["structural_class"]}<title>{html.escape(p["parent_id"])}</title></text>')
        points=' '.join(f'{x},{y}' for x,y in r['body_path']);nassign=sum(p['structural_class']!='UNK' for p in classes[r['row_id']]);parts.append(f'<article><h2>{r["row_id"]} · source caption {html.escape(r["caption"])} · {r["split"]}</h2><p>Native {html.escape(r["native_source"])}; x endpoints {r["physical_endpoint_x_intervals"]}; {nassign}/{len(classes[r["row_id"]])} V3 assigned parents. Hover boxes for source records.</p><div class="view"><svg viewBox="0 {b} {c} {d-b}" width="{c}" height="{d-b}"><image href="../figures/row_benchmark_v5/{r["row_id"]}_context.png" x="0" y="{b}" width="{c}" height="{d-b}"/>{"".join(rects)}<polyline class="path" points="{points}" fill="none" stroke="#00a6be" stroke-dasharray="5 4" stroke-width="1"/>{"".join(labels)}</svg></div><p>{html.escape(r["notes"])}</p><details><summary>Source-only record and sequence alternatives</summary><pre>{html.escape(json.dumps(dict(row_id=r["row_id"],source_endpoint_status=r["endpoint_status"],confirmed_joins=r["confirmed_joins"],possible_joins=r["possible_joins"],parents=classes[r["row_id"]]),indent=2))}</pre></details></article>')
    page='''<!doctype html><html><head><meta charset="utf-8"><title>V5 native source row reference</title><style>body{font:16px/1.5 system-ui;margin:2rem;color:#182327;background:#f8f6f0}h1,h2{line-height:1.2}article{padding:1rem;background:white;margin:2rem 0;border:1px solid #d9d3c5}.view{overflow:auto;max-height:620px;border:1px solid #bbb}svg{display:block;max-width:none}pre{font:12px monospace;white-space:pre-wrap}.controls{position:sticky;top:0;background:#fff;padding:12px;border:1px solid #ccc;z-index:2}.off-writing .writing,.off-nonwriting .nonwriting,.off-unknown .unknown,.off-classlabel .classlabel,.off-path .path{display:none}label{margin-right:1rem}p{max-width:1000px}</style></head><body><h1>V5 native source row reference</h1><p>Source membership was sealed before V3 labels. Green = writing (target, neighbor or margin; hover shows ownership), gray = nonwriting source detections, pink = unresolved, orange = mixed. Blue labels apply frozen V3; UNK is retained. Cyan is the reviewed body path, not stroke order. Boxes locate whole source/raster proposals and can enclose other ink; they are not hand-painted ink-pixel truth or graphemes. Scroll each native-width source panel.</p><div class="controls">'''+''.join(f'<label><input checked type="checkbox" data-kind="{k}">{name}</label>' for k,name in [('writing','Writing'),('nonwriting','Nonwriting'),('unknown','Unknown/mixed'),('classlabel','V3 labels'),('path','Body path')])+'''</div>'''+''.join(parts)+'''<script>document.querySelectorAll('input').forEach(e=>e.addEventListener('change',()=>document.body.classList.toggle('off-'+e.dataset.kind,!e.checked)))</script></body></html>'''
    (OUT/'reports/16_source_row_reference_atlas_v5.html').write_text(page,encoding='utf-8')
    # Two static diagnostic overlays for source-coordinate visual verification.
    for rid in ['B003','B014']:
        r=next(q for q in rows if q['row_id']==rid);box=contexts[rid]['review_context_bbox'];im=Image.open(OUT/r['native_source']).convert('RGB').crop(box);draw=ImageDraw.Draw(im)
        for p in classes[rid]:
            x,y,c,d=p['native_bbox'];draw.rectangle((x,y-box[1],c,d-box[1]),outline='#168a43',width=1);draw.text((int(p['root_x']),d-box[1]+1),p['structural_class'],fill='#1644ce')
        for p in r['objects']:
            if p['membership'] not in ['unresolved','mixed_writing_and_unresolved']:continue
            x,y,c,d=p['native_bbox'];draw.rectangle((x,y-box[1],c,d-box[1]),outline='#d72585',width=1)
        im.save(G/f'{rid}_frozen_reference_overlay.png')
    verify_source_seal();print('Prepared V5 source report and native reference atlas',flush=True)
if __name__=='__main__':main()
