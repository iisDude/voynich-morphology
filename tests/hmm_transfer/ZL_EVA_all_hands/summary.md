# ZL_EVA_all_hands hidden-state transfer

Hypothesis: adapting emissions while holding a pooled transition kernel predicts held-out within-group sequences better than a fully frozen model. Four/five exchangeable hidden states, two pooled restarts selected on validation, cap 200 groups/document, 30 EM steps. Groups restart the HMM; this is not a physical-line accumulator.

Seed: 20261005. Exact source paths and SHA-256 digests: `input_manifest.json`. Inclusion, exclusions, model settings and null definitions: `config.json`.

Visual source groups and prototype categories are provisional. Unknown assignments are excluded without renumbering original physical/rank slots. Caption/document resampling is not a verified physical-bifolio independence proof. Post-exposure repairs are diagnostic, not newly blind. Multiple exploratory endpoints are dependent.

| States | Context | Adaptation | Excess held-out bits/unit | Document bootstrap 95% interval |
|---:|---|---|---:|---|
| 4 | B | frozen_both | 0.000000 | [0.0, 0.0] |
| 4 | B | fixed_transitions | -0.049178 | [-0.07955591041314403, -0.031701313097010964] |
| 4 | B | fixed_emissions | -0.008946 | [-0.021356067498699893, 0.006038069371686827] |
| 4 | B | adapt_both | -0.059793 | [-0.09285115455173674, -0.012762778480330805] |
| 4 | H | frozen_both | 0.000000 | [0.0, 0.0] |
| 4 | H | fixed_transitions | -0.022003 | [-0.043398047401435935, 0.01942302039909949] |
| 4 | H | fixed_emissions | -0.006347 | [-0.012834338705187687, 0.001029516089698923] |
| 4 | H | adapt_both | -0.029417 | [-0.05560576141979601, 0.01628076847162907] |
| 5 | B | frozen_both | 0.000000 | [0.0, 0.0] |
| 5 | B | fixed_transitions | -0.034109 | [-0.05622754488885384, -0.01920835303679318] |
| 5 | B | fixed_emissions | -0.009882 | [-0.025255767458745915, -0.0010744899308812172] |
| 5 | B | adapt_both | -0.048298 | [-0.10439430594078702, -0.0178452594073768] |
| 5 | H | frozen_both | 0.000000 | [0.0, 0.0] |
| 5 | H | fixed_transitions | -0.017953 | [-0.03829839702508364, 0.007287097822471722] |
| 5 | H | fixed_emissions | -0.005069 | [-0.006921257046168083, -0.003351504512648873] |
| 5 | H | adapt_both | -0.020209 | [-0.04966193662480256, 0.004580129169401648] |

Negative excess bits favor adaptation. Frozen-both, fixed-emission, fixed-transition and joint-adaptation models are competing transfer baselines; no random-label HMM refit null was run. Bootstrap 1,000 document blocks. Convergence warnings and likelihood changes are preserved; EM states are not uniquely identified or decoded symbols.

Latin compares Cicero works; Finnish b/w are source partitions, not verified semantic genres. The all-hand Voynich sensitivity confounds hand/section. Ordinary-language gains show why this pattern cannot uniquely identify a shared computational runtime. Failure: fewer than four train or two test documents/context, incomplete visual groups, or unstable optimization. Prior art: standardized ledger 14 analogue; no exact unpublished historical replication or novelty claim.
