# Frozen visual candidates versus inherited transcriptions

No complete writing-unit or grapheme correspondence is accepted. The original manuscript-derived candidate snapshot froze before the comparison transcription contents opened. The revised tracked snapshot froze separately after source-only repair and is explicitly post-exposure. Failed and partial mappings remain visible rather than being used to redefine the visual atlas.

## Inputs and order of work

The original `visual_dataset_v0/FREEZE_MANIFEST.json` SHA-256 is `eb1dff78adf9409757812a2aa7fca0a8c7a03ccbb102362276081e2bfd0ff656`, frozen at `2026-10-05T17:24:15.776782+00:00`. It contains 204 views and 1,512 hashed files. The second `visual_dataset_v11/FREEZE_MANIFEST.json` SHA-256 is `cab58c0dd8a0d344b15eec7aeac08f822a6dfc55fcf2aa66bc54d5ed3f888097`. Neither claims a canonical alphabet.

Comparison parser v1 failed format review and is preserved as an invalid diagnostic. Parser v2 handles logical continuations, comments/annotations, retained ligature signs, scoped metadata, same-row continuation loci, uncertain comma boundaries, ambiguous readings and literal v101 punctuation/numeric signs. Uncertain readings abstain; split/join alternatives remain separate. Metadata attaches only to post-freeze copies. Inherited section, hand, Currier, quire and bifolio fields do not become visual-unit truth.

RF is automatically derived from ZL and GC, so agreement among these encodings is not three independent manuscript replications. [Primary transcription provenance](https://www.voynich.nu/transcr.html). Format handling is checked against the [IVTFF specification](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf).

## Native writing-group alignment

The original snapshot produced 42 unique four-row count-anchor proposals. All 18 prespecified sampled proposals failed complete-row source review. The exact-mask recheck corrected an earlier error: mere neighboring ink in an RGB bounding crop is not assigned ink. Some bodies are coherent, while other assigned masks mix rows, drawings or paper fragments and omit writing. See [the correction](03_crosswalk_membership_correction_v1.md).

The tracked snapshot produced 60 row proposals containing 439 candidate groups. All 22 sampled proposals were reviewed with exact native masks. No complete-row/group alignment was certified. Audit 17 has plausible f47r first-row identity and interior gaps; incomplete initial/detached marks remain. This partial plausibility is preserved. The remaining 38 proposals are unverified, not declared failures by extrapolation. See [the reviewed records](05_tracked_crosswalk_source_review_v11.md).

The proposed count patterns are geometry hypotheses. Drawing fragments can replace writing groups while preserving a count, and a wrong row can share the same four-row pattern. Full writing membership, row identity and every slot require source support. Coherent body presence alone does not meet that condition. No conventional group receives a fabricated native pixel coordinate.

## Convention-to-convention correspondence

There are 48,275 proposed ZL→RF/v101 group pairs at the same physical locator and equal apparent-boundary count; 3,019 row comparisons fail count/coverage agreement. These are ordinal pairing hypotheses, not established shared grapheme boundaries. One-to-many, context-dependent and unresolved mappings remain possible.

A separate train-only correspondence test requires at least three occurrences and 80% dominance of whole-form pairs, then at least five distinct single-edit contexts and 90% agreement for a literal-unit mapping. Before graph comparison it must predict at least 30 completely covered held-out groups with ≥90% exact accuracy. RF covers 924 groups at 83.1% accuracy and v101 covers 620 at 72.6%; both fail. Consequently all eight proposed cross-system graph-correlation endpoints are withheld. High historical correlations are not recreated by assuming a shared alphabet.

## Conclusion

The crosswalk is a reproducible rejection/ambiguity record, not a successful alphabet conversion. ZL, RF and v101 can be tested within their own conventions after the visual freeze. They cannot presently validate or repair complete native writing segmentation, and their ordinal positions cannot be renamed physical pixel positions. No meanings or plaintext mappings are proposed.
