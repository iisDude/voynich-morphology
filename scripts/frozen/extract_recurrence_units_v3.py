"""New source-only parent raster corpus. Does not edit/read V2 assignments."""
from common import OUT,read_json,write_json,write_csv,sha256,SEED
from visual_extract import ink_mask
from regional_extract_v11 import normalise
from calibrate_assemblies import topology
import numpy as np,cv2
from PIL import Image
from datetime import datetime,timezone

ROOT=OUT/'data/observations/recurrence_v3_development'
PROTOCOL=dict(primary_contrast=9,sensitivity_contrasts=[6,12],preblur_sigma=.8,
 minimum_area=35,minimum_height_body=.32,maximum_height_body=3.8,
 minimum_width=4,maximum_width_body=12,core_band=[-.95,.25],
 significant_hole_minimum_area=8,significant_hole_area_fraction=.012,
 split_fragment_fraction=.05,variant_minimum_iou=.5,
 unit='Whole threshold-connected raster parent, with detached/compound hypotheses unresolved',
 deduplication='One native-view connected-parent ID, regardless of overlapping row proposals',
 ownership='Row assignment may remain unknown; local source writing field does not certify atomicity or pen lifts',
 class_inputs='Source pixels, connectivity, topology, relative geometry only. No transcription or metadata labels',
 status='Development protocol, not segmentation freeze')

def holes(mask):
    padded=np.pad(mask.astype(np.uint8),1);n,_,st,_=cv2.connectedComponentsWithStats(1-padded,8)
    cutoff=max(8,mask.sum()*.012)
    return int(sum(s[4]>=cutoff for s in st[2:]))

def feature(mask,body):
    h,w=mask.shape;t=topology(mask.astype(bool),body)
    yy,xx=np.where(mask);sk=cv2.resize(mask.astype(np.float32),(24,24),interpolation=cv2.INTER_AREA)
    return [float(np.log(h/body)),float(np.log(w/body)),float(np.log(w/h)),
      float(mask.mean()),float(holes(mask)),float(np.log1p(t['skeleton_endpoint_pixels'])),
      float(np.log1p(t['skeleton_branch_clusters'])),float(t['longest_horizontal_ink_run_px']/max(w,1)),
      float(np.log1p(t['column_ink_ridge_count'])),float((yy<h*.35).mean()),float((yy>h*.7).mean()),
      float((xx<w*.35).mean()),float((xx>w*.7).mean())]

