# Voynich Manuscript — Ground-Up Script Investigation Handoff

## Purpose

This document hands the Voynich investigation to GPT-6.1 Sol / Codex for a **ground-up reconstruction of the manuscript's writing units from the physical manuscript images**.

The central methodological change is deliberate:

> **The manuscript imagery is primary evidence. EVA, ZL3b, RF/Reference, v101, Currier labels, hand labels, and prior analytical models are comparison data — not ground truth for what constitutes a character, glyph, token, word, prefix, suffix, or language unit.**

The immediate objective is **not decipherment**.

The objective is to determine, as conservatively and reproducibly as possible:

1. What physical marks and recurring stroke assemblies the writer(s) actually made.
2. Which visible assemblies behave like reusable units.
3. Which apparent units may instead be allographs, ligatures, frames, insertions, modifiers, or compound constructions.
4. Whether height, connectivity, stroke continuation, placement, and other visual features carry information that conventional transcriptions flatten away.
5. Whether the structural effects previously measured from EVA/v101 survive when the unit system is reconstructed from the manuscript itself.

---

# 1. Primary Evidence and Local Project Files

The project folder should contain some or all of the following.

## Primary visual source

- `Voynich-Manuscript_all_Pages.pdf`
  - Downloaded from the Yale manuscript material.
  - Treat this as the **primary visual source** for the new investigation.
  - Work from the page imagery rather than from a transcription during the initial discovery phase.
  - If higher-resolution individual Yale scans are already present locally, prefer them where they materially improve stroke inspection.

## Existing Voynich transcriptions / reference corpora

These are **validation and comparison sources**, not initial segmentation authority:

- `httpswww.voynich.nudataZL3b-(1).txt`
  - ZL3b / EVA-family transcription used in the earlier experiments.
- `httpsvoynich-nudataRF1b-e.txt`
  - Reference transcription in EVA-style notation.
- `httpsvoynich.nudataGC2a-n.txt`
  - Glen Claston / v101 native transcription with substantially different glyph assumptions.
- `voynich-main.zip`
  - Additional Voynich repository/material collected during the investigation.
- Yoshida repository archive / extracted project, if present.
- Any other transcription or manuscript-analysis repository already in the folder.

## Conversation / provenance record

- `Voynich_Decipher_test_Chat.txt`
- `Voynich_Decipher_test_Chat_More_Chat.txt`
- The saved record of the current conversation.

These are provenance. They contain hypotheses, failed tests, numerical results, and rationale.  
**Do not treat conclusions in the chats as facts. Reproduce important results from code/data whenever possible.**

## Natural-language control corpora

If retained in the folder:

- `UD_Finnish-TDT-master.zip`
- `UD_Turkish-IMST-master.zip`
- `UD_Latin-PROIEL-master.zip`

These were used as controls for some morphology/position tests. Keep them available for future falsification work, but they are not needed for the initial visual reconstruction.

---

# 2. Research Stance

## 2.1 What must NOT be assumed

Do not assume any of the following during the ground-up phase:

- one visible Voynich sign = one letter
- EVA character = manuscript grapheme
- v101 character = manuscript grapheme
- blank-delimited group = word
- line = sentence
- tall/gallows forms = independent alphabetic letters
- bench-like forms = sequences such as `ch`, `sh`, `cth`, etc.
- repeated minim-like marks = separate letters
- apparent prefixes/suffixes are linguistic morphology
- Currier A/B are languages
- Davis hand classes necessarily represent different people
- the text is phonetic
- the text is encrypted prose
- the text is non-linguistic notation
- the text runs logically in the same direction as the pen
- an existing Voynich theory is correct because it is standard or widely cited

Existing labels may be used later as metadata for testing correlations.

## 2.2 What may be observed directly

Prefer statements of the form:

- "This stroke rises X times the local median body height."
- "These two outer strokes remain connected by a horizontal stroke."
- "A third component appears inserted within that connected frame."
- "This shape occurs at the beginning of a space-delimited group."
- "This variant is visually taller but otherwise shares the same lower structure."
- "There is a visible gap here."
- "The scan does / does not make a pen lift distinguishable."

Avoid premature statements such as:

- "This is the letter k."
- "This is a prefix."
- "This means plural."
- "This is a ligature."

Those belong under **Hypothesis**, not **Observation**.

---

# 3. Why This Restart Is Necessary

The earlier work used ZL/EVA, RF, and v101 because they make the manuscript computationally tractable.

