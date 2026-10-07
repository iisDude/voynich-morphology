# Visual unit atlas v0

This is a frozen, manuscript-derived candidate atlas with substantial unresolved coverage. It is not a recovered alphabet. Source imagery defines the candidates; EVA, RF and v101 contents remained unopened until this snapshot.

## Evidence and model comparison

All 204 folio-captioned views have native Yale images and reversible registration. The twelve-view pilot calibrated the extraction; candidate analysis then expanded across all views. Captions are not verified physical panel maps.

Four partitions compete on the same held-out native assigned-ink masks. Training template mean IoU on 1,824 test groups is 0.621 for fine components, 0.538 for medium assemblies, 0.458 for coarse compounds and 0.415 for whole groups. This favors finer geometry within the admitted subset, not graphemes. Rectangle costs and binary residuals are coding proxies, not lossless source compression.

The medium source audit found clear writing in 100/120 test crops, 12 failures and 8 ambiguous cases. A fresh stratified fine audit found clear writing in 106/128 crops, 6 failures and 16 ambiguous cases; 8 broad-structure assignments were visibly incompatible. Neither audit estimates recall or boundary accuracy. No threshold was retuned on these outcomes.

About 31% of held-out sampled crops changed component count across contrast thresholds; about 32% changed connectivity under a two-pixel erosion probe. Disconnection cannot be promoted to pen-lift evidence.

Height remains continuous. A two-component training mixture modestly improves validation log density, but this can reflect different assemblies, detector truncation and scribal variation. Tall-form thresholds do not establish a sign class.

## Boundaries and structural hypotheses

Fine components are threshold-connected raster objects. Medium and coarse models join objects by geometric gaps; whole-group models preserve space-gap assemblies. Native skeleton valleys add candidate internal cuts without declaring an alphabet. Every group retains alternative partitions and native coordinates.

Long upright and horizontal segments, end supports, above-bar ink, repeated column ridges and erosion sensitivity are explicit geometric measurements in `native_structure_v4`. Frames and insertions remain hypotheses; the simple frame detector is sparse and not validated as a complete bench inventory. Upper and lower extents use a provisional local baseline/body estimate. Raster endpoints are not stroke ends.

Twenty-one broad structure merges and six compound analogies are alternate interpretations, not canonical graphemes. Similar rounded loops recur in many prototype bins; merging can remove allographic duplication or conflate different structures. Tall structures occur alongside or connected to lower traces, but photographs and masks do not establish stroke order.

Circular text has orientation-preserving unwrapping proposals in 17 views. Approximate ellipses leave curved/sinusoidal rows and fragment paths; these remain unresolved and excluded from horizontal position statistics. Sparse and rotated labels are not silently converted into linear rows.

Section and attributed-hand labels were withheld from family fitting and are used only after this freeze for stability comparisons. They are inherited annotations, not independent physical hand identifications.

## Candidate families

### Fine partition

#### VF_fine_components_K128_001

rounded open return, variable closure

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 261 training instances across 34 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_001.png).

#### VF_fine_components_K128_002

small closed rounded compartment

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 325 training instances across 39 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_002.png).

#### VF_fine_components_K128_003

two low curl-like traces connected horizontally

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 544 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_003.png).

#### VF_fine_components_K128_004

Texture, paint or long non-writing traces dominate source exemplars.

- Source review: artifact; confidence: unresolved.
- Recurrence: 202 training instances across 42 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_004.png).

#### VF_fine_components_K128_005

Texture, paint or long non-writing traces dominate source exemplars.

- Source review: artifact; confidence: unresolved.
- Recurrence: 356 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_005.png).

#### VF_fine_components_K128_006

short repeated slant or arch-like traces

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 296 training instances across 38 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_006.png).

#### VF_fine_components_K128_007

Texture, paint or long non-writing traces dominate source exemplars.

- Source review: artifact; confidence: unresolved.
- Recurrence: 465 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_007.png).

#### VF_fine_components_K128_008

Source exemplars mix writing, drawing, blank texture or incompatible extents.

- Source review: mixed; confidence: unresolved.
- Recurrence: 502 training instances across 42 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_008.png).

#### VF_fine_components_K128_009

Tiny isolated fragments recur but identity and completeness remain unresolved.

- Source review: fragment; confidence: unresolved.
- Recurrence: 360 training instances across 40 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_009.png).

#### VF_fine_components_K128_010

small closed rounded compartment

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 280 training instances across 42 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_010.png).

#### VF_fine_components_K128_011

small single slant-like or angled trace

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 424 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_011.png).

#### VF_fine_components_K128_012

two stacked loop-like compartments; closure varies

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 362 training instances across 33 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_012.png).

#### VF_fine_components_K128_013

tall downward stem, upper bar and nearby ring-like compartment

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 251 training instances across 26 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_013.png).

#### VF_fine_components_K128_014

narrow loop joined to angular descending return

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 171 training instances across 34 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_014.png).

#### VF_fine_components_K128_015

small upper loop with a longer curved descending tail

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 348 training instances across 34 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_015.png).

#### VF_fine_components_K128_016

upper curve descending to an angular lower return

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 300 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_016.png).

#### VF_fine_components_K128_017

low connected curls followed by a closed compartment

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 590 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_017.png).

#### VF_fine_components_K128_018

two stacked loop-like compartments; closure varies

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 409 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_018.png).

#### VF_fine_components_K128_019

Tiny isolated fragments recur but identity and completeness remain unresolved.

