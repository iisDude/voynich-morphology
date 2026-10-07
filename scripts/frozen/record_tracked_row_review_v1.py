"""Record source/mask observations for the prespecified 32-row diagnostic."""
from common import OUT, read_json, write_json

notes = {
 'V_018':[
  'Left and right writing flows largely retained; plant-edge/root fragments are also assigned. The separated flows need independent path annotation.',
  'Main writing body largely coherent; upper tall-form/contact ownership remains ambiguous. Faint and detached marks require review.',
  'Main row broadly coherent; faint marks and separate left writing flow remain uncertain.',
  'Substantial left-side writing is unassigned while the right flow is retained; plant-stem fragments enter the mask.'],
 'V_038':[
  'Left writing row retained; conspicuous flower drawing assigned on the right.',
  'Left final writing row retained; conspicuous plant drawing and stem assigned on the right.',
  'Writing body broadly coherent; a leaf/drawing-edge fragment is assigned at right.',
  'Writing body broadly coherent; upper contacts and plant-edge fragments remain uncertain.'],
 'V_065':[
  'Left and right writing bodies largely coherent; detached lower marks and omissions remain.',
  'Main writing body broadly coherent; upper contacts and widely separated flows need local checking.',
  'Main writing row and tall structures broadly coherent; faint omissions and a small stem fragment remain possible.',
  'Main writing row broadly coherent; contact ownership remains unresolved.'],
 'V_094':[
  'Long writing body largely retained; left starting-row identity and adjacent tall contacts remain ambiguous.',
  'One writing body broadly coherent; complete detached-mark recall unestablished.',
  'Main writing body retained; extra lower upright/contact fragments are visible, with ownership unresolved.',
  'Main writing body broadly coherent; source preview clips upper context, preventing confident ownership of tiny top fragments.'],
 'V_120':[
  'Main writing body largely coherent; an extra lower tall fragment under the right middle needs neighboring-row/contact annotation.',
  'Main writing body largely coherent; faint right ending is fragmented and omitted in part.',
  'Writing body largely coherent; descending or neighboring tall-form ownership remains ambiguous.',
  'Writing body largely coherent; tall descenders and contacts require local ownership annotation.'],
 'V_140':[
  'Writing body retained; left drawing contour and right repeated drawing strokes are assigned.',
  'Writing body retained; conspicuous left drawing strokes assigned.',
  'Writing body broadly coherent; tiny left border fragment and tall-contact ownership remain uncertain.',
  'Writing body retained; conspicuous drawing fragments assigned at both ends.'],
 'V_155':[
  'Main writing body retained with partial groups; upper neighboring/contact structures and a lower right fragment remain unresolved.',
  'Main writing body retained; right drawing-edge fragment assigned and tall contacts unresolved.',
  'Main writing body retained; right drawing fragments assigned.',
  'Writing body only partly retained; end groups and detached marks omitted, upper contacts unresolved.'],
 'V_203':[
  'Writing body broadly coherent; right marginal drawing fragments also assigned.',
  'Substantial middle writing omitted; left star and right margin/paper fragments assigned.',
  'Writing body retained; left star fragments assigned.',
  'Substantial writing omitted at both ends, leaving a middle sequence and isolated fragments.']}

plan=read_json(OUT/'data/observations/assigned_visual_candidates_v11/tracked_row_source_audit_plan.json')
indices={key:0 for key in notes}
for row in plan['rows']:
    vid=row['view_id']; index=indices[vid];indices[vid]+=1
    row.update(outcome='reviewed: complete writing membership and boundaries not certified',
      observation=notes[vid][index],review_basis='RGB context and exact assigned native mask; conventional strings hidden',
      pen_lift_evidence='unresolved',grapheme_boundary_evidence='unresolved')
assert len(plan['rows'])==32 and all(v==4 for v in indices.values())
plan.update(status='Completed all 32 prespecified diagnostic reviews',
 acceptance='No row certified as a complete writing-unit segmentation. Broadly coherent bodies are retained as provisional observations, with recorded errors and uncertainty.',
 interpretation='Whole-row audit of candidate membership, not a sign-recognition accuracy or manuscript-wide recall estimate. No protocol retuning from this audit.')
write_json(OUT/'data/observations/assigned_visual_candidates_v11/tracked_row_source_audit_reviewed.json',plan)
report=['# Tracked-row source audit v11','',plan['selection'],'',plan['limitation'],'',plan['acceptance'],'',
 'The locally tracked density path improves some dense-row bodies over the horizontal proposals. It does not solve drawing exclusion, faint ink recall, detached upper/lower ownership, separated text flows or group boundaries. Density-derived paths are baseline proxies. No stroke-order or pen-lift conclusion follows.','',
 '| View / candidate row | Source and exact-mask observation |','|---|---|']
report.extend(f"| {r['line_id']} | {r['observation']} |" for r in plan['rows'])
(OUT/'reports/05_tracked_row_source_audit_v11.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
print('Recorded 32 whole-row source reviews; no complete boundary certification.')
