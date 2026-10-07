"""Source-only second-pass review; preserves the earlier crop audit verbatim."""
from common import OUT,read_json,write_json

audit=read_json(OUT/'data/comparisons/v2/visual_membership_overlay_audit_plan.json')
clear={5,7,9,10,13,14,15,16,17,18}
possible={2,6,11}
artifacts={1,3,4,5,7,8,11,15,16,17,18}
for number,row in enumerate(audit,1):
    row['overlay_review']={
        'review_basis':'Source RGB, exact assigned pixels highlighted, and exact binary mask; conventional strings hidden',
        'assigned_neighboring_row_ink':'visible' if number in clear else 'possible_contact_or_assignment' if number in possible else 'not_demonstrated',
        'assigned_nonwriting_fragments':'conspicuous' if number in artifacts else 'small_or_uncertain',
        'writing_coverage':'Incomplete; several visible writing strokes remain unassigned',
        'crosswalk_status':'rejected; no native pixel position transferred to a conventional group',
        'caution':'A tall form can legitimately extend into another row. Mere neighboring ink in the RGB bounding crop is not a membership error. This selected alignment audit is not a manuscript-wide error-rate sample.'}
write_json(OUT/'data/comparisons/v2/visual_membership_overlay_review_v1.json',audit)
(OUT/'reports/03_crosswalk_membership_correction_v1.md').write_text('''# Exact-mask correction to the failed alignment audit

The 18 ordinal row/group alignment proposals remain rejected. No visual-to-conventional group correspondence, grapheme correspondence, or conventional native pixel position is accepted.

The earlier bounding-crop review overstated row mixing in some examples. This second review shows the saved assigned masks directly: neighboring ink in an RGB crop is context unless the exact mask includes it. Ten examples show assigned portions of distinct neighboring writing rows, three show possible contacts/assignment ambiguity, and five do not demonstrate that error. Tall forms extending above the body are not automatically foreign-row ink. Eleven examples contain conspicuous assigned paper/drawing fragments. Writing omissions occur too.

These judgments apply to a selected, failed alignment audit, not a random 204-view extraction audit; their fractions cannot estimate manuscript-wide prevalence. Some masks retain a coherent writing row despite incorrect group slots or missing strokes. The audit rejects the proposed ordinal alignments and demonstrates specific extraction defects; it does not prove every candidate row is unusable, nor validate any inherited transcription boundaries.

The original frozen candidate model remains unchanged. A later raw-mask diagnostic on V_004 also distinguishes foreground detection from component assignment: substantial writing survives in the v4/v5/v6 raw masks but is omitted during row ownership. The stronger v5 threshold alone does not explain the missing assigned writing. v7 over-connects background; v8 ridge filtering fragments writing. Later ownership and path experiments remain calibration experiments, not an accepted replacement.
''',encoding='utf-8')
print('Recorded all 18 exact-mask reviews; original audit and visual freeze preserved.')