- Source review: fragment; confidence: unresolved.
- Recurrence: 280 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_019.png).

#### VF_fine_components_K128_020

small arch-like or nearly enclosed angular trace

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 205 training instances across 39 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_020.png).

#### VF_fine_components_K128_021

paired tall uprights connected by upper bar and loop

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 342 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_021.png).

#### VF_fine_components_K128_022

small open curl-like trace

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 310 training instances across 33 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_022.png).

#### VF_fine_components_K128_023

small closed rounded compartment

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 464 training instances across 40 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_023.png).

#### VF_fine_components_K128_024

paired tall uprights connected by upper bar and loop

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 314 training instances across 37 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_024.png).

#### VF_fine_components_K128_025

two low curl-like traces connected horizontally

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 468 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_025.png).

#### VF_fine_components_K128_026

tall downward stem, upper bar and nearby ring-like compartment

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 230 training instances across 27 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_026.png).

#### VF_fine_components_K128_027

small upper loop with a longer curved descending tail

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 369 training instances across 42 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_027.png).

#### VF_fine_components_K128_028

Source exemplars mix writing, drawing, blank texture or incompatible extents.

- Source review: mixed; confidence: unresolved.
- Recurrence: 170 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_028.png).

#### VF_fine_components_K128_029

paired tall uprights connected by upper bar and loop

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 452 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_029.png).

#### VF_fine_components_K128_030

small open curl-like trace

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 227 training instances across 40 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_030.png).

#### VF_fine_components_K128_031

Source exemplars mix writing, drawing, blank texture or incompatible extents.

- Source review: mixed; confidence: unresolved.
- Recurrence: 569 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_031.png).

#### VF_fine_components_K128_032

small closed rounded compartment

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 442 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_032.png).

#### VF_fine_components_K128_033

paired tall uprights connected by upper bar and loop

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 91 training instances across 30 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_033.png).

#### VF_fine_components_K128_034

narrow loop joined to angular descending return

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 235 training instances across 39 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_034.png).

#### VF_fine_components_K128_035

Writing visible but connected assemblies include variable neighboring structures or rows.

- Source review: writing_variable; confidence: unresolved.
- Recurrence: 630 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_035.png).

#### VF_fine_components_K128_036

narrow loop joined to angular descending return

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 472 training instances across 42 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_036.png).

#### VF_fine_components_K128_037

paired tall uprights connected by upper bar and loop

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 241 training instances across 40 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_037.png).

#### VF_fine_components_K128_038

rounded open return, variable closure

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 440 training instances across 40 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_038.png).

#### VF_fine_components_K128_039

Tiny isolated fragments recur but identity and completeness remain unresolved.

- Source review: fragment; confidence: unresolved.
- Recurrence: 391 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_039.png).

#### VF_fine_components_K128_040

two stacked loop-like compartments; closure varies

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 435 training instances across 42 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_040.png).

#### VF_fine_components_K128_041

Tiny isolated fragments recur but identity and completeness remain unresolved.

- Source review: fragment; confidence: unresolved.
- Recurrence: 182 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_041.png).

#### VF_fine_components_K128_042

paired tall uprights connected by upper bar and loop

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 290 training instances across 42 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_042.png).

#### VF_fine_components_K128_043

small single slant-like or angled trace

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 391 training instances across 39 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_043.png).

#### VF_fine_components_K128_044

small closed rounded compartment

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 400 training instances across 39 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_044.png).

#### VF_fine_components_K128_045

Source exemplars mix writing, drawing, blank texture or incompatible extents.

- Source review: mixed; confidence: unresolved.
- Recurrence: 157 training instances across 42 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_045.png).

#### VF_fine_components_K128_046

paired tall uprights connected by upper bar and loop

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 439 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_046.png).

#### VF_fine_components_K128_047

Tiny isolated fragments recur but identity and completeness remain unresolved.

- Source review: fragment; confidence: unresolved.
- Recurrence: 211 training instances across 40 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_047.png).

#### VF_fine_components_K128_048

low curl joined to stacked loop-like compartments

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 495 training instances across 28 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_048.png).

#### VF_fine_components_K128_049

Texture, paint or long non-writing traces dominate source exemplars.

- Source review: artifact; confidence: unresolved.
- Recurrence: 394 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_049.png).

#### VF_fine_components_K128_050

small closed rounded compartment

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 430 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_050.png).

#### VF_fine_components_K128_051

Source exemplars mix writing, drawing, blank texture or incompatible extents.

- Source review: mixed; confidence: unresolved.
- Recurrence: 456 training instances across 42 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_051.png).

#### VF_fine_components_K128_052

two low curl-like traces connected horizontally

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 466 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_052.png).

#### VF_fine_components_K128_053

Writing visible but connected assemblies include variable neighboring structures or rows.

- Source review: writing_variable; confidence: unresolved.
- Recurrence: 356 training instances across 42 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_053.png).

#### VF_fine_components_K128_054

small closed rounded compartment

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 259 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_054.png).

#### VF_fine_components_K128_055

Source exemplars mix writing, drawing, blank texture or incompatible extents.

- Source review: mixed; confidence: unresolved.
- Recurrence: 322 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_055.png).

#### VF_fine_components_K128_056

Source exemplars mix writing, drawing, blank texture or incompatible extents.

- Source review: mixed; confidence: unresolved.
- Recurrence: 181 training instances across 40 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_056.png).

#### VF_fine_components_K128_057

small closed rounded compartment

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 462 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_057.png).

