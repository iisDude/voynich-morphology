from feature_trial2_common import *
from common import write_csv
from collections import Counter
from scipy.stats import spearmanr
import numpy as np,html
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    guard();spec=read_json(D/'PLAN.json');rows=read_json(D/'feature_profiles.json')['parents'];source={r['parent_id']:r for r in read_json(D/'source_decisions.json')['parents']};aids={r['parent_id']:r for r in read_json(D/'source_location_aids.json')['parents']};lab={r['parent_id']:r['class_reporting_only'] for r in read_json(D/'V3_reporting_labels.json')};cov=read_json(T/'coverage_and_source_agreement.json');coh=read_json(T/'V3_feature_coherence.json');un=read_json(T/'unknown_continuous_recurrence.json');sim=read_json(T/'heldout_source_similarity.json');hist=read_json(T/'historical_reused_input_sensitivity.json');fresh=[r for r in rows if r['corpus']=='fresh' and r['membership']=='confirmed_writing'];resolved=[r for r in fresh if r['source_resolved']];failure=Counter()
    for r in fresh:
        if not r['source_resolved']:failure['source_parent_extent_contact']+=1
        elif not r['whole_parent_correspondence']:failure['whole_parent_threshold_correspondence']+=1
        elif r['stable_core_count']<8:failure['insufficient_stable_core_fields']+=1
        elif not r['usable_partial_profile']:failure['missing_required_family']+=1
        else:failure['usable']+=1
    table=[]
    for k,ff in spec['features'].items():
        applicable=[r for r in fresh if r['features'][k]['raster_status']!='not_applicable'];table.append(dict(descriptor=k,core=ff['core'],family=ff['family'],tolerance=ff['range_tolerance'],confirmed_writing_n=len(fresh),applicable_n=len(applicable),raster_stable_n=sum(r['features'][k]['raster_status']=='stable' for r in fresh),source_qualified_stable_n=sum(r['features'][k]['source_qualified_status']=='stable' for r in fresh),source_unknown_n=sum(r['features'][k]['source_qualified_status'].startswith('unknown_source') for r in fresh),not_applicable_n=len(fresh)-len(applicable)))
    write_csv(T/'descriptor_stability_confirmed_writing.csv',table)
    # Span comparison is distributional: no post-result semantic run cutoff.
    span=[r for r in resolved if source[r['parent_id']]['source_horizontal_span']!='unknown'];span_stats={v:dict(n=sum(source[r['parent_id']]['source_horizontal_span']==v for r in span),median_run=float(np.median([r['features']['horizontal_run_fraction']['primary'] for r in span if source[r['parent_id']]['source_horizontal_span']==v]))) for v in ['evident','absent']}
    save(T/'source_run_association.json',dict(span_source_audit=span_stats,not_a_binary_accuracy_score=True,reason='Protocol has no source-semantic run cutoff. Long near-horizontal source span differs from a horizontal contiguous raster run; no threshold chosen after results.'))
    save(T/'membership_feature_failure_diagnosis.json',dict(primary_mutually_exclusive_first_failure=dict(failure),selection_denominator='129 confirmed writing parent proposals; possible joins not separate accepted whole parents',cavity_disagreements=[dict(parent_id=r['parent_id'],audit_id=r['audit_id'],source=source[r['parent_id']]['source_cavity_count'],raster=r['features']['significant_cavity_count']['primary'],raster_status=r['features']['significant_cavity_count']['raster_status']) for r in resolved if source[r['parent_id']]['source_cavity_count'] is not None and not r['source_cavity_compatible']],cavity_count_source_unknown_but_raster_stable=sum(source[r['parent_id']]['source_cavity_count'] is None and r['features']['significant_cavity_count']['raster_status']=='stable' for r in resolved),method='First failure partition source extent then threshold correspondence then8 core/family requirement. Different gates overlap; no causal fraction inferred from overlapping raw descriptors.'))
    # Preserve pair absten­tions and both denominators.
    key=read_json(D/'similarity_hidden_key.json')['pairs'];ratings={r['pair_id']:r['rating'] for r in read_json(D/'similarity_decisions.json')['pairs']};primary=[r for r in key if ratings[r['pair_id']] in [0,2] and r['profile_distance'] is not None];save(T/'similarity_observability.json',dict(primary_positive=sum(ratings[r['pair_id']]==2 for r in primary),primary_negative=sum(ratings[r['pair_id']]==0 for r in primary),pair_statuses=dict(Counter('scorable' if r['profile_distance'] is not None else 'feature_abstention' for r in key)),unavailable_rating_counts=dict(Counter(str(ratings[r['pair_id']]) for r in key if r['profile_distance'] is None)),both_whole_profiles_usable_pairs=sum(rows[r['anchor_index']]['usable_partial_profile'] and rows[r['reference_index']]['usable_partial_profile'] for r in key),interpretation='Primary comparison uses shared qualified descriptors under the registered8-field/family rule, not full-profile usability. Whole-parent acceptance coverage is separate; unavailable distances abstain rather than being scored as dissimilar. Selection was balanced across profile/contour/random-aspect methods, deduplicated. No missing-value imputation.'))
    gates=cov['gates'];gates['source_uncertainty_preserved']=read_json(T/'deterministic_replay.json')['source_uncertainty_preserved'];gates['deterministic_replay']=True
    save(T/'acceptance_summary.json',dict(coverage_source_gates=gates,coverage_source_pass=all(gates.values()),similarity_gates=sim['gates'],similarity_superiority_pass=sim['similarity_superiority_gate_pass'],frozen_feature_protocol_unchanged=True,no_new_classes=True,no_downstream_tests=True,central_answer='Partial representations remain reproducible for a subset, but broad fresh-source and V3-unknown coverage and all-baseline superiority are not validated.'))
    fig,ax=plt.subplots(1,2,figsize=(10,4));ax[0].bar(['Fresh all','Fresh resolved','Fresh V3 UNK','Reference'],[81/129,81/118,44/92,75/88],color=['#347c98','#347c98','#b07747','#879f81']);ax[0].set_ylim(0,1);ax[0].set_ylabel('Usable partial-profile fraction');ax[0].tick_params(axis='x',rotation=20);ax[0].set_title('Separate declared denominators');ax[1].bar(list(sim['metrics']),[v['auc'] for v in sim['metrics'].values()],color=['#347c98','#999','#b07747','#879f81']);ax[1].set_ylim(0,1);ax[1].set_ylabel('AUROC on common99 source pairs');ax[1].set_title('54 same,67 different in full185-pair audit');fig.tight_layout();fig.savefig(G/'trial2_summary.png',dpi=160);plt.close(fig)
    details=[]
    for r in rows:
        src=source[r['parent_id']];q=aids[r['parent_id']];ff=[]
        for k,v in r['features'].items():
            val='NA' if v['primary'] is None else f"{v['primary']:.4g}";rng='NA' if v['range'] is None else f"{v['range'][0]:.4g}..{v['range'][1]:.4g}";ff.append(f"<tr><td>{k}</td><td>{val}</td><td>{rng}</td><td>{v['raster_status']}</td><td>{v['source_qualified_status']}</td></tr>")
        details.append(f"<details><summary>{r['audit_id']} / {r['parent_id']} / caption {r['caption']} / usable {r['usable_partial_profile']} / reporting V3 {lab[r['parent_id']]}</summary><img src='../{q['native_crop']}' style='max-width:600px;image-rendering:pixelated'><p>Native {r['native_source']} bbox {r['native_bbox']}; {src['membership']}; {src['source_parent_status']}. Visible cavity count {src['source_cavity_count']}; {src['source_cavity_placement']}. {html.escape(src['note'])}</p><table><tr><th>Descriptor</th><th>Primary</th><th>Full range</th><th>Raster</th><th>Source-qualified</th></tr>{''.join(ff)}</table></details>")
    atlas=OUT/'reports/22_neutral_feature_profiles_trial2.html';atlas.write_text("<!doctype html><meta charset='utf-8'><title>Trial2 partial profiles</title><style>body{font:16px system-ui;max-width:1350px;margin:25px auto}summary{padding:12px;background:#edf1f2;margin-top:5px}td,th{padding:5px;border-bottom:1px solid #ddd}table{border-collapse:collapse}p{max-width:1100px}</style><h1>Neutral structural feature profiles — Trial2</h1><p>221 source-traceable proposals. Whole-parent evidence remains primary. Source semantics and raster repeatability are separate columns. V3 labels were introduced only after source/metric/rating seals and are diagnostic. These fields define no letters, internal units, pen lifts, stroke order or meaning. Unknown source cavities are never replaced by numerically stable guesses.</p>"+''.join(details),encoding='utf-8')
    f=cov['summary']['fresh'];u=cov['summary']['fresh_V3_UNKNOWN'];sa=cov['source_agreement']['fresh'];ct='\n'.join(f"| {c} | {s['confirmed']} | {s['resolved']} | {s['usable']} | {s['overall_rate']:.1%} |" for c,s in cov['by_fresh_caption'].items());ft='\n'.join(f"| {r['descriptor']} | {'core' if r['core'] else 'secondary'} | {r['raster_stable_n']}/129 | {r['source_qualified_stable_n']}/129 |" for r in table);co='\n'.join(f"| {c} | {v['parents']} | {v['captions']} | {v['crosscaption_mean_distance']:.3f} | {v['null999_median']:.3f} | {v['p_lower']:.3f} |" for c,v in coh['classes'].items());mt='\n'.join(f"| {k} | {v['auc']:.3f} | {v['spearman']:.3f} |" for k,v in sim['metrics'].items());gt='\n'.join(f"| {k} | {'pass' if v else 'fail'} |" for k,v in gates.items());obs=read_json(T/'similarity_observability.json');failuretext=', '.join(f'{k}: {v}' for k,v in failure.items())
    report=f'''# Neutral Structural Feature Profiles Trial2

Trial2 is preregistered, executed and ready for an immutable evidence freeze. **The broad validation claim fails.** Usable source-qualified partial profiles cover **81/129 (62.8%)** fresh confirmed-writing proposals and **44/92 (47.8%)** fresh V3-unknown confirmed-writing proposals. The fixed feature distance predicts source-rated similarity better than aspect alone, but worse than contour: AUROC **0.795 vs0.917**. Preserve the partial-description result without promoting it to a practical notation or validated compositional inventory.

Trial1 remains exploratory and unchanged. V3, V4, V5 and V6 remain immutable. No position, section, conventional-transcription, sequence or decipherment correlations were inspected. Class labels were used solely for the explicitly registered diagnostics after source decisions, features, metrics and pair judgments were sealed.

## Protocol and chronological protection

[PLAN](../data/observations/neutral_feature_trial2/PLAN.json) was registered at {spec['registered_at_utc']} and hashed in [SPECIFICATION_SEAL](../data/observations/neutral_feature_trial2/SPECIFICATION_SEAL.json) before fresh source inspection. Revisions came from Trial1 **overall** operational stability and definition failures, not V3-conditioned coverage or downstream results. Of36 descriptors,25 are core. Skeleton graph counts, raster components and redundant thirds remain secondary uncertain fields; they cannot rescue or block eligibility solely by graph instability. Native dimensions are secondary, excluded from cross-capture similarity.

Height/body and width/body tolerances are0.40: full log body-reference range log(1.1/0.9)=0.20067 plus permitted native measurement span0.18 totals0.38067, rounded upward before measurements. Native log dimensions retain0.18. Other tolerances were not retuned. Every field retains the seven variant values, primary value, interval, raw raster status and separate source-qualified status. No tolerance adjustment followed the failures.

The frozen stages are [source judgments](../data/observations/neutral_feature_trial2/SOURCE_SEAL.json), [metric inputs](../data/observations/neutral_feature_trial2/METRIC_SEAL.json), [anonymous similarity judgments](../data/observations/neutral_feature_trial2/RATING_SEAL.json) and [repeat judgments](../data/observations/neutral_feature_trial2/REPEAT_SEAL.json). A reporting implementation initially projected a nonexistent V6 class field and would have made reference labels all UNK. The unsealed diagnostic runner was corrected to assert agreement with V6's **retained_v3_class** and use sealed fresh **v3_class** values. Diagnostics were regenerated; features, source judgments, distances, ratings and acceptance criteria were unchanged.

## Source corpus and whole-parent qualification

88 reference parents were sampled by fixed seed, up to8 from each11 existing caption groups, using confirmed writing/resolved source evidence and no class selection. Six fresh captions17,19,22,52,56,100 supply133 proposals from preselected ordinary horizontal fields. Native Yale RGB, parent crops and expanded context were reviewed before numerical features or V3 suggestions. These captions are fresh for Trial2 specification and Trial1/V6 feature tuning, although earlier V3/V4 imagery exposure exists; they are not globally unseen manuscript photographs.

129 fresh proposals are confirmed writing,11 with unresolved contact/whole-parent extent;3 remain unresolved writing/texture/association;1 is confirmed nonwriting substrate contrast. The11 uncertain writing cases remain in the primary confirmed-writing denominator. Their numeric fields are diagnostic and they are not accepted complete parents. In particular, N094/N095 have a faint upper-bridge join alternative, visible in [extended source context](../figures/neutral_feature_trial2/V_112_upper_context_extension.png); neither raster part is promoted to an accepted separate whole parent. No bridge pixels were invented. These are parent **proposals**, not a certified count of distinct physical writing units. Proposal selection(area≥35/core support≥8) excludes some fine fragments and does not establish all-ink recall.

| Fresh caption | Confirmed proposals | Resolved whole parent | Usable profiles | All-confirmed coverage |
|---|---:|---:|---:|---:|
{ct}

Fresh conditional resolved coverage is81/118=68.6%; reference coverage75/88=85.2%. The fresh overall caption-bootstrap95% interval is {cov['fresh_overall_caption_bootstrap95'][0]:.1%}–{cov['fresh_overall_caption_bootstrap95'][1]:.1%}, based on only six clusters. Among fresh V3 unknowns,44/81 resolved parents qualify conditionally(54.3%). All37 fresh frozen-V3 assigned parents have usable profiles; this reporting split did not choose the features. First-failure partition of129 confirmed proposals: **{failuretext}**. Threshold correspondence failure is a whole-parent recovery limitation, separate from sparse stable-field representation. Removing it for coverage would change the registered question.

Historical reused-data sensitivity gives{hist['usable_n']}/{hist['resolved_n']} resolved parents using704 Trial1 variant arrays under the new fixed tolerances/core rules. Only88 have Trial2 source-cavity audits; other cavity fields remain source-unknown. This reused result cannot replace the failed fresh test or be used to retune it.

## Descriptor stability and source evidence

The following denominators are129 fresh confirmed-writing proposals, including uncertain whole-parent cases. Stable numeric fields on an uncertain extent do not make the parent usable. Cavity centroids can be genuinely not applicable when no cavity exists; the full machine-readable table reports applicability separately.

| Descriptor | Eligibility role | Raster stable | Stable after source qualification |
|---|---|---:|---:|
{ft}

On118 source-resolved fresh parents,107 have photographically adjudicable cavity counts; **78/107=72.9%** agree with the primary significant-cavity measurement, below85%.65 are both count-compatible and raster-stable.11 counts remain source-unknown. Visible cavity counts and the fixed significant-mask cutoff(max8px/1.2% ink) have different definitions, and faint closures/filled regions further limit agreement. Disagreements become source-unknown fields rather than deletion or cutoff repair. Position-qualified cavities additionally require compatible resolved upper/lower/both/none placement; near-midpoint±0.05 uncertainty stays unknown. Raster-area/centroid values are measurements of the qualified masked cavities, not independently certified physical contours.

Coarse source aspect agrees114/118=96.6%, passing85%, but judgments were bbox-aided; this is not independent accuracy against external physical truth. Near-horizontal span judgments are retained, and [run association](../tests/neutral_feature_trial2/source_run_association.json) reports distributions without choosing a new semantic run cutoff. A contiguous horizontal raster run cannot by itself establish a bench, frame or insertion. Source membership, cavities, aspect and span judgments were all made by the same AI observer, not an independent human panel.

## Known-class diagnostic coherence

Frozen V3 was applied unchanged to fresh resolved writing; old labels were projected for reporting only. Six classes meet the registered≥5 usable instances/≥3-caption diagnostic requirement. The other classes have inadequate sampled support; their absence here is not evidence of incoherence. No learned distance or classifier was fitted.

| V3 reporting class | Usable parents | Captions | Within-class cross-caption distance |999-label null median | Lower-tail p |
|---|---:|---:|---:|---:|---:|
{co}

Leave-caption nearest-class retrieval is49/54=90.7% **restricted to these eligible classes**; this is neither broad fourteen-class accuracy nor independent source-class validation. The999 within-caption known-label permutations preserve caption frequencies. P values are exploratory/unadjusted; class assignments and descriptors share image geometry, and repeated parents/captions constrain inference.

## Class-resistant continuous configurations

There are{un['source_confirmed_unknown_n']} confirmed V3 unknown proposals in the combined source audit;{un['usable_unknown_n']} have usable partial profiles. With the fixed≤0.25 qualified-family distance,{un['crosscaption_neighbor_n']} have another-caption unknown neighbor and **{un['three_caption_support_n']}** have support spanning≥3 captions including self. **{un['fresh_reference_transport_n']} fresh unknowns** match a reference unknown under that neighborhood rule. These overlapping neighborhoods are not transitive equivalence classes or compositional units.

The999 caption-conditional independently permuted family-vector null has mean{un['null999_threecaption_mean']:.3f} three-caption-supported parents(95% interval{un['null999_threecaption95']}; upper-tail p={un['p_upper']:.3f}). This supplies limited evidence of recurrent feature combinations in a few unknowns, not broad recurrent unknown coverage. The null preserves per-caption family-vector/missingness marginals, not each parent's cross-family association; it is a composite-morphology control, not a writing-system or language null. No unknown was merged, split or assigned a new discrete class.

## Held-out source-image similarity

72 resolved-writing anchors, up to12 per fresh caption, produced185 deduplicated pairs from profile-nearest, contour-nearest and seeded aspect-matched-random references. Anonymous source RGB pairs were rated before prediction/selector keys or V3 reporting labels were opened:54 same whole organization(2),64 partial(1),67 different(0),0 unresolvable(U). Differences in visible organization were retained as partial rather than forced into same/different. Neighbouring contextual ink is excluded from the parent judgment where source ownership is resolved.

33 pairs lack the registered≥8 shared-core/family distance and explicitly abstain. Primary AUROC uses the common99 available-distance pairs rated0/2({obs['primary_positive']} positive,{obs['primary_negative']} negative);64 partials remain reported. This misses the declared120-pair minimum. Distance observability and whole-parent usability are distinct: the registered distance can compare shared qualified descriptors even when whole-parent raster correspondence fails. [Observability details](../tests/neutral_feature_trial2/similarity_observability.json) report both, without imputing missing profiles or treating abstention as dissimilarity.

| Fixed metric | Primary AUROC | Ordinal similarity association |
|---|---:|---:|
{mt}

Feature-minus-aspect delta+0.168, paired six-caption bootstrap95%+0.075 to+0.291. Feature-minus-contour delta−0.122,95%−0.204 to−0.030. Feature-minus-combined delta−0.069,95%−0.156 to+0.026. Features fail the required≥0.05 improvement with positive lower interval against **each** baseline. These are selected hard/nearest-reference pairs with repeated anchors/references, not a random-pair population. Caption bootstrap does not remove reference reuse. Source ratings are same-AI judgments and are not independent physical truth.

The12 preregistered anonymous repeated pairs agree12/12(3 different,4 partial,5 same). Prior IDs/ratings were hidden in the repeat display, with intervening replay work, but separation was short and prior conversational exposure persists. This is same-adjudicator repeatability only; no independent inter-rater reliability or memory washout is claimed.

## Registered disposition and freeze

| Coverage/source criterion | Result |
|---|---|
{gt}

Similarity AUROC≥0.75 passes; sample≥120 and superiority against all baselines fail. Feature-specific unknowns are preserved and all221×36 seven-variant profiles and five distance matrices reproduce exactly from sealed native masks. Integrity/replay is bookkeeping and operational reproducibility, not validation of source semantics.

**Answer:** reproducible partial descriptions exist, and a few class-resistant forms share configurations across captions. Trial2 does **not** validate a partial representation of most fresh confirmed writing under the declared coverage standards, particularly V3 unknowns. The strongest current limitations are whole-parent threshold recovery and source/raster cavity discordance; stable graph counts were unnecessary and body normalization was repaired without rescuing broad coverage. These results justify retaining the feature evidence and uncertainty, not reopening downstream assays or optimizing features to improve sequence behavior.

The [Trial2 manifest](../data/observations/neutral_feature_trial2/FREEZE_MANIFEST.json) seals the specification, source evidence, profiles, fixed metrics, source judgments, repeat, diagnostics, failures, report and scripts. Previous freezes/Trial1 remain untouched. New hypotheses require a separately preregistered trial. This package is a neutral-feature trial, not V7 segmentation, new classes or a decipherment result.

[Source-profile atlas](22_neutral_feature_profiles_trial2.html) · [summary figure](../figures/neutral_feature_trial2/trial2_summary.png) · [acceptance gates](../tests/neutral_feature_trial2/acceptance_summary.json) · [postfreeze audit](../tests/neutral_feature_trial2_postfreeze/integrity.json)
'''
    (OUT/'reports/21_neutral_structural_feature_profiles_trial2.md').write_text(report,encoding='utf-8');print('Trial2 report,221-profile atlas and diagnostics written',flush=True)
if __name__=='__main__':main()
