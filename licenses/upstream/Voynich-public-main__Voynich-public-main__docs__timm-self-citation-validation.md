# Timm–Schinner self-citation validation — Issue #98

## 結論

Timm–Schinnerの中心的な弱い命題、すなわち**同じpageの既出語形をsourceにする局所edit channelには、global training-reservoir editを越える予測情報がある**ことを支持する。

ただし公開Java生成器そのものはrejection、forced suggestion、Voynich固有validity rule、実在初期行を含み、normalized `log_prob`を提供しない。従って、公開生成器が歴史的制作法だった、本文が無意味だった、という強い結論は採用しない。

```text
local page-conditioned form memory     supported
literal visual self-copying             not identified
public full generator as normalized C   not accepted
meaningless-text conclusion             not implied
```

## 外部実装の固定と再現

- Repository: `TorstenTimm/SelfCitationTextgenerator`
- Commit: `a6ede2202dd7ad6285ce2c007bf22c2a0e7709b7`
- License: MIT
- Runtime: Eclipse Temurin JRE 17.0.20+8、temporary local extraction
- Default seed: 19
- 配布sample SHA-256: `1e954a17b157e83f04ea21353ba877f70084b828b812fab3944347ac2888dc11`
- 再実行sample SHA-256: 同一。Bit-identical reproduction。

公開実装は前page linesからsourceを選び、same-position preference 28%、add/remove 20%、combine/split 30%、replace 50%、immediate reuse 10%、`-in/-ol/-dy`不足時suggestion等を用いる。これは単純one-glyph channelより広い。

## 正規化した中心仮説

完全なJava control flowはtractable likelihoodを公開していないため、中心予測だけをnormalized prequential adapterとして固定した。

```text
source = target pageの観測済みprevious linesのみ
parent choice = page occurrence + fixed 28% same-position preference
operation = training-only insert/delete/substitute weights
future line/current line token = source候補にしない
global one-glyph channel = frozen competitor
```

Outer splitはphysical bifolio。H discovery、C/F replication、clean/strict、sealed quire Eで同じ仕様を用いた。Mixtureはinner bifolio devだけで選択し、source-choiceとgrid costをMDLへ課した。

## Held-out result

Global exemplar editを保持した上でlocal page channelを追加したtotal-MDL gain:

| track | bifolio CV bits/token | positive folds | sealed E bits/token |
|---|---:|---:|---:|
| H clean | +0.00785 | 4/5 | -0.00067 |
| H strict | +0.01446 | 5/5 | +0.00127 |
| C clean | +0.00656 | 4/5 | +0.00804 |
| C strict | +0.01229 | 4/5 | +0.01298 |
| F clean | +0.01139 | 4/5 | +0.00601 |
| F strict | +0.01410 | 5/5 | +0.00236 |

Pooled CVは131,434 tokenで+0.01128 bits/token、26/30 folds正。Sealed pooledは8,515 tokenで+0.00492、5/6 track正。効果はcompact global editの+0.59〜+0.72より小さいが、安定した追加成分である。

## Matched-donor guard

局所channelが単なる任意の小標本adaptationである可能性に対し、domain、Currier、page line countをmetadata/layoutだけで近似した別physical-bifolio pageの同じline ordinalまでのprefixをdonorにした。

- True page history − matched other-page history: pooled CV +0.02228 bits/token。
- 28/30 CV folds正。
- Sealed pooled +0.02133、6/6 track正。

従って、任意のmatched pageではなく**正しいpageの既出form identity**が必要である。ただしpage content/stateが継続するだけでもこの差は生じるため、literal eye-copyingの同定ではない。

## 公開sampleのjoint diagnostic

Default public sampleはexact adjacent repeat 0.01017でobserved H 0.01006に近く、mean top2 shareも0.2972 vs 0.3030だった。一方:

- one-edit adjacency: 0.04921 vs observed 0.03551（過大）
- ABA/line: 0.10417 vs 0.06400（過大）
- unique fraction: 0.95103 vs 0.96883（低い）

一つの固定sampleによる記述比較でありp-valueではないが、公開default generatorを十分なjoint generatorとして受理する根拠にはならない。Strong Cと同様、複数統計の同時再現は未達である。

## Verdict

Timm–Schinner研究は単なる下位互換ではなかった。既存のglobal one-glyph channelが見落としていた**page-local source scope**を予測可能な形で追加した。この弱いmechanismはcommon surface generatorへ昇格候補とする。

しかし、Timmの完全なhistorical Cを支持するには、公開full processのnormalized scoring、new sealed challenge、physical-distance/source-direction nullが必要。現在の結論は`local self-citation-compatible memory supported`であり、`meaningless self-citation manuscript established`ではない。
