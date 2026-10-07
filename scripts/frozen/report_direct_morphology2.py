from direct_morphology2_common import *
from PIL import Image,ImageDraw
import numpy as np,html
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    guard();verify_seal(D/'DISTANCE_SEAL.json'); data=read_json(D/'source_parent_ensembles.json'); fields=np.load(D/'direct_image_fields.npz'); sim=read_json(T/'primary_and_secondary_metrics.json'); ret=read_json(T/'uncertainty_and_retrieval.json'); rep=read_json(T/'same_adjudicator_repeatability.json'); unc=read_json(T/'representation_coverage_and_uncertainty.json'); diagnosis={p['parent_id']:p for p in unc['parents']}; thumbs=G/'parent_ensembles';thumbs.mkdir(exist_ok=True);cards=[]
    for p in data['parents']:
        ids=p['candidate_indices'];can=Image.new('RGB',(min(6,len(ids))*150,((len(ids)+5)//6)*185),'#f4f4f4'); dr=ImageDraw.Draw(can)
        for j,k in enumerate(ids):
            x=j%6*150;y=j//6*185;im=Image.fromarray((1-fields['shape64'][k])*255).convert('RGB').resize((128,128),Image.Resampling.NEAREST);can.paste(im,(x+8,y+23));q=data['candidates'][k];dr.text((x+6,y+4),q['candidate_id']+' c'+str(q['contrast']),fill='black');role=q['role'].replace('_',' ');dr.text((x+6,y+155),role[:22],fill='black');dr.text((x+6,y+170),role[22:44],fill='black')
        path=thumbs/(p['corpus']+'_'+p['audit_id']+'.png');can.save(path);d=diagnosis[p['parent_id']];cards.append(f"<details><summary>{p['corpus']} {p['audit_id']} / caption {p['caption']} / {p['full_extent_state']}</summary><p>{html.escape(p['parent_id'])}; native bbox {p['native_bbox']}; {p['native_source']}. Observed candidates {len(ids)}; split {d['split']}; merge {d['merge']}. Full physical distance interval: unknown.</p><img class='source' src='../{p['native_crop']}' alt='Native Yale RGB source context'><p>Aspect and orientation preserved. Every observed candidate is retained; fragments and contaminated merges are not certified whole parents.</p><img class='ensemble' src='../{path.relative_to(OUT).as_posix()}' alt='All observed contour candidates'></details>")
    atlas=OUT/'reports/26_direct_contour_morphology_atlas_trial2.html';atlas.write_text("<!doctype html><meta charset='utf-8'><title>Direct Morphology Trial2 source atlas</title><style>body{font:16px system-ui;max-width:1300px;margin:24px auto}summary{padding:12px;background:#edf2f5;margin:5px 0}.source{max-width:650px;image-rendering:pixelated}.ensemble{max-width:100%}</style><h1>Direct Morphology Trial2 source ensembles</h1><p>192 fresh source-confirmed proposals and 88 separate frozen reference parents. Whole extent is source-resolved for165 fresh proposals;27 remain UNKNOWN. Finite observed-part coordinates do not certify physical whole extent. No classes or transcription units are assigned.</p>"+''.join(cards),encoding='utf-8')
    lookup={p['audit_id']:p for p in data['parents'] if p['corpus']=='fresh'};fig,axes=plt.subplots(3,4,figsize=(11,8))
    for row,aid in enumerate(['S001','S051','S181']):
        p=lookup[aid];idx=p['primary_index'];axes[row,0].imshow(Image.open(OUT/p['native_crop']));axes[row,0].set_title(aid+' native RGB');axes[row,1].imshow(fields['shape64'][idx],cmap='gray_r',vmin=0,vmax=1);axes[row,1].set_title(p['full_extent_state']);axes[row,2].imshow(fields['sdf64'][idx],cmap='coolwarm',vmin=-.15,vmax=.15);axes[row,2].set_title('Observed SDF64');axes[row,3].imshow(fields['shape64'][p['candidate_indices'][1]],cmap='gray_r',vmin=0,vmax=1);axes[row,3].set_title('Recovery alternative')
        for ax in axes[row]:ax.axis('off')
    fig.suptitle('Unknown whole extent stays unknown despite finite observed-part coordinates');fig.tight_layout();fig.savefig(G/'source_and_uncertainty_examples.png',dpi=140);plt.close(fig)
    table='\n'.join(f"| {k} | {v['AUROC']:.3f} | {v['ordinal_spearman']:.3f} |" for k,v in sim['metrics'].items());ci=sim['primary_caption_node_bootstrap95'];dci=sim['paired_delta_bootstrap95'];iv=sim['interval_ordering'];lo=[r['AUROC'] for r in sim['leave_one_caption_out'].values() if r['AUROC'] is not None];gates='\n'.join(f'- {k}: {v}.' for k,v in {**sim['sample_gates'],**sim['metric_gates']}.items())
    report=f'''# Direct Continuous Contour/Morphology Trial2 — frozen evidence report

The unchanged primary **contour64 AUROC is {sim['metrics']['contour64']['AUROC']:.3f}** on211 fresh cross-caption binary source judgments. The caption-node bootstrap95% interval is **{ci[0]:.3f}–{ci[1]:.3f}**. Aspect-only AUROC is **{sim['metrics']['aspect_only']['AUROC']:.3f}**; paired improvement is **{sim['contour_minus_aspect']:.3f}**, with bootstrap95% **{dci[0]:.3f}–{dci[1]:.3f}**. This report records measurements and registered gate evaluations. Interpretive disposition is written separately **after the complete Trial2 freeze**.

## Freshness and corpus selection

The [eligibility audit](../data/observations/direct_morphology_trial2/CAPTION_ELIGIBILITY.json) projects caption/source identifiers against V3–V6 detailed parent and source corpora, both feature trials, Direct Trial1 and prior source-similarity pairs. It covers102 caption groups and resolves all prior pair references.45 groups meet the conservative eligibility definition. The first partial audit missed some source-view mappings; it was repaired before selection freeze, with the initial diagnostic preserved. No morphology outcomes existed during this repair.

Globally untouched photographs are unavailable after earlier overview exposure and extraction. **Fresh** means unused in the audited detailed V3 fitting/selection, V5/V6 source adjudication, feature-trial inputs/specification, Direct Trial1 corpus and known prior similarity pair sets. Earlier overview processing and V4 broad extraction/frozen-model application remain. This is new caption-level similarity validation, not globally blind image discovery.

Eight captions **7,11,29,31,45,48,54,87**, two ordinary horizontal fields each, were chosen by layout and source quality from the eligible pool before extraction. The caption54 field edge was trimmed after RGB layout inspection to avoid visible drawing; no morphology informed it.24 seeded foreground proposals per caption yielded192 parents. Selection uses source layout, contrast and fixed area/core criteria, not resemblance, recurrence, labels or outcomes. It is a proposal-conditioned clear-field sample, **not a writing-ink census**. Source selection and all coordinates are preserved in [SELECTED_FIELDS](../data/observations/direct_morphology_trial2/SELECTED_FIELDS.json) and [selection seal](../data/observations/direct_morphology_trial2/SELECTION_SEAL.json).

## Source judgments first

Native Yale RGB fields and parent contexts were inspected before distances, neighbors, structural labels or conventional information. All192 sampled objects are confirmed writing.165 have photographically resolved whole extent;27 retain unknown full extent. Membership certainty and extent certainty are separate. This selected foreground sample therefore supplies no estimate of nonwriting rejection, complete writing recall or exact row extraction.

[Source decisions](../data/observations/direct_morphology_trial2/source_decisions.json) retain joins/splits, contacts, faint ink, neighboring contamination, detached alternatives, field-edge status and physical coordinates. Wider RGB contexts qualify difficult cases. S051/S052 and S055/S056 retain possible source joins; their partial unions contain no invented bridge. S181 lacks a source-certified full-parent contour beyond its detected lower part. A finite raster candidate never resolves these source questions. Automatic row bands and boxes are locational aids, not independent certification of row ownership or pixel-perfect physical ink boundaries.

The [source seal](../data/observations/direct_morphology_trial2/SOURCE_SEAL.json) predates candidate construction and predictions. Unknown full geometry remains explicit. Whole connected evidence is primary; no internal graphemes, stroke order, pen lifts or linguistic units were inferred.

## Unchanged representation

Frozen Trial1 functions are imported unchanged: aspect-preserving tight masks centered in64×64 with56px support; nearest resampling; signed-distance fields normalized by support; symmetric inner/outer raster contour Chamfer normalized by56. Orientation and aspect are preserved. Translation and absolute scale are normalized away, with native dimensions retained. There is no rotation/reflection alignment, PCA, clustering, learned embedding, prototype, V3 label or required handcrafted vector.

Native contrast9 primary masks and all observed contrast6/12 correspondences covering≥5% of primary ink are retained. Split fragments and native-coordinate unions, possible merges, missing-state checks and±.04 synthetic slant sensitivities follow the exact Trial1 procedure. None is selected to improve similarity. They are recovery hypotheses, not equally certified physical shapes. Fresh counts:13 split cases,20 merge cases and0 missing threshold matches; categories overlap.

There are280 parent records:192 fresh plus88 separately frozen reference parents, with1,437 candidate image fields. All imported reference fields match Trial1 exactly. Unknown extents have observed-part coordinates and absent full-parent geometry. Source alternatives are retained separately rather than inserted into the primary evaluation as resolved whole parents. [Ensembles](../data/observations/direct_morphology_trial2/source_parent_ensembles.json) map every coordinate to the native source, box and candidate.32px/128px contour remain sensitivity checks; SDF64 remains secondary.

## Sealed source evaluation

The [preregistration](../data/observations/direct_morphology_trial2/PLAN.json) specifies deterministic600-pair sampling before ratings: half broad cross-caption random, half aspect-matched, cycling caption dyads and native-envelope area quartiles, with parent degree≤12. No contour-nearest selection is used for the primary pool. Only165 source-resolved parents are eligible; the27 unknowns stay represented but do not supply invented full-shape judgments.

Anonymous RGB pairs were rated2 same whole organization,1 partial/related,0 different orU unresolved. Captions, pair-selection stratum, source IDs, shape distances, neighbors, feature profiles and class labels were hidden. Initial240 contained25 same judgments, below registered30; exactly the predetermined next120 were reviewed before any metric was computed. All360 opened pairs remain included:35 same,176 different,149 partial and0 unresolved.211 binary pairs enter primary AUROC;149 partials are preserved and used only in secondary ordinal association. Both binary categories involve all eight captions. Remaining240 pool pairs were prepared and sealed but **not reviewed or analyzed**.

These are same-AI source judgments, not independent human validation. Captions are fresh to the audited detailed similarity work; the same adjudicator and earlier overall photo exposure persist.

| Metric | Binary AUROC | Ordinal association on360 |
|---|---:|---:|
{table}

The primary remains contour64 even though secondary SDF64 scores higher.2,000 two-endpoint caption-node bootstrap draws use pair weight=count(left caption)×count(right caption).1,993 retain both binary categories, exceeding registered1,800. Paired contour/aspect differences use identical weights. These conditional intervals account for shared captions, but cannot remove systematic adjudication bias or all repeated-parent dependence. Leave-one-caption-out contour AUROCs range{min(lo):.3f}–{max(lo):.3f}.

The frozen mixture matters: broad-random binary subset98(10 same) has contour64 AUROC0.798 and aspect0.812; aspect-matched subset113(25 same) has contour64 AUROC0.907 and aspect0.655. Overall superiority **does not establish superiority within every sampling stratum**, a uniform all-manuscript performance estimate or universal shape recognition. Neither stratum changes the registered pooled success criterion.

## Repeatability

Twenty uniform seeded repeats from all opened pairs, including partials, were presented under changed IDs/sides with prior decisions hidden. Representation replay intervened. Exact agreement is **{rep['exact_agreement_n']}/20 ({rep['exact_agreement']:.0%})**, unweighted kappa{rep['unweighted_kappa']:.3f}. Six changes are partial↔different; the repeat sample contains only one original same pair, so it provides little evidence about repeatability of the positive category. Separation is short and same-session conversational memory persists. This is **same-AI repeatability only**, not independent human inter-rater validation. No repeatability pass threshold was preregistered, and none is introduced now. The modest repeatability limits confidence in the source target labels.

## Uncertainty and retrieval

Every reviewed pair stores primary/min/max observed contour and SDF distances and source extent status. These are sensitivity envelopes, **not probabilities, posterior intervals, exhaustive physical bounds or source-truth confidence intervals**. Among6,160 positive-negative pair-order comparisons,{iv['certain_correct']} are correct under every separate observed envelope choice,{iv['certain_wrong']} reversed, and{iv['overlapping_or_tied']} overlap/tie. The{iv['guaranteed_correct_fraction']:.3f}–{iv['possible_correct_upper_fraction']:.3f} ordering envelope is not an AUROC confidence interval; correlated candidate choices and contaminated recoveries matter.

Separately,165 fresh source-resolved query parents are compared with88 frozen Trial1 reference parents from disjoint captions. **{ret['all_alternative_stable_nearest_n']}/165** retain a unique nearest reference across every observed query alternative and independently variable reference alternatives. A stricter global-envelope sufficient criterion certifies23. Median conservative not-excluded set size is{ret['median_not_excluded_neighbors']:.1f}. Query recovery alternatives change the primary-reference nearest identity for{ret['query_alternative_changes_n']}/165 queries. Nearest identity agrees with64px in{ret['same_nearest32_n']}/165 at32px and{ret['same_nearest128_n']}/165 at128px; median full-reference rank correlation is{ret['rank_spearman32_median']:.3f}/{ret['rank_spearman128_median']:.3f} respectively.

These ranks are image resemblance ranks. Neighbor sets are not classes or equivalence relations. Sparse unique-neighbor stability is a registered diagnostic, not an automatic failure. The [retrieval records](../tests/direct_morphology_trial2/uncertainty_and_retrieval.json) preserve changed-neighbor witnesses and full not-excluded sets. No source ownership decision is derived from retrieval. Unknown full extents are excluded only from this qualified whole-parent diagnostic and remain in the corpus.

## Registered gates, failures and freeze

The primary gates were≥6 captions,≥120 binary pairs,≥30 in each category, each category spanning≥4 captions, contour64 AUROC≥.80, caption-bootstrap lower≥.65, contour-aspect delta≥.05 and paired lower>0,≥1,800 valid bootstrap draws, exact deterministic replay and preserved source unknowns. Mechanical statistical gate values:

{gates}

Exact replay and native-source recovery checks are stored separately. Implementation syntax validation caught one unmatched parenthesis before evaluator execution and before any prediction computation; it was corrected without changing methods. No outcome-directed retuning occurred. Limitations remain:27 unknown whole extents; raster splits/contamination;149 partial targets; small positive count; modest short-session repeatability; qualified source selection; no global image blindness; finite, nonexhaustive candidate alternatives.

The [final manifest](../data/observations/direct_morphology_trial2/FREEZE_MANIFEST.json) seals this report, source audit/judgments, native masks/crops, candidate fields,600-pair sampling pool, used anonymous ratings, repeatability, metrics, uncertainty, code, dependencies and deterministic replay. [Postfreeze integrity](../tests/direct_morphology_trial2_postfreeze/INTEGRITY.json) verifies this package and earlier evidence. [Postfreeze interpretation](../tests/direct_morphology_trial2_postfreeze/SUMMARY.md) applies the pre-outcome decision rule only after freeze. Earlier freezes are preserved. No conventional, positional, section, semantic, sequence or decipherment assay has been opened.

[Source atlas](26_direct_contour_morphology_atlas_trial2.html) · [Native uncertainty examples](../figures/direct_morphology_trial2/source_and_uncertainty_examples.png)
'''
    (OUT/'reports/25_direct_contour_morphology_trial2.md').write_text(report,encoding='utf-8')
    save(T/'FAILURES_AND_LIMITATIONS.json',dict(unknown_full_extent_n=27,partial_pair_n=149,rating_repeat_disagreement_n=6,primary_pair_sample_selection='Registered random/aspect mixture; not uniform manuscript census',broad_random_contour_not_superior_to_aspect=True,no_independent_human_validation=True,no_global_image_blindness=True,finite_candidate_envelopes_only=True,implementation_errors=[dict(error='Unmatched parenthesis detected before execution',fixed_before_metrics=True,method_changed=False)],no_method_retuning=True,no_downstream_assays=True))
    print('Frozen evidence report and280-parent atlas prepared; disposition remains deferred',flush=True)
if __name__=='__main__':main()