That work was useful, but it also demonstrated the danger of inherited segmentation.

A previously observed Currier-B pattern in which **interior substitutions appeared more associated with thematic displacement** weakened or disappeared when probable compound forms were resegmented.

By contrast, the more important **token-edge / physical-line-position effect in Currier B survived**:

- ZL/EVA segmentation
- Reference transcription
- v101 / Glen Claston segmentation
- conservative collapsing of likely compound units
- one-unit and two-unit edge definitions
- length/frequency controls
- leave-one-folio-out checks

This is precisely why the project should now go beneath the transcriptions.

If a result survives a unit system derived independently from the physical handwriting, that is much stronger than merely showing agreement among established transcription conventions.

---

# 4. Current Provisional Findings to Replicate, Not Assume

These are **leads**. Sol must not design the new segmentation to preserve them.

## 4.1 Currier-B edge / physical-line-position effect

Using common same-length forms differing by one transcribed unit, substitutions near the token boundary were associated with greater horizontal line-position displacement than comparable interior substitutions.

Under a stricter length requirement (tokens at least five units long) and a common frequency threshold, the approximate Currier-B effects previously obtained were:

- ZL3b/EVA: about `+0.044` normalized line width
- RF/Reference: about `+0.047`
- v101: about `+0.029`

All were positive; all were statistically detectable in that reconstruction.

With only the outermost unit defined as the edge, v101 also produced a strong positive result.

Treat these values as **replication targets**, not priors.

## 4.2 Directional edge substitutions

Specific edge substitutions appeared to have reproducible signed positional effects.

Schematically:

`A + core -> B + core`

could tend to move the resulting form consistently earlier or later in a physical line.

The signed relations showed strong agreement between ZL/RF and v101 and generalized across held-out folio splits.

Again: replicate independently.

## 4.3 Approximate additive positional ordering

For some Currier-B left-edge substitutions, observed relations approximately satisfied:

`Δ(A->B) + Δ(B->C) ~= Δ(A->C)`

Held-out alternate-path predictions retained substantial accuracy.

However:

- ordinary Finnish/Latin morphology can show partial additive positional ordering too
- therefore additivity is **not evidence of mathematics, code, or numerical values by itself**
- there was only weak evidence for a running accumulator/state-machine effect across successive tokens

The restrained interpretation is currently:

> Currier-B left-edge variants may possess a stable approximately one-dimensional positional ordering.

The property represented by that ordering remains unknown.

## 4.4 Section / mode effects

Same-hand, same-Currier comparisons showed large section-dependent changes in token construction.

Some low-complexity sequence models could transfer a substantial portion of their transition structure across Currier-B sections while allowing emitted units/frequencies to change.

This broadly resembles:

> shared machinery + section/domain-conditioned configuration

but substantial prior art already exists for shared grammar / section-specific regimes.

Do not frame this as a novel discovery.

## 4.5 Findings that were weakened

Do **not** carry these forward as established:

- "token interiors carry content while edges carry syntax"
- "EVA vowel-like characters are a special compression class"
- "e/ee/eee are numerical values"
- "the manuscript is a programming language"
- "one person wrote the entire manuscript"
- "Currier A/B are two literal languages"
- "the script is a cipher"
- "the script is non-linguistic"

They remain possible ideas only where separately testable.

---

# 5. Visual Questions That Triggered the Ground-Up Restart

Recent inspection of manuscript crops raised several questions that existing transcriptions may prejudge.

## 5.1 Height / tall forms

Some signs extend much higher than the local writing body.

Questions:

- Is tallness categorical or continuous?
- Is the tall form a separate glyph, or a modified version of a lower form?
- Does height correlate with:
  - line position
  - space-delimited-group position
  - paragraph position
  - neighboring construction
  - manuscript section
  - attributed hand
- Are there intermediate-height variants?
- Can the tall component be decomposed from a lower structural base?

Do not begin from the label "gallows." Record geometry first.

## 5.2 Connected frame / bench-like forms

Some recurring forms appear to contain two outer components connected by a stroke, sometimes with another component apparently inserted between them.

Competing possibilities include:

`A + B + C`

versus

`FRAME(B)`

versus

`LEFT_FRAME + B + RIGHT_FRAME`

versus one indivisible compound glyph.

Questions:

