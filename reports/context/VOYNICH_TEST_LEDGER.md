# Voynich Investigation — Test Ledger and Reproduction Record

## Purpose

This document records the empirical tests performed during the Voynich investigation so that GPT-6.1 Sol / Codex can distinguish:

- what was actually tested,
- what the test was intended to show,
- which datasets were used,
- what numerical results were reported,
- what robustness attacks were tried,
- which findings weakened or failed,
- and which results currently exist **only as conversation-reported outputs rather than saved scripts/results**.

This is not a decipherment claim and not a polished paper.

It is a **reproduction ledger**.

---

# Status Key

Each test is marked with one of the following:

- **RECONSTRUCTED / HIGH DETAIL** — methodology and numerical result are sufficiently documented to reproduce closely.
- **REPORTED / NEEDS RE-RUN** — numerical result was produced during the investigation but no dedicated script/output artifact was saved; Codex should reproduce it.
- **EXPLORATORY** — useful directional result, but not strong enough to carry as a finding until reproduced and formalized.
- **FAILED / WEAKENED** — the result did not survive robustness testing or was explained by controls.
- **PRIOR ART COLLISION** — concept/result was subsequently found in earlier work.

Where a value is approximate, it is written with `~` or "about".

---

# 1. Core Data Sources Used

## Voynich

### ZL3b / EVA-family transcription

Filename used:

`httpswww.voynich.nudataZL3b-(1).txt`

Key metadata fields in page headers:

- `$L` = Currier language A/B
- `$I` = illustration / section class
- `$H` = attributed hand
- other metadata also present

Conservative parsing in the reconstructed assay produced approximately:

- 37,597 running tokens
- 7,455 unique forms
- Currier B: 23,388 tokens
- Currier A: 11,089 tokens
- unlabeled / other: ~3,120

These numbers should be recomputed rather than trusted blindly.

### RF / Reference transcription

Filename:

`httpsvoynich-nudataRF1b-e.txt`

Used as an independent/reference transcription with EVA-style notation.

### v101 / Glen Claston transcription

Filename:

`httpsvoynich.nudataGC2a-n.txt`

Used specifically because it makes substantially different assumptions about glyph identity and segmentation.

---

## Natural-language controls

Archives used:

- `UD_Finnish-TDT-master.zip`
- `UD_Turkish-IMST-master.zip`
- `UD_Latin-PROIEL-master.zip`

Control corpora:

- Finnish TDT
- Turkish IMST
- Latin PROIEL

These were used as morphology/position controls, especially for the edge-vs-interior assay and later additive-substitution tests.

---

# 2. Minimal-Pair Edge vs Interior Assay

**Status: RECONSTRUCTED / HIGH DETAIL**

## Research question

Do nearly identical Voynich forms behave differently depending on whether their one-character difference occurs near the edge of the token or in the interior?

The original motivating pattern was:

- edge mutation -> greater physical-line-position displacement
- interior mutation -> greater thematic/section displacement

This test was reconstructed from earlier chat records and rerun on ZL3b.

---

## Pair construction

Within each Currier language separately:

1. restrict vocabulary by minimum token frequency
2. take same-length token forms
3. retain pairs differing at exactly one character
4. identify the single edit index
5. classify the edit by distance from the nearest token boundary

Primary reconstructed definition:

- **edge width = 2**
- edit is "edge" if it occurs within the first two or last two characters
- deeper edits are "interior"

A one-character edge definition was also tested as sensitivity.

---

## Physical line position

For a line with `n` tokens and token index `i`:

`normalized_position = i / (n - 1)`

Single-token lines were assigned 0.5.

For each token form, compute mean normalized physical line position.

For a minimal pair:

`position_displacement = abs(mean_pos(form1) - mean_pos(form2))`

---

## Thematic / section displacement

For each token form, construct its distribution over `$I` section classes.

Distances tested included:

- total variation
- Jensen-Shannon divergence
- square-root JS distance
- Hellinger distance
- additional sensitivity metrics in exploratory passes

Primary regression controls:

- edge indicator
- token length
- log geometric mean pair frequency:

`logf = log(sqrt(freq1 * freq2))`

HC3 heteroskedasticity-robust OLS was used in the basic reconstruction.

Connected minimal-pair graph / family dependence was also explored separately.

---

## Primary reconstruction: minimum frequency 8, edge width 2

### Currier A

268 minimal pairs.

Physical position:

`edge beta ≈ +0.06374`
`p ≈ 0.000765`

Thematic displacement:

- TV beta ≈ +0.0144, not significant
- JSD beta ≈ +0.0028, not significant
- Hellinger beta ≈ +0.0064, not significant

Interpretation:

Currier A reproduced the earlier reported positional coefficient near `+0.066`, but did not show a stable thematic edge/interior effect.

### Currier B

664 minimal pairs.

Physical position:

`edge beta ≈ +0.03234`
`p ≈ 0.00253`

Thematic displacement:

- TV beta ≈ `-0.0453`, p≈0.0655
- JSD beta ≈ `-0.0528`, p≈0.00568
- sqrt-JS beta ≈ `-0.0500`, p≈0.0272
- Hellinger beta ≈ `-0.0523`, p≈0.0160

Interpretation:

This closely reproduced the older reported Currier-B pattern:

- edge change -> more positional displacement
- edge change -> less thematic displacement than interior change

The exact original thematic metric from the older session was not fully documented.

---

# 3. Frequency Threshold Sensitivity

**Status: RECONSTRUCTED / HIGH DETAIL**

Edge width 2.

## Minimum frequency 5

Currier B:

- position beta ≈ `+0.03443`
- p≈`9.1e-5`
- TV thematic beta ≈ `-0.06097`
- p≈`0.0021`

This matched the old positional magnitude extremely closely.

## Minimum frequency 10

Currier A:

- position beta ≈ `+0.06291`
- p≈`0.0023`

Currier B:

- position beta ≈ `+0.02820`
- p≈`0.0177`
- Hellinger thematic beta ≈ `-0.06147`
- p≈`0.01894`

The thematic p-value here was close to the earlier reported ~0.019.

---

# 4. Edge-Width Sensitivity

**Status: RECONSTRUCTED / HIGH DETAIL**

At minimum frequency 8:

## One-character edge

Currier A:

- position ≈ `+0.0219`
- not significant
- thematic displacement showed a stronger negative effect

Currier B:

- position ≈ `+0.0572`
- highly significant
- thematic effect near zero / not significant

## Two-character edge

Currier A:

- position ≈ `+0.0637`
- significant
- thematic effect absent

Currier B:

- position ≈ `+0.0323`
- significant
- thematic effect negative

Important conclusion:

> The originally described crossed A/B fingerprint was **not invariant to the exact edge definition**.

This is a caveat, not a failure of the broader positional effect.

---

# 5. Mutation-Depth Analysis

**Status: RECONSTRUCTED / HIGH DETAIL**

Instead of binary edge/interior, edits were grouped by depth from the nearest boundary:

- `outer`: depth 0
- `near`: depth 1
- `interior`: depth >=2

Minimum frequency 8.

## Currier A

Approximate group means:

### Interior
- n=15
- position displacement ≈ 0.0714
- TV ≈ 0.1896
- Hellinger ≈ 0.2433

### Near
- n=78
- position ≈ 0.1286
- TV ≈ 0.2365
- Hellinger ≈ 0.2727

### Outer
- n=175
- position ≈ 0.1358
- TV ≈ 0.1484
- Hellinger ≈ 0.2108

Adjusted relative to interior:

- near positional beta ≈ `+0.05636`, p≈0.00394
- outer positional beta ≈ `+0.07190`, p≈0.000692
- thematic Hellinger effects not stable

## Currier B

### Interior
- n=70
- position ≈ 0.0877
- TV ≈ 0.3523
- Hellinger ≈ 0.3804

### Near
- n=186
- position ≈ 0.0978
- TV ≈ 0.3076
- Hellinger ≈ 0.3131

### Outer
- n=408
- position ≈ 0.1608
- TV ≈ 0.3151
- Hellinger ≈ 0.3356

