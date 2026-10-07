from direct_morphology_common import *
from benchmark_membership_v5 import page_features
from PIL import Image
import numpy as np,cv2

def tight(mask):
    ys,xs=np.where(mask)
    return mask[ys.min():ys.max()+1,xs.min():xs.max()+1] if len(xs) else None
def normalize(mask,size=64):
    m=tight(mask)
    if m is None:return np.zeros((size,size),np.uint8)
    margin=max(2,round(size/16));support=size-2*margin;h,w=m.shape;sc=support/max(h,w);ww=max(1,round(w*sc));hh=max(1,round(h*sc));small=cv2.resize(m,(ww,hh),interpolation=cv2.INTER_NEAREST);out=np.zeros((size,size),np.uint8);x=(size-ww)//2;y=(size-hh)//2;out[y:y+hh,x:x+ww]=small;return out
def sdf(mask):
    return (cv2.distanceTransform(mask,cv2.DIST_L2,3)-cv2.distanceTransform(1-mask,cv2.DIST_L2,3))/(mask.shape[0]-2*max(2,round(mask.shape[0]/16)))
def slant(mask,s):
    p=np.pad(mask,20);h,w=p.shape;return cv2.warpAffine(p,np.float32([[1,s,-s*h/2],[0,1,0]]),(w,h),flags=cv2.INTER_NEAREST,borderValue=0)
