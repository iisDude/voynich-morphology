"""Read-only frozen inputs; audit report written outside the frozen dataset."""
from common import OUT,ROOT,read_json,read_csv,write_json,sha256
from collections import Counter,defaultdict
from PIL import Image
from datetime import datetime,timezone
import pickle,numpy as np
from evaluate_source_classes_v3 import transform,assign

def main():
    dest=OUT/'data/observations/visual_dataset_v3';checks=[];bad=[];total=0
    for v in ['v0','v11','v2','v3']:
        path=OUT/f'data/observations/visual_dataset_{v}/FREEZE_MANIFEST.json';m=read_json(path);fails=[]
        for r in m['files']:
            total+=1
            if not (OUT/r['path']).exists() or sha256(OUT/r['path'])!=r['sha256']:fails.append(r['path'])
        checks.append(dict(version=v,files_checked=len(m['files']),failures=fails,manifest_sha256=sha256(path)));bad+=fails
        print('integrity',v,len(m['files']),'failures',len(fails),flush=True)
    evidence=read_csv(OUT/'data/source/evidence_manifest.csv');original_bad=[r['path'] for r in evidence if sha256(ROOT/r['path'])!=r['sha256']];bad+=original_bad
    parents=read_json(dest/'source_parent_segmentation.json');groups=read_json(dest/'competing_group_hypotheses.json');lookup={r['parent_id']:r for r in parents};core=read_json(dest/'freeze_qualification.json')['core_classes']
    assert len(lookup)==len(parents),'Duplicate native parent identity'
    assert all(not r['structural_class'] or (r['structural_class'] in core and r['class_eligible'] and r['threshold_class_stable'] and r['alignment_class_stable']) for r in parents)
    assert all(set(g['parent_ids'])<=set(lookup) for g in groups)
    used=Counter(i for g in groups if g['gap_body']==.55 for i in g['parent_ids']);assert all(n==1 for n in used.values()),'Same source parent counted twice within one gap hypothesis'
    # A source-only sealed-model rerun confirms test assignments; it never refits a class.
    base=OUT/'data/observations/recurrence_v3_structural_candidate';rec=read_json(base/'source_parents.json');data=np.load(base/'source_shapes.npz');model=pickle.loads((base/'sealed_class_model.pkl').read_bytes());ii=np.array([i for i,r in enumerate(rec) if r['split']=='test' and r['class_eligible']]);pred=assign(transform(data['shapes'][ii],data['geometry'][ii],model),data['geometry'][ii],model);saved={r['parent_id']:r for r in read_json(base/'heldout_class_assignments.json') if r['split']=='test'}
    assert all((saved[rec[i]['parent_id']]['class_id']==str(pred['classes'][j])) if pred['accepted'][j] else saved[rec[i]['parent_id']]['class_id'] is None for j,i in enumerate(ii))
    plan=read_json(base/'PLAN.json');sets={s:set(v['folio_component'] for v in plan['selected_views'] if v['split']==s) for s in ['train','validation','test']};assert not (sets['train']&sets['test'] or sets['validation']&sets['test'] or sets['train']&sets['validation'])
    # Make non-finite exports fail loudly; unknown distances must be JSON null.
    for path in [base/'heldout_class_assignments.json',dest/'source_parent_segmentation.json',dest/'model_contract.json']:
        import json
        json.loads(path.read_text(encoding='utf-8'),parse_constant=lambda x:(_ for _ in ()).throw(ValueError('Non-finite JSON value '+x)))
    assert not bad,bad[:10]
    result=dict(time_utc=datetime.now(timezone.utc).isoformat(),freeze_checks=checks,original_files_checked=len(evidence),original_failures=original_bad,total_frozen_file_checks=total,unique_parent_records=len(parents),core_classes=len(core),group_parent_conservation=True,native_parent_no_duplicate_counts=True,caption_splits_disjoint=True,sealed_test_assignments_reproduced=len(ii),all_pass=True,no_positional_assay_run=True)
    write_json(OUT/'tests/recurrence_v3_development/final_freeze_audit.json',result);print('FINAL AUDIT PASS',total,'frozen file checks,',len(evidence),'originals',len(ii),'test assignments',flush=True)

if __name__=='__main__':main()
