"""Preregister source sequence investigation before new source review/results."""
from common import OUT,read_json,read_csv,write_json,sha256,SEED
from datetime import datetime,timezone
from collections import defaultdict
import numpy as np
D=OUT/'data/observations/sequence_v4_development'
T=OUT/'tests/sequence_v4'
def main():
    if (D/'PLAN.json').exists():raise RuntimeError('Already registered')
    D.mkdir(exist_ok=True);T.mkdir(exist_ok=True)
    old=[]
    for name in ['recurrence_v3_development','recurrence_v3_structural_candidate']:
        old+=read_json(OUT/f'data/observations/{name}/PLAN.json')['selected_views']
    usedcaps={v['folio_component'] for v in old};usedviews={v['view_id'] for v in old}
    curved={r['view_id'] for r in read_json(OUT/'data/observations/source_adjudication_v2/curved_judgments.json')}
    pool=[]
    for s in read_csv(OUT/'data/source/yale_native_all_manifest.csv'):
        vid=s['view_id'];o=read_json(OUT/f'data/observations/regional_candidates_v11/{vid}.json')
        if vid in usedviews or vid in curved or o['view']['split']=='calibration':continue
        rows=[]
        for l in o['lines']:
            a,b,c,d=l['bbox_xyxy'];body=l['body_height_proxy_px'];n=l['component_count']
            if c-a>=550 and n>=8 and 12<=body<=65:
                rows.append(dict(line_id=l['line_id'],bbox_xyxy=l['bbox_xyxy'],body_height=body,source_line=l))
        if len(rows)<3:continue
        rows=sorted(rows,key=lambda r:(r['bbox_xyxy'][1],r['bbox_xyxy'][0]));ii=np.unique(np.linspace(0,len(rows)-1,min(24,len(rows))).round().astype(int))
        pool.append(dict(view_id=vid,folio_component=o['view']['folio_component'],previous_split=o['view']['split'],native_source=s['path'],rows=[rows[i] for i in ii]))
    reserve=set()
    for lo,hi in [(4,55),(55,106),(106,157),(157,208)]:
        choices=sorted([v for v in pool if lo<=int(v['view_id'][2:])<hi and v['folio_component'] not in usedcaps],key=lambda v:(-len(v['rows']),v['view_id']))
        n=0
        for v in choices:
            if v['folio_component'] in reserve:continue
            reserve.add(v['folio_component']);n+=1
            if n==2:break
    for v in pool:v['split']='test' if v['folio_component'] in reserve else 'development'
    rng=np.random.default_rng(SEED+4)
    rowkeys=[(v['view_id'],i+1) for v in pool for i in range(len(v['rows']))]
    sample=[rowkeys[i] for i in rng.choice(len(rowkeys),24,replace=False)]
    plan=dict(version='V4 source sequence protocol',registered_at_utc=datetime.now(timezone.utc).isoformat(),seed=SEED+4,
      v3_manifest_sha256=sha256(OUT/'data/observations/visual_dataset_v3/FREEZE_MANIFEST.json'),
      v3_model_sha256=sha256(OUT/'data/observations/recurrence_v3_structural_candidate/sealed_class_model.pkl'),
      selection='All previously unselected, non-calibration, non-curved captures with >=3 ordinary geometric row proposals; width>=550 pixels, components>=8, body12..65; evenly sample up to24 fields per capture. No recurrence/class or conventional inputs.',
      fresh_caption_reserve=sorted(reserve),previously_exposed_v3_captions=sorted(usedcaps),selected_views=pool,
      reviewed_scope='Overview triage of each proposed field; native contexts for preregistered and risk samples. Overview triage never certifies faint ink completeness or whole physical row endpoints.',
      taxonomy='Use sealed V3 model and its fourteen validated classes unchanged. ST09 and unreliable source matches are UNK. Whole connected parents are not split across gaps; atomicity and pen lifts unknown.',
      membership='Primary9 contrast after sigma0.8 Gaussian, background25, sensitivities6/12. Retain parent-sized ink and small marks >=8 pixels as explicit candidates. Marks<35px or height<.32body or width<4 are unresolved detached marks, not silently removed. Ink with alternative row support >=.30 best, raster split/merge, drawing contact or field edge remains ambiguous. Very faint contrast6-only ink retained as unresolved region.',
      boundaries=dict(body_gap_hypotheses=[.35,.55,.75],ordering='Increasing native x, physical horizontal coordinate order only; not linguistic reading direction',alternatives='Keep all three partitions; overlay detached include/exclude/attach-to-neighbor and multirow ownership alternatives as constraints, without enumerating exponential combinations. No canonical gap winner.',edge_truncation='Candidate touching local field limit prevents membership completeness; local limits are not line endpoints'),
      review_repeatability=dict(sample=sample,passes=2,masked='Anonymous native RGB contexts, no algorithm class suggestion or previous group/boundary decision shown. Same adjudicator, repeatability only.',criteria='Writing/body membership clear vs uncertain vs drawing; relative gap physically clear vs narrow/competing; detached and connected contacts; no labels from conventional transcriptions.',agreement_target=.85),
      class_generalization_gates=dict(test_captions_min=6,recurring_classes_min=10,training_captions_per_class_min=3,test_instances_per_class_min=5,test_captions_per_class_min=3,positive_pair_agreement_min=.85,source_different_pair_false_grouping_max=.15,threshold_assignment_stability_min=.80,clear_test_class_coverage_min=.50),
      source_pair_audit='Deterministic up to3 fresh test positive and different-class nearest comparisons per validated class; shuffled anonymous source RGB, labels/key hidden until judgments saved; unknown judgments retained.',
      sequence_support_gates=dict(new_views_min=40,new_row_fields_min=600,fresh_test_captions_min=6,ordered_membership_rows_min=.80,complete_parent_membership_groups_min=.80,unknown_parent_rate_max=.20,boundary_ambiguity_rate_max=.20,fully_identified_groups_min=.50,heldout_complete_sequence_recurrence_ge3_min=.20,repeatability_min=.85,all_three_gap_hypotheses_required=True,native_row_endpoint_certification_min=.80),
      gates_rationale='Practical general notation requires broad membership, low ambiguity and majority identified sequences. Endpoint gate is additionally necessary for rank and physical-x assays. These are operational support thresholds, not palaeographic truth.',
      metrics='Use all triaged retained row fields as denominator; excluded fields separately. Unknown class != unknown membership. Complete sequence excludes UNK and unresolved optional/row/edge membership. Recurrence reported all lengths AND >=3 parents, cross-caption only; test match against development only. Caption bootstrap uncertainty. No deletion of unknowns to create false adjacency.',
      null='Within source row shuffle class order, preserve group sizes, parent class frequencies and incomplete flags; compare cross-caption repeated sequence coverage >=3. Null is sequence-order control, not linguistic evidence.',
      failure_policy='Freeze honest partial V4 representation with qualification failed if thresholds fail; never retune V3 or sequence protocol to pass. Notation may remain observational notation only. No downstream assay or crosswalk if support gates fail.',
      prohibited_inputs=['EVA','RF','v101','Currier','inherited hand/section','prior positional outcomes','minimal-pair existence'],
      source_resolution='Use already cached maximum advertised Yale native JPEGs, all frozen in V3. Fresh means outside V3 selected captions, not globally unseen photographs.')
    write_json(D/'PLAN.json',plan);write_json(T/'config.json',{k:v for k,v in plan.items() if k!='selected_views'})
    print('registered',len(pool),'new views',sum(len(v['rows']) for v in pool),'row fields; fresh captions',sorted(reserve),flush=True)
if __name__=='__main__':main()
