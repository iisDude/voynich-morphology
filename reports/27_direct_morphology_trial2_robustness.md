# Direct Morphology Trial 2 — postfreeze robustness investigation v 1

**Classification: sensitive to one or more evaluation assumptions.** A substantial same/different morphology signal remains. Its strongest interpretation depends on the binary target, the sampling mixture and a limited set of repeated source parents. Conservative disjoint-parent analysis loses precision and the pooled advantage over aspect alone. Flagged raster recovery does not explain away the signal: removing those cases strengthens the original binary result.

Direct Morphology Trial 2 remains immutable and supported within its registered sample. This investigation is a separate sensitivity analysis, **not another validation pass**. It uses only frozen contour 64, frozen source judgments and the original 360 reviewed pairs. No unused evaluation pairs, new pages, structural classes or downstream information are opened. SDF 64, contour 32/128 and learned representations are not substituted.

## Dependence and ambiguous recovery

| Condition | Pairs (positive/negative) | Contour64 AUROC | Caption-node 95% | Aspect AUROC | Conditional support |
|---|---:|---:|---|---:|---|
| Original binary pairs | 211 (35/176) | 0.879 | 0.762–1.000 | 0.737 | yes |
| Each parent once | 63 (14/49) | 0.805 | 0.496–1.000 | 0.805 | yes |
| Each caption-dyad once | 28 (8/20) | 0.963 | 0.765–1.000 | 0.688 | yes |
| Each parent and dyad once | 28 (3/25) | 0.840 | 0.368–1.000 | 0.760 | limited |
| Extent + recovery clean | 150 (27/123) | 0.942 | 0.857–1.000 | 0.780 | yes |
| Clean, each parent once | 50 (15/35) | 0.964 | 0.879–1.000 | 0.789 | yes |
| Clean, parent + dyad once | 28 (5/23) | 1.000 | 1.000–1.000 | 0.800 | yes |
| Clean, field-edge aids excluded | 114 (21/93) | 0.929 | 0.839–1.000 | 0.816 | yes |

Original binary eligibility already excludes all 27 source-unknown whole extents, and the frozen extent/contact flags exclude **zero additional evaluated pairs**. Extent-clean unrestricted results therefore equal the original result. This redundant filter cannot test morphology generalization to the excluded unknown physical extents. Recovery-clean excludes missing, split or merged contrast 6/12 correspondence, using existing flags and no new numeric morphology cutoff.61/211 binary pairs are removed:8 same and 53 different. Across all 360 reviewed pairs,99 are removed, leaving 261. Connected-compound description alone does not discard a source-resolved whole parent. Field-edge exclusion is a separate sensitivity to a location aid, not a retrospective claim of unresolved physical extent.

Each-parent-once selection gives 63 binary pairs,14 same and 49 different, with 126 distinct parents. Its contour 64 AUROC 0.805 has conditional 95%0.496–1.000 and ties aspect-only AUROC 0.805. This does not establish a disappearance of morphology discrimination; it removes the previously precise evidence for its superiority to aspect on this particular subset. Shared captions and source-adjudicator bias remain.

The selection constrained by parent and caption-dyad has only 3 same pairs and 3,793/5,000 valid resamples. Its 0.840 point estimate is descriptive. Broad-random dyad selection is even sparser; a 0.370 score from one positive is **not treated as an adequately supported reversal**. Perfect 1.000 scores and degenerate 1.000–1.000 empirical intervals in other small selections likewise cannot establish perfect population discrimination. Resampling cannot introduce errors absent from a tiny selected sample.

Maximum-cardinality selections use parent≤1 and/or caption-dyad≤1 constraints, with seeded secondary priorities after count is maximized. Same/different category balance and distances are never objectives. All eligible dyads can be represented once where shown; some resulting category support is weak. The point estimates are conditional on the stored graph selections.

**Identical filtered populations can have different matched subsets.** Each analysis has its preregistered seed: extent-clean and original pools are identical, while recovery-clean and combined-clean pools are identical among eligible pairs. Differences between their matched scores reflect tie-breaking, not source exclusion. Reported unrestricted filter comparisons avoid that confounding. No seed was chosen to rescue a score.

Fifty additional seeded greedy admissible selections per binary constrained condition expose selection variability. They are supplementary to maximum-cardinality primary selections and may retain fewer pairs. Their min/median/max AUROCs are **selection ranges, not confidence intervals**:

