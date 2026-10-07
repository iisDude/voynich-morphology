"""Direct source-only judgments; no candidate assignment file read."""
from inventory_v6_common import *
CONTACTS={
 'V_032_P005502':['V_032_P006450','V_032_P006551'],
 'V_032_P006450':['V_032_P005502'],
 'V_032_P006551':['V_032_P005502'],
 'V_032_P006118':['V_032_P006363'],
 'V_032_P006363':['V_032_P006118'],
 'V_170_P006571':['V_170_P006736'],
 'V_170_P006736':['V_170_P006571']}
NONWRITING={'V_094_P012762','V_094_P013039'}
UNRESOLVED={'V_032_P006717','V_094_P012984'}
INSUFFICIENT={'V_094_P012891','V_170_P006374'}
NEIGHBOR={'V_032_P006714','V_170_P006925'}
def main():
    guard()
    if (D/'FRESH_SOURCE_SEAL.json').exists():raise RuntimeError('Source already sealed')
    if (D/'fresh_assignments.json').exists():raise RuntimeError('Source must precede candidate suggestions')
    rows=read_json(D/'fresh_parent_location_aids.json')
    for r in rows:
        pid=r['parent_id'];r['source_review']='Native RGB parent galleries and full source contexts; no V6 class suggestion or conventional strings. Same AI adjudicator.'
        r['membership']='confirmed_nonwriting' if pid in NONWRITING else 'unresolved' if pid in UNRESOLVED else 'confirmed_writing'
        r['source_parent_status']='possible_contact' if pid in CONTACTS else 'insufficient_photographic_evidence' if pid in INSUFFICIENT else 'not_writing_parent' if r['membership']!='confirmed_writing' else 'confirmed_connected_writing_trace'
        r['possible_contacts']=CONTACTS.get(pid,[]);r['row_ownership']='neighbor' if pid in NEIGHBOR else 'selected_field' if r['membership']=='confirmed_writing' else 'unknown'
        r['source_note']='Visible ordinary brown writing trace. A threshold-connected box is a location aid, not an atomicity or pen-lift assertion.'
        if pid in NONWRITING:r['source_note']='Green drawing/paint region at field boundary, not ordinary brown horizontal writing.'
        if pid in UNRESOLVED:r['source_note']='Small/diffuse contrast close to visible writing/drawing cannot establish writing membership from this photograph.'
        if pid in INSUFFICIENT:r['source_note']='Writing is visible but whole-parent form is too faint or interferes with drawing edge; morphology insufficient.'
        if pid in CONTACTS:r['source_note']='Neighboring brown writing structures visibly approach/overlap; faint connection could change the whole parent. Separate raster objects are retained as unresolved contact alternatives.'
        if pid in NEIGHBOR:r['source_note']='Clear lower neighboring-row upright/loop writing. Kept in confirmed-writing validation with neighboring ownership disclosed; not treated as target-row completeness.'
        if r['field_edge']:r['source_note']+=' Parent extends beyond local geometric safe field; full native parent is visible in padded RGB, not clipped.'
    save(D/'fresh_source_reference.json',dict(created_at_utc=now(),parents=rows,all_proposals_reviewed=True,membership_before_candidate_suggestions=True,scope='Three local fields, not exhaustive ordinary-row truth; no sequence extraction from these fields.'))
    seal([D/'fresh_source_reference.json',D/'fresh_parent_location_aids.json',D/'fresh_shapes.npz',D/'fresh_contexts.json',Path(__file__)],D/'FRESH_SOURCE_SEAL.json')
    from collections import Counter
    print(Counter(r['membership'] for r in rows),Counter(r['source_parent_status'] for r in rows),flush=True)
if __name__=='__main__':main()
