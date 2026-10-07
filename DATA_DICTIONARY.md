# Public data dictionary

`manifests/FILE_INDEX.json` is the exhaustive public object inventory. Every original logical file has an original SHA/size, freeze provenance and canonical payload or external-source state. `data/*/INDEX.json` provides category navigation. Compression is transport only; load with `scripts/evidence.py` or materialize outside the snapshot. `data/source_index/OBJECT_SCHEMAS.json.gz` lists observed field paths/types by public JSON object family and array-key/dtype/shape signatures for NPZ objects. These observational schemas do not silently reinterpret earlier data.

| Public object family | Meaning / governing record |
|---|---|
| source_index | Yale native image/caption/view metadata, eligibility/exposure and upstream audit, hashes, object schemas, field definitions; no full scan. |
| structural_v3/frozen | Source fields/parents, competing groups, contract and accepted neutral structural atlas. Development competitors remain under data/historical and include the rejected first model. |
| sequence_v4/frozen | Ordered proposals/class states/optional membership and three gap hypotheses; practical notation failed. |
| source_benchmark_v5/frozen | Source-object row truth, writing/nonwriting/unknown ownership, endpoints, class mapping and sequence diagnostics; not exhaustive ground truth of every photograph pixel. |
| unknown_inventory_v6/frozen | Confirmed unknown-parent diagnoses, candidate/factor investigations and rejected validation outcome. V3 classes remain unchanged. |
| neutral_features/trial1,trial2 | Registered descriptor profiles, native variants, source qualification, pair ratings and numeric distances; failures retained. |
| direct_morphology/trial1,trial2 | Source-parent ensembles and alternative extent/recovery records, native masks,32/64/128 binary fields, SDF64, matrices, anonymous pairs/ratings, protocols/seals. Whole connected parent is primary. |
| robustness/trial2 | Frozen filter flags, graph subsets, repeat selection/ratings, bootstrap draws; read-only analysis of original Trial2, not a replacement trial. |
| data/historical | Original earlier segmentation/proposal/development/comparison artifacts named in freezes; conventional metadata is quarantined from direct morphology/lab inputs. |
| tests | Original computational diagnostics and post-freeze assessments, plus clearly separated publication checks. A test output is not source annotation. |
| reports, atlases, figures | Original report bytes, public link-adapted views and attributed source-derived examples/plots. No whole-page raster is automatically a writing unit. |
| manifests/original | Every original freeze/seal byte-for-byte. New FILE_INDEX/master ledger/publication freeze are separate objects. |
| scripts/frozen | Original project producers/replay/guards. Do not execute mutation scripts against this immutable contribution. Historical pickle models require trusted inputs. |

## Parent and proposal terminology

A proposal is a detector hypothesis. A source-confirmed writing parent is a photographed connected writing organization that has received a writing judgment; this need not settle its whole extent or class. A connected parent can include loops, frame-like structures, branches or repeated traces without being internally segmented into letters. Compound/contact cases remain separate from new-class discovery. Detached marks can be writing while their owner remains uncertain. Groups are competing white-space partitions, not words. Rows are source-layout/ownership hypotheses unless explicitly adjudicated.

Native coordinates use top-left origin, x rightward/y downward and half-open bboxes. Source endpoint intervals preserve uncertainty. A normalized ordinal rank is a different quantity from physical pixel x. A caption is a source grouping aid; no linguistic/hand/section truth is encoded in that term.

## Representation and uncertainty

The candidate table fixes array correspondence, contrast/recovery role and parent index. Binary64 is aspect/orientation-preserving; contour distance is the frozen symmetric raster Chamfer metric. SDF64 is secondary.32/128 are sensitivity representations. Full-extent unknown is an absent physical coordinate, even if local masks exist. Observed low/high envelopes cover admitted finite recoveries only and cannot be treated as probability/confidence bounds. Nearest-neighbor sets are not equivalence classes.

Feature uncertainty states distinguish stable, variant-sensitive, unknown-presence and not-applicable. Source qualification is additional to raster stability. Null/None, UNK and numeric0 are not interchangeable. Direct pair ordinal ratings0/1/2 mean different/partial/same, with U unresolved; other early rating systems retain their own protocol definitions.

Frozen V3 hypothesis labels ST01–ST15 are neutral identifiers;14 passed acceptance. Descriptions, example coordinates, topology/geometry criteria and competitors are in the V3 atlas/model contract. Do not fill rejected hypotheses or infer an alphabet from the numbering. V4/V5 preserve0.35/0.55/0.75 boundaries separately. Negative and abstained outcomes remain records rather than disappearing from denominators.

The machine-readable [field definitions](data/source_index/FIELD_DEFINITIONS.json) define important shared fields. For historical unshared fields, the object-family schema links back to the original producer/report/protocol; keep that meaning instead of forcing a new public schema onto old evidence.
