> Publication link-adapted view; the original report is preserved unchanged in `reports/`.

# Calibration findings

The pilot is a method calibration stage. It is not the manuscript-wide visual dataset and no manuscript-derived unit vocabulary has been frozen.

All 204 folio-captioned scans now have native Yale counterparts and verified reversible image registration. Nine cover/binding views are outside manuscript-script processing. The native and PDF images are the same captures at different resolutions, not independent examples.

## Rejected shortcuts

1. Page-global baseline voting confounds writing with drawing edges and parchment texture. Native resolution exposes more of both. A machine path proposal is not an observed physical line.
2. Scaling path-detector parameters by the photo scale fails on foldouts: photo scale and local writing height differ.
3. Tiny raster fragments pulled the unweighted median body-height estimate downward. An anchored, area-weighted estimate replaces it provisionally; it still needs source review.
4. A first classifier evaluation incorrectly labeled a mixed text/drawing row negative because its centre lay in the drawing. Those accuracy figures are invalid.
5. Requiring the whole row to lie in an explicitly negative region leaves negatives concentrated in one view. Leave-one-view-out specificity cannot be estimated from that sample. Its apparent high accuracy is not evidence of a successful quality gate.
6. Local-window classification adds explicit negatives across views but generalizes poorly. At probability 0.7, the pilot leave-one-view-out evaluation has 19 true positives, 21 false negatives, 4 false positives and 544 true negatives. The dependent window samples are not independent statistical trials. This classifier will not decide which manuscript ink enters the atlas.

The next route uses reviewed spatial regions and source-crop audits. The region-review rules were registered before reviewing nonpilot layout. All automatic masks, paths, and subdivisions remain proposals; disconnected raster components do not establish strokes or pen lifts.

## Coverage and independence

All folios touched by the twelve pilot views are calibration, including additional views of those folios. The remaining split comprises 90 training, 36 validation and 48 test views, grouped by folio numbers appearing together in captions. A complete panel/bifolio map is still unverified, so this split does not yet establish bifolio independence.

No transcription content has been opened for segmentation. Prior conventional strings and results were encountered in the supplied provenance chats; the correct description is transcription-withheld, not psychologically blind.

No pen-lift, stroke-order, alphabet, meaning, or structural-assay finding is asserted here.
