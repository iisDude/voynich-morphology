"""Freeze a second, explicitly post-exposure candidate dataset without refitting."""
from common import OUT,read_json,write_json,write_csv,sha256
from build_visual_dataset import measurement
from datetime import datetime,timezone
from jsonschema import Draft202012Validator

def main():
    root=OUT/'data/observations/visual_dataset_v11';freeze=root/'FREEZE_MANIFEST.json'
    if freeze.exists():raise ValueError('Do not overwrite frozen v11')
    checks=read_json(OUT/'tests/candidate_integrity_v1/results.json')
    assert checks['status']=='passed' and checks['views']==204
    review=read_json(OUT/'data/observations/assigned_visual_candidates_v11/tracked_row_source_audit_reviewed.json');assert len(review['rows'])==32
    validator=Draft202012Validator(read_json(OUT/'data/observations/annotation_schema.json'))
    reg={r['view_id']:r for r in read_json(OUT/'data/source/yale_registration_all.json')};coverage=[];allgroups=[]
    source=OUT/'data/observations/regional_candidates_v11'
    for path in sorted(source.glob('V_*.json')):
        if not path.stem[2:].isdigit():continue
        obj=read_json(path);assigned=read_json(OUT/f'data/observations/assigned_visual_candidates_v11/{path.name}');vid=path.stem
        dataset=dict(schema_version='0.1.0',status='frozen',provenance=dict(source_pdf_sha256='b048d09835c66522cc7a6d93e3edf4693edacc403aa79f738c47a421d840f761',prior_exposure='Second source-only repair after conventional/statistical exposure; no renewed blind claim. Original prototype definitions and gates transferred without refitting.',comparison_data_withheld=False,run_id='tracked_snapshot_v11',frozen_sha256=None),
          views=[dict(view_id=vid,pdf_page=int(obj['view']['pdf_page']),image_sha256=obj['image_sha256'],image_path=obj['native_source'],width_px=reg[vid]['native_width'],height_px=reg[vid]['native_height'],split=obj['view']['split'])],panels=[],lines=[],groups=[],components=[],assemblies=[],segmentations=[],observations=[],hypotheses=[])
        def loc(bbox):return dict(view_id=vid,image_sha256=obj['image_sha256'],bbox_xyxy=bbox,coordinate_frame='native_yale_image')
        for line in obj['lines']:
            pts=[[float(x),max(0.,float(y))] for x,y in line['baseline_polyline_xy']]
            dataset['lines'].append(dict(line_id=line['line_id'],location=loc(line['bbox_xyxy']),panel_id=None,region_id=line['region_id'],path_kind='linear',path_points=pts,baseline_points=pts,confidence='low',measurements={'body_height_proxy':measurement(line['body_height_proxy_px'],'native_pixel','area-weighted component-height proxy with local density track; no true x-height certification')}))
        bygroup={}
        for rec in obj['instances']:
            if rec['model']=='fine_components':bygroup.setdefault(rec['group_id'],[]).append(rec)
        for rec in obj['instances']:
            u=assigned['units'].get(rec['instance_id']);family=u['family'] if u and u['admitted'] else None
            measures={k:measurement(v,'dimensionless' if 'ratio' in k or 'body2' in k else 'raster_count_or_pixel','exact assigned native mask; estimated local density baseline/body') for k,v in rec['features'].items() if isinstance(v,(int,float))}
            if rec['model']=='fine_components':
                children=[rec['instance_id']];dataset['components'].append(dict(component_id=rec['instance_id'],location=loc(rec['bbox_xyxy']),quality='limited',confidence='low' if family else 'unresolved',measurements=measures,quality_flags=['raster component, not pen stroke','omitted writing and drawing contamination known','threshold/contact sensitive']))
            else:
                x,y,c,d=rec['bbox_xyxy'];children=[r['instance_id'] for r in bygroup.get(rec['group_id'],[]) if min(c,r['bbox_xyxy'][2])>max(x,r['bbox_xyxy'][0]) and min(d,r['bbox_xyxy'][3])>max(y,r['bbox_xyxy'][1])]
            dataset['assemblies'].append(dict(assembly_id=rec['instance_id']+'_A',location=loc(rec['bbox_xyxy']),group_id=rec['group_id'],component_ids=children,candidate_family_id=family,confidence='low' if family else 'unresolved',measurements=measures,alternatives=[],description=rec['model']+': geometric hypothesis; pen lift and atomic identity unresolved'))
        for group in assigned['groups']:
            assert all(group.get(k) is None for k in ['section','hand','currier','conventional_mapping'])
            allgroups.append(group);ids=[f'{group["group_id"]}_SEG_{m}' for m in group['models']]
            dataset['groups'].append(dict(group_id=group['group_id'],line_id=group['line_id'],location=loc(group['bbox_xyxy']),boundary_confidence='low',alternatives=ids,measurements={'ordinal_group_rank':measurement(group['normalized_group_rank'],'ordinal_fraction','rank among all primary gray-gap candidates'), 'native_pixel_x':measurement(group['source_pixel_center_x'],'native_pixel','assigned-mask group bbox centre'), 'normalized_line_pixel_x':measurement(group['normalized_pixel_center'],'pixel_fraction','group bbox centre relative to assigned row ink extent')}))
            for model,nodes in group['models'].items():dataset['segmentations'].append(dict(segmentation_id=f'{group["group_id"]}_SEG_{model}',target_id=group['group_id'],node_ids=[i+'_A' for i in nodes],model_kind={'fine_components':'fine_components','medium_assemblies':'assemblies','compound_candidates':'compound','group_only':'group_only'}[model],relations=[],supporting_observations=[],contradicting_observations=[],status='open'))
        dataset['hypotheses'].append(dict(hypothesis_id=vid+'_TRACKED_BOUNDARIES',proposition='Local density tracking improves some candidate writing flows; four geometric partitions still compete and complete writing membership is unvalidated.',supporting_observations=[],contradicting_observations=[],falsifier='Independent source review finds missing writing, drawings or inconsistent reusable structures.',confidence='unresolved',next_test='Post-snapshot positional/context tests and source-audited conventional crosswalk; no inherited boundary truth.'))
        validator.validate(dataset);write_json(root/path.name,dataset)
        coverage.append(dict(view_id=vid,split=obj['view']['split'],lines=len(dataset['lines']),groups=len(dataset['groups']),fine_components=len(dataset['components']),assemblies=len(dataset['assemblies']),admitted_fine_groups=sum(bool(g['visual_fine_units']) for g in assigned['groups']),admitted_medium_groups=sum(bool(g['primary_candidate_units']) for g in assigned['groups']),schema_valid=True))
        print(vid,len(dataset['groups']),flush=True)
    assert len(coverage)==204
    write_csv(root/'coverage.csv',coverage);write_json(root/'assay_groups.json',allgroups)
    patterns=['data/observations/visual_dataset_v11/*','data/observations/regional_candidates_v11/*','data/observations/assigned_visual_candidates_v11/*','data/observations/extraction_v11_protocol.json','tests/candidate_integrity_v1/*','data/observations/visual_family_models_v4/*','data/observations/*family_source_review_v4.json']
    files=sorted(set(p for pattern in patterns for p in OUT.glob(pattern) if p.is_file()))
    files+= [OUT/'src'/name for name in ['regional_extract_v11.py','prepare_extraction_v11.py','assign_v11_frozen_prototypes_v1.py','record_tracked_row_review_v1.py','verify_candidate_partitions_v1.py','build_tracked_snapshot_v1.py']]
    write_json(freeze,dict(snapshot_id='tracked_visual_candidate_v11',frozen_at_utc=datetime.now(timezone.utc).isoformat(),status='Frozen partial/failed candidate ensemble, not a certified alphabet or complete segmentation',views=204,canonical_grapheme_claim=False,comparison_transcription_contents_opened=True,exposure='Post-exposure source-only repair; original prototype/gate definitions unchanged. Test split is diagnostic, not newly blind.',original_visual_freeze_sha256=sha256(OUT/'data/observations/visual_dataset_v0/FREEZE_MANIFEST.json'),files=[dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p),bytes=p.stat().st_size) for p in files],unresolved=['Physical panels and bifolios not reconstructed','Circular, sparse, rotated and separate writing flows remain incomplete','Baseline and body heights are proxies','Missing faint/detached writing and drawing/contact contamination persist','Gray gaps and connected components are not established words or signs','Pen lifts and stroke order unresolved']))
    print('Frozen second snapshot',sha256(freeze),len(allgroups),'candidate groups',flush=True)

if __name__=='__main__':main()
