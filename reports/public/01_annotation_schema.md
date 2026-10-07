> Publication link-adapted view; the original report is preserved unchanged in `reports/`.

# Neutral annotation schema v0

Status: draft specification; no observed unit dataset exists yet. Companion machine-readable structural specification: `../data/observations/annotation_schema.json`. All quantities below use source-image pixels unless an explicit unit says otherwise.

## Coordinate and provenance contract

An image view has `V_...`; a physical folio surface/panel has `P_...`. A view may include several panels and a panel may occur in several views. Until verified, panel identity is null. The initial `B_...` IDs are image-view aliases, not folio identities or glyph classes.

Every observed object stores `view_id`, a source image SHA-256, and a source-coordinate bounding box `[x0,y0,x1,y1]`. Origin is top left, x increases rightward, y downward, and the box is half-open. Cropping at native size uses an integer box and exact translation: `x_source = x_crop + x0`, `y_source = y_crop + y0`. If deskewing or scaling is later used, retain the full invertible transform and use a separate coordinate-frame identifier. Never overwrite the native image.

A displayed PDF page has its own canvas coordinates. The embedded image is the annotation coordinate frame. Neither page points nor thumbnail pixels can be substituted for native pixels. A geometrically normalized comparison must retain the original coordinates.

## Entities and fields

| Entity | Required identity and geometry | Additional neutral fields |
|---|---|---|
| View | `view_id`, PDF SHA-256/page/index, image SHA-256/dimensions | caption/image ID, extraction method, coordinate frame, display transforms |
| Panel | `panel_id`, `view_id`, bbox | folio caption, verification status, alternate panel assignments |
| Physical line or text path | `line_id`, `view_id`, bbox, ordered path points | panel reference, path kind (`linear`, `arc`, `irregular`, `unknown`), region ID, optional baseline/body band, endpoint uncertainty |
| Space-delimited group candidate | `group_id`, line/view references, bbox | path interval, neighboring gap measurements, boundary confidence, competing split/merge alternatives |
| Visible component instance | `component_id`, view reference, bbox | trace points if warranted, loops, endpoints, intersections, connectivity assertions, ink/quality flags |
| Assembly candidate instance | `assembly_id`, view/group references, bbox | proposed component members, candidate visual-family ID or null, variant features, geometry measurements, competing membership hypotheses |
| Segmentation hypothesis | `segmentation_id`, target reference, alternative nodes/relations | supporting and contradicting observation IDs, status; shared-stroke relations permitted |
| Observation | `observation_id`, target reference, direct claim or measurement | evidence crop and coordinates, method, observer/run ID, confidence, resolution flag |
| Interpretive hypothesis | `hypothesis_id`, explicit proposition | supporting/contradicting observations, predicted falsifier, confidence, next discriminating test |

Group boundaries are proposals even when spacing looks clear. A component here means a visually traced ink region, not a known pen stroke or character. Raster connected components are stored with threshold/method parameters and must not be conflated with physical ink continuity. Several assemblies may share a connector under an alternative model; a rigid tree cannot represent that uncertainty.

## Geometry and connectivity

Measurements use an object with `value`, `unit`, `method`, `uncertainty`, and `missing_reason`. Missing values are null, never zero. For finite values state uncertainty as an interval or `unestimated`.

- Body height: local estimate from a reviewed band of ordinary writing, with its sample and excluded tall/descending marks recorded. Do not compute it from a preassigned alphabet.
- Tall and lower extent: distances from the local body band/baseline with uncertainty. The height ratio records both numerator and denominator; it is not initially a unit-class decision.
- Connectivity: relation endpoints plus `connected`, `disconnected`, or `unresolved`; evidence and image quality. A crossing alone does not identify stroke order.
- Pen lift/order: `supported`, `unsupported`, or `unresolved`, with the precise visible basis. Default is unresolved. Component count does not establish pen lifts.
- Loops/intersections/endpoints: counts may be null or bounded when scan quality prevents a unique count.
- Whitespace: geometric gap interval and measurement direction. Do not equate a gap with a lexical boundary.
- Position: both raw bbox/path coordinates and normalized position. For a linear text region, proposed center position is `(group_center_x - line_left)/(line_right - line_left)`, where line bounds describe the reviewed text path/region. Preserve alternative bounds, line width, and group width. Treat lines wrapping around an illustration as separate path segments with a shared context identifier until reviewed.
- Circular text: use path arc length `s / total_length`, retain orientation and alternative start points, and keep it out of a horizontal-line assay unless a separately registered conversion justifies inclusion. Arc order is a geometric traversal, not assumed reading order.

## Uncertainty and hypotheses

Separate confidence in location, boundary, geometry, connectivity, and family assignment. Confidence values are ordinal (`high`, `medium`, `low`, `unresolved`), not calibrated probabilities. Record image quality (`adequate`, `limited`, `unusable`) for the particular claim, rather than one rating for an entire page.

Alternative segmentation nodes can mean `assembly`, `component`, `compound`, or `frame_with_insertion`. They reference instances; they do not silently create established units. Relations explicitly include `contains`, `shares_trace`, `connected_to`, `adjacent_to`, and `inserted_within_candidate_frame`. The latter is a proposed structural relation.

No raw-data fields named letter, word, vowel, prefix, suffix, meaning, phoneme, or translation. Neutral family IDs use `A_0001`, `S_0001`, etc.; the existence of a family does not establish an indivisible character.

## Separate metadata and freeze procedure

Currier, conventional section labels, attributed hand, and EVA/RF/v101 strings belong in a later comparison table, joined through independently verified panel/locus mappings. The visual-only discovery tables exclude these labels.

Before a crosswalk or structural assay: finish annotations, validate references and coordinate bounds, export the competing segmentations, record annotation/source hashes and prior exposure, and freeze a version. Use reserve physical folios once for evaluation after that freeze. If rules change afterward, version them and acquire another holdout set. Do not relabel reserve failures as discovery successes.

This specification establishes storage requirements. It does not establish how many reusable assemblies exist or select a preferred segmentation.

The scaffold is intentionally empty and is not Deliverable 5. JSON Schema checks cannot establish geometric validity or scientific neutrality by themselves: before freeze, separately validate unique IDs, reference targets, ascending/in-bounds coordinates, panel overlap, supported claims, and null-value reasons. The bundled environment lacks `jsonschema`; setup verification checks JSON syntax, local schema references, and scaffold keys only. Full Draft 2020-12 validation remains unverified.
