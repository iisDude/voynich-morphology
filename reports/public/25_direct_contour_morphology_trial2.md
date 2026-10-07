> Publication link-adapted view; the original report is preserved unchanged in `reports/`.

# Direct Continuous Contour/Morphology Trial2 — frozen evidence report

The unchanged primary **contour64 AUROC is 0.879** on211 fresh cross-caption binary source judgments. The caption-node bootstrap95% interval is **0.767–1.000**. Aspect-only AUROC is **0.737**; paired improvement is **0.141**, with bootstrap95% **0.020–0.261**. This report records measurements and registered gate evaluations. Interpretive disposition is written separately **after the complete Trial2 freeze**.

## Freshness and corpus selection

The [eligibility audit](../../data/direct_morphology/trial2/CAPTION_ELIGIBILITY.json) projects caption/source identifiers against V3–V6 detailed parent and source corpora, both feature trials, Direct Trial1 and prior source-similarity pairs. It covers102 caption groups and resolves all prior pair references.45 groups meet the conservative eligibility definition. The first partial audit missed some source-view mappings; it was repaired before selection freeze, with the initial diagnostic preserved. No morphology outcomes existed during this repair.

Globally untouched photographs are unavailable after earlier overview exposure and extraction. **Fresh** means unused in the audited detailed V3 fitting/selection, V5/V6 source adjudication, feature-trial inputs/specification, Direct Trial1 corpus and known prior similarity pair sets. Earlier overview processing and V4 broad extraction/frozen-model application remain. This is new caption-level similarity validation, not globally blind image discovery.

Eight captions **7,11,29,31,45,48,54,87**, two ordinary horizontal fields each, were chosen by layout and source quality from the eligible pool before extraction. The caption54 field edge was trimmed after RGB layout inspection to avoid visible drawing; no morphology informed it.24 seeded foreground proposals per caption yielded192 parents. Selection uses source layout, contrast and fixed area/core criteria, not resemblance, recurrence, labels or outcomes. It is a proposal-conditioned clear-field sample, **not a writing-ink census**. Source selection and all coordinates are preserved in [SELECTED_FIELDS](../../data/direct_morphology/trial2/SELECTED_FIELDS.json) and [selection seal](../../data/direct_morphology/trial2/SELECTION_SEAL.json).

## Source judgments first

Native Yale RGB fields and parent contexts were inspected before distances, neighbors, structural labels or conventional information. All192 sampled objects are confirmed writing.165 have photographically resolved whole extent;27 retain unknown full extent. Membership certainty and extent certainty are separate. This selected foreground sample therefore supplies no estimate of nonwriting rejection, complete writing recall or exact row extraction.

[Source decisions](../../data/direct_morphology/trial2/source_decisions.json.gz) retain joins/splits, contacts, faint ink, neighboring contamination, detached alternatives, field-edge status and physical coordinates. Wider RGB contexts qualify difficult cases. S051/S052 and S055/S056 retain possible source joins; their partial unions contain no invented bridge. S181 lacks a source-certified full-parent contour beyond its detected lower part. A finite raster candidate never resolves these source questions. Automatic row bands and boxes are locational aids, not independent certification of row ownership or pixel-perfect physical ink boundaries.

The [source seal](../../data/direct_morphology/trial2/SOURCE_SEAL.json) predates candidate construction and predictions. Unknown full geometry remains explicit. Whole connected evidence is primary; no internal graphemes, stroke order, pen lifts or linguistic units were inferred.

## Unchanged representation

Frozen Trial1 functions are imported unchanged: aspect-preserving tight masks centered in64×64 with56px support; nearest resampling; signed-distance fields normalized by support; symmetric inner/outer raster contour Chamfer normalized by56. Orientation and aspect are preserved. Translation and absolute scale are normalized away, with native dimensions retained. There is no rotation/reflection alignment, PCA, clustering, learned embedding, prototype, V3 label or required handcrafted vector.

Native contrast9 primary masks and all observed contrast6/12 correspondences covering≥5% of primary ink are retained. Split fragments and native-coordinate unions, possible merges, missing-state checks and±.04 synthetic slant sensitivities follow the exact Trial1 procedure. None is selected to improve similarity. They are recovery hypotheses, not equally certified physical shapes. Fresh counts:13 split cases,20 merge cases and0 missing threshold matches; categories overlap.

There are280 parent records:192 fresh plus88 separately frozen reference parents, with1,437 candidate image fields. All imported reference fields match Trial1 exactly. Unknown extents have observed-part coordinates and absent full-parent geometry. Source alternatives are retained separately rather than inserted into the primary evaluation as resolved whole parents. [Ensembles](../../data/direct_morphology/trial2/source_parent_ensembles.json.gz) map every coordinate to the native source, box and candidate.32px/128px contour remain sensitivity checks; SDF64 remains secondary.

## Sealed source evaluation

The [preregistration](../../data/direct_morphology/trial2/PLAN.json) specifies deterministic600-pair sampling before ratings: half broad cross-caption random, half aspect-matched, cycling caption dyads and native-envelope area quartiles, with parent degree≤12. No contour-nearest selection is used for the primary pool. Only165 source-resolved parents are eligible; the27 unknowns stay represented but do not supply invented full-shape judgments.

Anonymous RGB pairs were rated2 same whole organization,1 partial/related,0 different orU unresolved. Captions, pair-selection stratum, source IDs, shape distances, neighbors, feature profiles and class labels were hidden. Initial240 contained25 same judgments, below registered30; exactly the predetermined next120 were reviewed before any metric was computed. All360 opened pairs remain included:35 same,176 different,149 partial and0 unresolved.211 binary pairs enter primary AUROC;149 partials are preserved and used only in secondary ordinal association. Both binary categories involve all eight captions. Remaining240 pool pairs were prepared and sealed but **not reviewed or analyzed**.