#### VF_fine_components_K128_058

Tiny isolated fragments recur but identity and completeness remain unresolved.

- Source review: fragment; confidence: unresolved.
- Recurrence: 286 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_058.png).

#### VF_fine_components_K128_059

short repeated slant or arch-like traces

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 257 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_059.png).

#### VF_fine_components_K128_060

small open curl-like trace

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 256 training instances across 42 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_060.png).

#### VF_fine_components_K128_061

small closed rounded compartment

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 483 training instances across 42 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_061.png).

#### VF_fine_components_K128_062

low curls and closed compartment with descending tail

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 240 training instances across 40 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_062.png).

#### VF_fine_components_K128_063

small upper loop with a longer curved descending tail

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 272 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_063.png).

#### VF_fine_components_K128_064

small upper loop with a longer curved descending tail

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 194 training instances across 37 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_064.png).

#### VF_fine_components_K128_065

Tiny isolated fragments recur but identity and completeness remain unresolved.

- Source review: fragment; confidence: unresolved.
- Recurrence: 355 training instances across 38 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_065.png).

#### VF_fine_components_K128_066

Source exemplars mix writing, drawing, blank texture or incompatible extents.

- Source review: mixed; confidence: unresolved.
- Recurrence: 258 training instances across 42 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_066.png).

#### VF_fine_components_K128_067

short repeated slant or arch-like traces

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 292 training instances across 42 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_067.png).

#### VF_fine_components_K128_068

Source exemplars mix writing, drawing, blank texture or incompatible extents.

- Source review: mixed; confidence: unresolved.
- Recurrence: 539 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_068.png).

#### VF_fine_components_K128_069

Tiny isolated fragments recur but identity and completeness remain unresolved.

- Source review: fragment; confidence: unresolved.
- Recurrence: 305 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_069.png).

#### VF_fine_components_K128_070

two stacked loop-like compartments; closure varies

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 516 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_070.png).

#### VF_fine_components_K128_071

narrow loop joined to angular descending return

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 264 training instances across 40 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_071.png).

#### VF_fine_components_K128_072

Writing visible but connected assemblies include variable neighboring structures or rows.

- Source review: writing_variable; confidence: unresolved.
- Recurrence: 364 training instances across 40 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_072.png).

#### VF_fine_components_K128_073

raised short return above horizontally connected low curls

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 241 training instances across 37 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_073.png).

#### VF_fine_components_K128_074

Tiny isolated fragments recur but identity and completeness remain unresolved.

- Source review: fragment; confidence: unresolved.
- Recurrence: 220 training instances across 39 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_074.png).

#### VF_fine_components_K128_075

Tiny isolated fragments recur but identity and completeness remain unresolved.

- Source review: fragment; confidence: unresolved.
- Recurrence: 239 training instances across 39 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_075.png).

#### VF_fine_components_K128_076

paired tall uprights connected by upper bar and loop

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 272 training instances across 32 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_076.png).

#### VF_fine_components_K128_077

narrow loop joined to angular descending return

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 239 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_077.png).

#### VF_fine_components_K128_078

Writing visible but connected assemblies include variable neighboring structures or rows.

- Source review: writing_variable; confidence: unresolved.
- Recurrence: 388 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_078.png).

#### VF_fine_components_K128_079

two low curl-like traces connected horizontally

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 382 training instances across 37 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_079.png).

#### VF_fine_components_K128_080

upper curve descending to an angular lower return

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 233 training instances across 33 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_080.png).

#### VF_fine_components_K128_081

upper curve descending to an angular lower return

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 154 training instances across 30 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_081.png).

#### VF_fine_components_K128_082

Source exemplars mix writing, drawing, blank texture or incompatible extents.

- Source review: mixed; confidence: unresolved.
- Recurrence: 186 training instances across 39 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_082.png).

#### VF_fine_components_K128_083

Tiny isolated fragments recur but identity and completeness remain unresolved.

- Source review: fragment; confidence: unresolved.
- Recurrence: 340 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_083.png).

#### VF_fine_components_K128_084

Source exemplars mix writing, drawing, blank texture or incompatible extents.

- Source review: mixed; confidence: unresolved.
- Recurrence: 125 training instances across 33 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_084.png).

#### VF_fine_components_K128_085

Texture, paint or long non-writing traces dominate source exemplars.

- Source review: artifact; confidence: unresolved.
- Recurrence: 491 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_085.png).

#### VF_fine_components_K128_086

small closed rounded compartment

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 340 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_086.png).

#### VF_fine_components_K128_087

Writing visible but connected assemblies include variable neighboring structures or rows.

- Source review: writing_variable; confidence: unresolved.
- Recurrence: 252 training instances across 37 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_087.png).

#### VF_fine_components_K128_088

low curl joined to stacked loop-like compartments

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 470 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_088.png).

#### VF_fine_components_K128_089

upper curve descending to an angular lower return

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 295 training instances across 40 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_089.png).

#### VF_fine_components_K128_090

small open curl-like trace

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 310 training instances across 38 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_090.png).

#### VF_fine_components_K128_091

paired tall uprights with adjoining low arch or loop

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 87 training instances across 20 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_091.png).

#### VF_fine_components_K128_092

upper curve descending to an angular lower return

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 364 training instances across 40 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_092.png).

#### VF_fine_components_K128_093

narrow loop joined to angular descending return

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 184 training instances across 31 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_093.png).

#### VF_fine_components_K128_094

two stacked loop-like compartments; closure varies

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 282 training instances across 28 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_094.png).