- Does the connecting stroke physically continue through or around the inserted component?
- Are there visible pen lifts?
- Is the inserted element drawn before, after, or as part of the frame where stroke evidence permits inference?
- Does the frame occur without an insertion?
- Can multiple different insertions occupy the same frame?
- Does the outer frame retain stable shape across insertions?
- Do those variants share positional/contextual behavior?

This is a high-priority family for ground-up study.

## 5.3 Apparent multi-part signs

Some individual-looking constructions visually contain several distinguishable components.

Do not automatically call these "three characters."

Record:

- connected components
- intersections
- shared strokes
- baseline relations
- relative drawing height
- recurring subassemblies
- plausible competing segmentations

---

# 6. Neutral Representation

The new representation must avoid baking linguistic assumptions into the data model.

Suggested hierarchy:

`page`
→ `physical line`
→ `space-delimited group`
→ `candidate assembly`
→ `stroke / component`

Use neutral identifiers such as:

- `P_f1r`
- `L_001`
- `G_000245` for a space-delimited group
- `A_0031` for an assembly candidate
- `S_0001` for a stroke/component class

Avoid names such as `word`, `letter`, `prefix`, `suffix`, `vowel`, etc. in raw-data schemas.

Those terms may appear in analysis layers later.

---

# 7. Preserve Ambiguity Instead of Forcing a New Alphabet

The objective is **not** to replace EVA with "our alphabet" after looking at twenty pages.

For an ambiguous mark, preserve multiple segmentation hypotheses.

Example:

```text
instance: G_000245
hypotheses:
  H1: [A][B][C]
  H2: [A][BC]
  H3: [ABC]
  H4: FRAME(B)
```

Each hypothesis should be testable against recurrence and context.

Evidence that may favor one segmentation:

- visual continuity
- recurring stroke order
- stable geometry
- substitutability
- distributional consistency
- positional consistency
- compression / description length
- cross-page and cross-hand recurrence

Do not resolve ambiguity merely because one option matches EVA or v101.

---

# 8. Observation vs Interpretation Ledger

Maintain two explicit layers.

## OBSERVED

Only direct or measured facts.

Example:

> The two outer strokes remain connected by one horizontal trace in 84% of high-confidence instances; the middle component varies among four recurrent shapes.

## HYPOTHESIZED

Interpretations.

Example:

> The connected outer structure may be a reusable frame accepting an inserted parameter.

Every hypothesis should include:

- supporting observations
- falsifying observations
- current confidence
- next discriminating test

This separation is mandatory.

---

# 9. Ground-Up Workflow

## Phase 0 — Inventory and Reproducibility

Before analysis:

1. Inventory all local files.
2. Record exact filenames, hashes, and source/provenance where known.
3. Confirm the manuscript PDF is readable and determine page-to-folio mapping.
4. Establish a reproducible project structure, for example:

```text
voynich-groundup/
  README.md
  data/
    source/
    page_images/
    crops/
    observations/
    transcriptions/
    controls/
  src/
  notebooks/
  reports/
  figures/
  tests/
```

5. Do not modify source files.
6. Put derived data under version control where practical.
7. Fix random seeds for statistical tests where relevant.

## Phase 1 — Representative Blind Visual Sample

Do **not** attempt the entire manuscript first.

Choose a representative initial page set covering variation in:

- manuscript section / illustration type
- Currier A and B **only as later metadata**
- attributed hands **only as later metadata**
- dense text / sparse text
- paragraphs / labels / circular text where useful
- early and late manuscript folios

During selection, page identity may be known, but do not use EVA/v101 glyph labels in segmentation.

Target enough pages to test recurrence without creating an annotation project too large to audit manually.

## Phase 2 — Page Image Extraction and Geometry

From the manuscript PDF:

- extract high-quality page images
- preserve original pixel coordinates
- record page dimensions
- avoid lossy rescaling where possible
- create line and group crops with reversible mappings to source coordinates

Initial processing may use image analysis to assist cropping, but do not let an OCR model silently assign characters.

Where line segmentation is automated, retain confidence and allow manual correction.

## Phase 3 — Stroke/Assembly Annotation

For each high-confidence sample:

Record, as feasible:

- bounding box
- body-height estimate
- ascender/tall extent
- descender extent
- number of visible connected components
- joins / intersections
- probable pen lifts (with confidence)
- loops
- horizontal connector strokes
- vertical strokes
- repeated minim-like strokes
- baseline relation
- neighboring whitespace
- group-internal position
- physical line position
- uncertainty / image-quality flags

Do not pretend stroke order is known unless the physical trace supports it.

