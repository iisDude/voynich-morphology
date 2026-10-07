"""Prioritize source uncertainty without Currier labels or positional statistics."""
from common import OUT, read_json, read_csv, write_json, write_csv, sha256, SEED
from collections import defaultdict
from datetime import datetime, timezone
from PIL import Image, ImageDraw
import numpy as np

ROOT2=OUT/'data/observations/source_adjudication_v2'

def main():
    if (ROOT2/'queue_plan.json').exists(): raise ValueError('Queue already registered')
    ROOT2.mkdir(parents=True,exist_ok=True)
    sources={r['view_id']:r for r in read_csv(OUT/'data/source/yale_native_all_manifest.csv')}
    candidates=[];resolution=[];views={}
    for vid,source in sources.items():
        info=read_json(OUT/f'data/source/yale_native/{source["yale_image_id"]}_info.json')
        with Image.open(OUT/source['path']) as image: wh=image.size
        valid=wh==(info['width'],info['height'])
        if not valid: raise ValueError('Source not native resolution')
        resolution.append(dict(view_id=vid,width=wh[0],height=wh[1],advertised_native_width=info['width'],advertised_native_height=info['height'],highest_advertised_pixel_grid=True,source_sha256=sha256(OUT/source['path']),service=info.get('@id'),info_sha256=sha256(OUT/f'data/source/yale_native/{source["yale_image_id"]}_info.json')))
        obj=read_json(OUT/f'data/observations/regional_candidates_v11/{vid}.json');views[vid]=obj
        assigned=read_json(OUT/f'data/observations/assigned_visual_candidates_v11/{vid}.json')
        groups=defaultdict(list)
        for g in assigned['groups']:groups[g['line_id']].append(g)
        for line in obj['lines']:
            gg=groups[line['line_id']];n=len(gg)
            if not n: continue
            counts=[len(line['groups_by_gap'][str(x)]) for x in [.35,.55,.75]]
            unknown=sum(not g.get('visual_fine_units') for g in gg)/n
            contacts=line['multiline_component_count']/max(1,line['component_count'])
            disagreement=(max(counts)-min(counts))/max(counts)
            body=line['body_height_proxy_px'];a,b,c,d=line['bbox_xyxy']
            tall_ratio=(d-b)/max(body,1)
            # Material changes in row membership and gaps, not sign-effect support.
            score=4*contacts+2*disagreement+unknown+min(2,max(0,tall_ratio-2))*.3
            candidates.append(dict(case_id=f'ROW_{line["line_id"]}',kind='whole_row',view_id=vid,line_id=line['line_id'],split=obj['view']['split'],folio_component=obj['view']['folio_component'],bbox_xyxy=line['bbox_xyxy'],body_height_proxy_px=body,groups=n,priority_score=score,uncertain_unit_fraction=unknown,multiline_contact_fraction=contacts,gap_count_range=counts,questions=['writing_membership','row_ownership','visible_group_gaps','detached_marks'],status='pending',native_source=source['path']))
    # One high-priority row per selected view; coverage quotas constrain risk ranking.
    best={}
    for r in sorted(candidates,key=lambda r:(-r['priority_score'],r['case_id'])):best.setdefault(r['view_id'],r)
    selected=[]
    for lo,hi in [(4,55),(55,106),(106,157),(157,208)]:
        for split,quota in [('train',6),('validation',2),('test',3),('calibration',1)]:
            pool=[r for r in best.values() if lo<=int(r['view_id'][2:])<hi and r['split']==split]
            selected.extend(sorted(pool,key=lambda r:(-r['priority_score'],r['case_id']))[:quota])
    chosen={r['case_id'] for r in selected}
    # Four material local assemblies per selected row. Native crop, not normalized template.
    local=[]
    for row in selected:
        obj=views[row['view_id']];lineid=row['line_id'];body=row['body_height_proxy_px']
        pool=[r for r in obj['instances'] if r['model']=='fine_components' and r['group_id'].startswith(lineid+'_G')]
        def risk(r):
            f=r['features'];return 2*float(r.get('multiline_contact',False))+max(0,f.get('height_ratio',0)-1.5)+.5*f.get('raster_loops',0)+.1*f.get('skeleton_branch_clusters',0)
        for rec in sorted(pool,key=lambda r:(-risk(r),r['instance_id']))[:4]:
            local.append(dict(case_id='UNIT_'+rec['instance_id'],kind='local_assembly',view_id=row['view_id'],parent_case_id=row['case_id'],instance_id=rec['instance_id'],bbox_xyxy=rec['bbox_xyxy'],body_height_proxy_px=body,priority_score=risk(rec),questions=['writing_vs_drawing','tall_lower_contact','frame_or_compound','detached_marks','internal_boundary'],status='pending',native_source=row['native_source']))
    curved=[]
    for p in sorted((OUT/'data/observations/curved_path_candidates_v2').glob('V_*.json')):
        curved.append(dict(case_id='CURVE_'+p.stem,kind='curved_view',view_id=p.stem,priority_score=5,questions=['curved_writing_membership','orientation','path_seam','panel_mapping'],status='pending',native_source=sources[p.stem]['path'],hypotheses_path=p.relative_to(OUT).as_posix()))
    overlap=read_json(OUT/'tests/physical_overlap_v1/source_reviewed.json')
    write_json(ROOT2/'queue_plan.json',dict(protocol='source-adjudication-v2',registered_at_utc=datetime.now(timezone.utc).isoformat(),seed=SEED,selection='risk-ranked row per view, with fixed manuscript-quartile and existing split quotas; no Currier, hand, transcription or effect inputs',selected_rows=selected,selected_local_assemblies=local,curved_views=curved,foldout_pairs=overlap,all_candidate_rows=len(candidates),unselected_status='unknown, not reviewed',known_exposure='Existing findings previously seen; this is source-only adjudication after exposure, not renewed blinding',stopping_rule='Resolve every selected queue entry to direct observation or explicit unknown; expanded rows must pass membership/gap source review before primary use; never adjust thresholds after effect inspection'))
    write_csv(ROOT2/'all_row_priority.csv',sorted(candidates,key=lambda r:-r['priority_score']))
    write_json(ROOT2/'highest_resolution_verification.json',resolution)
    write_json(ROOT2/'protocol.json',dict(unit_policy='Connected visible ink assemblies retained whole in conservative model; geometric fine alternatives retained; no pen-lift claims; old source-trained prototype/gates transferred without refit',row_policy='Manual native-coordinate corridor correction; writing, drawing and uncertain ownership zones explicit; unreviewed rows unknown',group_policy='Source-verified visible gaps with explicit merge/split overrides; disputed gaps retained as unknown; group not word',pixel_policy='Center of assigned writing bbox normalized to independently adjudicated complete row writing extent; not rank',rank_policy='Original adjudicated group slots including unresolved slots; no rank recomputation after unit exclusions',primary_assay=dict(minimum_frequency=8,edge_width=2,length_min=5),sensitivities=dict(frequencies=[5,8,10,12],edge_widths=[1,2],minimum_length_strict=5),null='within-line measured-position slot shuffle',dependence='joint caption-block occurrence bootstrap and connected-family uncertainty; heldout caption splits retained',comparison_metadata='Only attach after v2 freeze; no conventional forms or effect inputs during source stage'))
    gallery=OUT/'figures/source_adjudication_v2';gallery.mkdir(parents=True,exist_ok=True)
    for row in selected:
        im=Image.open(OUT/row['native_source']).convert('RGB');obj=views[row['view_id']]
        a,b,c,d=row['bbox_xyxy'];body=row['body_height_proxy_px'];x0=max(0,a-100);x1=min(im.width,c+100);y0=max(0,int(b-2*body));y1=min(im.height,int(d+2*body))
        patch=im.crop((x0,y0,x1,y1));patch.thumbnail((1800,700))
        canvas=Image.new('RGB',(1820,patch.height+65),'white');canvas.paste(patch,(10,55));draw=ImageDraw.Draw(canvas);draw.text((10,8),row['case_id']+' context; native crop '+str([x0,y0,x1,y1]),fill='black')
        sx=patch.width/(x1-x0);sy=patch.height/(y1-y0);draw.rectangle([10+(a-x0)*sx,55+(b-y0)*sy,10+(c-x0)*sx,55+(d-y0)*sy],outline='magenta',width=2)
        canvas.save(gallery/(row['view_id']+'_row_context.png'))
        overview=im.copy();overview.thumbnail((900,1200));draw=ImageDraw.Draw(overview);sc=overview.width/im.width;draw.rectangle([a*sc,b*sc,c*sc,d*sc],outline='magenta',width=3);overview.save(gallery/(row['view_id']+'_overview.png'))
        for case in [x for x in local if x['view_id']==row['view_id']]:
            aa,bb,cc,dd=case['bbox_xyxy'];pad=int(max(20,body*.6));box=[max(0,aa-pad),max(0,bb-pad),min(im.width,cc+pad),min(im.height,dd+pad)]
            crop=im.crop(box);crop.save(gallery/(case['case_id']+'.png'));case['inspection_crop_bbox']=box
    write_json(ROOT2/'queue_plan.json',dict(read_json(ROOT2/'queue_plan.json'),selected_local_assemblies=local))
    print('Selected',len(selected),'rows,',len(local),'assemblies,',len(curved),'curved views; native sources',len(resolution),flush=True)

if __name__=='__main__':main()