#### VF_fine_components_K128_095

Tiny isolated fragments recur but identity and completeness remain unresolved.

- Source review: fragment; confidence: unresolved.
- Recurrence: 275 training instances across 39 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_095.png).

#### VF_fine_components_K128_096

upper curve descending to an angular lower return

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 202 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_096.png).

#### VF_fine_components_K128_097

paired tall uprights connected by upper bar and loop

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 137 training instances across 30 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_097.png).

#### VF_fine_components_K128_098

two stacked loop-like compartments; closure varies

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 295 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_098.png).

#### VF_fine_components_K128_099

small upper loop with a longer curved descending tail

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 409 training instances across 35 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_099.png).

#### VF_fine_components_K128_100

Writing visible but connected assemblies include variable neighboring structures or rows.

- Source review: writing_variable; confidence: unresolved.
- Recurrence: 338 training instances across 36 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_100.png).

#### VF_fine_components_K128_101

Source exemplars mix writing, drawing, blank texture or incompatible extents.

- Source review: mixed; confidence: unresolved.
- Recurrence: 346 training instances across 42 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_101.png).

#### VF_fine_components_K128_102

low connected curls followed by a closed compartment

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 347 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_102.png).

#### VF_fine_components_K128_103

raised short return above horizontally connected low curls

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 155 training instances across 33 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_103.png).

#### VF_fine_components_K128_104

Tiny isolated fragments recur but identity and completeness remain unresolved.

- Source review: fragment; confidence: unresolved.
- Recurrence: 219 training instances across 42 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_104.png).

#### VF_fine_components_K128_105

small upper loop with a longer curved descending tail

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 535 training instances across 40 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_105.png).

#### VF_fine_components_K128_106

short slants joined to rounded returning trace

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 193 training instances across 36 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_106.png).

#### VF_fine_components_K128_107

tall downward stem, upper bar and nearby ring-like compartment

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 256 training instances across 40 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_107.png).

#### VF_fine_components_K128_108

small closed rounded compartment

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 576 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_108.png).

#### VF_fine_components_K128_109

paired tall uprights connected by upper bar and loop

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 300 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_109.png).

#### VF_fine_components_K128_110

small arch-like or nearly enclosed angular trace

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 309 training instances across 40 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_110.png).

#### VF_fine_components_K128_111

upper curve descending to an angular lower return

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 400 training instances across 43 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_111.png).

#### VF_fine_components_K128_112

narrow loop joined to angular descending return

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 141 training instances across 33 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_112.png).

#### VF_fine_components_K128_113

small arch-like or nearly enclosed angular trace

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 442 training instances across 40 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_113.png).

#### VF_fine_components_K128_114

small arch-like or nearly enclosed angular trace

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 464 training instances across 40 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_114.png).

#### VF_fine_components_K128_115

two stacked loop-like compartments; closure varies

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 250 training instances across 34 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_115.png).

#### VF_fine_components_K128_116

Source exemplars mix writing, drawing, blank texture or incompatible extents.

- Source review: mixed; confidence: unresolved.
- Recurrence: 149 training instances across 35 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_116.png).

#### VF_fine_components_K128_117

small upper loop with a longer curved descending tail

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 177 training instances across 37 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_117.png).

#### VF_fine_components_K128_118

two stacked loop-like compartments; closure varies

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 218 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_118.png).

#### VF_fine_components_K128_119

two low curl-like traces connected horizontally

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 335 training instances across 37 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_119.png).

#### VF_fine_components_K128_120

paired tall structure with lower horizontal connection and curls

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 261 training instances across 42 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_120.png).

#### VF_fine_components_K128_121

low curls and closed compartment with descending tail

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 133 training instances across 31 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_121.png).

#### VF_fine_components_K128_122

closed compartment adjoining narrow looped angular return

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 160 training instances across 35 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_122.png).

#### VF_fine_components_K128_123

narrow loop joined to angular descending return

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 141 training instances across 31 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_123.png).

#### VF_fine_components_K128_124

Tiny isolated fragments recur but identity and completeness remain unresolved.

- Source review: fragment; confidence: unresolved.
- Recurrence: 348 training instances across 41 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_124.png).

#### VF_fine_components_K128_125

paired tall uprights with adjoining low arch or loop

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 82 training instances across 33 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_125.png).

#### VF_fine_components_K128_126

short repeated slant or arch-like traces

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 307 training instances across 42 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_126.png).

#### VF_fine_components_K128_127

paired tall uprights connected by upper bar and loop

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 194 training instances across 38 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_127.png).

#### VF_fine_components_K128_128

two low curl-like traces connected horizontally

- Source review: writing_consistent; confidence: moderate for recurrence, low for atomic identity.
- Recurrence: 263 training instances across 38 caption-connected folio components.
- Context: source writing-region proposals; unknown hand and section; physical x order is not pen order.
- Variants: Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences..
- Competing segmentations: connected object as whole, sparse-crossing internal cuts, larger medium assembly, visual allograph merge with related prototype bins.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/fine_components/VF_fine_components_K128_128.png).

### Medium partition

#### VF_medium_assemblies_K128_001

Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.

- Source review: mixed; confidence: insufficient for an accepted unit identity.
- Recurrence: 165 training instances across 41 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_001.png).

#### VF_medium_assemblies_K128_002

Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.

- Source review: mixed; confidence: insufficient for an accepted unit identity.
- Recurrence: 112 training instances across 33 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_002.png).

#### VF_medium_assemblies_K128_003

Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.