## Phase 4 — Unsupervised / Weakly Supervised Unit Discovery

Cluster recurring visual structures using geometry and image similarity.

Important:

- compare whole assemblies
- compare subcomponents
- test whether tall forms decompose into base + modifier
- test frame/insertion hypotheses
- allow context-sensitive variants
- retain uncertainty

The goal is to propose **candidate structural units**, not plaintext letters.

Use neutral IDs.

## Phase 5 — Competing Segmentation Models

Build multiple segmentation models rather than one winner.

At minimum compare:

1. fine stroke/component model
2. medium assembly model
3. compound/frame-aware model
4. space-delimited-group-only model
5. EVA mapping (validation baseline)
6. v101 mapping (validation baseline)

Evaluate with held-out pages.

Useful criteria include:

- visual reconstruction accuracy
- recurrence
- model description length
- predictive likelihood
- stability across pages/hands/sections
- ability to predict neighboring assemblies
- ability to reproduce known positional phenomena without being trained on those phenomena

## Phase 6 — Crosswalk to Existing Transcriptions

Only after candidate units have been learned:

Map them to:

- ZL/EVA
- RF/Reference
- v101

Report explicitly:

- one-to-one correspondences
- one-to-many splits
- many-to-one merges
- contextual/allographic correspondences
- structures not represented cleanly by existing transcriptions
- disagreements among systems

This crosswalk is a result, not a starting assumption.

## Phase 7 — Re-run Structural Assays

Using each candidate segmentation independently, re-run:

### A. Edge vs interior minimal-pair assay

For sufficiently common same-length forms differing by one **candidate unit**:

- edit depth from physical group boundary
- normalized physical line position
- controls for group length and frequency
- connected-family dependence
- Currier/section/hand only in analysis, not segmentation

Ask whether the Currier-B positional effect survives.

### B. Signed substitution graph

For edge-state substitutions:

- estimate signed earlier/later displacement
- test held-out folios
- test alternate-path prediction
- test triangle closure
- compare against within-line shuffles

### C. Section-conditioned structure

Ask whether candidate unit usage changes by section while deeper construction rules remain transferable.

### D. Direction-of-information tests

Do not assume "prefix controls following text."

Compare:

- current left-edge state predicting later structure
- right-side structure predicting the left-edge state
- bidirectional models
- models controlling absolute line position and line length

This directly tests whether a left-edge marker behaves more like:
- position marking
- scope/mode
- classifier
- consequence/result
- or merely correlated morphology

---

# 10. Natural-Language and Null Controls

Do not claim uniqueness without controls.

Available controls include Finnish TDT, Turkish IMST, and Latin PROIEL.

Also construct manuscript-internal nulls:

- shuffle groups within each physical line
- shuffle lines within folios
- preserve line lengths while randomizing placement
- preserve group frequencies / family structure where possible
- matched resampling by token/group length and frequency

When testing visual-unit hypotheses, create null segmentations where possible to ask whether an apparent improvement follows simply from having more/fewer units.

---

# 11. Prior Art / Mercurial Rule

Before claiming novelty:

1. Search prior Voynich scholarship, conference papers, repositories, forum archives, and named researchers.
2. Distinguish:
   - known result
   - independent replication
   - methodological extension
   - genuinely unlocated prior art
3. Never use "novel" merely because the immediate search did not find the exact phrasing.
4. Prefer wording such as:
   - "independent replication"
   - "cross-transcription robustness check"
   - "I have not located this exact assay in prior work"
   - "potential methodological extension"

Relevant nearby prior work already encountered includes:

- Currier: statistical A/B distinction and subject-matter possibility
- Lisa Fagin Davis: five-hand palaeographic classification
- Patrick Feaster: positional/rightward minimal-pair effects and cumulative-differential speculation
- Stolfi: formal word grammar
- Yoshida-related work: shared transition / positional models
- recent VoynichNotation and other 2026 structural analyses
- EVA / v101 / STA/Reference transcription methodology

Do not spend time "rediscovering" these as if they were new.

---

# 12. Programming / DSL Analogy — Use Carefully

A productive analogy emerged:

> The manuscript might behave more like a compact domain-specific notation than ordinary prose.

This is **not** a historical claim.

Do not write "the Voynich Manuscript is a programming language."

The analogy is useful only insofar as it generates falsifiable models involving:

- reusable units
- state-like transformations
- slots
- scope
- type/class markers
- section-specific libraries
- shared structural runtime
- declarative record syntax

