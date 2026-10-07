"""Source membership candidates plus read-only sealed V3 inference; no fitting."""
from common import OUT,read_json,write_json,sha256
from register_sequence_v4 import D,T
from visual_extract import ink_mask
from regional_extract_v11 import normalise
from extract_recurrence_units_v3 import holes,feature
from evaluate_source_classes_v3 import transform,assign
from PIL import Image
from collections import defaultdict
import numpy as np,cv2,pickle
V3=OUT/'data/observations/recurrence_v3_structural_candidate'
def main():
    if (D/'source_parents.json').exists():raise RuntimeError('Extraction already exists')
    plan=read_json(D/'PLAN.json');assert sha256(V3/'sealed_class_model.pkl')==plan['v3_model_sha256']
    model=pickle.loads((V3/'sealed_class_model.pkl').read_bytes());old=read_json(V3/'source_parents.json')
    reviews={r['view_id']:r for r in read_json(D/'ordinary_source_reviews.json')};contexts=read_json(D/'native_row_index.json')
    cfg=read_json(OUT/'data/observations/visual_protocol_draft.json');cfg['background_gaussian_sigma_px']=25
    allrec=[];rowout=[];allsh=[];allg=[]
    for v in plan['selected_views']:
        vid=v['view_id'];rows=[r for r in contexts if r['view_id']==vid];rv=reviews[vid]
        rgb=np.asarray(Image.open(OUT/v['native_source']).convert('RGB'));smooth=cv2.GaussianBlur(rgb,(0,0),.8)
        masks=[ink_mask(smooth,cfg,c) for c in [9,6,12]];cc=[cv2.connectedComponentsWithStats(m,8) for m in masks]
        _,lab,st,_=cc[0];support=defaultdict(list);faint=defaultdict(list);rowlookup={r['row_number']:r for r in rows}
        for r in rows:
            rn=r['row_number'];a,b,c,d=r['native_bbox'];xa,xb=max(a,rv['safe_x'][0]),min(c,rv['safe_x'][1]);body=r['body_height']
            status='excluded_source_drawing_or_empty' if rn in rv['exclude_rows'] or xb<=xa else 'triaged_local_writing_field'
            rowout.append(dict(**r,status=status,safe_x=[xa,xb],native_row_endpoints=None,complete_physical_line=False,ink_recall_certified=False,review_level='overview_field_triage',panel_mapping=rv['panel_mapping']))
            if status.startswith('excluded'):continue
            knots=np.array(r['body_path_knots']);grid=np.arange(xa,xb);base=np.interp(grid,knots[:,0],knots[:,1]);yy=np.arange(b,d)[:,None]
            broad=(yy>=base[None,:]-1.65*body)&(yy<=base[None,:]+.55*body);core=(yy>=base[None,:]-.95*body)&(yy<=base[None,:]+.25*body)
            ids,cnt=np.unique(lab[b:d,xa:xb][broad],return_counts=True);ci,cn=np.unique(lab[b:d,xa:xb][core],return_counts=True);cores=dict(zip(ci,cn))
            for k,n in zip(ids,cnt):
                if k==0 or n<2 or st[k,4]<8:continue
                support[int(k)].append(dict(row_number=rn,core_pixels=int(cores.get(k,0)),broad_pixels=int(n),body=float(body),field=[xa,xb]))
            # Whole low-threshold regions absent from the primary raster, no clipped fake parents.
            lowlab=cc[1][1];fl,fn=np.unique(lowlab[b:d,xa:xb][broad & (lab[b:d,xa:xb]==0)],return_counts=True)
            for k,n in zip(fl,fn):
                if k==0 or n<2 or cc[1][2][k,4]<8:continue
                x,y,w,h,area=map(int,cc[1][2][k]);lm=(lowlab[y:y+h,x:x+w]==k)
                if np.any(lab[y:y+h,x:x+w][lm]>0):continue
                faint[int(k)].append(dict(row_number=rn,core_pixels=0,broad_pixels=int(n),body=float(body),field=[xa,xb]))
        records=[];shapes=[];geoms=[];lows=[];highs=[];variantgeom=[]
        for k,poss in sorted(support.items()):
            poss.sort(key=lambda p:(-p['core_pixels'],-p['broad_pixels'],p['row_number']));p=poss[0];body=p['body'];x,y,w,h,area=map(int,st[k]);mask=(lab[y:y+h,x:x+w]==k).astype(np.uint8)
            small=area<35 or h<.32*body or w<4;oversize=h>3.8*body or w>12*body
            ownership=p['core_pixels']<8 or (len(poss)>1 and poss[1]['core_pixels']>=max(8,p['core_pixels']*.3))
            edge=x<p['field'][0]+2 or x+w>p['field'][1]-2
            rec=dict(parent_id=f'{vid}_P{k:06d}',view_id=vid,folio_component=v['folio_component'],split=v['split'],native_source=v['native_source'],native_bbox=[x,y,x+w,y+h],row_number=p['row_number'],row_support=poss,body_height_proxy=body,area=area,small_detached_candidate=bool(small),field_edge=bool(edge),row_ownership='unknown' if ownership else 'single_proposed_body_path',writing_membership='unknown' if small or oversize or edge or ownership else 'source_field_writing_candidate',atomicity='unknown',pen_lifts='unknown',structural_class=None,competing_class=None,class_eligible=False,threshold_stable=False,alignment_stable=False,shape_index=None,unknown_reasons=[])
            for condition,name in [(small,'detached_small_mark'),(oversize,'oversize_compound_or_drawing'),(ownership,'row_ownership'),(edge,'field_edge')]:
                if condition:rec['unknown_reasons'].append(name)
            if not small and not oversize:
                baseys,basexs=np.where(mask);iou=[];connected=[];loop=[holes(mask)];vv=[];vg=[];raster=[]
                for j in [1,2]:
                    _,vl,vs,_=cc[j];matches,cnts=np.unique(vl[y+baseys,x+basexs],return_counts=True);valid=sorted([(int(q),int(z)) for q,z in zip(matches,cnts) if q!=0],key=lambda t:-t[1])
                    if not valid:vv.append(normalise(mask,body));vg.append([x,y,x+w,y+h]);iou.append(0.);connected.append(False);loop.append(-1);raster.append(dict(contrast=[6,12][j-1],native_bbox=[x,y,x+w,y+h],split=True,merge=False,iou=0.));continue
                    winner,inter=valid[0];vx,vy,vw,vh,va=map(int,vs[winner]);vm=(vl[vy:vy+vh,vx:vx+vw]==winner).astype(np.uint8)
                    ii=inter/(area+va-inter);split=sum(z>=area*.05 for q,z in valid)>1
                    others,oc=np.unique(lab[vy:vy+vh,vx:vx+vw][vm>0],return_counts=True);merge=sum(q!=0 and st[q,4]>=35 and z>=st[q,4]*.2 for q,z in zip(others,oc))>1
                    iou.append(float(ii));connected.append(not(split or merge));loop.append(holes(vm));vv.append(normalise(vm,body));vg.append([vx,vy,vx+vw,vy+vh]);raster.append(dict(contrast=[6,12][j-1],native_bbox=vg[-1],split=bool(split),merge=bool(merge),iou=float(ii)))
                stable=all(connected) and min(iou)>=.5 and len(set(loop))==1
                rec.update(class_eligible=bool(stable),competing_rasters=raster,topology_across_thresholds=loop,shape_index=len(allsh)+len(shapes))
                if not stable:rec['unknown_reasons'].append('raster_connectivity_topology_or_coverage')
                rec['local_feature_index']=len(shapes);shapes.append(normalise(mask,body));geoms.append(feature(mask,body));lows.append(vv[0]);highs.append(vv[1]);variantgeom.append(vg)
            records.append(rec)
        if shapes:
            sh=np.array(shapes);g=np.array(geoms);base=assign(transform(sh,g,model),g,model);variants=[]
            for j,ss in enumerate([lows,highs]):
                gg=g.copy()
                for i,boxes in enumerate(variantgeom):
                    a,b,c,d=boxes[j];body=records[[q.get('local_feature_index') for q in records].index(i)]['body_height_proxy'];gg[i,:3]=[np.log((d-b)/body),np.log((c-a)/body),np.log((c-a)/(d-b))]
                variants.append(assign(transform(np.array(ss),gg,model),gg,model))
            nuisance=np.array([cv2.warpAffine(s,np.float32([[1,.04,-1],[0,1,1]]),(48,48),flags=cv2.INTER_LINEAR,borderValue=0) for s in sh]);nu=assign(transform(nuisance,g,model),g,model)
            for rec in records:
                if 'local_feature_index' not in rec:continue
                i=rec.pop('local_feature_index');cid=str(base['classes'][i]);nominal=bool(base['accepted'][i]);ts=nominal and all(a['accepted'][i] and a['classes'][i]==cid for a in variants);ns=nominal and nu['accepted'][i] and nu['classes'][i]==cid
                reliable=rec['class_eligible'] and nominal and ts and ns and cid!='ST09' and rec['row_ownership']!='unknown' and not rec['field_edge']
                rec.update(proposed_class=cid if np.isfinite(base['distance'][i]) else None,competing_class=str(base['alternatives'][i]) if np.isfinite(base['alternative_distance'][i]) else None,nominal_accepted=nominal,threshold_stable=bool(ts),alignment_stable=bool(ns),structural_class=cid if reliable else None,distance=float(base['distance'][i]) if np.isfinite(base['distance'][i]) else None,nearest_training_parent=old[base['nearest'][i]]['parent_id'] if base['nearest'][i]>=0 else None,nearest_training_crop=old[base['nearest'][i]]['native_crop'] if base['nearest'][i]>=0 else None,negative_training_crop=old[base['negative'][i]]['native_crop'] if base['negative'][i]>=0 else None)
                if not reliable:rec['unknown_reasons'].append('frozen_class_abstention_or_perturbation')
            allsh.extend(shapes);allg.extend(geoms)
        for k,poss in sorted(faint.items()):
            poss.sort(key=lambda p:-p['broad_pixels']);p=poss[0];x,y,w,h,area=map(int,cc[1][2][k]);records.append(dict(parent_id=f'{vid}_F{k:06d}',view_id=vid,folio_component=v['folio_component'],split=v['split'],native_source=v['native_source'],native_bbox=[x,y,x+w,y+h],row_number=p['row_number'],row_support=poss,body_height_proxy=p['body'],area=area,small_detached_candidate=True,field_edge=x<p['field'][0] or x+w>p['field'][1],row_ownership='unknown',writing_membership='unknown',atomicity='unknown',pen_lifts='unknown',structural_class=None,competing_class=None,class_eligible=False,threshold_stable=False,alignment_stable=False,shape_index=None,unknown_reasons=['faint_contrast6_only_region']))
        allrec.extend(records);print(vid,len(records),'candidates',sum(r['structural_class'] is not None for r in records),'assigned',flush=True)
    write_json(D/'source_parents.json',allrec);write_json(D/'source_rows.json',rowout);np.savez_compressed(D/'source_shapes.npz',shapes=np.array(allsh),geometry=np.array(allg))
    write_json(T/'extraction_summary.json',dict(views=len(plan['selected_views']),row_fields=len(rowout),retained_row_fields=sum(r['status']=='triaged_local_writing_field' for r in rowout),candidate_parents=len(allrec),assigned=sum(r['structural_class'] is not None for r in allrec),notes='Photographic candidates include optional tiny/faint ink; not certified writing recall. V3 unchanged.'))
if __name__=='__main__':main()
