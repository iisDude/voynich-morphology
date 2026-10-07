# Source and transformation provenance

Primary collection: [Cipher manuscript, Beinecke MS 408](https://collections.library.yale.edu/catalog/2002046), Beinecke Rare Book and Manuscript Library, Yale University. The manuscript author is unknown. Yale is the custodian/source of photographs, not a project collaborator or endorsing institution.

`data/source_index/yale_native_all_manifest.csv` records 204 cached native views, their exact Yale image IDs, IIIF full/full URLs, byte hashes, native width/height and nominal PDF scaling. For example image 1006076 is retrieved from `https://collections.library.yale.edu/iiif/2/1006076/full/full/0/default.jpg`. These are image/view identifiers, not an assumption of 204 independently mapped physical leaves. The collection description advertises high-resolution page images; the cached full-size image and its metadata are the source used, with no upsampling advertised as new evidence.

Coordinates are native RGB pixels: origin top left, x rightward, y downward, `[x0,y0,x1,y1]` half-open crop convention unless an original object explicitly supplies a different representation. Native coordinates must not be replaced by PDF display pixels or normalized ordinal group rank. Endpoint intervals represent adjudicated source uncertainty. Nominal PDF/native scale is not proof of subpixel alignment, and foldout/panel/view overlap uncertainty remains recorded.

The source lineage is:

1. Yale native photograph, ID, retrieval URL, dimensions and SHA-256.
2. Source/layout field and parent proposal in native coordinates; RGB context and source adjudication.
3. Whole-extent state, membership, possible contact/split/contamination/detached alternatives, frozen before morphology predictions.
4. Primary and observed alternative threshold masks in the original candidate ensemble; unknown whole extent is not imputed.
5. Aspect-preserving binary64 field, signed-distance64 field, contour32/128 sensitivity fields, with original candidate/parent indexes.
6. Primary numerical distance and observed candidate envelope, then source-blind pair-rating evaluation and conditional uncertainty.

`data/direct_morphology/trial2/source_parent_ensembles.json` and its candidate table carry this parent/candidate/native-coordinate linkage. Arrays use table indices, not conventional transcription labels. The full source image is excluded from the snapshot; attributed example crops/annotations are retained separately. `manifests/FILE_INDEX.json` maps every frozen logical file to its original hash and canonical transport location; all old manifest bytes remain at `manifests/original/`.

## Exposure audit

Direct Trial 1 used previously exposed parents and ratings: feasibility only. Trial 2 audited 102 caption groups, identified 45 eligible groups relative to specified detailed prior uses, and selected 8 by source/layout criteria before outcomes. Selected caption groups were 7, 11, 29, 31, 45, 48, 54 and 87, with two ordinary fields per caption. Caption54 required a preregistered drawing-region trim. “Fresh” excludes recorded V3 detailed fitting/selection, V5/V6 adjudication corpora, feature tuning/ratings and Direct Trial 1 similarity use; it does not mean globally image-blind or untouched by overview/V4 processing. See the unchanged caption audit and selection/source seals. No V3 labels constructed the direct morphology space.

## Upstream audit and private inputs

[REFERENCES.md](REFERENCES.md) and `data/source_index/UPSTREAM_RESOURCES.json` distinguish actual use, comparison, prior art and dependencies. `data/source_index/audit/archive_audit.json` preserves exact supplied ZIP hashes, Git archive comments, and preferred citation/license member hashes. The code-origin audit records static imports/URLs and normalized nontrivial function comparison; no exact matches were found, but this does not certify independent algorithm invention. No downloaded repository code was executed or redistributed.

Original handoff and test-ledger documents are retained in `reports/context/`. Private chat transcripts and full source PDF are excluded; their historical project existence is not presented as public data. The initial evidence index retains original filenames/hashes without silently rewriting original manifests. A fresh researcher can reproduce numerical results from the snapshot and can obtain the source photographs independently for crop/mask checks. Source annotations cannot be independently validated simply by rerunning code.
