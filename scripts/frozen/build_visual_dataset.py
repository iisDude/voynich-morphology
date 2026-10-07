"""Build a schema-conforming neutral dataset, with explicit unknowns.

Writing-unit identities remain candidate hypotheses. Conventional data must
remain unopened until freeze_visual_dataset records this complete snapshot.
"""
from common import OUT,read_json,write_json,write_csv,sha256,SEED
import numpy as np
from PIL import Image,ImageDraw
from jsonschema import Draft202012Validator


def measurement(value,unit,method):
    return dict(value=value,unit=unit,method=method,uncertainty='unestimated',missing_reason=None)


def main():
    root=OUT/'data/observations/visual_dataset_v0';root.mkdir(parents=True,exist_ok=True)
    schema=read_json(OUT/'data/observations/annotation_schema.json');validator=Draft202012Validator(schema)
    reviews=read_json(OUT/'data/observations/fine_family_source_review_v4.json')['records']
    fine_review={r['family_id']:r for r in reviews};registrations={r['view_id']:r for r in read_json(OUT/'data/source/yale_registration_all.json')}
    summaries=[];assays=[];audit_pool=[];seen_audit=read_json(OUT/'data/observations/heldout_source_audit_v4_reviewed.json')
    used_folios=set()
    for path in sorted((OUT/'data/observations/assigned_visual_candidates_v4').glob('V_*.json')):
        if not path.stem[2:].isdigit():continue
        a=read_json(path);obj=read_json(OUT/f'data/observations/regional_candidates_v4/{path.name}');vid=path.stem;reg=registrations[vid]
        dataset=dict(schema_version='0.1.0',status='draft',provenance=dict(
            source_pdf_sha256='b048d09835c66522cc7a6d93e3edf4693edacc403aa79f738c47a421d840f761',
            prior_exposure='Supplied handoff, chats and ledger contain conventional examples; transcription contents withheld throughout visual derivation.',
            comparison_data_withheld=True,run_id='visual_snapshot_v0',frozen_sha256=None),
            views=[dict(view_id=vid,pdf_page=int(obj['view']['pdf_page']),image_sha256=obj['image_sha256'],
                image_path=obj['native_source'],width_px=reg['native_width'],height_px=reg['native_height'],split=obj['view']['split'])],
            panels=[],lines=[],groups=[],components=[],assemblies=[],segmentations=[],observations=[],hypotheses=[])
        def location(bbox):return dict(view_id=vid,image_sha256=obj['image_sha256'],bbox_xyxy=bbox,coordinate_frame='native_yale_image')
        line_records={r['line_id']:r for r in obj['lines']}
        for line in obj['lines']:
            x,y,c,d=line['bbox_xyxy'];xx=line['baseline_xref'];yy=line['baseline_y_at_xref'];sl=line['baseline_slope']
            pts=[[x,max(0,yy+sl*(x-xx))],[c,max(0,yy+sl*(c-xx))]]
            dataset['lines'].append(dict(line_id=line['line_id'],location=location(line['bbox_xyxy']),panel_id=None,
                region_id=line['region_id'],path_kind='linear',path_points=pts,baseline_points=pts,confidence='low',
                measurements={'body_height_proxy':measurement(line['body_height_proxy_px'],'native_pixel','area-weighted component-bottom baseline proposal; not a measured x-height truth')}))
        group_components={};byid={r['instance_id']:r for r in obj['instances']}
        for r in obj['instances']:
            if r['model']=='fine_components':group_components.setdefault(r['group_id'],[]).append(r)
        for r in obj['instances']:
            u=a['units'][r['instance_id']];model=r['model'];measurements={k:measurement(v,'dimensionless' if 'ratio' in k or 'body2' in k else 'raster_count_or_pixel','exact assigned native mask; provisional baseline/body') for k,v in r['features'].items() if isinstance(v,(int,float))}
            if model=='fine_components':
                review=fine_review[u['nearest_family_id']];eligible=u['recognized_within_training_radius'] and review['prototype_gate_eligible']
                dataset['components'].append(dict(component_id=r['instance_id'],location=location(r['bbox_xyxy']),quality='limited',
                    confidence='low' if eligible else 'unresolved',measurements=measurements,
                    quality_flags=['threshold-sensitive raster object; not pen stroke','detached or faint ink may be omitted',review['review_category']]))
                children=[r['instance_id']];family=u['nearest_family_id'] if eligible else None
            else:
                x,y,c,d=r['bbox_xyxy'];children=[f['instance_id'] for f in group_components.get(r['group_id'],[]) if
                    min(c,f['bbox_xyxy'][2])>max(x,f['bbox_xyxy'][0]) and min(d,f['bbox_xyxy'][3])>max(y,f['bbox_xyxy'][1])]
                family=u['unit_identity'] if model=='medium_assemblies' else None
            assembly_id=r['instance_id']+'_A'
            dataset['assemblies'].append(dict(assembly_id=assembly_id,location=location(r['bbox_xyxy']),group_id=r['group_id'],
                component_ids=children,candidate_family_id=family,confidence='low' if family else 'unresolved',measurements=measurements,
                alternatives=[],description=f'{model}: reversible pixel-derived subdivision; atomic identity, pen lift and stroke order unresolved'))
        for g in a['groups']:
            fine=[a['units'][i] for i in g['models']['fine_components']]
            admitted=[u['recognized_within_training_radius'] and fine_review[u['nearest_family_id']]['prototype_gate_eligible'] for u in fine]
            raw=[u['nearest_family_id'] for u in fine] if fine and all(admitted) else None
            merged=[fine_review[u['nearest_family_id']]['visual_structure_merge_hypothesis'] for u in fine] if raw else None
            factored=None
            if merged:
                factors={'VS12':['VS04','VS01'],'VS16':['VS13','VS07'],'VS17':['VS08','VS15'],'VS18':['VS08','VS04'],
                    'VS19':['VS04','VS11'],'VS21':['VS01','VS10']}
                factored=[v for sid in merged for v in factors.get(sid,[sid])]
            record=dict(**g,visual_fine_units=raw,visual_merged_units=merged,visual_factored_units=factored,
                conventional_mapping=None,section=None,hand=None,currier=None,
                source_quality='unresolved unless independently audited; prototype gate only',
                source_pixel_x_page_fraction=g['source_pixel_center_x']/g['native_image_width_px'])
            assays.append(record)
            mids=[f'{g["group_id"]}_SEG_{m}' for m in g['models']]
            dataset['groups'].append(dict(group_id=g['group_id'],line_id=g['line_id'],location=location(g['bbox_xyxy']),
                boundary_confidence='low',alternatives=mids,
                measurements={'ordinal_group_rank':measurement(g['normalized_group_rank'],'ordinal_fraction','rank among ALL original primary space-gap candidates in row'),
                    'native_pixel_x':measurement(g['source_pixel_center_x'],'native_pixel','centre of exact assigned-mask bbox'),
                    'normalized_line_pixel_x':measurement(g['normalized_pixel_center'],'pixel_fraction','native group bbox centre relative to proposed row ink extent')}))
            for model,ids in g['models'].items():
                kind={'fine_components':'fine_components','medium_assemblies':'assemblies','compound_candidates':'compound','group_only':'group_only'}[model]
                nodes=[i+'_A' for i in ids];dataset['segmentations'].append(dict(segmentation_id=f'{g["group_id"]}_SEG_{model}',target_id=g['group_id'],node_ids=nodes,
                    model_kind=kind,relations=[],supporting_observations=[],contradicting_observations=[],status='open'))
        for r in obj['regions']:
            oid=r['region_id']+'_SOURCE';dataset['observations'].append(dict(observation_id=oid,target_id=r['region_id'],location=location(r['native_bbox']),
                statement='Approximate writing-region layout reviewed; proposed rows and group memberships remain uncertain.',method='source contact-sheet review and registered native raster extraction',
                observer_run='layout_review_v0',confidence='low',quality='limited',evidence_path=f'figures/regional_audit_v4/{vid}.png'))
        dataset['hypotheses'].append(dict(hypothesis_id=vid+'_UNIT_BOUNDARIES',proposition='Raster components, medium assemblies, compounds and group-only partitions compete; no partition is canonical grapheme truth.',
            supporting_observations=[],contradicting_observations=[],falsifier='Independent source annotation and held-out template prediction fail to support stable reusable structures.',
            confidence='unresolved',next_test='Source quality, frame/cut geometry, contextual allography and cross-transcription comparison AFTER snapshot freeze.'))
        errors=list(validator.iter_errors(dataset))
        if errors:raise ValueError(f'{vid}: {errors[0].message} at {list(errors[0].path)}')
        write_json(root/path.name,dataset)
        summaries.append(dict(view_id=vid,split=obj['view']['split'],lines=len(dataset['lines']),groups=len(dataset['groups']),
            fine_components=len(dataset['components']),assemblies=len(dataset['assemblies']),candidate_fine_groups=sum(r['visual_fine_units'] is not None for r in assays if r['view_id']==vid),schema_valid=True))
        if any(r['view_id']==vid for r in seen_audit):used_folios.add(obj['view']['folio_component'])
        if obj['view']['split']=='test':
            accepted=[dict(u,merge=fine_review[u['nearest_family_id']]['visual_structure_merge_hypothesis']) for u in a['units'].values() if
                u['model']=='fine_components' and u['recognized_within_training_radius'] and fine_review[u['nearest_family_id']]['prototype_gate_eligible']]
            if len(accepted)>=16:audit_pool.append((obj['view'],accepted,obj['native_source']))
        print(vid,summaries[-1]['candidate_fine_groups'],flush=True)
    write_json(root/'assay_groups.json',assays);write_csv(root/'coverage.csv',summaries)
    # New source audit reserves entire folio components not visually audited before.
    # Fixed manuscript-index strata address the early-view limitation of v4 audit.
    rng=np.random.default_rng(SEED);audit=[];gallery=OUT/'figures/fine_source_audit_v0';gallery.mkdir(parents=True,exist_ok=True)
    write_json(root/'fine_source_audit_plan.json',dict(seed=SEED,prior_audited_folios=sorted(used_folios),
        review_sha256=sha256(OUT/'data/observations/fine_family_source_review_v4.json'),
        selection='up to two test folio components per fixed view-index quartile; exclude previously audited components; 16 uniform admitted fine instances per view',
        rule='source audit cannot refit templates or tune the gate; failures and ambiguity remain in snapshot'))
    for lo,hi in [(4,54),(54,104),(104,154),(154,208)]:
        pool=[p for p in audit_pool if p[0]['folio_component'] not in used_folios and lo<=int(p[0]['pdf_page'])<hi]
        rng.shuffle(pool);chosen=[];seen=set()
        for p in pool:
            if p[0]['folio_component'] in seen:continue
            seen.add(p[0]['folio_component']);chosen.append(p)
            if len(chosen)==2:break
        for view,accepted,source in chosen:
            rgb=Image.open(OUT/source).convert('RGB');sheet=Image.new('RGB',(800,800),'white');draw=ImageDraw.Draw(sheet)
            for cell,j in enumerate(rng.choice(len(accepted),16,replace=False)):
                u=accepted[j];aid=f'F{len(audit)+1:03d}';x=(cell%4)*200;y=(cell//4)*200
                crop=rgb.crop(u['bbox_xyxy']);crop.thumbnail((190,150));sheet.paste(crop,(x+5,y+25));draw.text((x+5,y+5),f'{aid} {view["view_id"]}',fill='black')
                draw.text((x+5,y+180),u['nearest_family_id'].split('_')[-1]+' '+str(u['merge']),fill='black')
                audit.append(dict(audit_id=aid,view_id=view['view_id'],folio_component=view['folio_component'],instance_id=u['instance_id'],
                    family_id=u['nearest_family_id'],bbox_xyxy=u['bbox_xyxy'],outcome='unreviewed',gallery=f'figures/fine_source_audit_v0/{view["view_id"]}.png'))
            sheet.save(gallery/f'{view["view_id"]}.png')
    write_json(root/'fine_source_audit.json',audit);print('Fine audit',len(audit))

if __name__=='__main__':main()
