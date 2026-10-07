"""Register a source-only recurrence investigation; V2 is strictly read-only."""
from common import OUT,read_json,read_csv,write_json,write_csv,sha256,SEED
from datetime import datetime,timezone
from collections import defaultdict
import numpy as np

ROOT3=OUT/'data/observations/recurrence_v3_development'
def main():
    ROOT3.mkdir(exist_ok=True);test=OUT/'tests/recurrence_v3_development';test.mkdir(exist_ok=True)
    if (ROOT3/'PLAN.json').exists():raise ValueError('Already registered')
    frozen=OUT/'data/observations/visual_dataset_v2/FREEZE_MANIFEST.json';manifest=read_json(frozen)
    bad=[r['path'] for r in manifest['files'] if sha256(OUT/r['path'])!=r['sha256']]
    if bad:raise ValueError('V2 changed '+str(bad[:5]))
    write_json(test/'v2_initial_integrity.json',dict(manifest_sha256=sha256(frozen),files_checked=len(manifest['files']),failures=bad))
    sources={r['view_id']:r for r in read_csv(OUT/'data/source/yale_native_all_manifest.csv')};curved={r['view_id'] for r in read_json(OUT/'data/observations/source_adjudication_v2/curved_judgments.json')};pool=[]
    for vid,s in sources.items():
        obj=read_json(OUT/f'data/observations/regional_candidates_v11/{vid}.json');w=int(s.get('native_width',s.get('width',0)) or 0)
        if vid in curved or obj['view']['split']=='calibration':continue
        rows=[]
        for line in obj['lines']:
            a,b,c,d=line['bbox_xyxy'];body=line['body_height_proxy_px'];n=line['component_count'];contact=line['multiline_component_count']/max(1,n)
            if c-a<550 or n<8 or body<12 or body>65:continue
            score=contact+(d-b)/body*.12
            rows.append(dict(view_id=vid,line_id=line['line_id'],bbox_xyxy=line['bbox_xyxy'],body_height=body,contacts=contact,components=n,ordinary_score=score,source_line=line))
        if len(rows)>=3:pool.append(dict(view_id=vid,split=obj['view']['split'],folio_component=obj['view']['folio_component'],native_source=s['path'],eligible_rows=len(rows),rows=rows))
    selected=[]
    # Fixed source-geometry coverage quota; no unit assignments or text metadata.
    for lo,hi in [(4,55),(55,106),(106,157),(157,208)]:
        for split,quota in [('train',8),('validation',3),('test',3)]:
            choices=sorted([r for r in pool if lo<=int(r['view_id'][2:])<hi and r['split']==split],key=lambda r:(-min(r['eligible_rows'],24),r['view_id']))[:quota]
            for v in choices:
                # Review up to 24 candidates per view, ordinary risk first but sample full height.
                rr=sorted(v['rows'],key=lambda r:(r['ordinary_score'],r['line_id']))[:32];rr=sorted(rr,key=lambda r:r['bbox_xyxy'][1]);idx=np.unique(np.linspace(0,len(rr)-1,min(24,len(rr))).round().astype(int));v=dict(v,rows=[rr[int(i)] for i in idx]);selected.append(v)
    plan=dict(registered_at_utc=datetime.now(timezone.utc).isoformat(),seed=SEED,question='Why is manuscript-derived visual-form recurrence sparse? Separate coverage, membership/boundary and class-specificity contributions.',v2_immutable_manifest_sha256=sha256(frozen),source_corpus='Highest-resolution local Yale imagery, ordinary-row proposals selected by physical geometry and manuscript-order/split coverage only',selection='Up to 8 train,3 validation,3 test views in each of 4 manuscript-order strata; up to 24 ordinary candidates per view. Risk targets straight/simple rows, not effect-supporting groups.',selected_views=selected,proposed_rows=sum(len(v['rows']) for v in selected),forbidden_inputs=['EVA','RF','v101','Currier','inherited hand/section','positional outcomes','minimal-pair support'],row_review='Every proposed row reviewed in native RGB and ownership context; source endpoints, body membership, drawing and detached marks handled separately. Clear local units may be usable even if full row endpoint unknown; no position eligibility gate for recurrence.',coverage_accounting='Observed pipeline losses only; unreviewed images not imputed. Separate full-line certification losses from local membership and family rejection. Within fixed source cohort compare classifier specificity, matched sample sizes and caption-block resampling.',classes='Whole connected assemblies primary; topology/connectivity/relative geometry and image similarity; lower/upper factor signatures and detached-component alternatives. No linguistic letters or word assumption.',candidates='Source-trained image/geometry families K=16,24,32,48,64; topology-constrained and image-only competitors. Validation uses held-out image loss and source pair judgments; token/minimal-pair counts never choose merges.',heldout='Existing caption-connected splits; model/config locked before test assignment evidence inspected. Source membership review can inspect test rows without using algorithm class suggestions. Prior exposure acknowledged; no new blind claim.',perturbations='Native contrast 6/9/12 and small alignment/slant nuisance transforms; topology changes cause abstention/alternatives, not forced matching.',freeze_requirements=dict(source_rows_reviewed_at_least=600,source_views_at_least=40,test_caption_groups_at_least=6,stable_recurring_structural_classes_at_least=10,each_core_class_training_captions_at_least=3,each_core_class_test_instances_at_least=5,each_core_class_test_captions_at_least=3,source_pair_audit_positive_agreement_at_least=.85,hard_negative_false_acceptance_at_most=.15,threshold_assignment_stability_at_least=.80,clear_test_component_assignment_coverage_at_least=.50),failure_policy='Preserve unknowns and competing systems. No V3 freeze merely because counts improve. Failed held-out criteria require a development report and a new source-only candidate with separately reserved evidence, not test tuning.',downstream='No positional rerun. Only reconsider assays after a validated new freeze; current work does not run them.')
    write_json(ROOT3/'PLAN.json',plan);write_json(test/'analysis_plan.json',{k:v for k,v in plan.items() if k!='selected_views'});write_csv(ROOT3/'selected_rows.csv',[{k:r[k] for k in ['view_id','line_id','bbox_xyxy','body_height','contacts','components','ordinary_score']} for v in selected for r in v['rows']]);print('Selected',len(selected),'views',plan['proposed_rows'],'ordinary row proposals',flush=True)
if __name__=='__main__':main()