- Source review: mixed; confidence: insufficient for an accepted unit identity.
- Recurrence: 238 training instances across 38 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_003.png).

#### VF_medium_assemblies_K128_004

low connected curls followed by a closed loop and returning tail

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 197 training instances across 42 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_004.png).

#### VF_medium_assemblies_K128_005

Closest training exemplars dominated by parchment texture, paint, long non-writing traces or extremely small fragments.

- Source review: artifact; confidence: insufficient for an accepted unit identity.
- Recurrence: 202 training instances across 41 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_005.png).

#### VF_medium_assemblies_K128_006

Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.

- Source review: mixed; confidence: insufficient for an accepted unit identity.
- Recurrence: 190 training instances across 39 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_006.png).

#### VF_medium_assemblies_K128_007

Readable writing assemblies recur, but included structures and neighboring rows vary; atomic boundary unsupported.

- Source review: writing_variable; confidence: insufficient for an accepted unit identity.
- Recurrence: 608 training instances across 43 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_007.png).

#### VF_medium_assemblies_K128_008

paired tall uprights with upper loop, followed by repeated short slants and a return

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 459 training instances across 43 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_008.png).

#### VF_medium_assemblies_K128_009

upper curved return descending to an angular lower foot

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 99 training instances across 36 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_009.png).

#### VF_medium_assemblies_K128_010

Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.

- Source review: mixed; confidence: insufficient for an accepted unit identity.
- Recurrence: 156 training instances across 40 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_010.png).

#### VF_medium_assemblies_K128_011

small closed loop; one exemplar is an open descending return

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 132 training instances across 36 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_011.png).

#### VF_medium_assemblies_K128_012

Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.

- Source review: mixed; confidence: insufficient for an accepted unit identity.
- Recurrence: 166 training instances across 35 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_012.png).

#### VF_medium_assemblies_K128_013

Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.

- Source review: mixed; confidence: insufficient for an accepted unit identity.
- Recurrence: 236 training instances across 41 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_013.png).

#### VF_medium_assemblies_K128_014

two vertically arranged loop-like compartments

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 86 training instances across 31 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_014.png).

#### VF_medium_assemblies_K128_015

single rounded loop, variable closure and slant

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 106 training instances across 30 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_015.png).

#### VF_medium_assemblies_K128_016

lower loop joined to an upper curved compartment

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 80 training instances across 20 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_016.png).

#### VF_medium_assemblies_K128_017

paired low curls joined by horizontal ink

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 148 training instances across 39 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_017.png).

#### VF_medium_assemblies_K128_018

small closed ring with variable thickness

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 186 training instances across 38 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_018.png).

#### VF_medium_assemblies_K128_019

low connected curls followed by a ring

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 346 training instances across 43 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_019.png).

#### VF_medium_assemblies_K128_020

upper curved return and angular lower foot

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 127 training instances across 38 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_020.png).

#### VF_medium_assemblies_K128_021

Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.

- Source review: mixed; confidence: insufficient for an accepted unit identity.
- Recurrence: 246 training instances across 36 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_021.png).

#### VF_medium_assemblies_K128_022

Readable writing assemblies recur, but included structures and neighboring rows vary; atomic boundary unsupported.

- Source review: writing_variable; confidence: insufficient for an accepted unit identity.
- Recurrence: 464 training instances across 41 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_022.png).

#### VF_medium_assemblies_K128_023

Closest training exemplars dominated by parchment texture, paint, long non-writing traces or extremely small fragments.

- Source review: artifact; confidence: insufficient for an accepted unit identity.
- Recurrence: 392 training instances across 43 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_023.png).

#### VF_medium_assemblies_K128_024

small repeated slant/arch-like traces

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 77 training instances across 27 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_024.png).

#### VF_medium_assemblies_K128_025

Closest training exemplars dominated by parchment texture, paint, long non-writing traces or extremely small fragments.

- Source review: artifact; confidence: insufficient for an accepted unit identity.
- Recurrence: 832 training instances across 43 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_025.png).

#### VF_medium_assemblies_K128_026

Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.

- Source review: mixed; confidence: insufficient for an accepted unit identity.
- Recurrence: 219 training instances across 41 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_026.png).

#### VF_medium_assemblies_K128_027

Readable writing assemblies recur, but included structures and neighboring rows vary; atomic boundary unsupported.

- Source review: writing_variable; confidence: insufficient for an accepted unit identity.
- Recurrence: 204 training instances across 41 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_027.png).

#### VF_medium_assemblies_K128_028

short angular returning trace

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 70 training instances across 28 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_028.png).

#### VF_medium_assemblies_K128_029

small forked or returning trace; fragmentation unresolved

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 71 training instances across 36 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_029.png).

#### VF_medium_assemblies_K128_030

open upper return above a bent lower trace

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 61 training instances across 21 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_030.png).

#### VF_medium_assemblies_K128_031

two low curl-like traces with horizontal connection

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 191 training instances across 42 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_031.png).

#### VF_medium_assemblies_K128_032

low curl followed by lower and upper loop-like compartments

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 129 training instances across 19 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_032.png).

#### VF_medium_assemblies_K128_033

paired tall uprights and upper loop followed by low connected curls

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 350 training instances across 39 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_033.png).

#### VF_medium_assemblies_K128_034

Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.

- Source review: mixed; confidence: insufficient for an accepted unit identity.
- Recurrence: 161 training instances across 41 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_034.png).

#### VF_medium_assemblies_K128_035

