# Direct continuous contour/morphology space — Trial1

**Yes: an explicit, reproducible image-shape representation can be constructed without discrete classes or a complete named-feature profile.** This separate preregistered feasibility trial represents217 source-confirmed writing proposals as1,124 direct contour/signed-distance image fields.206 have source-resolved whole extents;11 retain **unknown full-parent geometry**. Every observed candidate has coordinates, but an observed-part coordinate is not a certified whole-parent representation.

On121 reused same/different source pairs, fixed primary contour AUROC is **0.910**. Uncertainty remains consequential: only **10/118** source-resolved fresh-for-Trial2 parents have a nominal nearest reference that stays certainly nearest across observed raster/slant alternatives. Thus a continuous morphology space supports graded resemblance while often requiring an unresolved set of neighbors.

## Preregistration and scope

[PLAN](../data/observations/direct_morphology_trial1/PLAN.json) and [specification seal](../data/observations/direct_morphology_trial1/SPECIFICATION_SEAL.json) predate this trial's shape/distance outcomes. Trial2's superior contour result was already known and motivated the trial. This is **post-exposure feasibility and sensitivity**, not fresh independent confirmation. Trial1/Trial2 feature packages and V3–V6 remain immutable. No V3 class labels, semantic feature profiles, conventional strings, Currier data, positional/section effects, sequences or decipherment outcomes define the representation or metric.

The corpus reuses Trial2's frozen source adjudication:88 reference proposals and129 fresh-for-Trial2 confirmed-writing proposals from six caption groups. Three unresolved proposals and one nonwriting detection are excluded and enumerated. Native photographs, coordinates and original source judgments remain primary. No breadth expansion or new parent/source ownership decision occurred. Current proposal sampling cannot establish all-writing recall or a complete row/sequence extraction.

## Representation

Each parent record stores the native photo/mask/coordinates, source extent state and an **ensemble of observed recovery candidates**. Each candidate is represented directly by an aspect-preserving64×64 binary image and normalized signed-distance field. Tight envelope dimensions fit within56×56 support, centered, using nearest-neighbor resampling. Orientation/aspect are preserved; overall size and translation are normalized away. Native size/body proxy remain source metadata. There is no rotation, reflection, learned alignment, PCA, class prototype, cluster label or hand-designed completeness requirement. The ambient4,096 pixel-field coordinates are measurements of an image function, not a semantic alphabet.

Primary distance is symmetric contour Chamfer divided by56, using inner and outer **raster** boundaries. Secondary morphology distance is signed-distance-field RMS.32/128px are registered sensitivity resolutions;64px stays primary despite their observed scores. Normalization/resampling can remove or alter fine details, so the native photo/mask remains accessible. Negative space, apparent closure and raster connectivity are not automatically photographically certified cavities or physical joins.

At contrast6/12, every component covering≥5% of primary-mask ink is retained. Multiple matches produce both component candidates and a union preserving native relative placement. Possible merged extents retain contamination flags. These candidates include failed/incomplete recoveries and are **not all source-certified physical whole parents**. Missing matches would retain an explicit absence state; none occurs in this sample. Synthetic±0.04 slants probe nuisance sensitivity only. No connecting ink is fabricated.

Source uncertainty differs from raster variability. A source-resolved extent can still have multiple inadequate raster recoveries. An uncertain extent has provisional observed-part vectors plus an explicit unknown full-parent state. N094/N095 retain the frozen possible faint-bridge join and a partial union; unresolved bridge pixels are omitted, and its full-parent embedding remains absent. Similarity does not decide whether these parts physically connect.

## Coverage and correspondence

Observed primary coordinates are available for217/217 confirmed-writing proposals. Source-resolved whole extents are206/217, including118/129 fresh-for-Trial2 proposals. The other11 are not counted as resolved whole shapes. Availability therefore does not establish source fidelity, writing-unit boundaries or complete extraction.