Adjusted relative to interior:

- near position ≈ `+0.0030`, p≈0.772
- outer position ≈ `+0.05961`, p≈1e-6
- near Hellinger ≈ `-0.06288`, p≈0.00484
- outer Hellinger ≈ `-0.04250`, p≈0.05895

Interpretation:

Currier B's **outermost** changes were the clearest positional effect.

The second-in layer showed stronger thematic reduction without a comparable position shift.

This result was one reason to stop treating "edge" as a monolithic concept.

---

# 6. Connected-Family Dependence / Bootstrap

**Status: RECONSTRUCTED BUT UNRESOLVED**

Minimal-pair observations are dependent because one token form can participate in many pairs.

A graph was constructed:

- nodes = token forms
- edges = one-character minimal-pair relations
- connected components = candidate "families"

A simple family-resampling bootstrap did **not** reproduce every older claim.

Example, minimum frequency 5, edge width 2:

Currier B:

- position beta ≈ `+0.0344`
- bootstrap 95% interval approximately `[-0.0000, +0.0679]`
- two-sided p approximately 0.05

Currier B thematic TV:

- beta ≈ `-0.0610`
- interval approximately `[-0.111, -0.010]`
- p≈0.016

Currier A positional effect crossed zero in that implementation.

Cluster-robust component SE at minimum frequency 8 also widened Currier-B uncertainty strongly.

Conclusion:

> The exact family-bootstrap implementation from the earlier session was not recovered.

Codex should not claim that the old family-bootstrap result was replicated until it reproduces a principled dependence-aware analysis.

---

# 7. Natural-Language Control: Edge vs Interior

**Status: REPORTED / NEEDS RE-RUN**

The exact Voynich-style assay was applied to Finnish TDT, Turkish IMST, and Latin PROIEL using sentence-normalized word position as the structural analogue.

Reported approximate results:

| Corpus | Edge edit -> position | Edge edit -> thematic/context |
|---|---:|---:|
| Voynich A | +0.064 | ~0 |
| Voynich B | +0.032 | ~-0.04 to -0.05 |
| Finnish | +0.006 | ~-0.065 |
| Turkish | ~-0.001 | ~-0.052, uncertain |
| Latin | ~-0.011 | ~-0.106 |

Interpretation reported in-chat:

- the **interior/content** effect was reproduced well by natural languages, especially Finnish and Latin
- the **edge/position** effect was not reproduced in those controls

This was a key reason the thematic interpretation was downgraded while the physical-position effect became the main clue.

Important:

These control results should be rerun from the supplied UD corpora and saved properly.

---

# 8. Same-Hand / Same-Currier Section Discrimination

**Status: REPORTED / NEEDS RE-RUN**

Question:

Can section/domain differences be detected even when attributed hand and Currier regime are held constant?

Reported same-hand comparisons:

- Hand 1 / Currier A: Herbal vs Pharmaceutical
- Hand 2 / Currier B: Herbal vs Biological / Cosmological
- Hand 3 / Currier B: Pharmaceutical vs Stars/Recipes

Reported character-pattern discrimination:

| Comparison | Approx AUC |
|---|---:|
| Hand 1 Herbal vs Pharmaceutical | ~0.76 |
| Hand 2 Herbal vs Biological | ~0.78 |
| Hand 2 Herbal vs Cosmological | ~0.67 |
| Hand 3 Pharmaceutical vs Stars/Recipes | ~0.71 |

Same subject / same Currier / different hand example:

- Herbal B, Hand 2 vs Hand 5: AUC ~0.62

Interpretation:

In these comparisons, changing section under the same hand often changed morphology more than changing hand within the same section.

This supports section/domain effects but does not prove distinct "algorithms."

Re-run required.

---

# 9. Repeated `ee` / `eee` Distribution by Section

**Status: REPORTED / NEEDS RE-RUN**

A section-frequency check was performed on ZL3b.

Reported fraction of tokens containing `ee`:

| Section | `ee`-bearing tokens |
|---|---:|
| Astronomical | ~18.6% |
| Zodiac | ~18.6% |
| Stars/Q20 B | ~18.4% |
| Biological | ~13.4% |
| Pharmaceutical | ~12.6% |
| Herbal B | ~8.6% |
| Herbal A | ~5.4% |

Reported `eee` pattern:

- astronomical/zodiac ~2.3%
- Stars-B ~1.7%
- Herbal material ~0.6–0.8%

Interpretation:

Repeated `e`-like sequences are strongly section-conditioned.

However, literal "EVA vowels as a special compression class" was later weakened.

Re-run required.

---

# 10. EVA "Vowel" Compression Test

**Status: FAILED / WEAKENED; REPORTED**

Literal set tested:

`a e i o y`

(`u` is extremely rare in ZL3b)

Reported observations:

- these letters make up ~47% of the cleaned character stream
- removing them from common forms collapsed many forms onto shared skeletons
- however, random five-character sets with similar frequency often produced comparable collapse
- EVA-vowel set sat only around the ~65th percentile in raw compression

Reported conclusion:

> "Remove EVA vowels and a hidden compressed vocabulary appears" was not supported as a special effect.

The broader idea of heterogeneous glyph families remained open.

---

# 11. Same-Core / Section-Conditioned Wrapper Test

**Status: REPORTED / NEEDS RE-RUN**

Question:

Holding an internal token core fixed, do different sections use systematically different edge realizations under the same attributed hand and Currier regime?

Example reported for Hand 2, Currier B, Herbal vs Biological:

- observed wrapper displacement ≈ 0.517
- permutation expectation ≈ 0.390
- excess ≈ +0.127
- p≈0.003

However, a Cicero control (Letters to Atticus vs De officiis) produced a similar excess:

- ~+0.132
- p≈0.003

Conclusion:

> Same-core / different-wrapper by topic is **not diagnostic** of a special Voynich compression system.

Ordinary morphology/genre can reproduce it.

---

# 12. Blind Section Clustering / Abstract Construction Shape

**Status: EXPLORATORY / NEEDS RE-RUN**

Tokens were abstracted to repetition/construction shapes, e.g. conceptually:

`qokeedy -> ABCDDEF`

The exact glyph identities were discarded.

Initial clustering showed striking section separation, but page-length imbalance was identified as a confound.

After equalizing pages to a fixed token budget, some same-hand section signal remained.

Reported approximate equal-budget abstract-shape ARI:

- Hand 1 A, Herbal vs Pharmaceutical: ~0.20
- Hand 2 B, Herbal vs Biological: ~0.25
- Hand 3 B, Herbal vs Stars: ~0.00

Reported significance frequency over repeated equal-budget samples:

- Hand 1: ~90% significant section association
- Hand 2: ~85%

Interpretation:

Some section differences survive glyph-identity removal, but this is exploratory and must be rerun.

---

# 13. Full / Edge / Core / Abstract Shape Section Separation

**Status: REPORTED / NEEDS RE-RUN**

For Hand 2 Currier B, Herbal vs Biological, under an equalized token budget:

Reported mean blind ARI:

| Representation | Mean ARI |
|---|---:|
| full token morphology | ~0.929 |
| first/last two characters only | ~0.756 |
| internal core only | ~0.457 |
| abstract construction shape | ~0.257 |

A Cicero same-author cross-genre control was reported much lower:

| Representation | Cicero ARI |
|---|---:|
| full morphology | ~0.274 |
| edges | ~0.193 |
| core | ~0.041 |
| abstract shape | ~0.022 |

Interpretation:

Hand-2 Currier-B section separation was unusually strong, but this is not yet a uniqueness proof and needs reproduction.

---

# 14. Shared-Runtime / Different-Library Sequence Model

**Status: REPORTED / NEEDS RE-RUN**

A small hidden-state sequence model was used as a programming/DSL analogy.

Question:

When transferring from one section to another under the same hand/Currier regime, is it better to:

- keep transition grammar fixed and change symbol emissions ("library")
- keep symbol emissions fixed and change transitions ("grammar")
- refit both
- change neither