several short slants joined to a rounded returning trace

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 196 training instances across 40 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_035.png).

#### VF_medium_assemblies_K128_036

small angular enclosed or nearly enclosed trace

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 183 training instances across 36 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_036.png).

#### VF_medium_assemblies_K128_037

paired tall uprights and upper loop followed by a low angled trace

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 109 training instances across 32 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_037.png).

#### VF_medium_assemblies_K128_038

short slants followed by an upper returning curve

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 195 training instances across 34 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_038.png).

#### VF_medium_assemblies_K128_039

Closest training exemplars dominated by parchment texture, paint, long non-writing traces or extremely small fragments.

- Source review: artifact; confidence: insufficient for an accepted unit identity.
- Recurrence: 577 training instances across 43 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_039.png).

#### VF_medium_assemblies_K128_040

Readable writing assemblies recur, but included structures and neighboring rows vary; atomic boundary unsupported.

- Source review: writing_variable; confidence: insufficient for an accepted unit identity.
- Recurrence: 377 training instances across 42 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_040.png).

#### VF_medium_assemblies_K128_041

ring followed by looped angular return

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 132 training instances across 30 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_041.png).

#### VF_medium_assemblies_K128_042

Closest training exemplars dominated by parchment texture, paint, long non-writing traces or extremely small fragments.

- Source review: artifact; confidence: insufficient for an accepted unit identity.
- Recurrence: 316 training instances across 41 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_042.png).

#### VF_medium_assemblies_K128_043

upright narrow loop with angular descending return

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 167 training instances across 25 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_043.png).

#### VF_medium_assemblies_K128_044

two vertically stacked loop-like compartments

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 99 training instances across 31 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_044.png).

#### VF_medium_assemblies_K128_045

Readable writing assemblies recur, but included structures and neighboring rows vary; atomic boundary unsupported.

- Source review: writing_variable; confidence: insufficient for an accepted unit identity.
- Recurrence: 634 training instances across 43 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_045.png).

#### VF_medium_assemblies_K128_046

small open curl-like trace

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 137 training instances across 32 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_046.png).

#### VF_medium_assemblies_K128_047

two low connected curl-like traces

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 187 training instances across 39 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_047.png).

#### VF_medium_assemblies_K128_048

Closest training exemplars dominated by parchment texture, paint, long non-writing traces or extremely small fragments.

- Source review: artifact; confidence: insufficient for an accepted unit identity.
- Recurrence: 167 training instances across 40 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_048.png).

#### VF_medium_assemblies_K128_049

Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.

- Source review: mixed; confidence: insufficient for an accepted unit identity.
- Recurrence: 366 training instances across 41 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_049.png).

#### VF_medium_assemblies_K128_050

paired uprights with upper loop followed by low angled trace

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 113 training instances across 28 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_050.png).

#### VF_medium_assemblies_K128_051

Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.

- Source review: mixed; confidence: insufficient for an accepted unit identity.
- Recurrence: 496 training instances across 43 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_051.png).

#### VF_medium_assemblies_K128_052

Closest training exemplars dominated by parchment texture, paint, long non-writing traces or extremely small fragments.

- Source review: artifact; confidence: insufficient for an accepted unit identity.
- Recurrence: 235 training instances across 40 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_052.png).

#### VF_medium_assemblies_K128_053

small horizontally oval closed ring

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 271 training instances across 34 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_053.png).

#### VF_medium_assemblies_K128_054

Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.

- Source review: mixed; confidence: insufficient for an accepted unit identity.
- Recurrence: 273 training instances across 39 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_054.png).

#### VF_medium_assemblies_K128_055

lower loop with upper return followed by low angled trace

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 202 training instances across 39 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_055.png).

#### VF_medium_assemblies_K128_056

Readable writing assemblies recur, but included structures and neighboring rows vary; atomic boundary unsupported.

- Source review: writing_variable; confidence: insufficient for an accepted unit identity.
- Recurrence: 360 training instances across 41 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_056.png).

#### VF_medium_assemblies_K128_057

small upper curved loop descending into short lower trace

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 198 training instances across 42 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_057.png).

#### VF_medium_assemblies_K128_058

Closest training exemplars dominated by parchment texture, paint, long non-writing traces or extremely small fragments.

- Source review: artifact; confidence: insufficient for an accepted unit identity.
- Recurrence: 343 training instances across 42 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_058.png).

#### VF_medium_assemblies_K128_059

Readable writing assemblies recur, but included structures and neighboring rows vary; atomic boundary unsupported.

- Source review: writing_variable; confidence: insufficient for an accepted unit identity.
- Recurrence: 176 training instances across 34 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_059.png).

#### VF_medium_assemblies_K128_060

low connected curls and an oval compartment

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 205 training instances across 38 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_060.png).

#### VF_medium_assemblies_K128_061

closed ring followed by looped angular return

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 137 training instances across 35 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_061.png).

#### VF_medium_assemblies_K128_062

Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.

- Source review: mixed; confidence: insufficient for an accepted unit identity.
- Recurrence: 96 training instances across 34 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_062.png).

#### VF_medium_assemblies_K128_063

small rounded ring

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 182 training instances across 38 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_063.png).

#### VF_medium_assemblies_K128_064

two long uprights connected by an upper bar and loop

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 154 training instances across 38 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_064.png).

#### VF_medium_assemblies_K128_065

paired tall uprights with upper loop and following low curl

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 189 training instances across 37 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_065.png).

#### VF_medium_assemblies_K128_066

