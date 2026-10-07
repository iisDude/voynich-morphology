# Registered Currier-B rerun v2

Question: do edge versus interior single-unit changes predict displacement when the units come from source imagery?

Run only after the v2 source freeze. Both ordinal rank and native pixel x use the same admitted occurrences; unknown slots are never re-ranked. Three representations, three cohorts, two endpoints, four frequency thresholds and two edge widths give 144 registered runs. None has qualifying minimal pairs; do not interpret a support failure as a zero effect.

Reproduction: project Python runtime, `src/run_adjudicated_currier_B_v2.py` (without `--register`). The runner verifies every v2 frozen file before and after execution. `analysis_plan.json` is frozen; result files are post-freeze outputs. See `reports/10_currier_B_adjudicated_v2.md` for measured-coordinate checks and limits.