Reported held-out bits/unit:

| Transfer | Full refit | grammar fixed, library changes | library fixed, grammar changes | nothing changes |
|---|---:|---:|---:|---:|
| Hand 1 A Herbal -> Pharma | 3.114 | 3.225 | 3.235 | 3.330 |
| Hand 2 B Herbal -> Biological | 3.308 | 3.328 | 3.448 | 3.473 |
| Hand 3 B Herbal -> Stars | 3.401 | 3.415 | 3.500 | 3.533 |
| Cicero letters -> De officiis | 3.592 | 3.672 | 3.676 | 3.706 |

Reported interpretation:

- Hand 1 looked relatively symmetric, similar to ordinary genre shift
- Hand 2 and Hand 3 showed stronger "same runtime / different library" behavior
- model-order sensitivity existed
- a 5-state fit weakened the asymmetry
- therefore "four hidden states" is not a finding

This idea also collided with related prior work in the Yoshida repository (`shared-transition-validation.md`) and broader shared-grammar literature.

Treat as independent replication / extension at best.

---

# 15. Inferred Recurrent Unit Inventory

**Status: EXPLORATORY / NEEDS RE-RUN**

A simple type-weighted compression / recurrent-substring pass reportedly recovered frequent pieces such as:

- `ch`
- `ee`
- `ol`
- `sh`
- `ai`
- `dy`
- `che`
- `al`
- `ok`
- `ar`
- `or`
- `ot`
- `aiin`

Reported overlap:

~91–100% of the common inferred unit inventory was shared across Herbal, Biological, Pharmaceutical, and Stars, while frequencies changed substantially.

Example reported frequencies:

- `ch`: Herbal ~9.1%, Biological ~2.5%
- `dy`: Herbal ~4.2%, Biological ~9.9%
- `ee`: Herbal ~2.1%, Stars ~5.6%
- `ol`: Herbal ~4.8%, Pharmaceutical ~8.4%

Interpretation:

More consistent with a shared tool/instruction inventory whose usage shifts by section than with entirely separate alphabets.

This must be rerun and should not be treated as a canonical unit inventory.

---

# 16. Mixed-Script / Alternate-Rendering Context Test

**Status: REPORTED / NEEDS RE-RUN**

Hypothesis:

If two glyph families are alternate renderings of the same underlying value/script role, they should be locally interchangeable while their section usage swaps.

Reported context-similar pairs:

- `iin <-> in`: context distance ~0.049
- `k <-> t`: ~0.140
- `ch <-> sh`: ~0.150
- `f <-> p`: ~0.155
- `e <-> ee`: ~0.255

Reported section-frequency correlations were strongly positive:

- `iin/in`: r~0.76
- `k/t`: r~0.96
- `ch/sh`: r~0.94
- `f/p`: r~0.85
- `e/ee`: r~0.96

Conclusion:

No strong evidence was found for two equivalent alphabets/scripts swapping by section.

Broader heterogeneous functional classes remained plausible.

---

# 17. Grapheme-Segmentation Stress Test Inside EVA

**Status: REPORTED / HIGH PRIORITY RE-RUN**

Likely compounds collapsed into atomic units, including a conservative set such as:

- `cth`
- `ckh`
- `cph`
- `cfh`
- `ch`
- `sh`
- `iin`
- `in`
- `ee`

Reported effect:

Currier B edge -> line-position remained about:

`+0.040`, p≈0.00024

while the old interior/thematic effect shrank to roughly:

`-0.013 to -0.015`, nonsignificant

Later segmentation comparisons were summarized as:

| Representation | Currier A edge->position | Currier B edge->position |
|---|---:|---:|
| raw EVA | +0.055, p~0.0049 | +0.0385, p~0.00029 |
| conservative compounds | +0.0268, p~0.125 | +0.0344, p~0.00099 |
| compounds + `ee` atomic | +0.0262, p~0.148 | +0.0329, p~0.0018 |

Interpretation:

- Currier A positional effect is much more segmentation-sensitive
- Currier B positional effect is comparatively robust
- thematic/interior result is segmentation-sensitive