two stacked closed compartments

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 225 training instances across 39 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_066.png).

#### VF_medium_assemblies_K128_067

Readable writing assemblies recur, but included structures and neighboring rows vary; atomic boundary unsupported.

- Source review: writing_variable; confidence: insufficient for an accepted unit identity.
- Recurrence: 256 training instances across 39 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_067.png).

#### VF_medium_assemblies_K128_068

small flattened ring

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 120 training instances across 29 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_068.png).

#### VF_medium_assemblies_K128_069

narrow loop with returning extension; one exemplar is faint

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 112 training instances across 34 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_069.png).

#### VF_medium_assemblies_K128_070

Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.

- Source review: mixed; confidence: insufficient for an accepted unit identity.
- Recurrence: 155 training instances across 41 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_070.png).

#### VF_medium_assemblies_K128_071

Readable writing assemblies recur, but included structures and neighboring rows vary; atomic boundary unsupported.

- Source review: writing_variable; confidence: insufficient for an accepted unit identity.
- Recurrence: 477 training instances across 43 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_071.png).

#### VF_medium_assemblies_K128_072

Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.

- Source review: mixed; confidence: insufficient for an accepted unit identity.
- Recurrence: 232 training instances across 42 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_072.png).

#### VF_medium_assemblies_K128_073

ring followed by narrow loop and angular return

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 103 training instances across 32 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_073.png).

#### VF_medium_assemblies_K128_074

small upper loop with a long descending curved tail

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 210 training instances across 33 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_074.png).

#### VF_medium_assemblies_K128_075

small oval ring

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 97 training instances across 31 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_075.png).

#### VF_medium_assemblies_K128_076

Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.

- Source review: mixed; confidence: insufficient for an accepted unit identity.
- Recurrence: 128 training instances across 41 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_076.png).

#### VF_medium_assemblies_K128_077

upper return descending to an angular lower foot

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 222 training instances across 35 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_077.png).

#### VF_medium_assemblies_K128_078

low connected curl followed by a looped extension

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 158 training instances across 35 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_078.png).

#### VF_medium_assemblies_K128_079

paired uprights with upper loop and nearby low traces

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 189 training instances across 38 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_079.png).

#### VF_medium_assemblies_K128_080

lower loop connected to upper narrow returning compartment

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 93 training instances across 21 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_080.png).

#### VF_medium_assemblies_K128_081

upper curved return followed by a low loop

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 37 training instances across 19 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_081.png).

#### VF_medium_assemblies_K128_082

short raised return above low horizontal connected curls

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 53 training instances across 18 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_082.png).

#### VF_medium_assemblies_K128_083

small rounded ring

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 80 training instances across 38 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_083.png).

#### VF_medium_assemblies_K128_084

narrow loop with angular descending return

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 141 training instances across 29 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_084.png).

#### VF_medium_assemblies_K128_085

Closest training exemplars dominated by parchment texture, paint, long non-writing traces or extremely small fragments.

- Source review: artifact; confidence: insufficient for an accepted unit identity.
- Recurrence: 795 training instances across 43 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_085.png).

#### VF_medium_assemblies_K128_086

small open curl-like trace

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 155 training instances across 38 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_086.png).

#### VF_medium_assemblies_K128_087

looped angular return with descending tail; neighboring ring sometimes present

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 97 training instances across 25 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_087.png).

#### VF_medium_assemblies_K128_088

tall downward stem below horizontal bar with nearby small ring

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 173 training instances across 25 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_088.png).

#### VF_medium_assemblies_K128_089

Readable writing assemblies recur, but included structures and neighboring rows vary; atomic boundary unsupported.

- Source review: writing_variable; confidence: insufficient for an accepted unit identity.
- Recurrence: 338 training instances across 41 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_089.png).

#### VF_medium_assemblies_K128_090

Readable writing assemblies recur, but included structures and neighboring rows vary; atomic boundary unsupported.

- Source review: writing_variable; confidence: insufficient for an accepted unit identity.
- Recurrence: 174 training instances across 37 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_090.png).

#### VF_medium_assemblies_K128_091

paired uprights connected by upper loop and bar

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 121 training instances across 31 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_091.png).

#### VF_medium_assemblies_K128_092

small closed loop; very small exemplar unresolved

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 65 training instances across 25 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_092.png).

#### VF_medium_assemblies_K128_093

Readable writing assemblies recur, but included structures and neighboring rows vary; atomic boundary unsupported.

- Source review: writing_variable; confidence: insufficient for an accepted unit identity.
- Recurrence: 410 training instances across 42 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_093.png).

#### VF_medium_assemblies_K128_094

small rounded ring of varying closure

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 29 training instances across 18 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_094.png).

#### VF_medium_assemblies_K128_095

Closest training exemplars dominated by parchment texture, paint, long non-writing traces or extremely small fragments.

- Source review: artifact; confidence: insufficient for an accepted unit identity.
- Recurrence: 220 training instances across 33 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_095.png).

#### VF_medium_assemblies_K128_096

small rounded ring of varying thickness

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 146 training instances across 37 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_096.png).

#### VF_medium_assemblies_K128_097

Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.

- Source review: mixed; confidence: insufficient for an accepted unit identity.
- Recurrence: 102 training instances across 28 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_097.png).

#### VF_medium_assemblies_K128_098

small ring of varying slant

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 100 training instances across 32 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_098.png).

#### VF_medium_assemblies_K128_099

low slants or loop followed by upper returning curve

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 87 training instances across 32 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_099.png).