Across217 parents,18 have split and43 have merge recovery cases(counts overlap);0 have missing threshold matches. Fresh-for-Trial2 counts are14 splits and33 merges. Median candidate count is5. Median maximum primary-to-raster candidate contour spread is0.0153,95th percentile0.0983. Median slant spread is0.0038. These are normalized geometric sensitivities, not source-rater disagreement or uncertainty probabilities. No threshold was chosen to convert spread into a writing class.

## Reused source-image similarity

The fixed185 pairs previously selected through pooled profile/contour/aspect methods retain54 same whole-organization ratings,64 partial,67 different,0 unresolvable. All121 binary pairs now have observed contour distances and source-resolved extents;64 partials remain reported, not forced into binary labels. The source judgments were made by the same AI with repeated references/anchors. Pair selection and outcomes were already exposed. Scores are conditional descriptive checks, not independent validation.

| Fixed direct metric | AUROC on121 binary pairs | Ordinal association on185 pairs |
|---|---:|---:|
| contour64 | 0.910 | 0.584 |
| sdf64 | 0.890 | 0.559 |
| contour32 | 0.919 | 0.594 |
| contour128 | 0.913 | 0.590 |

Primary contour six-caption bootstrap95% is0.874–0.946. This does not remove source-judgment dependence, repeated reference reuse or prior outcome exposure. Trial2's reported0.917 contour baseline used a different99-pair common-feature subset and24px normalization; direct comparisons of those values would mix estimands.

## Uncertainty-aware similarity

For each source pair, preserve its primary distance and the minimum/maximum over observed candidate recoveries/slants. These are **observed sensitivity envelopes**, not calibrated posterior intervals, exhaustive physical bounds or a probability of same writing identity. They intentionally include fragmented or contaminated recoveries; a wide envelope can diagnose extraction failure rather than variation of a true parent. Unknown full extent remains unknown regardless of a finite candidate envelope. Complete physical distance intervals are not estimated in any record.

Among3,618 same-vs-different pair comparisons,2,097(58.0%) are correctly ordered for every observed candidate-distance choice,63(1.7%) are reversed for every choice and1,458(40.3%) overlap/tie. The resulting0.580–0.983 sensitivity ordering bounds are **not an AUROC confidence interval**; repeated/correlated candidate choices make them conservative diagnostic envelopes rather than a joint posterior.

All118 source-resolved fresh-for-Trial2 parents were queried against88 reference parents from different captions, without any class labels. Only10(8.5%) have their primary nearest reference certainly nearest under the observed envelopes. Median not-excluded reference set size is7.5. Primary nearest reference is unchanged in93/118 cases at32px and110/118 at128px. These are **image-similarity ranks**, not manuscript token rank or pixel position. A neighbor set is not a discrete class or writing equivalence relation; no source parent boundary was selected to improve a match.

## Interpretation and disposition

The operational feasibility criteria pass: nonempty observed representation, explicit unknown source extents, and no discrete classes or mandatory named-feature vector. The registered descriptive AUROC/sample/caption checks also pass. **Fresh independent generalization remains untested.** The more informative limitation is uncertainty in recovered outlines and nearest matches, which a class-free representation makes visible rather than eliminating.

A defensible record is: native source evidence + extent hypotheses/UNKNOWN + candidate contour/SDF coordinates + provenance + observed distance envelope/abstention. It can describe graded morphology even when a form resists discrete assignment. It cannot establish letters, internal graphemes, pen lifts, stroke order, complete writing membership, physical connection, semantic identity or a usable sequence notation.

The separate [Trial1 freeze](../data/observations/direct_morphology_trial1/FREEZE_MANIFEST.json) preserves the protocol, candidate/native arrays, source alternatives, metrics, uncertainty failures, source atlas and code. [Postfreeze integrity/replay](../tests/direct_morphology_trial1_postfreeze/integrity.json) checks both this package and earlier freezes. No downstream assay is reopened. A later genuinely fresh source-image test must be preregistered before interpreting this as generalizable manuscript morphology.

[Source ensemble atlas](24_direct_contour_morphology_atlas_trial1.html) · [image-field examples](../figures/direct_morphology_trial1/direct_shape_examples.png) · [acceptance distinctions](../tests/direct_morphology_trial1/acceptance_summary.json)