def main():
    from recurrence_guard_v3 import require_unfrozen
    require_unfrozen(ROOT)
    write_json(ROOT/'extraction_protocol.json',dict(registered_at_utc=datetime.now(timezone.utc).isoformat(),**PROTOCOL))
    plan=read_json(ROOT/'PLAN.json');reviews={r['view_id']:r for r in read_json(ROOT/'ordinary_source_reviews.json')}
    contexts=read_json(ROOT/'native_row_review_index.json');all_records=[];all_shapes=[];low_shapes=[];high_shapes=[];features=[];rows_out=[]
    (ROOT/'native_parents').mkdir(exist_ok=True)
    cfg=read_json(OUT/'data/observations/visual_protocol_draft.json');cfg['background_gaussian_sigma_px']=25
    for view in plan['selected_views']:
        vid=view['view_id'];review=reviews[vid];rows=[r for r in contexts if r['view_id']==vid]
        rgb=np.asarray(Image.open(OUT/view['native_source']).convert('RGB'));smooth=cv2.GaussianBlur(rgb,(0,0),.8)
        masks=[ink_mask(smooth,cfg,c) for c in [9,6,12]];cc=[cv2.connectedComponentsWithStats(m,8) for m in masks]
        n,labels,stats,centers=cc[0];support={};row_lookup={r['row_number']:r for r in rows}
        for row in rows:
            rn=row['row_number'];field=review.get('row_safe_x',{}).get(str(rn),review['safe_x']);a,b,c,d=row['native_bbox'];xa,xb=max(a,field[0]),min(c,field[1]);body=row['body_height']
            status='excluded_unknown_or_drawing' if rn in review.get('exclude_rows',[]) or xb<=xa else 'reviewed_local_writing_field'
            rows_out.append(dict(view_id=vid,row_number=rn,line_id=row['line_id'],split=row['split'],folio_component=row['folio_component'],status=status,safe_x=[xa,xb],complete_physical_line=False,body_height=body))
            if status!='reviewed_local_writing_field':continue
            knots=np.array(row['body_path_knots']);grid=np.arange(xa,xb);base=np.interp(grid,knots[:,0],knots[:,1]);ys=np.arange(b,d)[:,None]
            band=(ys>=base[None,:]-.95*body)&(ys<=base[None,:]+.25*body)
            labs,cnt=np.unique(labels[b:d,xa:xb][band],return_counts=True)
            for lab,count in zip(labs,cnt):
                if lab==0 or count<8:continue
                x,y,w,h,area=map(int,stats[lab]);
                if area<35 or h<.32*body or h>3.8*body or w<4 or w>12*body:continue
                if x<xa or x+w>xb:continue # crossing field limit stays unknown; no clipping
                support.setdefault(int(lab),[]).append((rn,int(count),float(body)))
        count_good=0
        for lab,poss in sorted(support.items()):
            poss.sort(key=lambda a:-a[1]);rn,_,body=poss[0];row=row_lookup[rn];x,y,w,h,area=map(int,stats[lab]);mask=(labels[y:y+h,x:x+w]==lab).astype(np.uint8)
            alternatives=[];variants=[];ious=[];connectivity=[];loop_counts=[holes(mask)]
            base_ys,base_xs=np.where(mask)
            for ci in [1,2]:
                _,vl,vs,_=cc[ci];matches,cnt=np.unique(vl[y+base_ys,x+base_xs],return_counts=True);valid=[(int(k),int(v)) for k,v in zip(matches,cnt) if k!=0];valid.sort(key=lambda a:-a[1])
                if not valid:variants.append(normalise(mask,body));ious.append(0.);connectivity.append(False);loop_counts.append(-1);continue
                winner,inter=valid[0];vx,vy,vw,vh,va=map(int,vs[winner]);vm=(vl[vy:vy+vh,vx:vx+vw]==winner).astype(np.uint8);iou=inter/(area+va-inter);ious.append(float(iou));variants.append(normalise(vm,body));loop_counts.append(holes(vm))
                split=sum(v>=area*.05 for k,v in valid)>1
                others,other_count=np.unique(labels[vy:vy+vh,vx:vx+vw][vm>0],return_counts=True)
                merge=sum(k!=0 and stats[k,4]>=35 and z>=stats[k,4]*.2 for k,z in zip(others,other_count))>1
                connectivity.append(not(split or merge));alternatives.append(dict(contrast=[6,12][ci-1],native_bbox=[vx,vy,vx+vw,vy+vh],split=bool(split),merge=bool(merge),iou=float(iou)))
            ownership_unknown=len(poss)>1 and poss[1][1]>=poss[0][1]*.3
            topology_stable=len(set(loop_counts))==1
            eligible=all(connectivity) and min(ious)>=.5 and topology_stable
            pid=f'{vid}_P{lab:06d}';crop=ROOT/'native_parents'/f'{pid}.png'
            Image.fromarray(rgb[max(0,y-4):y+h+4,max(0,x-4):x+w+4]).save(crop)
            record=dict(parent_id=pid,view_id=vid,split=view['split'],folio_component=view['folio_component'],native_source=view['native_source'],native_bbox=[x,y,x+w,y+h],native_crop=crop.relative_to(OUT).as_posix(),row_number=rn,row_hypotheses=[p[0] for p in poss],row_ownership='unknown' if ownership_unknown else 'single_proposed_body_path',body_height_proxy=body,
             area=area,significant_holes=loop_counts[0],topology_across_thresholds=loop_counts,connectivity_stable=all(connectivity),threshold_ious=ious,competing_rasters=alternatives,
             writing_membership='source_field_writing_candidate',class_eligible=bool(eligible),atomicity='unknown',pen_lifts='unknown',detached_attachment='not asserted',
             uncertainty_reasons=([ 'threshold_connectivity'] if not all(connectivity) else [])+(['threshold_coverage'] if min(ious)<.5 else [])+(['threshold_topology'] if not topology_stable else [])+(['row_ownership'] if ownership_unknown else []))
            all_records.append(record);all_shapes.append(normalise(mask,body));low_shapes.append(variants[0]);high_shapes.append(variants[1]);features.append(feature(mask,body));count_good+=eligible
        print(vid,'unique writing parents',len(support),'stable',count_good,flush=True)
    np.savez_compressed(ROOT/'source_shapes.npz',shapes=np.array(all_shapes),low=np.array(low_shapes),high=np.array(high_shapes),geometry=np.array(features))
    write_json(ROOT/'source_parents.json',all_records);write_json(ROOT/'source_rows.json',rows_out)
    write_json(ROOT/'extraction_summary.json',dict(reviewed_views=len(reviews),row_proposals=len(rows_out),local_writing_row_fields=sum(r['status']=='reviewed_local_writing_field' for r in rows_out),unique_parent_instances=len(all_records),class_eligible=sum(r['class_eligible'] for r in all_records),by_split={s:dict(parents=sum(r['split']==s for r in all_records),eligible=sum(r['split']==s and r['class_eligible'] for r in all_records)) for s in ['train','validation','test']},unknown_atomicity='all',source_reviews_sha256=sha256(ROOT/'ordinary_source_reviews.json'),protocol_sha256=sha256(ROOT/'extraction_protocol.json')))

if __name__=='__main__':main()
