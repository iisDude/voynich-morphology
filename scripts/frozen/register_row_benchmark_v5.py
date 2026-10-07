"""Small complete-row reference benchmark, source decisions before class inference."""
from common import OUT,read_json,read_csv,write_json,sha256,SEED
from datetime import datetime,timezone
from PIL import Image,ImageDraw
import numpy as np
D=OUT/'data/observations/row_benchmark_v5_development';T=OUT/'tests/row_benchmark_v5';G=OUT/'figures/row_benchmark_v5';F=OUT/'data/observations/visual_dataset_v5'
TARGETS={'V_012':[1,3],'V_023':[1,4],'V_069':[1,5],'V_079':[1,2],'V_110':[1,4],'V_148':[1,3],'V_191':[1,4],'V_204':[2,3]}
def main():
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen(source_stage=True)
    if (D/'PLAN.json').exists():raise RuntimeError('Already registered')
    for p in [D,T,G]:p.mkdir(exist_ok=True)
    sources={s['view_id']:s for s in read_csv(OUT/'data/source/yale_native_all_manifest.csv')};rows=[]
    for vid,indices in TARGETS.items():
        o=read_json(OUT/f'data/observations/regional_candidates_v11/{vid}.json');s=sources[vid];w,h=int(s['width_px']),int(s['height_px'])
        for n in indices:
            l=o['lines'][n-1];body=l['body_height_proxy_px'];anchor=l['baseline_y_at_xref'];rid=f'B{len(rows)+1:03d}'
            rows.append(dict(row_id=rid,view_id=vid,caption=o['view']['folio_component'],native_source=s['path'],native_dimensions=[w,h],source_anchor_y=anchor,body_proxy=body,selection_proposal_id=l['line_id'],source_context_bbox=[0,max(0,int(anchor-3.5*body)),w,min(h,int(anchor+2.7*body))],split='heldout' if vid in ['V_023','V_191'] else 'development'))
    plan=dict(registered_at_utc=datetime.now(timezone.utc).isoformat(),version='V5 source row benchmark',seed=SEED+5,
      question='Can complete source membership and structural sequences be established in carefully adjudicated ordinary rows?',
      selection='16 physical-row targets in8 existing overview-triaged captions; two near top ordinary writing per caption, clear horizontal layout, contrast, broad visible margins and minimal drawing intrusion. Source overviews and geometric row proposals only. No new page coverage. Anchors select a physical row, not a membership truth or character boundary.',
      rows=rows,heldout_captions=['10','106'],development_captions=sorted({r['caption'] for r in rows if r['split']=='development'}),
      prior_exposure='Source captures and coarse V4 field triage previously seen. No V3 class suggestion or V4 sequence list used in row selection/annotation. Heldout is for new membership rules; photographs are not globally unseen.',
      reference='Direct native RGB review of full-width context and every visible relevant object, with coordinate boxes/connected-mask aids. Raster proposals assist locating objects; adjudicator can join/split/add missing objects. They do not define writing truth. Unresolvable contacts/marks preserved. Reference is operational photographic ground truth, not independent expert-rater or microscopic stroke truth.',
      annotation_categories=['confirmed_writing','confirmed_nonwriting','unresolved','detached_ownership_unknown','connected_writing_structure','possible_compound','neighbor_row_contact','possible_showthrough_or_artifact'],
      stages=['Development native RGB row endpoints/body envelope and full writing sweep','Development source-only object ledger, missing-object sweep and mask-assisted contacts','Source-only optional rule development from development errors; seal rules before heldout row ledger','Heldout native RGB reference adjudication without algorithm rule outcomes/classes','Repeat masked subset after intervening work; prior decision files hidden; same adjudicator','Freeze all source membership and physical row judgments before V3 class mapping','Apply frozen V3 unchanged, report separate accuracy/completeness/recurrence','Freeze V5 before any conventional input; postfreeze support assessment'],
      repeatability=dict(rows=['B002','B005','B010','B014'],minimum_intervening_work='Other row adjudication and rule development; report actual timing, no independent-rater claim',masked='Anonymous source objects/full context, previous labels and V3 class suggestions absent'),
      boundary_hypotheses=[.35,.55,.75],source_boundary_adjudication='Record each inter-parent gap as physical contact, clear separation, ambiguous spacing, or unresolved ownership. A visible gap is not a word boundary. Retain3 partitions unless physical continuous writing rules out a split.',
      accuracy='Confirmed writing-object recall; nonwriting false inclusion; optional category handling; owner accuracy; source parent split/merge errors; exact parent recovery; gap boundary precision/recall on physically resolvable boundaries and ambiguity coverage; endpoint pixel error; V3 assigned-parent coverage; exact complete-row/group structural sequence recovery. Separate numerator/denominator and caption intervals; unknown objects excluded from asserted truth but quantified.',
      matching='Mask overlap to manually reviewed source objects and source coordinates; membership overlap>=0.50, exact parent requires unique one-to-one support, source contact adjudication and IoU>=0.75; endpoints within0.25body; unresolved contacts do not count correct or incorrect, coverage reported.',
      rule_validation_gates=dict(heldout_writing_recall_min=.95,heldout_nonwriting_false_inclusion_max=.05,heldout_resolved_owner_accuracy_min=.95,heldout_exact_parent_recovery_min=.90,heldout_endpoint_accuracy_min=.90,repeatability_resolved_membership_min=.90),
      downstream_support=dict(complete_reference_rows_min=12,complete_identified_groups_ge3_min=100,heldout_complete_identified_groups_ge3_min=30,heldout_recurrence_ge3_min=.20,unknown_confirmed_parent_rate_max=.20,resolved_row_endpoint_fraction_min=.90,source_rule_validation_all_required=True,all_three_gap_hypotheses_required=True),
      failure='Freeze partial reference if image cannot decide. Validate rules on heldout once; preserve failures without retuning classes, thresholds or membership to conventional or recurrence targets.',
      prohibited=['EVA','RF','v101','Currier','positional outcomes','minimal-pair support','class recurrence selecting rows or membership'],
      immutable_dependencies={v:sha256(OUT/f'data/observations/visual_dataset_{v}/FREEZE_MANIFEST.json') for v in ['v3','v4']},
      v3_model_sha256=sha256(OUT/'data/observations/recurrence_v3_structural_candidate/sealed_class_model.pkl'))
    write_json(D/'PLAN.json',plan);write_json(T/'config.json',plan)
    # Raw native pixels, no baseline/parent/class overlay. Source anchor appears in text only.
    for r in rows:
        im=Image.open(OUT/r['native_source']).convert('RGB');patch=im.crop(r['source_context_bbox']);patch.save(G/(r['row_id']+'_raw.png'))
        # Full pixel horizontal sweep as overlapping800-pixel panels, without class or object suggestions.
        tiles=[]
        for x in range(0,im.width,750):
            a,b,c,d=r['source_context_bbox'];p=im.crop((x,b,min(im.width,x+850),d));p=p.resize((p.width*2,p.height*2),Image.Resampling.NEAREST);can=Image.new('RGB',(1700,p.height+25),'white');can.paste(p,(0,25));ImageDraw.Draw(can).text((4,4),f'{r["row_id"]} native x{x}:{min(im.width,x+850)} y{b}:{d}; row anchor y{r["source_anchor_y"]:.1f}',fill='black');tiles.append(can)
        can=Image.new('RGB',(1700,sum(t.height+5 for t in tiles)),'#ddd');y=0
        for t in tiles:can.paste(t,(0,y));y+=t.height+5
        can.save(G/(r['row_id']+'_sweep.png'))
    print('Registered16 rows/8 captions:12 development,4 heldout; classes concealed',flush=True)
if __name__=='__main__':main()