These are same-AI source judgments, not independent human validation. Captions are fresh to the audited detailed similarity work; the same adjudicator and earlier overall photo exposure persist.

| Metric | Binary AUROC | Ordinal association on360 |
|---|---:|---:|
| contour64 | 0.879 | 0.364 |
| aspect_only | 0.737 | 0.202 |
| sdf64 | 0.895 | 0.355 |
| contour32 | 0.877 | 0.363 |
| contour128 | 0.871 | 0.355 |

The primary remains contour64 even though secondary SDF64 scores higher.2,000 two-endpoint caption-node bootstrap draws use pair weight=count(left caption)×count(right caption).1,993 retain both binary categories, exceeding registered1,800. Paired contour/aspect differences use identical weights. These conditional intervals account for shared captions, but cannot remove systematic adjudication bias or all repeated-parent dependence. Leave-one-caption-out contour AUROCs range0.857–0.916.

The frozen mixture matters: broad-random binary subset98(10 same) has contour64 AUROC0.798 and aspect0.812; aspect-matched subset113(25 same) has contour64 AUROC0.907 and aspect0.655. Overall superiority **does not establish superiority within every sampling stratum**, a uniform all-manuscript performance estimate or universal shape recognition. Neither stratum changes the registered pooled success criterion.

## Repeatability

Twenty uniform seeded repeats from all opened pairs, including partials, were presented under changed IDs/sides with prior decisions hidden. Representation replay intervened. Exact agreement is **14/20 (70%)**, unweighted kappa0.388. Six changes are partial↔different; the repeat sample contains only one original same pair, so it provides little evidence about repeatability of the positive category. Separation is short and same-session conversational memory persists. This is **same-AI repeatability only**, not independent human inter-rater validation. No repeatability pass threshold was preregistered, and none is introduced now. The modest repeatability limits confidence in the source target labels.

## Uncertainty and retrieval

Every reviewed pair stores primary/min/max observed contour and SDF distances and source extent status. These are sensitivity envelopes, **not probabilities, posterior intervals, exhaustive physical bounds or source-truth confidence intervals**. Among6,160 positive-negative pair-order comparisons,4738 are correct under every separate observed envelope choice,98 reversed, and1324 overlap/tie. The0.769–0.984 ordering envelope is not an AUROC confidence interval; correlated candidate choices and contaminated recoveries matter.

Separately,165 fresh source-resolved query parents are compared with88 frozen Trial1 reference parents from disjoint captions. **24/165** retain a unique nearest reference across every observed query alternative and independently variable reference alternatives. A stricter global-envelope sufficient criterion certifies23. Median conservative not-excluded set size is6.0. Query recovery alternatives change the primary-reference nearest identity for81/165 queries. Nearest identity agrees with64px in122/165 at32px and143/165 at128px; median full-reference rank correlation is0.983/0.996 respectively.

These ranks are image resemblance ranks. Neighbor sets are not classes or equivalence relations. Sparse unique-neighbor stability is a registered diagnostic, not an automatic failure. The [retrieval records](../../tests/direct_morphology_trial2/uncertainty_and_retrieval.json.gz) preserve changed-neighbor witnesses and full not-excluded sets. No source ownership decision is derived from retrieval. Unknown full extents are excluded only from this qualified whole-parent diagnostic and remain in the corpus.

## Registered gates, failures and freeze

The primary gates were≥6 captions,≥120 binary pairs,≥30 in each category, each category spanning≥4 captions, contour64 AUROC≥.80, caption-bootstrap lower≥.65, contour-aspect delta≥.05 and paired lower>0,≥1,800 valid bootstrap draws, exact deterministic replay and preserved source unknowns. Mechanical statistical gate values:

- caption_support: True.
- binary_support: True.
- same_support: True.
- different_support: True.
- each_category_caption_support: True.
- valid_bootstrap_support: True.
- primary_contour64_AUROC: True.
- caption_bootstrap_lower: True.
- aspect_delta: True.
- paired_delta_bootstrap_lower: True.

Exact replay and native-source recovery checks are stored separately. Implementation syntax validation caught one unmatched parenthesis before evaluator execution and before any prediction computation; it was corrected without changing methods. No outcome-directed retuning occurred. Limitations remain:27 unknown whole extents; raster splits/contamination;149 partial targets; small positive count; modest short-session repeatability; qualified source selection; no global image blindness; finite, nonexhaustive candidate alternatives.

The [final manifest](../../data/direct_morphology/trial2/FREEZE_MANIFEST.json.gz) seals this report, source audit/judgments, native masks/crops, candidate fields,600-pair sampling pool, used anonymous ratings, repeatability, metrics, uncertainty, code, dependencies and deterministic replay. [Postfreeze integrity](../../tests/direct_morphology_trial2_postfreeze/INTEGRITY.json) verifies this package and earlier evidence. [Postfreeze interpretation](../../tests/direct_morphology_trial2_postfreeze/SUMMARY.md) applies the pre-outcome decision rule only after freeze. Earlier freezes are preserved. No conventional, positional, section, semantic, sequence or decipherment assay has been opened.

[Source atlas](../../atlases/26_direct_contour_morphology_atlas_trial2.html) · [Native uncertainty examples](../../figures/direct_morphology_trial2/source_and_uncertainty_examples.png)
