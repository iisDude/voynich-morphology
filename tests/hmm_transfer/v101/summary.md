# v101 hidden-state transfer

Hypothesis: adapting emissions while holding a pooled transition kernel predicts held-out within-group sequences better than a fully frozen model. Four/five exchangeable hidden states, two pooled restarts selected on validation, cap 200 groups/document, 30 EM steps. Groups restart the HMM; this is not a physical-line accumulator.

Seed: 20261005. Exact source paths and SHA-256 digests: `input_manifest.json`. Inclusion, exclusions, model settings and null definitions: `config.json`.

Visual source groups and prototype categories are provisional. Unknown assignments are excluded without renumbering original physical/rank slots. Caption/document resampling is not a verified physical-bifolio independence proof. Post-exposure repairs are diagnostic, not newly blind. Multiple exploratory endpoints are dependent.

| States | Context | Adaptation | Excess held-out bits/unit | Document bootstrap 95% interval |
|---:|---|---|---:|---|

not_estimable: requires two contexts, at least four train and two test document blocks per context

[{'context': 'H', 'split': 'validation', 'count': 1}, {'context': 'H', 'split': 'train', 'count': 7}, {'context': 'H', 'split': 'test', 'count': 1}, {'context': 'B', 'split': 'train', 'count': 5}, {'context': 'B', 'split': 'test', 'count': 3}]

Negative excess bits favor adaptation. Frozen-both, fixed-emission, fixed-transition and joint-adaptation models are competing transfer baselines; no random-label HMM refit null was run. Bootstrap 1,000 document blocks. Convergence warnings and likelihood changes are preserved; EM states are not uniquely identified or decoded symbols.

Latin compares Cicero works; Finnish b/w are source partitions, not verified semantic genres. The all-hand Voynich sensitivity confounds hand/section. Ordinary-language gains show why this pattern cannot uniquely identify a shared computational runtime. Failure: fewer than four train or two test documents/context, incomplete visual groups, or unstable optimization. Prior art: standardized ledger 14 analogue; no exact unpublished historical replication or novelty claim.
