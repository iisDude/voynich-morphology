# Currier-B positional assay on frozen manuscript-derived v2

**Neither ordinal rank nor measured pixel x is estimable under the registered primary assay.** The frozen admitted Currier-B subset supplies no qualifying minimal pairs. This is an evidence/support limit, not a negative effect estimate and not confirmation of the conventional finding.

The same 134 admitted group occurrences supply both endpoints, across 33 source row hypotheses and seven caption-connected groups: 111 training, 13 validation and 10 test occurrences. Page-level Currier/hand/section metadata were copied only after the v2 freeze; conventional strings, token positions and boundaries were not substituted for visual units or pixel coordinates.

## Registered results

| Representation | Ordinal rank: qualifying primary pairs | Native pixel x: qualifying primary pairs | Outcome |
|---|---:|---:|---|
| Whole connected fine image families | 0 | 0 | Not estimable |
| Broader visual merges | 0 | 0 | Not estimable |
| Compound factor hypotheses | 0 | 0 | Not estimable |

Both endpoints use minimum form frequency 8, edge width 2, and minimum sequence length 5. The response is absolute difference between mean form positions; the design is intercept + edge indicator + length + log geometric mean frequency. At least 12 pairs and a full-rank design are required. All-primary, train+validation and test cohorts separately fail the support requirement. The 144 preregistered representation/cohort/endpoint/frequency/edge-width runs contain 0 qualifying pairs and 0 estimable regressions. Frequencies 5/8/10/12 and edge widths 1/2 were reported without changing segmentation.

| Representation | B occurrences | Distinct literal forms | Maximum form frequency | Forms with frequency ≥8 and length ≥5 |
|---|---:|---:|---:|---:|
| visual_fine_units | 134 | 123 | 3 | 0 |
| visual_merged_units | 134 | 98 | 11 | 0 |
| visual_factored_units | 134 | 96 | 11 | 0 |

Coefficients, confidence intervals and p-values are unavailable rather than set to zero. Connected-family uncertainty, 199 joint caption-block bootstrap resamples, leave-one-caption checks and 199 within-line position-slot null iterations are registered in the runner; they are correctly withheld when there is no estimable pair model. There is no meaningful null regression to calculate on an empty pair set. The ten test occurrences do not provide a held-out replication.

## Rank and pixel position are different measurements

Rank uses frozen ordinal gap slots. Pixel x uses native assigned-writing bounding-box centers divided by native writing extent; it is not obtained by distributing groups evenly. The frozen source ranks include unknown-unit slots even when only a few admitted groups remain in a line. The same occurrences enter both endpoints.

Of the 134 paired observations, 133 have different numerical endpoints. Median absolute difference is 0.0381; maximum is 0.1985. This is a coordinate bookkeeping check, not an assay effect. Source uncertain endpoints were excluded before Currier labels were attached. Ordinal results would remain conditional on the fixed gap hypothesis even if enough pairs existed.

![Coverage and distinct source measurements](../figures/source_adjudication_v2_results.png)

## Interpretation and controls

The conventional rank finding cannot be validated or rejected from this admitted manuscript-derived subset. The new source review improves writing/drawing separation and records real geometry, but complete membership, grapheme boundaries and recurrence remain too uncertain for the registered question. Existing natural-language ordinal controls are retained in the earlier ledger as external reference; they cannot manufacture missing manuscript-derived pairs. No native-image natural-language pixel control is claimed, and no ordinal control is converted into evenly spaced fictitious pixels.

No segmentation, family merge, admission gate, primary threshold or gap hypothesis was retuned after the result. V2 is immutable. New writing annotation or a better source-only ownership method would require a new version frozen before its effect evaluation. Prior exposure to conventional findings and targeted uncertainty selection limit confirmation claims. The outcome remains **unknown**.

Freeze SHA-256: `bbfd0e6f4e25dbad613c4b713d2b5bb50b6bd5d856487bfd9c6fd030ee408dc6`

- [Source adjudication and limitations](09_source_adjudication_v2.md)
- [Analysis plan](../tests/adjudicated_currier_B_v2/analysis_plan.json)
- [All registered results](../tests/adjudicated_currier_B_v2/results.json)
- [Support diagnostics](../tests/adjudicated_currier_B_v2/support_diagnostics.json)
- [Post-freeze run manifest](../tests/adjudicated_currier_B_v2/run_manifest.json)
- [Prior conventional assays and natural-language controls](07_full_test_ledger_results.md)
