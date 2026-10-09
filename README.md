# Source-traceable Voynich morphology

**Primary author and creator: Dylan Bedford** · [ORCID 0009-0005-9766-224X](https://orcid.org/0009-0005-9766-224X). Codex AI assisted implementation and source adjudication. No independent palaeographer or human-rater validation is claimed.

This contribution preserves a frozen research snapshot of a ground-up investigation of visible writing in the Voynich manuscript (Beinecke MS 408). Its narrow current contribution is a **source-traceable, class-free continuous morphological representation of selected confirmed writing**, retaining source/raster uncertainty and alternative recoveries, validated on a qualified fresh-caption sample and stress-tested under conservative sensitivity analyses.

This is not a transcription system, alphabet, identification of letters/graphemes/allographs/words, language result, or decipherment. A finite raster candidate is not proof of a physical whole-parent contour. Conventional EVA/RF/v101 boundaries did not define the source representations.

## Why this project exists
This started as a fun side project to see whether the Voynich Manuscript could be approached from the ground up, beginning with the manuscript images rather than assuming the existing transcription systems were the final word.
It did not decipher the manuscript, but experiments showed that some of the ways the writing is currently represented depend on interpretive choices about boundaries, structure, and classification. The project also showed that those choices can be revisited: a source-first, uncertainty-aware representation can be built and tested without requiring every visible form to be assigned to a predefined character or transcription unit.
If this work helps someone else, or gives them a useful dataset to build on, then the project did something worthwhile.

## Findings

- V3 supports 14 recurrent structural classes within its tested sample. It does not establish linguistic units.
- V4 failed practical sequence support; V5 improved source-writing recognition but established no complete structural rows or complete groups of length ≥3. V6 validated no additional classes. These failures remain evidence.
- Neutral Feature Trials 1 and 2 show useful partial measurements but failed their respective validation/coverage gates. Raster repeatability and source-visible agreement are distinct.
- Direct Morphology Trial 1 was post-exposure feasibility. Trial 2 passed its registered sample/gates: contour64 AUROC **0.879** on **211 same/different pairs**, across **8 qualified fresh captions**; caption-bootstrap 95% interval **0.767–1.000**, aspect baseline **0.737**.
- The separate robustness investigation is **sensitive to one or more evaluation assumptions**. A parent-disjoint subset scored 0.805 with an interval crossing chance; broad-random discrimination was weaker than aspect-matched discrimination; treating all partial ratings as same changed the target and reduced AUROC to 0.672. These do not replace or retune Trial 2.

## Inspect

[Methods](METHODS.md) · [Evidence ledger](RESULTS.md) · [Machine-readable claims](manifests/MASTER_EVIDENCE_LEDGER.json) · [Data dictionary](DATA_DICTIONARY.md) · [Provenance](PROVENANCE.md) · [Limitations](LIMITATIONS.md) · [References](REFERENCES.md)

Important reports: [V3](reports/public/11_recurrence_bottleneck_and_structural_v3.md), [V4](reports/public/13_source_sequence_validation_v4.md), [V5](reports/public/15_source_adjudicated_row_benchmark_v5.md), [V6](reports/public/17_confirmed_unknown_structures_v6.md), [Feature 1](reports/public/19_neutral_structural_feature_profiles_trial1.md), [Feature 2](reports/public/21_neutral_structural_feature_profiles_trial2.md), [Direct 1](reports/public/23_direct_contour_morphology_trial1.md), [Direct 2](reports/public/25_direct_contour_morphology_trial2.md), [Robustness](reports/public/27_direct_morphology_trial2_robustness.md).

Atlases: [V3](atlases/12_neutral_structural_atlas_v3.html), [V5 source rows](atlases/16_source_row_reference_atlas_v5.html), [Direct Trial 2](atlases/26_direct_contour_morphology_atlas_trial2.html), [Robustness dashboard](atlases/28_direct_morphology_trial2_robustness_dashboard.html). Open downloaded HTML locally or serve this directory read-only; GitHub ordinarily displays HTML source.

## Quick start

Use Python 3.12.14 and an environment outside this snapshot. From the parent of `CONTRIBUTION/`:

```sh
python -m venv replay_env
# Activate replay_env using your shell's usual command.
python -m pip install -r CONTRIBUTION/environment/requirements-lock.txt
python CONTRIBUTION/tests/verify_integrity.py
python CONTRIBUTION/tests/replay_results.py --output replay_output/numerical_replay.json
python CONTRIBUTION/tests/verify_package.py
```

This numerical replay reads only contribution evidence and installed software dependencies. Original source-image re-extraction additionally requires independently obtained Yale images; [reproduction instructions](REPRODUCIBILITY.md) give IDs, hashes and command order. Source judgments are fixed observations, not reproducible palaeographic truth.


The snapshot includes the complete listed freeze chain, unchanged original manifests, source-derived data, historical code/tests/reports and attributed example crops. Large JSON transport objects are losslessly compressed; `scripts/evidence.py` provides direct access. `manifests/FILE_INDEX.json` maps original logical paths to canonical payloads or external native sources. Historical pickles are preserved for inspection; class-free replay does not require them, and trusted hash verification helps establish their provenance before loading. Full Yale scans, private conversations, software wheels, downloaded third-party code repositories and raw UD controls remain separate source inputs.

Citation details are available in [CITATION.cff](CITATION.cff). The scoped [LICENSE](LICENSE), [source notice](NOTICE.md) and [third-party notices](THIRD_PARTY_NOTICES.md) describe the applicable reuse and attribution terms. The author ORCID and repository URL have been added in a separately recorded [publication-metadata update](manifests/metadata_updates/ORCID_REPOSITORY_UPDATE.json); the original snapshot manifest and pre-update files are preserved. DOI, release version and Zenodo record metadata remain unassigned.

## Note

This repo was made with the help of an LLM. I’ve reviewed it for awkward wording, errors or specifics/criteria that's meant for me personally, but I may have missed some.
Use the repo however it helps you, and good luck with your experiments.