| Constraint | Primary maximal pairs | Greedy AUROC min / median / max |
|---|---:|---|
| parent | 63 | 0.765 / 0.882 / 0.993 |
| dyad | 28 | 0.427 / 0.947 / 1.000 |
| parent_dyad | 28 | 0.531 / 0.862 / 1.000 |

The strong variation among dyad selections shows why one favorable subset cannot support a universal robustness claim. All 50 selections and category counts are preserved.

## Target sensitivity and the partial boundary

| Condition | Pairs (positive/negative) | Contour64 AUROC | Caption-node 95% | Aspect AUROC | Conditional support |
|---|---:|---:|---|---:|---|
| same vs partial | 184 (35/149) | 0.824 | 0.689–0.962 | 0.685 | yes |
| partial vs different | 325 (149/176) | 0.623 | 0.525–0.713 | 0.558 | yes |
| partial as same | 360 (184/176) | 0.672 | 0.593–0.748 | 0.592 | yes |
| partial as different | 360 (35/325) | 0.853 | 0.730–0.980 | 0.713 | yes |

Contour 64 separates **same from partial** reasonably well(AUROC 0.824), while **partial from different** is weaker(AUROC 0.623). Reclassifying every partial as same lowers pooled AUROC to 0.672, a 0.207 drop. Reclassifying every partial as different yields 0.853. The 0.672–0.853 range is an envelope of the **two uniform recoding scenarios**; it is not a sharp bound over all possible mixed assignments, a statement of true labels or permission to overwrite partial judgments.

Both scenarios change the binary question. A related organization is not established as the same whole organization. These calculations explain which distinction the frozen contour signal supports, without selecting a preferred recoding. Recovery cleaning leaves this asymmetry: same/partial AUROC 0.886, partial/different 0.626, partial-as-same 0.688 and partial-as-different 0.915. Disjoint-parent versions and both sampling strata are retained among all 108 conditions.

## Sampling mixture

| Condition | Pairs (positive/negative) | Contour64 AUROC | Caption-node 95% | Aspect AUROC | Conditional support |
|---|---:|---:|---|---:|---|
| broad random | 98 (10/88) | 0.798 | 0.520–1.000 | 0.812 | yes |
| broad random | 45 (6/39) | 0.786 | 0.237–1.000 | 0.846 | limited |
| broad random | 28 (3/25) | 0.547 | 0.136–1.000 | 0.813 | limited |
| aspect matched | 113 (25/88) | 0.907 | 0.770–1.000 | 0.655 | yes |
| aspect matched | 48 (16/32) | 0.855 | 0.623–1.000 | 0.602 | yes |
| aspect matched | 28 (6/22) | 0.977 | 0.905–1.000 | 0.750 | yes |

The broad-random subset gives contour 0.798 versus aspect 0.812; its 10 same judgments provide limited precision. The aspect-matched subset gives contour 0.907 versus aspect 0.655, with 25 same judgments. After parent-disjoint selection, aspect-matched contour remains 0.855 versus aspect 0.602. Broad-random disjoint estimates are less precise and do not establish contour superiority. The registered pooled mixture supplies a real conditional result, but its advantage over aspect is concentrated in geometric hard comparisons rather than demonstrated uniformly across both strata.

## Larger anonymous same-adjudicator repeat

The sealed 125-pair sample contains all 35 original same judgments, plus seeded uniform 45 partial and 45 different judgments. It is 6.25 times the earlier 20-pair repeat. New IDs, shuffled sides and randomized order hid original ratings/categories, source identities, strata and contour scores during nativeRGB review. Sealed subset preparation intervened. Prior image exposure and same-session conversational memory persist. This is **same-AI repeatability**, not independent human or inter-rater validation.

Exact agreement is **101/125 (80.8%)**, conditional caption-node 95%70.4–90.0%. Linear ordinal agreement, defined 1−|original−repeat|/2, is **90.4%**; quadratic agreement is 95.2%. Chance-corrected kappas are 0.708 unweighted,0.772 linear and 0.841 quadratic. All 24 disagreements are adjacent:15 partial↔different,8 same→partial and 1 partial→same. No direct same↔different flips occurred. The unstable boundary therefore includes both edges of the partial category.

| Original category | Retained | Retention | Conditional caption-node95% |
|---|---:|---:|---|
| same | 27/35 | 77.1% | 0.520–1.000 |
| partial | 36/45 | 80.0% | 0.538–0.971 |
| different | 38/45 | 84.4% | 0.634–1.000 |