#### VF_medium_assemblies_K128_100

Readable writing assemblies recur, but included structures and neighboring rows vary; atomic boundary unsupported.

- Source review: writing_variable; confidence: insufficient for an accepted unit identity.
- Recurrence: 260 training instances across 36 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_100.png).

#### VF_medium_assemblies_K128_101

small upper loop with descending curved tail

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 212 training instances across 37 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_101.png).

#### VF_medium_assemblies_K128_102

two low curls with horizontal connection

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 222 training instances across 38 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_102.png).

#### VF_medium_assemblies_K128_103

stacked loop-like compartments; some exemplars have adjacent low traces

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 169 training instances across 41 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_103.png).

#### VF_medium_assemblies_K128_104

upper curve descending to angular lower foot

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 68 training instances across 30 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_104.png).

#### VF_medium_assemblies_K128_105

low curl and loop with descending tail

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 71 training instances across 26 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_105.png).

#### VF_medium_assemblies_K128_106

lower closed loop joined to upper returning compartment

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 120 training instances across 39 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_106.png).

#### VF_medium_assemblies_K128_107

paired uprights with upper loop followed by low loop and tail

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 151 training instances across 39 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_107.png).

#### VF_medium_assemblies_K128_108

closed ring followed by narrow loop and angular return

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 104 training instances across 31 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_108.png).

#### VF_medium_assemblies_K128_109

low connected curls and ring followed by returning trace

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 444 training instances across 41 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_109.png).

#### VF_medium_assemblies_K128_110

lower loop joined to upper returning compartment

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 84 training instances across 31 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_110.png).

#### VF_medium_assemblies_K128_111

Readable writing assemblies recur, but included structures and neighboring rows vary; atomic boundary unsupported.

- Source review: writing_variable; confidence: insufficient for an accepted unit identity.
- Recurrence: 374 training instances across 43 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_111.png).

#### VF_medium_assemblies_K128_112

raised curved return above low horizontally connected curls

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 92 training instances across 26 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_112.png).

#### VF_medium_assemblies_K128_113

raised short return above low connected curls

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 98 training instances across 27 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_113.png).

#### VF_medium_assemblies_K128_114

multiple short slants joined to upper rounded return

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 306 training instances across 42 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_114.png).

#### VF_medium_assemblies_K128_115

Closest training exemplars dominated by parchment texture, paint, long non-writing traces or extremely small fragments.

- Source review: artifact; confidence: insufficient for an accepted unit identity.
- Recurrence: 285 training instances across 42 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_115.png).

#### VF_medium_assemblies_K128_116

small rounded ring

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 134 training instances across 35 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_116.png).

#### VF_medium_assemblies_K128_117

Closest training exemplars dominated by parchment texture, paint, long non-writing traces or extremely small fragments.

- Source review: artifact; confidence: insufficient for an accepted unit identity.
- Recurrence: 192 training instances across 40 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_117.png).

#### VF_medium_assemblies_K128_118

small angled arch or nearly closed loop

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 99 training instances across 31 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_118.png).

#### VF_medium_assemblies_K128_119

Closest training exemplars dominated by parchment texture, paint, long non-writing traces or extremely small fragments.

- Source review: artifact; confidence: insufficient for an accepted unit identity.
- Recurrence: 976 training instances across 43 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_119.png).

#### VF_medium_assemblies_K128_120

Readable writing assemblies recur, but included structures and neighboring rows vary; atomic boundary unsupported.

- Source review: writing_variable; confidence: insufficient for an accepted unit identity.
- Recurrence: 323 training instances across 40 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_120.png).

#### VF_medium_assemblies_K128_121

two short slant/arch-like traces

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 77 training instances across 30 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_121.png).

#### VF_medium_assemblies_K128_122

lower loop and upper return followed by a low loop with tail

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 121 training instances across 36 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_122.png).

#### VF_medium_assemblies_K128_123

upper curved return descending to angular foot

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 132 training instances across 39 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_123.png).

#### VF_medium_assemblies_K128_124

raised small return above low connected curls

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 31 training instances across 17 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_124.png).

#### VF_medium_assemblies_K128_125

paired tall uprights with upper connecting bar and loop

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 63 training instances across 25 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_125.png).

#### VF_medium_assemblies_K128_126

small rounded ring

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 159 training instances across 32 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_126.png).

#### VF_medium_assemblies_K128_127

lower loop and upper return followed by low loop with descending tail

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 137 training instances across 37 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_127.png).

#### VF_medium_assemblies_K128_128

lower loop and upper return followed by low slants and returning curve

- Source review: writing_consistent; confidence: moderate for visible recurrence; low for atomic-unit identity.
- Recurrence: 188 training instances across 37 caption-connected folio components.
- Context: native writing-region proposals across listed source views; section and hand annotations withheld.
- Variants: See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure..
- Competing segmentations: whole assembly, separate raster components, cuts at low skeleton crossings, larger space-gap group.
- Pen lift and atomic identity: unresolved.
- Source examples: [gallery](../figures/visual_atlas_v4/medium_assemblies/VF_medium_assemblies_K128_128.png).

## Freeze and reproducibility

The machine-readable schema-conforming per-view dataset is in `data/observations/visual_dataset_v0`. `FREEZE_MANIFEST.json` hashes source-derived candidates, native masks, unit hypotheses, protocols, model artifacts, scripts and visual test results before comparison transcriptions are opened. The freeze preserves failed and unknown assignments rather than forcing a single alphabet.
