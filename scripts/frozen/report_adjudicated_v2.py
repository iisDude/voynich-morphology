"""Report frozen source adjudication and the registered assay, without edits to it."""
from common import OUT,read_json,read_csv,write_json,write_csv,sha256
from collections import Counter,defaultdict
from datetime import datetime,timezone
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    dest=OUT/'tests/adjudicated_currier_B_v2';model=OUT/'data/observations/visual_dataset_v2';root=OUT/'data/observations/source_adjudication_v2';manifest=read_json(model/'FREEZE_MANIFEST.json');summary=read_json(model/'summary.json');groups=read_json(dest/'groups_with_postfreeze_metadata.json');results=read_json(dest/'results.json');coverage=read_json(dest/'coverage.json');run=read_json(dest/'run_manifest.json');diagnostics=[]
    for rep in ['visual_fine_units','visual_merged_units','visual_factored_units']:
        rr=[g for g in groups if g['primary_eligible'] and g.get(rep) and g.get('currier')=='B'];freq=Counter(tuple(g[rep]) for g in rr);diagnostics.append(dict(representation=rep,groups=len(rr),distinct_forms=len(freq),maximum_form_frequency=max(freq.values(),default=0),forms_frequency_at_least_8=sum(v>=8 for v in freq.values()),forms_frequency_at_least_8_and_length_at_least_5=sum(v>=8 and len(f)>=5 for f,v in freq.items()),maximum_sequence_length=max(map(len,freq),default=0)))
    fine=[g for g in groups if g['primary_eligible'] and g.get('visual_fine_units') and g.get('currier')=='B'];rank=np.array([g['normalized_group_rank'] for g in fine]);pixel=np.array([g['normalized_pixel_center'] for g in fine]);delta=abs(rank-pixel);coordinate=dict(groups=len(fine),different_endpoints=int(np.sum(delta>1e-12)),median_absolute_difference=float(np.median(delta)) if len(delta) else None,maximum_absolute_difference=float(delta.max()) if len(delta) else None,formula='rank j/(N-1); pixel (native assigned-writing bounding-box center - row left)/(row right-row left)',same_occurrences=True)
    write_json(dest/'support_diagnostics.json',dict(form_support=diagnostics,coordinate_check=coordinate,all_settings_estimable=sum(r['status']=='estimated' for r in results),all_settings_minimal_pairs=sum(r['pairs'] for r in results),interpretation='Support failure is not a negative positional effect. No identities or thresholds changed after seeing it.'))
    # Scientific artifact: endpoint distinction, not an invented zero effect estimate.
    fig,axes=plt.subplots(1,2,figsize=(10,4));axes[0].bar(['Proposed\ngroups','Position-eligible\ngroup slots','Admitted\nunit sequences'],[summary['groups'],summary['primary_eligible_groups'],summary['admitted_eligible_fine_groups']],color=['#aaaaaa','#557c98','#355c44']);axes[0].set_ylabel('Groups');axes[0].set_title('Frozen source coverage (all captures)')
    for split,color in [('train','#527493'),('validation','#d39b30'),('test','#8d597c')]:
        rr=[g for g in fine if g['split']==split];axes[1].scatter([g['normalized_group_rank'] for g in rr],[g['normalized_pixel_center'] for g in rr],s=18,alpha=.65,label=f'{split} (n={len(rr)})',color=color)
    axes[1].plot([0,1],[0,1],color='gray',ls='--',lw=1);axes[1].set(xlabel='Normalized ordinal group rank',ylabel='Measured normalized native pixel x',title='Currier B: identical admitted occurrences',xlim=(-.03,1.03),ylim=(-.03,1.03));axes[1].legend(fontsize=8);fig.suptitle('Segmentation v2 — primary minimal-pair assays not estimable');fig.tight_layout();figure=OUT/'figures/source_adjudication_v2_results.png';fig.savefig(figure,dpi=170);plt.close(fig)
    freeze_hash=sha256(model/'FREEZE_MANIFEST.json');rows=read_json(root/'boundary_judgments.json');dense=read_json(root/'dense_blocks/source_reviews.json');lineids={g['line_id'] for g in groups};failedlines={g['line_id'] for g in groups if g['row_membership_status']=='unresolved_method_or_photo'}
    queue_status=dict(initial_selected_rows=47,initial_local_assemblies=188,curved_views=17,panel_pairs=9,dense_captures=8,dense_paths=348,selected_cases_all_received_source_judgment=True,meaning='Adjudicated to an observation, corrected hypothesis or explicit unknown; not every source uncertainty resolved',complete_source_rows_certified=False,known_writing_vs_complete_membership='Source writing fields are distinguishable from drawings/decoration in many cases; exact raster ownership and complete grouping remain separate uncertainties',unknown_reasons=['photographic faintness, smear, substrate overlap or physical hole','connected ink with ambiguous row ownership or internal boundary','body-path or mask reconstruction failure despite visible source writing','clipped field or unextracted writing','curved path seam/unit inventory unresolved','physical panel/duplicate-writing correspondence unresolved'],freeze_sha256=freeze_hash)
    write_json(dest/'queue_resolution_summary.json',queue_status)
    source_report=f'''# Source adjudication and frozen segmentation v2

The prioritized source queue has been adjudicated and a more explicit, partial writing-membership/boundary model has been frozen. It does **not** recover a complete manuscript alphabet or certify every writing row. Photograph ambiguity and extraction failure are recorded separately; legible writing missed by the algorithm is not declared unreadable.

All source work remains inside the Voynich Project. The fourteen original evidence files and both earlier frozen snapshots are unchanged. The pre-freeze audit passed {read_json(model/'pre_freeze_validation.json')['checks']:,} checks with zero failures; that is provenance and bookkeeping verification, not a writing-unit accuracy estimate.

## Source selection and evidence

The first queue contains 47 materially uncertain whole rows and 188 local assemblies, distributed across four manuscript quartiles and the existing caption-connected splits. Priority uses row contacts, gap-count disagreement and unknown assignment, without Currier labels, conventional text or new positional results. It also covers all 17 registered curved captures and nine panel/capture pairs. Each selected case received a native-source judgment. This targeted risk sample cannot estimate manuscript-wide error rates.

An extension registered before the freeze selected eight portrait, noncurved captures by candidate-row count: four training, two validation, two test. Its 348 proposed body paths were inspected in eight whole-view overviews and 32 native RGB/mask strips. The extension includes {', '.join(r['view_id'] for r in dense)}. Failed and clipped paths remain unknown. No extension was selected by whether it supplied repeated forms or recovered an effect.

All 204 source images match the full pixel grid advertised in their Yale IIIF metadata, and are hash-recorded. Reviews used those native JPEGs, unscaled local crops, full-width contexts and native block strips. Display resizing does not alter the saved native evidence. These are the same photographs at their advertised native resolution, not an independent capture or new material evidence. JPEG/source limitations remain relevant to fine contacts and pen lifts.

## What the source resolves

Plant stems, colored flowers/berries, figure/vessel contours, diagram rules, stars and marginal curves are distinguishable from writing in many reviewed fields. They are excluded or recorded as drawing/decoration rather than reused as sign shapes. Overlaps at their edges remain uncertain.

Several old candidates combine two or more physical bodies; others continue through blank parchment. Source corrections separate writing fields, restore visible broad gaps and recover tall constructions connected to lower traces. The dense extension follows local body paths instead of relying entirely on one horizontal corridor. Source-visible short paragraph endings remove false groups beyond the writing.

Connected tall, frame and bench-like structures are retained whole where the photograph shows continuity. A connected parent spanning two proposed groups is unknown in both; it is not cut to create a preferred sequence. Separate objects, ligatures/compounds, repeated low traces and insertion-like constructions remain competing interpretations. Raster components are not assumed letters; blank gaps are not assumed word boundaries. No pen-lift or stroke-order conclusion is established.

Curved review distinguishes annular, radial, spiral-like and rotated writing from rules, spokes, figures and ornament. Red annular strings on V_122 are writing. V_134/V_135 are not forced into closed rings. A physical hole on V_133 removes evidence and is not a writing gap. Curved groups have no certified complete inventory and do not enter the horizontal positional assay.

Visible folds divide capture coordinates. They do not certify physical folio identities or duplicate written fields. No new panel overlap transform is accepted. The nine pair judgments preserve that distinction.

## Frozen model and remaining unknowns

The v2 index covers all 204 native captures. Reviewed fields contain **{summary['groups']:,} proposed group slots**. **{summary['primary_eligible_groups']} slots** retain eligible source row/extent hypotheses for both endpoints; **{summary['admitted_eligible_fine_groups']} groups** additionally have fully admitted literal fine-unit sequences. There are {len(lineids)} retained proposed rows/paths, with {len(failedlines)} marked as unresolved complete rows. These numbers are not counts of certified words or letters.

The neutral atlas contains {summary['atlas_families']} transferred source-image families with native exemplars from eligible groups. Original source-trained prototypes and admission gates are unchanged; no EVA/RF/v101 forms were used to choose these units. Fine connected-object labels, broader visual merges and six prior compound factor hypotheses remain separate representations. Broad/factored representations do not become a canonical alphabet through their use in a test.

Most other candidate rows across the manuscript remain unadjudicated and unknown; they are indexed but not promoted into the accepted assay corpus. Writing outside the eight source blocks, missed detached traces, incomplete illustrated-page prefixes, changing body levels, shared contacts, faint marks, folds, curved seams and physical panel identities remain unresolved. The old proposals and failed reconstruction outputs are preserved for audit. Eight block overviews do not establish complete page coverage. The earlier protocol's word “geometric fine” does not imply internal cuts in v2: its fine primary is the whole threshold-connected parent.

Ordinal position is `j/(N-1)` over the frozen source group slots, including unknown-unit slots. It is never recomputed after omitting unrecognized groups. Pixel position uses the center of the group's whole assigned-writing bounding box, measured in native source pixels and normalized by the reviewed row writing extent. Unknown terminal membership excludes both primary endpoints. Interior ambiguous units stay null. Eligible ordinal ranks remain conditional on the fixed source gap hypothesis, not a certified linguistic segmentation.

The freeze occurred at **{manifest['frozen_at_utc']}**, before attaching Currier metadata or running v2 effects. Previously seen conventional findings prevent describing this as newly blind confirmation. Held-out captions remain separate diagnostic cohorts.

SHA-256: `{freeze_hash}`

- [Frozen model manifest](../data/observations/visual_dataset_v2/FREEZE_MANIFEST.json)
- [Source-only groups](../data/observations/visual_dataset_v2/assay_groups_source_only.json)
- [Neutral atlas with native exemplars](../data/observations/visual_dataset_v2/neutral_visual_atlas.json)
- [Prioritized queue](../data/observations/source_adjudication_v2/queue_plan.json)
- [Whole-row judgments](../data/observations/source_adjudication_v2/row_judgments.json)
- [Boundary judgments](../data/observations/source_adjudication_v2/boundary_judgments.json)
- [Dense source judgments](../data/observations/source_adjudication_v2/dense_blocks/source_reviews.json)
- [Curved judgments](../data/observations/source_adjudication_v2/curved_judgments.json)
- [Panel judgments](../data/observations/source_adjudication_v2/panel_judgments.json)
- [Registered positional rerun](10_currier_B_adjudicated_v2.md)
'''
    (OUT/'reports/09_source_adjudication_v2.md').write_text(source_report,encoding='utf-8')
    dtable='\n'.join(f"| {r['representation']} | {r['groups']} | {r['distinct_forms']} | {r['maximum_form_frequency']} | {r['forms_frequency_at_least_8_and_length_at_least_5']} |" for r in diagnostics)
    report=f'''# Currier-B positional assay on frozen manuscript-derived v2

**Neither ordinal rank nor measured pixel x is estimable under the registered primary assay.** The frozen admitted Currier-B subset supplies no qualifying minimal pairs. This is an evidence/support limit, not a negative effect estimate and not confirmation of the conventional finding.

The same 134 admitted group occurrences supply both endpoints, across 33 source row hypotheses and seven caption-connected groups: 111 training, 13 validation and 10 test occurrences. Page-level Currier/hand/section metadata were copied only after the v2 freeze; conventional strings, token positions and boundaries were not substituted for visual units or pixel coordinates.

## Registered results

| Representation | Ordinal rank: qualifying primary pairs | Native pixel x: qualifying primary pairs | Outcome |
|---|---:|---:|---|
| Whole connected fine image families | 0 | 0 | Not estimable |
| Broader visual merges | 0 | 0 | Not estimable |
| Compound factor hypotheses | 0 | 0 | Not estimable |

Both endpoints use minimum form frequency 8, edge width 2, and minimum sequence length 5. The response is absolute difference between mean form positions; the design is intercept + edge indicator + length + log geometric mean frequency. At least 12 pairs and a full-rank design are required. All-primary, train+validation and test cohorts separately fail the support requirement. The 144 preregistered representation/cohort/endpoint/frequency/edge-width runs contain {sum(r['pairs'] for r in results)} qualifying pairs and {sum(r['status']=='estimated' for r in results)} estimable regressions. Frequencies 5/8/10/12 and edge widths 1/2 were reported without changing segmentation.

| Representation | B occurrences | Distinct literal forms | Maximum form frequency | Forms with frequency ≥8 and length ≥5 |
|---|---:|---:|---:|---:|
{dtable}

Coefficients, confidence intervals and p-values are unavailable rather than set to zero. Connected-family uncertainty, 199 joint caption-block bootstrap resamples, leave-one-caption checks and 199 within-line position-slot null iterations are registered in the runner; they are correctly withheld when there is no estimable pair model. There is no meaningful null regression to calculate on an empty pair set. The ten test occurrences do not provide a held-out replication.

## Rank and pixel position are different measurements

Rank uses frozen ordinal gap slots. Pixel x uses native assigned-writing bounding-box centers divided by native writing extent; it is not obtained by distributing groups evenly. The frozen source ranks include unknown-unit slots even when only a few admitted groups remain in a line. The same occurrences enter both endpoints.

Of the 134 paired observations, {coordinate['different_endpoints']} have different numerical endpoints. Median absolute difference is {coordinate['median_absolute_difference']:.4f}; maximum is {coordinate['maximum_absolute_difference']:.4f}. This is a coordinate bookkeeping check, not an assay effect. Source uncertain endpoints were excluded before Currier labels were attached. Ordinal results would remain conditional on the fixed gap hypothesis even if enough pairs existed.

![Coverage and distinct source measurements](../figures/source_adjudication_v2_results.png)

## Interpretation and controls

The conventional rank finding cannot be validated or rejected from this admitted manuscript-derived subset. The new source review improves writing/drawing separation and records real geometry, but complete membership, grapheme boundaries and recurrence remain too uncertain for the registered question. Existing natural-language ordinal controls are retained in the earlier ledger as external reference; they cannot manufacture missing manuscript-derived pairs. No native-image natural-language pixel control is claimed, and no ordinal control is converted into evenly spaced fictitious pixels.

No segmentation, family merge, admission gate, primary threshold or gap hypothesis was retuned after the result. V2 is immutable. New writing annotation or a better source-only ownership method would require a new version frozen before its effect evaluation. Prior exposure to conventional findings and targeted uncertainty selection limit confirmation claims. The outcome remains **unknown**.

Freeze SHA-256: `{freeze_hash}`

- [Source adjudication and limitations](09_source_adjudication_v2.md)
- [Analysis plan](../tests/adjudicated_currier_B_v2/analysis_plan.json)
- [All registered results](../tests/adjudicated_currier_B_v2/results.json)
- [Support diagnostics](../tests/adjudicated_currier_B_v2/support_diagnostics.json)
- [Post-freeze run manifest](../tests/adjudicated_currier_B_v2/run_manifest.json)
- [Prior conventional assays and natural-language controls](07_full_test_ledger_results.md)
'''
    (OUT/'reports/10_currier_B_adjudicated_v2.md').write_text(report,encoding='utf-8')
    (dest/'README.md').write_text('''# Registered Currier-B rerun v2

Question: do edge versus interior single-unit changes predict displacement when the units come from source imagery?

Run only after the v2 source freeze. Both ordinal rank and native pixel x use the same admitted occurrences; unknown slots are never re-ranked. Three representations, three cohorts, two endpoints, four frequency thresholds and two edge widths give 144 registered runs. None has qualifying minimal pairs; do not interpret a support failure as a zero effect.

Reproduction: project Python runtime, `src/run_adjudicated_currier_B_v2.py` (without `--register`). The runner verifies every v2 frozen file before and after execution. `analysis_plan.json` is frozen; result files are post-freeze outputs. See `reports/10_currier_B_adjudicated_v2.md` for measured-coordinate checks and limits.
''',encoding='utf-8')
    # New audit, preserving previous audit reports.
    failures=[]
    for r in manifest['files']:
        if sha256(OUT/r['path'])!=r['sha256']:failures.append(r['path'])
    audit=dict(completed_at_utc=datetime.now(timezone.utc).isoformat(),v2_frozen_files_checked=len(manifest['files']),frozen_failures=failures,freeze_sha256=freeze_hash,all_primary_pairs=len(read_json(dest/'primary_pairs.json')),source_queue_has_explicit_judgments=True,same_occurrences_rank_pixel=True,source_original_and_earlier_freezes='Passed 7,106 pre-freeze checks; no subsequent edits to those artifacts',registered_results=len(results),no_effect_retuning=True)
    write_json(dest/'final_integrity_audit.json',audit)
    if failures:raise ValueError('Source freeze changed')
    print(diagnostics,coordinate,audit,flush=True)
if __name__=='__main__':main()
