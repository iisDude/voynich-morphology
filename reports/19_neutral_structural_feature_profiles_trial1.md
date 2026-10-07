# Neutral structural feature profiles: feasibility trial1

**Yes, partially. Confirmed writing parents can carry reproducible combinations of neutral numeric properties even while remaining unassigned to a discrete class.** This trial supports partial measurement profiles, not a validated compositional notation or recovered grapheme system. Its reused-validation support gate failed:45/57 source-resolved parents (78.9%) versus the registered80% minimum. V3–V6 remain immutable; no sequences or downstream tests were opened.

The [protocol](../data/observations/neutral_feature_trial_v1/PLAN.json) fixed34 descriptors, tolerances and a usable-profile criterion before results. It used638 V5 confirmed writing parents and66 confirmed parents from the three V6 validation captions. Those images and source decisions were previously exposed; this is a reserved region generalization check for a new feature specification, not globally fresh imagery or independent source annotation.

## Representation

A parent is an uncertain feature vector: geometry + ink distribution + raster cavity/connectivity + graph/run measurements. It retains its whole source parent, native coordinates, primary values, perturbation ranges, and `stable`, `unknown_variant_sensitive`, `unknown_presence` or `not_applicable` states. Cavity-centroid absence is not a coordinate value of zero. Source contact/photographic ambiguity remains separate from numeric stability.

Features include relative aspect, ink density, ink centroid/spread, thirds and3×3 ink fractions, enclosed negative-space count/position/area, connected-component count, skeleton endpoint/branch counts and longest horizontal/vertical ink runs. These are neutral measurements. Skeleton endpoints are not pen lifts; branches are not graphemes; a horizontal run is not automatically a bench/frame. Features can coexist in one vector without asserting detachable subunits or stroke order.

Contrast6/9/12, native±0.04 slant and body-proxy±10% perturbations test operational repeatability. Counts require exact equality; continuous features have preregistered range tolerances. A usable partial profile requires resolved source parent evidence, whole-parent raster correspondence, at least eight stable applicable descriptors, and geometry/distribution plus a third substantive family. Connectivity count alone does not satisfy the third family. Correlated ink fractions are not independent pieces of evidence.

## Coverage

| Corpus | Usable partial profiles | Source-resolved denominator | Rate |
|---|---:|---:|---:|
| V5 confirmed writing | 513 | 589 | 87.1% |
| V5 parents with existing class | 300 | 301 | 99.7% |
| V5 class-unknown parents | 213 | 288 | 74.0% |
| Reused validation regions | 45 | 57 | 78.9% |

Among all327 V5 unknowns,213 (65.1%) have a usable numeric profile after source/correspondence exclusions. The remaining cases retain partial descriptor measurements plus unknown/source-hypothesis flags; they are not forced into profile usability. Forty-one source contacts and eight insufficient-morphology V5 parents remain outside the resolved-parent denominator. Seven contacts and two insufficient-evidence validation parents likewise remain excluded.

Validation-caption rates are12/15 (caption16),16/22 (47),17/20 (94). Each passes the70% per-caption minimum; the pooled80% minimum fails. Caption-bootstrap95% intervals: discovery84.4–89.7%, validation72.7–85.0%. These do not include adjudicator error. No tolerance was relaxed after observing the failure.

## Which properties survive

![Feature perturbation repeatability](../figures/neutral_feature_trial_v1/feature_repeatability.png)

For the327 V5 unknowns, aspect is stable in249, density in288, ink centroid x/y in309/318, significant raster cavity count in245, and horizontal/vertical runs in226/240. Skeleton endpoints and branch clusters are stable in only54/57. Median stable descriptor count is28/34, but many distribution descriptors are correlated.

Height/body and width/body fail the registered range tolerance in every parent **by construction**: a±10% body-proxy interval alone spans log(1.1/0.9)≈0.2007, exceeding the0.18 limit. This is normalization-reference uncertainty, not universal inability to measure native height/width. Native coordinate envelopes remain available; normalized dimensions are retained as intervals. The tolerance and perturbation were not adjusted to improve coverage. A complete34-feature point vector is therefore unsupported.

## Source-visible meaning versus raster repeatability

A preregistered22-parent anonymous RGB audit hid previous numeric values and class suggestions. It sampled an assigned and unknown resolved parent in each V5 caption plus two resolved validation parents per caption. This is the same AI adjudicator with prior photograph familiarity, not independent human-rater validation.

Seventeen source-visible cavity counts were resolved: primary raster counts agree in16/17. Among fifteen numerically stable resolved counts, fourteen agree. Five photographic cavity counts remain unresolved, and three of those still have stable numeric raster counts. **Repeatable numbers can describe a thresholded image without establishing the corresponding source-visible feature.** Cavity statuses in [source-qualified profiles](../data/observations/neutral_feature_trial_v1/source_qualified_profiles.json) therefore retain source uncertainty and definition discordance instead of promoting raster stability into visual truth.

The discrepant B006_O144 has small/enclosed background details affected by the significant-area definition. Source-visible cavities and significant raster cavities are not identical quantities; the cutoff was not retuned. The principal-horizontal-span audit remains descriptive because a straight-row run ratio is not equivalent to a qualitative bridge/frame judgment.

## What this supports

The [B001_O121 example](../tests/neutral_feature_trial_v1/example_partial_profile.json) remains class-unknown but carries stable aspect, density, ink-location, significant-cavity and run measurements with source coordinates. Its single significant cavity has vertical centroid0.677–0.681 of the parent height from the top; source RGB also supports one cavity. Skeleton branch count varies3–4 and remains unknown. A neutral description can retain the lower cavity and other reproducible properties while abstaining on branch count. This demonstrates the advantage of feature-specific uncertainty: one unstable count need not erase the rest of the parent description.

This representation can support source-traceable similarity research and uncertainty diagnosis. It has not established reusable internal components, source-certified feature truth for every parent, unique reconstruction of the shape, an alphabet, complete row membership, or sequence recurrence. The same feature vector can describe several different forms. Source-window ownership and raster-correspondence problems remain limiting cases.

The trial is an evidence package, **not a V7 segmentation freeze**. Existing writing membership, V3 classes and V6 inventory stay unchanged. Neither Currier, native pixel-x, EVA/RF/v101, minimal-pair nor decipherment tests were reopened.
