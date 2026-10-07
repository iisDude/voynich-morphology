"""Prior-use audit projects caption/parent/source metadata only; no class values."""
from direct_morphology2_common import *
from common import read_csv
import re
def main():
    guard();assert not (D/'SELECTION_SEAL.json').exists()
    for p in [D,T,G]:p.mkdir(parents=True,exist_ok=True)
    fields=read_json(OUT/'data/observations/sequence_v4_development/source_rows.json');mapping=read_csv(OUT/'data/source/page_folio_map.csv');viewcap={f"V_{int(r['pdf_page']):03d}":re.search(r'\d+',r['caption']).group() for r in mapping if re.match(r'^\d+',r['caption'])};caps=sorted(set(viewcap.values()),key=int);use={c:set(['earlier_native_overview_or_processing']) for c in caps};evidence=[dict(path='data/source/page_folio_map.csv',sha256=sha256(OUT/'data/source/page_folio_map.csv'),projected_fields=['pdf_page','caption'])];lookup={};crop_lookup={}
    for r in fields:use[str(r['folio_component'])].add('V4_frozen_model_application')
    inputs=[('recurrence_v3_development/source_parents.json','V3_parent_analysis'),('recurrence_v3_structural_candidate/source_parents.json','V3_parent_analysis'),('sequence_v4_development/source_parents.json','V4_parent_model_application'),('structural_inventory_v6_development/discovery_parents.json','V5_V6_detailed_parent_source'),('structural_inventory_v6_development/fresh_source_reference.json','V6_detailed_parent_source'),('neutral_feature_trial_v1/parent_feature_profiles.json','FeatureTrial1_input_and_revision_evidence'),('neutral_feature_trial2/source_location_aids.json','FeatureTrial2_specification_and_validation_corpus'),('direct_morphology_trial1/source_parent_ensembles.json','DirectTrial1_corpus')]
    for rel,label in inputs:
        p=OUT/'data/observations'/rel;raw=read_json(p);rows=raw['parents'] if isinstance(raw,dict) else raw;evidence.append(dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p),projected_fields=['caption','folio_component','parent_id','native_crop','split']))
        for r in rows:
            c=str(r.get('caption',r.get('folio_component','')))
            if c not in use:continue
            use[c].add(label)
            if r.get('parent_id'):lookup[r['parent_id']]=c
            if r.get('native_crop'):crop_lookup[r['native_crop']]=c
            if label=='V3_parent_analysis' and r.get('split')=='train':use[c].add('V3_parent_morphology_fit')
            if label=='V3_parent_analysis' and r.get('split')=='validation':use[c].add('V3_morphology_model_selection')
    # Known reference use from source-only V5 rows; no class-assignment file opened.
    p=OUT/'data/observations/visual_dataset_v5/source_reference.json';raw=read_json(p);evidence.append(dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p),projected_fields=['rows.caption']))
    for r in raw['rows']:
        c=str(r['caption'])
        if c in use:use[c].add('V5_detailed_row_source')
    pair_inputs=[('recurrence_v3_development/pair_audit_key.json','V3_previous_source_similarity'),('recurrence_v3_structural_candidate/pair_audit_key.json','V3_previous_source_similarity'),('sequence_v4_development/class_pair_key.json','V4_previous_source_similarity'),('structural_inventory_v6_development/pair_audit_hidden_key.json','V6_previous_source_similarity')]
    unknown_refs=[]
    for rel,label in pair_inputs:
        p=OUT/'data/observations'/rel;rows=read_json(p);evidence.append(dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p),projected_fields=['folio_component','left_parent','right_parent','parent_id','left','right','left_crop','right_crop']))
        for r in rows:
            if str(r.get('folio_component','')) in use:use[str(r['folio_component'])].add(label)
            for k in ['left_parent','right_parent','parent_id','left','right','left_crop','right_crop']:
                val=r.get(k)
                if not isinstance(val,str):continue
                c=lookup.get(val,crop_lookup.get(val));view=re.search(r'V_\d{3}',val)
                if c is None and view:c=viewcap.get(view.group())
                if c in use:use[c].add(label)
                elif val.endswith('.png') or '_P' in val or '_O' in val:unknown_refs.append(dict(path=rel,field=k,reference=val))
    # All old feature/direct captions are conservatively excluded regardless of specific pair involvement.
    exclude={'V3_parent_analysis','V5_V6_detailed_parent_source','V6_detailed_parent_source','FeatureTrial1_input_and_revision_evidence','FeatureTrial2_specification_and_validation_corpus','DirectTrial1_corpus','V5_detailed_row_source','V3_previous_source_similarity','V4_previous_source_similarity','V6_previous_source_similarity'}
    rows=[dict(caption=c,prior_use=sorted(use[c]),eligible_for_new_caption_validation=not bool(use[c]&exclude),reasons_excluded=sorted(use[c]&exclude),globally_unseen_image=False) for c in caps];eligible=[r['caption'] for r in rows if r['eligible_for_new_caption_validation']]
    save(D/'CAPTION_ELIGIBILITY.json',dict(audited_at_utc=now(),captions=rows,eligible_captions=eligible,evidence=evidence,unresolved_prior_pair_references=unknown_refs,meaning_of_fresh='New to prior V3 detailed parent/morphology fitting/selection, V5/V6 detailed source corpora, feature-trial inputs/specification, direct Trial1 corpus and known prior source-similarity pair sets. V4 broad parent extraction/application and older native overview exposure remain, so not globally unseen photography. Audit uses source identifiers only; no class labels or prohibited metadata values inspected.',selection_pending=True))
    print('Audited',len(rows),'captions;',len(eligible),'eligible; unresolved pair references',len(unknown_refs),flush=True);print('Eligible',eligible,flush=True)
    # Source-layout candidates only. Large first clear field scope, no morphology selection.
    options=[]
    for c in eligible:
        rr=[r for r in fields if str(r['folio_component'])==c and r['status']=='triaged_local_writing_field' and r['safe_x'][1]-r['safe_x'][0]>=650]
        if rr:
            r=sorted(rr,key=lambda r:(r['view_id'],r['row_number']))[0];options.append({k:r[k] for k in ['view_id','row_number','native_source','source_row_bbox','safe_x','body_height','body_path_knots','folio_component']})
    save(D/'SOURCE_LAYOUT_OPTIONS.json',options);print('Layout candidates',[(r['folio_component'],r['view_id']) for r in options],flush=True)
if __name__=='__main__':main()
