# Latin hidden-state transfer

Hypothesis: adapting emissions while holding a pooled transition kernel predicts held-out within-group sequences better than a fully frozen model. Four/five exchangeable hidden states, two pooled restarts selected on validation, cap 200 groups/document, 30 EM steps. Groups restart the HMM; this is not a physical-line accumulator.

Seed: 20261005. Exact source paths and SHA-256 digests: `input_manifest.json`. Inclusion, exclusions, model settings and null definitions: `config.json`.

Visual source groups and prototype categories are provisional. Unknown assignments are excluded without renumbering original physical/rank slots. Caption/document resampling is not a verified physical-bifolio independence proof. Post-exposure repairs are diagnostic, not newly blind. Multiple exploratory endpoints are dependent.

| States | Context | Adaptation | Excess held-out bits/unit | Document bootstrap 95% interval |
|---:|---|---|---:|---|
| 4 | Atticum | frozen_both | 0.000000 | [0.0, 0.0] |
| 4 | Atticum | fixed_transitions | -0.004812 | [-0.009581364353215742, 0.00010240449954426181] |
| 4 | Atticum | fixed_emissions | -0.002171 | [-0.003551822175783812, -0.0007535516812976591] |
| 4 | Atticum | adapt_both | -0.030807 | [-0.03784135901056524, -0.025315761516522105] |
| 4 | Officiis | frozen_both | 0.000000 | [0.0, 0.0] |
| 4 | Officiis | fixed_transitions | -0.030571 | [-0.03377476162290727, -0.027266806823701313] |
| 4 | Officiis | fixed_emissions | -0.001305 | [-0.0022192476234603096, -0.00039950922828068443] |
| 4 | Officiis | adapt_both | -0.050850 | [-0.056385891294194065, -0.04615782139922095] |
| 5 | Atticum | frozen_both | 0.000000 | [0.0, 0.0] |
| 5 | Atticum | fixed_transitions | -0.000198 | [-0.003968850741736326, 0.003225933299760814] |
| 5 | Atticum | fixed_emissions | 0.001084 | [-0.001021678728197465, 0.003298008632972629] |
| 5 | Atticum | adapt_both | -0.003035 | [-0.009755837509525623, 0.003239282812537543] |
| 5 | Officiis | frozen_both | 0.000000 | [0.0, 0.0] |
| 5 | Officiis | fixed_transitions | -0.023963 | [-0.02708568847218321, -0.020964754272007485] |
| 5 | Officiis | fixed_emissions | -0.012781 | [-0.014918952332940728, -0.010613490004314483] |
| 5 | Officiis | adapt_both | -0.041447 | [-0.047131894699600614, -0.03640206495077795] |

Negative excess bits favor adaptation. Frozen-both, fixed-emission, fixed-transition and joint-adaptation models are competing transfer baselines; no random-label HMM refit null was run. Bootstrap 1,000 document blocks. Convergence warnings and likelihood changes are preserved; EM states are not uniquely identified or decoded symbols.

Latin compares Cicero works; Finnish b/w are source partitions, not verified semantic genres. The all-hand Voynich sensitivity confounds hand/section. Ordinary-language gains show why this pattern cannot uniquely identify a shared computational runtime. Failure: fewer than four train or two test documents/context, incomplete visual groups, or unstable optimization. Prior art: standardized ledger 14 analogue; no exact unpublished historical replication or novelty claim.