This was the direct motivation for the ground-up manuscript-first restart.

---

# 18. Cross-Transcription Positional Replication: ZL / RF / v101

**Status: REPORTED / VERY HIGH PRIORITY RE-RUN**

The same minimal-pair positional assay was rerun independently within:

- ZL3b/EVA
- RF/Reference
- v101

A methodological correction was introduced:

With a two-unit edge definition, forms shorter than 5 units cannot contain a true interior position, so the stricter version retained only token lengths >=5.

Reported Currier-B results at minimum frequency ~8:

| Transcription | edge -> position |
|---|---:|
| ZL3b | +0.0438, p~5.1e-5 |
| RF | +0.0472, p~5.5e-6 |
| v101 | +0.0285, p~0.0125 |

Using only the outermost unit as "edge":

v101 Currier B reportedly gave:

`+0.0640`, p≈`8e-5`

Leave-one-folio-out:

- ZL: all 83 deletion estimates positive
- RF: all 83 positive
- v101: all 83 positive
- ~80/83 v101 deletion fits individually p<0.05

Reported ranges:

RF:
`+0.0426 -> +0.0535`

ZL:
`+0.0398 -> +0.0504`

v101:
`+0.0209 -> +0.0325`

Interpretation:

Currier-B edge/line-position coupling survived substantially different transcription/segmentation assumptions.

This is one of the most important results to reproduce and save properly.

---

# 19. Signed Directional Edge-Substitution Graph

**Status: REPORTED / VERY HIGH PRIORITY RE-RUN**

Instead of absolute displacement, the test estimated signed positional displacement for a particular edge substitution.

For otherwise-matched forms:

`A + core`
`B + core`

define:

`delta(A->B) = mean_position(B+core) - mean_position(A+core)`

Positive = B tends farther right.

The symbol correspondence between RF/ZL and v101 was reportedly built from aligned physical token positions **without using line position**.

At minimum occurrence ~5:

25 comparable substitution relations were reportedly available between RF and v101.

Reported agreement:

RF vs v101:

- Pearson r ~0.915
- Spearman rho ~0.887
- 84% same direction
- sign-flip null p~0.00033

ZL vs v101:

- Pearson r ~0.929
- Spearman rho ~0.882
- 88% same direction
- p~0.00033

At a stricter threshold ~8:

- RF/v101 r ~0.944
- ZL/v101 r ~0.950
- only ~11 well-supported relations

Interpretation:

Not only the existence of positional displacement but the **direction of specific edge substitutions** survived incompatible transcription schemes.

Prior-art note:

Patrick Feaster's "Rightward and Downward" work already studied directional minimal-pair effects. Therefore the basic concept is **not novel**.

The cross-transcription graph replication may still be a methodological extension.

---

# 20. Independent Folio-Split Reproducibility of Directional Graph

**Status: REPORTED / VERY HIGH PRIORITY RE-RUN**

Currier-B folios were repeatedly split into independent halves.

The directional substitution graph was estimated separately in each half.

Reported over ~30–60 splits:

- ~36–37 comparable substitutions per split
- median Pearson r ~0.79 to 0.80
- median Spearman ~0.70 to 0.76
- median same-direction agreement ~77.8%

Reported whole-folio splitting still gave ~0.80 correlation.

Interpretation:

The directional system was not merely the same physical text echoing through two transcriptions.

---

# 21. Within-Line Shuffle Null

**Status: REPORTED / VERY HIGH PRIORITY RE-RUN**

Null:

Shuffle tokens within every physical line while preserving:

- token vocabulary
- frequencies
- line membership
- line lengths
- morphology/family structure

This destroys only physical horizontal placement.

Reported effect:

Real manuscript:

- median directional r ~0.785
- median same-direction ~77.8%

Within-line shuffle:

- median r ~-0.13
- same-direction ~49.9%

Later summarized shuffle runs produced roughly:

- r ~0.13–0.27 in some implementations
- direction agreement ~54–59%

The precise null implementation should be standardized during reproduction.

Main conclusion:

The directional graph depends strongly on actual physical ordering.

---

# 22. Directional Graph Natural-Language Controls

**Status: REPORTED / NEEDS RE-RUN**

At approximately Voynich-sized sample budgets, the strict graph was much denser in Voynich than natural controls.

Reported approximate relation counts:

| Corpus | left relations | right relations | triangles |
|---|---:|---:|---:|
| Voynich Currier B | 34 | 12 | 60 left / 6 right |
| Finnish | 1 | 3 | 0 |
| Latin | 0 | 7 | 1 |
| Turkish | 0 | 0 | 0 |

With full corpora:

Finnish right edge reportedly showed:

- held-out path prediction r ~0.61
- ~77% correct direction

Latin left edge:

- r ~0.36
- ~65% direction agreement

Turkish remained too sparse.

Conclusion:

Additive/ordered morphology is **not unique** to Voynich.

Voynich appears unusually dense and bilateral in this crude assay, but broader controls are needed.

---

# 23. Triangle Closure / Additive Positional Potential

**Status: REPORTED / VERY HIGH PRIORITY RE-RUN**

For edge substitutions, test:

`delta(A->B) + delta(B->C) ~= delta(A->C)`

Reported Currier-B left-edge results:

## ZL

- 60 closed triangles
- mean closure error ~0.070
- sign-randomization null ~0.28
- p<0.001

## RF

- 11 triangles
- error ~0.052
- null ~0.24
- p<0.001

## v101

- 3 well-supported triangles
- error ~0.029
- null ~0.31
- p~0.017

Example reportedly observed:

`l -> o ~ -0.038`
`o -> y ~ -0.148`

predicted:

`l -> y ~ -0.186`

observed:

`l -> y ~ -0.201`

error ~0.015

Another example:

`d -> k ~ +0.213`
`k -> r ~ +0.177`

predicted:

`d -> r ~ +0.390`

observed:

`+0.385`

error ~0.005

Interpretation:

Currier-B left-edge substitutions can be approximated by an additive scalar potential.

However ordinary morphology can also show partial additivity.

Do not interpret as numbers/equations without independent evidence.

---

# 24. Held-Out Alternate-Path Prediction

**Status: REPORTED / VERY HIGH PRIORITY RE-RUN**

Harder test:

1. split folios into training/test
2. choose target substitution A->C
3. remove the direct A->C edge from the training graph
4. predict A->C only from alternate graph paths, e.g. A->B->C
5. compare with the independently measured A->C effect on held-out folios

Reported median results:

| Transcription | left-edge held-out r | direction correct |
|---|---:|---:|
| ZL | ~0.83 | ~85–86% |
| RF | ~0.82 | ~80% |
| v101 | ~0.72 | ~77% |

Right edges were also above chance but weaker / sparser.

Interpretation:

A low-dimensional ordering/potential explains a substantial part of unseen edge-substitution positional effects.

---

# 25. Section Stability of Left-Edge Ordering

**Status: REPORTED / NEEDS RE-RUN**

Reported cross-section agreement in Currier B:

- Biological vs Herbal: r~0.83, ~90% same direction
- Biological vs Stars/Recipes: r~0.93, ~84%
- Herbal vs Stars/Recipes: r~0.83, ~82%

Same Hand-2 Herbal vs Biological:

- r~0.68
- ~73% same direction

Interpretation:

The left-edge ordering may sit beneath section-specific morphology rather than being redefined by each section.

Needs formal reproduction.

---

# 26. Right Edge vs Left Edge

**Status: REPORTED / NEEDS RE-RUN**

Reported observation:

The right-edge scalar ordering correlates extremely strongly with the simple global positional preference of the right-edge glyph itself:

- RF r~0.98
- v101 r~0.99

Therefore much of the right-edge "algebra" may reduce to ordinary suffix-like positional preference.

Left edge was less trivially explained:

- correlation with simple global initial-symbol position ~0.54–0.68 depending on transcription

Current restrained status:

- **Currier-B left edge**: stronger candidate for nontrivial ordered positional structure
- **right edge**: real positional structure but more likely reducible to ordinary global positional preference

