"""Single-reviewer source audit, preserving failures without repairing matches."""
from common import OUT,read_json,write_json

def main():
    root=OUT/'data/comparisons/v2';rows=read_json(root/'visual_row_alignment_audit_plan.json')
    reasons={1:'Texture at left; partial neighboring rows and plant fragments.',2:'Adjacent rows and tiny margin fragments.',3:'Texture, drawing fragments and neighboring rows.',4:'Texture, partial ink and plant fragments.',5:'Texture and adjacent rows.',6:'Neighboring rows and tiny fragments.',7:'Cropped components from several rows.',8:'Texture and plant fragments; no coherent complete row.',9:'Upper-row ink and fragmented/omitted writing.',10:'Texture and upper-row ink mixed with a lower row.',11:'Upper-row ink and plant fragments.',12:'Approximately one row, but an artifact slot and interrupted groups; proposed pairing does not match visible forms.',13:'Preceding-row tall forms included with lower bodies.',14:'Upper/lower rows, minim fragments and margin texture.',15:'Texture slots and multi-row constructions.',16:'Upper/lower rows and margin fragments.',17:'Preceding-row tall forms and right texture slot.',18:'Multiple rows in one group and texture slots.'}
    for i,r in enumerate(rows,1):r.update(audit_status='rejected',source_observation=reasons[i],accepted_group_pairs=0,reviewer='single Codex source-image reviewer',unit_correspondence='unresolved')
    write_json(root/'visual_row_alignment_source_audit.json',rows)
    summary=read_json(root/'crosswalk_summary.json');summary.update(audited_rows=len(rows),rejected_audited_rows=len(rows),accepted_visual_pixel_group_pairs=0,accepted_unit_pairs=0,
        conclusion='All sampled row-count proposals failed source verification. Automatic count alignment rejected. v4 row membership/grouping not validated.',next_action='Separate source-only v5 repair; frozen failure record retained.')
    write_json(root/'crosswalk_summary.json',summary)
    (OUT/'reports/03_crosswalk_failure_v0.md').write_text('''# Source crosswalk failure

The partial candidate snapshot froze before conventional contents were opened. The comparison pass proposed 42 rows using unique four-row sequences of group counts, without unit identities or positional coefficients. Eighteen proposals were sampled across training, validation, test and calibration and reviewed on native source crops. All eighteen failed: texture or drawings create false groups, and several candidate rows combine ink from neighboring physical lines. One crop approximately follows a row, but its proposed group slots still fail visible boundary correspondence.

There are **zero accepted visual-to-conventional group pairs and zero accepted unit pairs**. Conventional native pixel positions remain unknown. Count agreement is not row identity; equal unit counts are not a grapheme crosswalk. The 48,275 conventional group pairs are conditional on identical source loci and group counts; they are inherited boundary hypotheses.

The v4 pixel assays therefore measure candidate raster-group locations, not validated writing groups. They cannot establish the requested manuscript positional signal. The earlier fine-family audit measured whether a local object resembles writing; it did not validate row membership or whole-group boundaries.

A separately versioned v5 source-only repair tests native path detection, stronger foreground contrast and removal of tiny components. The frozen snapshot remains unchanged. Because conventional contents are now known, v5 is a post-unblinding repair. No parameter will be selected from conventional counts, strings or positional coefficients.
''',encoding='utf-8')

if __name__=='__main__':main()
