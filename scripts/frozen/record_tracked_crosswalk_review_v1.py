"""Source adjudication of all 22 tracked alignment audit proposals."""
from common import OUT,read_json,write_json

NOTES=[
 'Writing body largely follows one row, but a merged writing group and plant-stem groups replace several conventional slots. Equal count does not preserve boundaries.',
 'Drawing strokes at both ends and contacts from neighboring rows are assigned. Proposed conventional row identity/boundaries are unsupported.',
 'Assigned writing jumps between adjacent row bodies and omits groups; an upper right neighboring ending is included.',
 'Four main writing bodies are retained but right leaf drawing fragments create extra groups; detached writing is omitted.',
 'Assigned writing switches between two adjacent bodies; several upper-row portions are missing.',
 'Writing row incomplete: parts of tall and lower traces omitted; left texture/border fragments are assigned.',
 'Assigned star, marginal fragments and neighboring upper/lower tall portions accompany the main body.',
 'Left body shifts between rows and loses faint parts; small drawing/paper fragments enter slots.',
 'Several entire central writing structures are omitted; retained group count cannot certify full boundaries.',
 'Main body retained, but a lower neighboring tall portion and right marginal drawing enter the mask.',
 'Main body retained with a lower neighboring upright and incomplete boundary ownership.',
 'Initial large horizontal structure omitted; a lower neighboring tall/body portion is included.',
 'Upper neighboring upright joins a lower-row body; writing ending is incomplete.',
 'Upper neighboring tall portion joins the main body; partial and faint strokes omitted.',
 'A large internal upright is omitted although lower parts remain; group extent is incomplete.',
 'Source body broadly coherent, but the displayed conventional sequence and proposed row identity do not match the visible assembly sequence. Count anchor is insufficient.',
 'f47r first-row identity and several interior gray gaps are plausible. The initial high structure and detached/faint marks are incomplete; complete row and unit-boundary correspondence are not certified.',
 'Main body retained but upper tall/contact ownership remains ambiguous and some detached marks are omitted.',
 'Star and neighboring tall/body portions are assigned; left writing is incomplete and body membership changes.',
 'Assigned body switches across adjacent rows; marginal star/drawing enters the mask.',
 'Assigned neighboring upper/lower tall portions and marginal drawing accompany a partly retained body.',
 'Multiple adjacent-row bodies, uprights and lower ending are combined; writing is substantially incomplete.'
]

def main():
    root=OUT/'data/comparisons/v11';rows=read_json(root/'visual_membership_overlay_audit_plan.json');assert len(rows)==len(NOTES)
    for n,(row,note) in enumerate(zip(rows,NOTES),1):
        row.update(audit_number=n,source_review='reviewed: complete row/group correspondence not accepted',source_observation=note,
          accepted_pixel_group_pairs=[],accepted_unit_pairs=[],native_position_transferred=False,
          review_basis='Full source RGB and exact assigned-mask overlay; boxed comparative sequences examined for selected row identities',
          limitation='A coherent writing body or plausible subset of gray gaps is not full writing recall, canonical grapheme boundaries or one-to-one alphabet correspondence.')
    write_json(root/'visual_row_alignment_source_audit.json',rows)
    summary=read_json(root/'crosswalk_summary.json');summary.update(audited_rows=len(rows),accepted_visual_pixel_group_pairs=0,accepted_unit_pairs=0,
       outcome='All 22 sampled complete-row alignment proposals fail certification. Audit 17 has plausible row identity/interior boundaries; retained as partial ambiguity, not silently called unusable.',
       selection_limitation='Fixed-seed audit of count-anchor proposals, not a manuscript-wide random error-rate sample. Remaining 38 proposals unverified, not rejected by extrapolation.',
       exposure='Second candidate snapshot and audits follow prior conventional/statistical exposure; no new blind claim.')
    write_json(root/'crosswalk_summary_reviewed.json',summary)
    report=['# Tracked visual crosswalk source review','',
      'Sixty four-row count-anchor proposals contain 439 candidate groups. All 22 prespecified sampled complete-row proposals were examined with exact assigned masks; no complete-row/group or unit correspondence is certified. The remaining 38 are unverified, not automatically rejected.','',
      'One proposed first row (audit 17, V_094/f47r) has plausible row identity and several interior gray gaps, but incomplete initial/detached writing prevents a complete-row certification. Other coherent bodies can still have false slots, missed strokes, wrong conventional row identities or contacts. No conventional native pixel position is transferred. No one-to-one alphabet is inferred.','',
      '| Audit / candidate row | Source observation |','|---|---|']
    report.extend(f"| {r['audit_number']} / {r['visual_line_id']} | {r['source_observation']} |" for r in rows)
    (OUT/'reports/05_tracked_crosswalk_source_review_v11.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    print('Recorded all 22 complete-row crosswalk audits; partial plausibility retained, no accepted pixel/unit transfers.')

if __name__=='__main__':main()
