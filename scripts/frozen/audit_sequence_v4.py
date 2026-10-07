"""Meaningful read-only conservation, source traceability and frozen inference audit."""
from common import OUT,ROOT,read_json,read_csv,write_json,sha256
from register_sequence_v4 import D,T
from build_sequence_model_v4 import F
from evaluate_source_classes_v3 import transform,assign
from PIL import Image
from collections import Counter
import numpy as np,pickle,json
def main():
    parents=read_json(F/'source_parent_states.json');raw=read_json(D/'source_parents.json');ids={r['parent_id'] for r in parents};assert len(ids)==len(parents)
    assert ids=={r['parent_id'] for r in raw};groups=read_json(F/'competing_group_sequences.json');rows=read_json(F/'row_sequences.json');optional=read_json(F/'optional_membership_constraints.json');lookup={r['parent_id']:r for r in parents}
    allrowids=[p for r in rows for p in r['parent_ids']];assert len(set(allrowids))==len(allrowids)
    optionalids=[r['parent_id'] for r in optional];assert len(set(optionalids))==len(optionalids);assert not set(allrowids)&set(optionalids)
    excluded={r['parent_id'] for r in parents if r['writing_membership']=='nonwriting'};assert set(allrowids)|set(optionalids)|excluded==ids
    for threshold in [.35,.55,.75]:
        gg=[g for g in groups if g['gap_body']==threshold];seen=Counter(p for g in gg for p in g['parent_ids']);assert set(seen)==set(allrowids);assert all(n==1 for n in seen.values())
        for g in gg:
            assert len(g['sequence'])==len(g['parent_ids']);assert g['sequence']==[lookup[p]['structural_class'] or 'UNK' for p in g['parent_ids']]
            if g['complete_sequence']:assert g['model_membership_complete'] and 'UNK' not in g['sequence'] and not g['optional_parent_ids']
    valid={'UNK'}|{f'ST{i:02d}' for i in range(1,16) if i!=9};assert all(s in valid for r in rows for s in r['sequence'])
    dims={}
    for r in parents:
        p=OUT/r['native_source'];assert p.resolve().is_relative_to(ROOT)
        if p not in dims:dims[p]=Image.open(p).size
        a,b,c,d=r['native_bbox'];w,h=dims[p];assert 0<=a<c<=w and 0<=b<d<=h
    plan=read_json(D/'PLAN.json');testcaps={v['folio_component'] for v in plan['selected_views'] if v['split']=='test'};devcaps={v['folio_component'] for v in plan['selected_views'] if v['split']=='development'};assert not testcaps&devcaps;assert not testcaps&set(plan['previously_exposed_v3_captions'])
    v3=OUT/'data/observations/recurrence_v3_structural_candidate';assert sha256(v3/'sealed_class_model.pkl')==plan['v3_model_sha256'];model=pickle.loads((v3/'sealed_class_model.pkl').read_bytes());data=np.load(D/'source_shapes.npz');q=[r for r in raw if r['shape_index'] is not None];ii=np.array([r['shape_index'] for r in q]);a=assign(transform(data['shapes'][ii],data['geometry'][ii],model),data['geometry'][ii],model)
    mismatch=[]
    for j,r in enumerate(q):
        cid=str(a['classes'][j]) if np.isfinite(a['distance'][j]) else None
        if cid!=r['proposed_class'] or bool(a['accepted'][j])!=r['nominal_accepted']:mismatch.append(r['parent_id'])
    assert not mismatch
    # Every optional or compound has explicit alternatives and no canonical resolution.
    assert all(r['canonical_choice'] is None and len(r['alternatives'])>=2 for r in optional)
    for base in [D,F,T]:
        for p in base.glob('*.json'):json.loads(p.read_text(encoding='utf-8'),parse_constant=lambda x:(_ for _ in ()).throw(ValueError('Nonfinite JSON '+x)))
    result=dict(unique_parent_candidates=len(ids),primary_parents_conserved=len(allrowids),optional_regions_conserved=len(optionalids),source_nonwriting_preserved=len(excluded),three_gap_hypotheses_parent_conservation=True,source_native_bbox_checks=len(parents),fresh_caption_separation=True,sealed_v3_nominal_inferences_reproduced=len(q),inference_mismatches=mismatch,strict_finite_json=True,classes_unchanged=True)
    target=OUT/'tests/sequence_v4_postfreeze' if (F/'FREEZE_MANIFEST.json').exists() else T;target.mkdir(exist_ok=True)
    if (F/'FREEZE_MANIFEST.json').exists():
        checks=[]
        for version in ['v0','v11','v2','v3','v4']:
            p=OUT/f'data/observations/visual_dataset_{version}/FREEZE_MANIFEST.json';m=read_json(p);bad=[r['path'] for r in m['files'] if sha256(OUT/r['path'])!=r['sha256']];checks.append(dict(version=version,manifest_sha256=sha256(p),files_checked=len(m['files']),failures=bad));print(version,len(m['files']),len(bad),flush=True)
        assert all(not c['failures'] for c in checks);result['freeze_checks']=checks
    original=read_csv(OUT/'data/source/evidence_manifest.csv');root_bad=[r['path'] for r in original if sha256(ROOT/r['path'])!=r['sha256']];assert not root_bad
    result['original_root_inputs_checked']=len(original);result['original_root_input_failures']=root_bad
    write_json(target/'conservation_and_integrity.json',result);print(result,flush=True)
if __name__=='__main__':main()
