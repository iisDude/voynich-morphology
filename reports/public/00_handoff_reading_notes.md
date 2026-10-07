> Publication link-adapted view; the original report is preserved unchanged in `reports/`.

# Handoff and supplementary conversation review

Date: 2026-10-05. Read the handoff first, then all 1,993 lines of `Voynich_Decipher_Test_2nd_Chat.txt`, then the subsequently supplied `VOYNICH_TEST_LEDGER.md`. All original files remain unchanged.

## Scope adopted

Reconstruct candidate reusable written structures from physical imagery. Preserve competing segmentations, use neutral IDs, and separate direct observations from interpretation. Do not choose boundaries to preserve the earlier positional effect. Existing EVA, RF, and v101 material becomes a validation layer only after the visual representation is frozen.

The saved file matches the supplemental name supplied by the user. The app's recent chat listing did not show that exact title, so the local transcript was used. No other chat was messaged or modified.

## Leads retained as reported, not reproduced

The final cross-transcription passage reports Currier-B edge-position coefficients of +0.0438 (ZL), +0.0472 (RF), and +0.0285 (v101), with length >=5 and frequency >=8. It reports a v101 outermost-unit coefficient of +0.0640 and positive leave-one-folio-out estimates in 83/83 exclusions. These are historical chat claims, not fresh measurements or independently verified statistics.

The handoff additionally reports signed substitution consistency and approximate additivity. Their complete analyses are not present in this supplementary chat. The test ledger now documents them in sections 19–26, including support counts, reported correlations, closure errors, and held-out alternate-path prediction. It identifies these as reported results requiring reruns, rather than saved executable outputs.

The conversation weakened the thematic-interior interpretation after compound regrouping. It also found ordinary-language parallels for same-core section-dependent wrappers and partial shared-grammar transfer. Neither phenomenon establishes a special semantic channel or a computational notation.

The conversation's categorical language, significance statements, and novelty suggestions must not be inherited as conclusions. In particular, agreement among transcriptions does not by itself establish agreement with measured physical pixel positions or rule out positional allography. The ledger resolves the prior normalized line-position definition: token index `i / (n - 1)`, with singleton lines assigned 0.5. This is ordinal token position, distinct from cumulative transcribed length and measured horizontal pixel position. Earlier coefficients are changes on a normalized token-rank scale, not measurements of physical line width.

## Reproducibility gaps

- No loose analysis scripts accompanied the chats. The ZIPs do contain extensive third-party analysis code and reports; these have been catalogued, not executed or audited. The original chat scratch scripts have not been identified.
- The ledger specifies frequency filtering, same-length one-unit pairs, edge width, token-rank position, pairwise absolute mean-position displacement, length/log-frequency controls, and HC3 OLS. Exact corpus parsing/locus filtering and ambiguous-group handling remain to be fixed; family-dependence and resampling implementation remain unresolved.
- RF's dependence on other transcriptions and overlapping source material must be checked before calling the three corpora independent measurements.
- Folio exclusions must be physical-folio exclusions: combined views and repeated/folded views must not leak between training and validation.
- Attributed-hand and Currier coverage of the initial visual pilot is not yet certified. These labels will live outside the annotation tables.

## Prior exposure and blinding

The annotating agent has read the chat, which contains EVA strings and earlier interpretations. This is therefore a transcription-withheld workflow, not a claim of psychological or double blinding. No transcription content has been opened to guide visual segmentation. Page identities are known during selection, as permitted by the handoff. Reserve pages are unviewed in the pilot; this does not imply nobody has seen them historically.

## First discriminating visual questions

1. Does the apparent connector remain visible across different inner structures, or is continuity unresolved/created by ink spread and resolution?
2. Does tall extent vary continuously once local body height, slant, and page scale are controlled, or support distinct geometric categories?
3. Do apparently recurring subassemblies recur independently, or only as parts of a larger construction?
4. Does a spacing boundary survive plausible image thresholds and direct inspection, or depend on arbitrary preprocessing?

Unconventional possibilities remain admissible hypotheses. None is a reason to assign meaning or to resolve ambiguous boundaries without image evidence.

## Ledger reconciliation

The ledger's reconstruction status is a historical status label. No result has been reproduced by this workspace run. Section 6 expressly states that the original family bootstrap was not recovered and some dependence-aware intervals crossed zero. Do not repeat the supplementary chat's earlier stronger family-bootstrap language as an established finding.

Sections 21 and 23 require special null care. Within-line shuffles have differing reported implementations. Also, differences between the same three means close algebraically by construction; a triangle test must specify independently estimated/context-matched edges and a null that preserves the relevant sampling/dependence structure. Otherwise small closure error may be an arithmetic consequence rather than additional evidence.

For future reproduction, each `tests/<test_name>/` directory must contain `README.md`, `run.py`, `config.json`, `input_manifest.json`, `results.csv`, `summary.md`, and `figures/`, as required in ledger section 30. Save inclusions, exclusions, support counts, seeds, uncertainty, failures, and prior-art status.

Work order for this initial setup follows the handoff's manuscript-first freeze gate. The ledger's high-priority transcription baseline reruns are queued for later comparison; none has been run or allowed to determine visual boundaries. A separate future replication phase can recover the ordinal baseline and then compare it against the new pixel endpoint without conflating their scales.