Same retention is 27/35 (77.1%), partial 36/45 (80.0%), and different 38/45 (84.4%). Precision is limited by eight captions and the 35 available same cases. Because same pairs are oversampled, original-category-frequency reweighted exact agreement is 81.9%, linear agreement 90.9%; these accompany the raw balanced-repeat sample rather than replacing it. Reweighting addresses original-category sampling proportions, not adjudicator bias or a fresh manuscript population.

Rerated binary comparisons are separately recorded:

| Condition | Pairs (positive/negative) | Contour64 AUROC | Caption-node 95% | Aspect AUROC | Conditional support |
|---|---:|---:|---|---:|---|
| original | 80 (35/45) | 0.888 | 0.770–1.000 | 0.808 | yes |
| repeat | 74 (28/46) | 0.911 | 0.788–1.000 | 0.816 | yes |
| stable original repeat | 65 (27/38) | 0.907 | 0.781–1.000 | 0.796 | yes |

Original ratings on this selected repeat corpus yield 80 binary pairs/AUROC 0.888; repeat ratings yield 74/AUROC 0.911. Their memberships differ because partials enter/leave the binary analysis. The 65 unchanged binary pairs give 0.907, a diagnostic conditioned on agreement. Strong binary discrimination persists after this repeat, despite category instability. None of these scores overwrites the frozen 211-pair evaluation or constitutes independent confirmation. Original-category-frequency weighted versions are also preserved.

## Conditional uncertainty and reproducibility

The 108 sensitivity conditions are strongly correlated. Their intervals are pointwise, not simultaneous guarantees, and they are not 108 independent confirmations. No p-value is selected across them.

All 108 conditions use the same preregistered 5,000 draws of the original eight-caption node bootstrap, with pair weights=count(left caption)×count(right caption); paired aspect deltas use identical weights. A weighted Mann–Whitney implementation gives half credit to distance ties and agrees with independent sklearn checks. Parent reuse is removed in constrained source samples; caption resampling still weights caption-shared observations. These are conditional empirical intervals, not complete uncertainty over source truth, rating bias or alternative matching choices.

Both categories,≥5 pairs/category,≥3 caption endpoints/category,≥4 captions overall and≥4,500 valid draws are required for the registered descriptive-support flag. This robustness flag is **not Trial 2's validation criterion**. Every available point score and conditional interval is shown, including weaker cases. Single-category or zero-weight comparisons remain not estimable. Sparse subsets are not rescued by another metric, seed, label interpretation or sample substitution.

The 5,000-draw pooled robustness interval 0.762–1.000 differs slightly from Trial 2's sealed 2,000-draw 0.767–1.000 interval because the registered robustness seed and draw count differ. The frozen point metric and its original interval remain unchanged.

Source filters, maximum-cardinality solutions, selected pair IDs,50-seed alternatives, all bootstrap counts, anonymous repeat ratings, category transitions and metric outputs are frozen in the separate package. Deterministic replay checks all 108 conditions, constraint limits and sampling; independent weighted AUROC/kappa calculations verify numerical implementation. Earlier freezes, the full Trial 2 manifest and its prior postfreeze evidence are checked without editing them. No source/raster/representation decision is retuned.

## Disposition

The robustness protocol was sealed before this investigation’s subset and repeat outcomes, after Trial 2 results were already known. Its descriptive rubric identifies sensitivity to sampling mixture, partial recoding and same-category repeat retention. The core same/different result is **not classified as unsupported under conservative analysis**: recovery-clean and disjoint-parent subsets retain substantial signal. Exact graph selection and reduced information budgets limit claims of uniform dependence-free precision. The defensible statement is that frozen contour 64 discriminates selected whole-organization same/different judgments, while broader “related morphology” discrimination and unique source-rater labeling remain less stable.

This investigates visible morphology only. It establishes no letters, graphemes, writing identities, allographs, boundaries, sequences, physical stroke order, pen lifts or meaning. Conventional transcription, Currier, position, sequence and decipherment analyses remain sealed.

[All-condition dashboard](28_direct_morphology_trial2_robustness_dashboard.html) · [Separate protocol](../data/observations/direct_morphology_trial2_robustness_v1/PLAN.json) · [All108 analyses](../tests/direct_morphology_trial2_robustness_v1/conservative_analyses.json) · [Repeat judgments and transitions](../tests/direct_morphology_trial2_robustness_v1/larger_repeatability.json) · [Separate freeze](../data/observations/direct_morphology_trial2_robustness_v1/FREEZE_MANIFEST.json) · [Postfreeze integrity](../tests/direct_morphology_trial2_robustness_v1_postfreeze/INTEGRITY.json)

![Robustness summary](../figures/direct_morphology_trial2_robustness_v1/robustness_summary.png)
