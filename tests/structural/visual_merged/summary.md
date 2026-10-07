# visual_merged: structural reproduction

Primary tests use 6,565 admitted rows/groups as defined in the source manifest; groups are not presumed words.

| Subset / position | Qualifying pairs | Edge effect | Caption bootstrap 95% interval |
|---|---:|---:|---|
| all / normalized_group_rank | 0 | Not estimable | Not estimable |
| all / normalized_pixel_center | 0 | Not estimable | Not estimable |
| all / source_pixel_center_x | 0 | Not estimable | Not estimable |
| all / source_pixel_x_page_fraction | 0 | Not estimable | Not estimable |
| A / normalized_group_rank | 0 | Not estimable | Not estimable |
| A / normalized_pixel_center | 0 | Not estimable | Not estimable |
| A / source_pixel_center_x | 0 | Not estimable | Not estimable |
| A / source_pixel_x_page_fraction | 0 | Not estimable | Not estimable |
| B / normalized_group_rank | 0 | Not estimable | Not estimable |
| B / normalized_pixel_center | 0 | Not estimable | Not estimable |
| B / source_pixel_center_x | 0 | Not estimable | Not estimable |
| B / source_pixel_x_page_fraction | 0 | Not estimable | Not estimable |

Frequency 8, edge width 2, minimum length 5 are primary. Frequency 5/10/12, one-unit edges, and legacy short forms are retained sensitivity specifications. Effects adjust for group length and log geometric-mean pair frequency. Caption/document occurrence bootstrap, connected-family inference where supported, leave-one-caption deletion and within-line slot shuffles have separate interpretations. Normalized ordinal rank is separate from measured native pixel x; conventional coordinates remain unknown.

Graphs report equal-core signed deltas, independent caption half-splits, train/test reproducibility, alternate predictions after removing the direct edge and every one of its training cores, and triangles with disjoint core buckets. Shared edges/cores are dependent; relation-naive confidence intervals are not supplied. Source masks and group boundaries are unvalidated, and known extraction failures prevent treating visual results as recovered writing-unit evidence.

Sequence tests retain gap resets and increasing/decreasing physical x hypotheses. The ordinal-rank running-state outcome is already exactly predictable from its rank baseline and is therefore not independently estimable. Pixel running-state tests use an additional trained state predictor with held-out caption losses and shuffled increments.

Null draws (99 graph/sequence; 199 primary pair bootstraps/shuffles) give coarse Monte Carlo resolution. Threshold sweeps are not independent confirmations. Exact undocumented historical settings are not claimed. Prior positional analysis predates this investigation; see the primary-source collision report.

Figures: `figures/primary_position.png`, `figures/heldout_predictions.png`. Full machine-readable results retain all non-estimable cases.