def build():
    guard();verify();verify_seal(D/'SPECIFICATION_SEAL.json');assert not (D/'SHAPE_SEAL.json').exists()
    aids=read_json(SOURCE/'source_location_aids.json')['parents'];src=read_json(SOURCE/'source_decisions.json');truth={r['parent_id']:r for r in src['parents']};out=[];candidates=[];native={};shapes=[];fields=[];small=[];large=[];lookup={};cacheview=None;cache=None
    def add(mask,meta):
        m=tight(mask)
        if m is None:return None
        cid=f'C{len(candidates):05d}';norm=normalize(m);assert norm.any(),cid
        candidates.append(dict(candidate_id=cid,index=len(candidates),native_shape=list(m.shape),**meta));native[cid]=m;shapes.append(norm);fields.append(sdf(norm));small.append(normalize(m,32));large.append(normalize(m,128));return len(candidates)-1
    for j,r in enumerate(aids):
        s=truth[r['parent_id']]
        if s['membership']!='confirmed_writing':continue
        if cacheview!=r['native_source']:cache=page_features(r);cacheview=r['native_source']
        rgb,delta,cc=cache;mask=(np.asarray(Image.open(OUT/r['mask_path']))>0).astype(np.uint8);x,y,c,d=r['native_bbox'];n=int(mask.sum());indices=[]
        primary=add(mask,dict(parent_id=r['parent_id'],contrast=9,role='primary_source_located_raster',native_bbox=r['native_bbox'],split=False,merge=False,iou=1.,complete_correspondence_claim=False));indices.append(primary);corr=[]
        for vi,contrast in [(1,6),(2,12)]:
            al,st=cc[vi][1:3];ids,cnt=np.unique(al[y:d,x:c][mask>0],return_counts=True);match=[(int(k),int(q)) for k,q in zip(ids,cnt) if k and q>=n*.05]
            if not match:corr.append(dict(contrast=contrast,missing=True,candidate_indices=[],split=False,merge=False));continue
            match.sort(key=lambda z:-z[1]);bboxs=[];ii=[];merged=[]
            for k,inter in match:
                a,b,w,h,area=map(int,st[k]);m=(al[b:b+h,a:a+w]==k).astype(np.uint8);other,nn=np.unique(cc[0][1][b:b+h,a:a+w][m>0],return_counts=True);merge=sum(oid!=0 and cc[0][2][oid,4]>=35 and z>=cc[0][2][oid,4]*.2 for oid,z in zip(other,nn))>1
                index=add(m,dict(parent_id=r['parent_id'],contrast=contrast,role='possible_merge_extent' if merge else 'fragment_correspondence_candidate' if len(match)>1 else 'single_correspondence_candidate',native_bbox=[a,b,a+w,b+h],split=len(match)>1,merge=bool(merge),iou=inter/(n+area-inter),complete_correspondence_claim=False));ii.append(index);bboxs.append([a,b,a+w,b+h]);merged.append(bool(merge))
            if len(match)>1:
                box=np.array(bboxs);a=int(box[:,0].min());b=int(box[:,1].min());e=int(box[:,2].max());f=int(box[:,3].max());um=np.isin(al[b:f,a:e],[k for k,q in match]).astype(np.uint8);ii.append(add(um,dict(parent_id=r['parent_id'],contrast=contrast,role='split_union_observed_recovery',native_bbox=[a,b,e,f],split=True,merge=any(merged),iou=None,complete_correspondence_claim=False)))
            corr.append(dict(contrast=contrast,missing=False,candidate_indices=ii,split=len(match)>1,merge=any(merged)));indices.extend(ii)
        for value in [.04,-.04]:indices.append(add(slant(mask,value),dict(parent_id=r['parent_id'],contrast=9,role='slant_sensitivity',native_bbox=r['native_bbox'],shear=value,split=False,merge=False,iou=None,complete_correspondence_claim=False)))
        photo_ok=s['source_parent_status']=='resolved_whole_parent';lookup[r['audit_id']]=len(out);out.append(dict(parent_id=r['parent_id'],audit_id=r['audit_id'],original_proposal_index=j,caption=r['caption'],corpus=r['corpus'],native_source=r['native_source'],native_bbox=r['native_bbox'],native_crop=r['native_crop'],body_proxy=r['body_proxy'],source_membership=s['membership'],source_parent_status=s['source_parent_status'],source_extent_resolved=photo_ok,full_extent_state='source_resolved' if photo_ok else 'unknown',full_physical_distance_bounded=False,primary_index=primary,candidate_indices=indices,correspondence=corr,source_family_or_class=None,semantic_features_required=False))
        if j%30==0:print('Direct morphology source proposals',j,'/',len(aids),flush=True)
    # Frozen source alternative: no new membership judgment, no painted connecting trace.
    a=out[lookup['N094']];b=out[lookup['N095']];box=src['source_alternatives'][0]['native_bbox'];x,y,c,d=box;um=np.zeros((d-y,c-x),np.uint8)
    for p in [a,b]:
        xx,yy,ee,ff=p['native_bbox'];mm=native[candidates[p['primary_index']]['candidate_id']];um[yy-y:ff-y,xx-x:ee-x]|=mm
    alt=add(um,dict(parent_id='N094_N095_extent_alternative',contrast=9,role='partial_union_missing_faint_bridge',native_bbox=box,split=True,merge=False,iou=None,complete_correspondence_claim=False));extent=[dict(source_audit_ids=['N094','N095'],relation='possible_faint_source_join_from_frozen_adjudication',observed_union_index=alt,unknown_bridge=True,ownership_unresolved=True,full_parent_embedding=None,complete_physical_distance=None)]
    np.savez_compressed(D/'native_candidate_masks.npz',**native);np.savez_compressed(D/'direct_image_fields.npz',shape64=np.array(shapes),sdf64=np.array(fields),shape32=np.array(small),shape128=np.array(large));save(D/'source_parent_ensembles.json',dict(created_at_utc=now(),parents=out,candidates=candidates,extent_alternatives=extent,excluded_source_proposals=[dict(parent_id=r['parent_id'],audit_id=r['audit_id'],membership=r['membership']) for r in src['parents'] if r['membership']!='confirmed_writing'],shape_claim='Candidate contour geometry remains source-traceable; source extent uncertainty and raster correspondence are not solved by similarity. No discrete writing labels or whole-parent posterior probabilities.'))
    # Strip all Trial2 feature distances, selector predictions and class fields.
    oldkey=read_json(SOURCE/'similarity_hidden_key.json')['pairs'];proj={r['original_proposal_index']:i for i,r in enumerate(out)};pairs=[dict(pair_id=r['pair_id'],anchor_parent=proj[r['anchor_index']],reference_parent=proj[r['reference_index']],caption=r['caption']) for r in oldkey];save(D/'reused_source_pairs.json',pairs);save(D/'reused_source_ratings.json',read_json(SOURCE/'similarity_decisions.json'))
    save(D/'IMPLEMENTATION.json',dict(implemented_at_utc=now(),normalization='Native mask tight envelope; nearest-neighbor proportional resizing; centered64/32/128; margins size/16 with minimum2px.64 has56px support. No rotation or learned registration.',candidate_match='All6/12 CC overlaps>=5% primary area; split union preserves native locations. Missing match is explicit, never all-zero shape.',uncertainty='Candidate envelope only, not confidence interval. Unknown extent is unknown, not mean or chosen closest morphology.',code_sha256=sha256(__file__)))
    seal([D/'native_candidate_masks.npz',D/'direct_image_fields.npz',D/'source_parent_ensembles.json',D/'reused_source_pairs.json',D/'reused_source_ratings.json',D/'IMPLEMENTATION.json',OUT/'src/build_direct_morphology.py'],D/'SHAPE_SEAL.json');print('Confirmed',len(out),'candidate image fields',len(candidates),'unresolved extents',sum(not r['source_extent_resolved'] for r in out),flush=True)
if __name__=='__main__':build()