A simple running accumulator / executable-state model was not strongly supported by earlier tests.

Treat "programming" as a modeling metaphor, not an answer.

---

# 13. One-Person / Multiple-Hand Issue

The manuscript has been classified palaeographically into multiple hands, often five under Lisa Fagin Davis's scheme.

That does **not** establish five separate authors beyond dispute.

For this project:

- retain hand classification as metadata
- do not infer authorship from it
- test whether visual unit structure is stable within and across attributed hands
- explicitly separate:
  - hand/style effects
  - section/domain effects
  - underlying structural effects

---

# 14. Initial Deliverables for Sol

Do not begin with a giant decipherment attempt.

Produce these first:

## Deliverable 1 — Evidence Inventory

`reports/00_evidence_inventory.md`

Include:

- files found
- hashes
- source status
- usable manuscript image resolution
- page/folio mapping
- known limitations

## Deliverable 2 — Ground-Up Annotation Schema

`reports/01_annotation_schema.md`

Define neutral fields for:

- page
- line
- space-delimited group
- stroke/component
- assembly
- geometry
- connectivity
- uncertainty
- competing segmentations

Keep terminology non-linguistic.

## Deliverable 3 — Representative Sample

Create a documented initial sample of manuscript pages and explain why it is sufficient to test the first unit hypotheses.

## Deliverable 4 — Visual Unit Atlas v0

`reports/02_visual_unit_atlas_v0.md`

For every candidate recurring structure:

- neutral ID
- representative crops
- visual description
- observed variants
- known contexts
- segmentation alternatives
- confidence
- cross-page recurrence

Do **not** attach meanings.

## Deliverable 5 — EVA/v101-Blind Candidate Segmentation

A machine-readable dataset for the sample using neutral units.

## Deliverable 6 — Crosswalk Report

Only after Deliverable 5 is frozen:

`reports/03_transcription_crosswalk.md`

Compare the blind units against EVA, RF, and v101.

## Deliverable 7 — Reproduction of the Currier-B Positional Assay

`reports/04_positional_replication.md`

Run the assay under:

- blind ground-up segmentation
- ZL/EVA
- RF
- v101

Report successes **and failures**.

---

# 15. Failure Criteria

The project should be willing to conclude that the ground-up restart did not improve the model.

Examples of useful negative outcomes:

- visually inferred compounds provide no predictive advantage over EVA
- height behaves as scribal flourish rather than a stable structural feature
- apparent frames do not recur consistently
- connectivity varies too much to define a unit
- the positional effect disappears under manuscript-derived units
- candidate unit classes are unstable across pages/hands
- a simpler ordinary-language morphology control explains the same effects

These are successful falsifications, not project failures.

---

# 16. Working Principles

1. **Manuscript first.**
2. **Observation before interpretation.**
3. **Preserve ambiguity.**
4. **Do not inherit a character inventory by convention.**
5. **Do not reinvent a new alphabet prematurely.**
6. **Hold hypotheses to held-out data.**
7. **Use natural-language and internal null controls.**
8. **Record negative results.**
9. **Mercurial-check prior art before novelty claims.**
10. **Prefer reproducible scripts over one-off visual impressions.**
11. **Keep every derived crop traceable to exact source coordinates.**
12. **Do not optimize the segmentation to preserve our earlier findings.**

---

# 17. First Instruction to Sol

A suitable opening instruction is:

> Read `AGENTS.md` if present, then read this handoff and inventory the Voynich project folder. Treat `Voynich-Manuscript_all_Pages.pdf` as the primary visual evidence and all existing transcriptions as later validation datasets. We are restarting script segmentation from the physical manuscript rather than accepting EVA, RF, or v101 as ground truth. Do not attempt decipherment and do not create a replacement alphabet yet. Establish the reproducible ground-up workflow, create the evidence inventory and neutral annotation schema, then propose a representative blind visual sample. Preserve competing segmentations and keep direct observations separate from hypotheses. Do not modify source evidence.

---

# 18. Central Research Question

The project is currently trying to answer a mechanical question before a semantic one:

> **What are the actual reusable written units and structural rules of the Voynich Manuscript when those units are inferred from the physical handwriting rather than inherited from a transcription convention?**

Only after that question is addressed should the project return to:

- positional grammar
- section/domain modes
- state/operator hypotheses
- linguistic/cipher/notation comparisons
- or decipherment.

The manuscript gets to define its own units first.
