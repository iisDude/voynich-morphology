# Finnish hidden-state transfer

Hypothesis: adapting emissions while holding a pooled transition kernel predicts held-out within-group sequences better than a fully frozen model. Four/five exchangeable hidden states, two pooled restarts selected on validation, cap 200 groups/document, 30 EM steps. Groups restart the HMM; this is not a physical-line accumulator.

Seed: 20261005. Exact source paths and SHA-256 digests: `input_manifest.json`. Inclusion, exclusions, model settings and null definitions: `config.json`.

Visual source groups and prototype categories are provisional. Unknown assignments are excluded without renumbering original physical/rank slots. Caption/document resampling is not a verified physical-bifolio independence proof. Post-exposure repairs are diagnostic, not newly blind. Multiple exploratory endpoints are dependent.

| States | Context | Adaptation | Excess held-out bits/unit | Document bootstrap 95% interval |
|---:|---|---|---:|---|
| 4 | b | frozen_both | 0.000000 | [0.0, 0.0] |
| 4 | b | fixed_transitions | -0.008154 | [-0.01962954905716574, 0.003617662968082136] |
| 4 | b | fixed_emissions | 0.000075 | [-0.0027413468436717605, 0.0026071977717890865] |
| 4 | b | adapt_both | -0.011835 | [-0.024744205372662708, 0.0018320829975944086] |
| 4 | w | frozen_both | 0.000000 | [0.0, 0.0] |
| 4 | w | fixed_transitions | -0.012537 | [-0.017741165568877976, -0.007713967457933335] |
| 4 | w | fixed_emissions | -0.002259 | [-0.003233581047378058, -0.0012607437622256935] |
| 4 | w | adapt_both | -0.017700 | [-0.023267256788395252, -0.012269194032624315] |
| 5 | b | frozen_both | 0.000000 | [0.0, 0.0] |
| 5 | b | fixed_transitions | -0.002956 | [-0.016483758126285733, 0.011773462464829723] |
| 5 | b | fixed_emissions | -0.002318 | [-0.004357802489072112, -0.0005957467844724421] |
| 5 | b | adapt_both | -0.007999 | [-0.024961695470755007, 0.010438452744390694] |
| 5 | w | frozen_both | 0.000000 | [0.0, 0.0] |
| 5 | w | fixed_transitions | -0.007678 | [-0.013111903481797138, -0.0029246972893633917] |
| 5 | w | fixed_emissions | -0.002583 | [-0.0036782890707358876, -0.0015830450935340682] |
| 5 | w | adapt_both | -0.012380 | [-0.018473365292318234, -0.007159175146321726] |

Negative excess bits favor adaptation. Frozen-both, fixed-emission, fixed-transition and joint-adaptation models are competing transfer baselines; no random-label HMM refit null was run. Bootstrap 1,000 document blocks. Convergence warnings and likelihood changes are preserved; EM states are not uniquely identified or decoded symbols.

Latin compares Cicero works; Finnish b/w are source partitions, not verified semantic genres. The all-hand Voynich sensitivity confounds hand/section. Ordinary-language gains show why this pattern cannot uniquely identify a shared computational runtime. Failure: fewer than four train or two test documents/context, incomplete visual groups, or unstable optimization. Prior art: standardized ledger 14 analogue; no exact unpublished historical replication or novelty claim.
