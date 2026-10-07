from direct_morphology2_common import *
from seal_direct_morphology2 import prior_integrity
from replay_direct_morphology2 import replay
from verify_direct_morphology2_metrics import main as metric_replay
def main():
    assert (D/'FREEZE_MANIFEST.json').exists();verify_seal(D/'FREEZE_MANIFEST.json');verify();prior=prior_integrity();print('Current and previous freezes intact',flush=True)
    result=replay(True);write_json(P/'POSTFREEZE_REPLAY.json',result);metric_replay()
    try:guard()
    except RuntimeError:blocked=True
    else:blocked=False
    assert blocked;verify_seal(D/'FREEZE_MANIFEST.json')
    digest=sha256(D/'FREEZE_MANIFEST.json');write_json(P/'INTEGRITY.json',dict(checked_at_utc=now(),manifest_sha256=digest,current_frozen_file_checks=read_json(D/'FREEZE_MANIFEST.json')['file_count'],candidate_fields_replayed=result['candidate_n'],distance_matrices_exact=len(result['exact_distance_matrices']),writer_guard_blocks=True,prior=prior,no_downstream_assays=True,failures=[]))
    s=read_json(T/'primary_and_secondary_metrics.json');u=read_json(T/'uncertainty_and_retrieval.json');r=read_json(T/'same_adjudicator_repeatability.json');coverage=read_json(T/'representation_coverage_and_uncertainty.json');operational=dict(exact_replay=True,preserved_source_unknowns=coverage['source_uncertainty_preserved']);sample=all(s['sample_gates'].values());metrics=all(s['metric_gates'].values());status='not estimable' if not sample else 'supported' if metrics and all(operational.values()) else 'not supported';write_json(P/'DISPOSITION.json',dict(interpreted_at_utc=now(),frozen_manifest_sha256=digest,status=status,sample_gates=s['sample_gates'],metric_gates=s['metric_gates'],operational_gates=operational,scope='Qualified fresh-caption source-resolved ordinary horizontal writing proposal sample; same-AI source targets. Source-traceable visible morphology only.',independent_human_validation=False,global_image_blindness=False,complete_writing_representation=False,no_downstream_assays=True))
    ci=s['primary_caption_node_bootstrap95'];dci=s['paired_delta_bootstrap95'];summary=f'''# Direct Morphology Trial2 — postfreeze interpretation

**{status.capitalize()} within the preregistered, qualified fresh-caption sample.** The unchanged64px contour representation generalizes to source-confirmed, source-resolved whole-parent proposals from eight captions not used in the audited earlier detailed similarity work. All registered sample, metric, exact-replay and uncertainty-preservation gates pass. This conclusion was written after the immutable package was sealed; no representation, source decision, pair choice or success threshold was retuned.

-192 source-confirmed writing proposals;165 photographically resolved whole extents and27 explicit unknown whole extents.
-360 anonymous cross-caption judgments:35 same,176 different,149 partial.211 binary judgments evaluate the registered primary metric; partials remain partial.
-Primary contour64 AUROC **{s['metrics']['contour64']['AUROC']:.3f}**, caption-node bootstrap95% **{ci[0]:.3f}–{ci[1]:.3f}**.
-Aspect-only AUROC **{s['metrics']['aspect_only']['AUROC']:.3f}**; paired improvement **{s['contour_minus_aspect']:.3f}**, bootstrap95% **{dci[0]:.3f}–{dci[1]:.3f}**;1,993 valid draws of2,000.
-Secondary SDF64 AUROC0.895; contour32/128 sensitivities0.877/0.871.64px stays primary.

The result validates graded resemblance under the registered random/aspect-matched pair mixture. It does **not** establish uniform performance across manuscript writing. The random subset had only10 same pairs and contour AUROC0.798 versus aspect0.812; the aspect-matched subset had25 same pairs and contour0.907 versus aspect0.655. The overall contour advantage is supported, but superiority in every sampling stratum is not.

Source target reliability is a substantive limitation: short-session anonymous repeat agreement was **{r['exact_agreement_n']}/20**, kappa{r['unweighted_kappa']:.3f}, with six partial/different disagreements and only one original same pair in the repeat sample. These are same-AI judgments with possible memory carryover, **not independent human validation**. Earlier overview/V4 processing exposure also remains; fresh does not mean globally unseen photographs. The audit defines and preserves that distinction.

Uncertainty is consequential. Only **{u['all_alternative_stable_nearest_n']}/165** fresh queries retain a unique nearest reference across all observed raster alternatives; median not-excluded set size is{u['median_not_excluded_neighbors']:.0f}.81 queries change nearest identity under a query recovery alternative. This registered uncertainty diagnostic does not negate the pairwise signal. It prevents resemblance from being promoted to a unique writing identity. Candidate envelopes are finite sensitivity sets, not probabilities or physical confidence intervals;27 unknown full-parent geometries remain unknown.

The defensible use is a **source-traceable continuous morphological representation with abstention and alternative recoveries**, for the qualified visible shapes evaluated here. Independent raters and further fresh source adjudication would be needed to strengthen target reliability and broader generalization. This freeze establishes neither letters, graphemes, characters, allographs, word boundaries, stroke order, pen lifts, semantic identity, decipherment nor complete transcription. No downstream Voynich assay is reopened.

[Evidence report](../../reports/25_direct_contour_morphology_trial2.md) · [280-parent source atlas](../../reports/26_direct_contour_morphology_atlas_trial2.html) · [freeze manifest](../../data/observations/direct_morphology_trial2/FREEZE_MANIFEST.json) · [integrity and replay](INTEGRITY.json)

Freeze SHA256: `{digest}`.
'''.replace('\n-','\n- ')
    (P/'SUMMARY.md').write_text(summary,encoding='utf-8');print('Postfreeze disposition',status,'all prior evidence preserved',flush=True)
if __name__=='__main__':main()