---

# 27. Running-State / Accumulator Test

**Status: FAILED / WEAKENED**

Question:

If the inferred edge ordering behaves like a cumulative differential state, does the state of the current token meaningfully predict the state of the next token after controlling physical position?

Reported held-out result:

- partial correlation ~0.06
- added predictive variance ~0.4%

Conclusion:

A strong running accumulator / executable state-machine interpretation was **not supported**.

This does not rule out all formal notation models; it rejects a simple strong serial-state version.

---

# 28. Prior-Art Collisions Identified

**Status: PRIOR ART COLLISION**

## Patrick Feaster

Directional minimal-pair / "rightwardness" work predates this investigation.

Feaster also speculated about a cumulative differential cipher / numerical state mechanism.

Therefore:

- directional minimal-pair positional effects are not novel
- cumulative-state interpretation is not novel as a speculative idea

Potentially less-explored extension:

- full substitution graph
- triangle closure
- held-out alternate-path prediction
- cross-transcription graph replication

These still require deeper prior-art checking before novelty language.

## Stolfi

Formal/finite word grammar is established prior work.

## Currier

A/B statistical regimes and possible subject-matter effects are established.

## Davis

Multiple hand classifications are established palaeographic work, though authorship interpretation remains debated.

## Yoshida / related current work

Shared transition grammar / domain-conditioned morphology / positional realization overlap substantially with the "same runtime, different libraries" analogy.

Do not frame that analogy as a new theory.

---

# 29. Most Important Reproduction Priorities for Sol

The following should be rerun first and saved as scripts + machine-readable outputs.

## Priority 1

**Cross-transcription Currier-B edge-vs-interior positional assay**

Datasets:

- ZL3b
- RF
- v101

Save:

- parser
- pair table
- regression table
- threshold sweep
- leave-one-folio-out outputs

## Priority 2

**Signed directional edge-substitution graph**

Save:

- substitution tables
- support counts
- cross-transcription symbol mapping procedure
- folio-split reproducibility
- sign-flip/null tests

## Priority 3

**Within-line shuffle null**

Standardize null procedure and rerun enough iterations for stable intervals.

## Priority 4

**Triangle closure and held-out alternate-path prediction**

Save:

- graph for each transcription
- all triangles
- direct-edge removal logic
- path-selection rule
- train/test split seeds
- held-out predictions

## Priority 5

**Natural-language controls**

Re-run:

- Finnish TDT
- Turkish IMST
- Latin PROIEL

using exactly the same graph/pair definitions where feasible.

## Priority 6

Only after the ground-up visual segmentation is frozen:

**repeat Priorities 1–4 under manuscript-derived units**

This is the decisive test of whether the positional phenomenon belongs to the manuscript or to inherited transcription conventions.

---

# 30. Required Reproduction Artifacts Going Forward

Every empirical test should generate:

```text
tests/<test_name>/
  README.md
  run.py
  config.json
  input_manifest.json
  results.csv
  summary.md
  figures/
```

`summary.md` should state:

- hypothesis
- exact data
- inclusion/exclusion rules
- seed
- model/statistic
- null
- effect size
- uncertainty
- failure conditions
- interpretation
- prior-art status

Do not leave future tests only in chat prose.

---

# 31. Bottom Line

The current investigation should not be summarized as "we deciphered the Voynich Manuscript."

The strongest empirical thread to reproduce is:

> **Currier-B token-boundary variation is unusually and reproducibly associated with physical horizontal line position, and specific left-edge substitutions appear to form a stable, approximately additive positional ordering that survives folio splits and alternative transcription systems.**

Important cautions:

- ordinary morphology can reproduce parts of this behavior
- the exact grapheme units remain uncertain
- some earlier thematic/interior effects were segmentation-sensitive
- the positional scalar is not known to be numerical, semantic, or computational
- no plaintext meanings have been recovered
- prior work already established related positional minimal-pair phenomena

The new manuscript-first project exists to determine whether this structural signal survives after the writing units are inferred from the physical script itself rather than inherited from EVA/v101.
