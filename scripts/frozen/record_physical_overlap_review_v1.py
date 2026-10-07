"""Source review of all nine same-caption-side capture pairs."""
from common import OUT,read_json,write_json

def main():
    root=OUT/'tests/physical_overlap_v1';rows=read_json(root/'results.json')
    notes={
      ('V_128','V_129'):'Different circular diagram fields are visible; no common writing field established.',
      ('V_132','V_133'):'Different diagram fields/panel configurations; recovered matches lie mainly on book edges, not a shared writing field.',
      ('V_156','V_157'):'Folded text view and extended multi-panel view; visible text placement differs. Shared caption does not establish a panel correspondence.',
      ('V_157','V_158'):'Different extended panel configurations and writing/drawing fields; no shared writing field established.',
      ('V_164','V_165'):'Different folded/extended configurations with different writing and plant fields; no common writing field established.',
      ('V_165','V_166'):'Extended field and plant page have different drawing and writing layouts; no common writing field established.',
      ('V_172','V_173'):'Different plant and writing fields despite the same folio-side caption reference.',
      ('V_180','V_181'):'Different folded/extended configurations, drawing fields and text layout; no common writing field established.',
      ('V_182','V_183'):'Different plant, container and writing fields; same caption reference covers distinct visible fields.'}
    assert len(rows)==9
    for row in rows:
        row.update(source_review='reviewed: no reusable writing-field alignment accepted',source_observation=notes[row['from_view'],row['to_view']],accepted_for_writing_deduplication=False)
    write_json(root/'source_reviewed.json',rows)
    (root/'summary.md').write_text('# Physical capture overlap review\n\nAll nine pairs sharing a folio-side caption reference were inspected. No reliable source-feature overlap or reusable writing-field alignment was accepted. Different folded/extended configurations and distinct diagram/text fields occur under the same caption reference. This does not prove all underlying parchment regions are disjoint. Neither physical panel boundaries nor bifolios are reconstructed by a caption or failed feature match. All connected caption views remain in one split; writing deduplication remains unresolved.\n',encoding='utf-8')
    print('Reviewed all nine source capture pairs; zero writing-deduplication transforms accepted.')

if __name__=='__main__':main()
