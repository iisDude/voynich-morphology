"""Fresh-source adapter. Frozen image encoders and candidate procedure unchanged."""
from direct_morphology2_common import *
from build_direct_morphology import tight,normalize,sdf,slant
from benchmark_membership_v5 import page_features
from PIL import Image
import numpy as np,cv2
def main():
    guard();verify();verify_seal(D/'SOURCE_SEAL.json');assert not (D/'SHAPE_SEAL.json').exists();rr=read_json(D/'source_location_aids.json')['parents'];src=read_json(D/'source_decisions.json');truth={r['parent_id']:r for r in src['parents']};parents=[];candidates=[];native={};shapes=[];fields=[];small=[];large=[];view=None;cache=None
    def add(mask,meta):
        m=tight(mask)
        if m is None:return None
        cid=f'C{len(candidates):05d}';norm=normalize(m);assert norm.any(),cid;candidates.append(dict(candidate_id=cid,index=len(candidates),native_shape=list(m.shape),**meta));native[cid]=m;shapes.append(norm);fields.append(sdf(norm));small.append(normalize(m,32));large.append(normalize(m,128));return len(candidates)-1
    for j,r in enumerate(rr):
        s=truth[r['parent_id']]
        if s['membership']!='confirmed_writing':continue
        if view!=r['native_source']:cache=page_features(r);view=r['native_source']
        rgb,delta,cc=cache;mask=(np.asarray(Image.open(OUT/r['mask_path']))>0).astype(np.uint8);x,y,c,d=r['native_bbox'];n=int(mask.sum());indices=[];primary=add(mask,dict(parent_id=r['parent_id'],contrast=9,role='primary_source_located_raster',native_bbox=r['native_bbox'],split=False,merge=False,iou=1.,complete_correspondence_claim=False));indices.append(primary);corr=[]
        for vi,contrast in [(1,6),(2,12)]:
            al,st=cc[vi][1:3];ids,cnt=np.unique(al[y:d,x:c][mask>0],return_counts=True);match=[(int(k),int(q)) for k,q in zip(ids,cnt) if k and q>=n*.05]
            if not match:corr.append(dict(contrast=contrast,missing=True,candidate_indices=[],split=False,merge=False));continue
            match.sort(key=lambda z:-z[1]);bboxs=[];ii=[];merged=[]
            for k,inter in match:
                a,b,w,h,area=map(int,st[k]);m=(al[b:b+h,a:a+w]==k).astype(np.uint8);other,nn=np.unique(cc[0][1][b:b+h,a:a+w][m>0],return_counts=True);merge=sum(oid!=0 and cc[0][2][oid,4]>=35 and z>=cc[0][2][oid,4]*.2 for oid,z in zip(other,nn))>1;index=add(m,dict(parent_id=r['parent_id'],contrast=contrast,role='possible_merge_extent' if merge else 'fragment_correspondence_candidate' if len(match)>1 else 'single_correspondence_candidate',native_bbox=[a,b,a+w,b+h],split=len(match)>1,merge=bool(merge),iou=inter/(n+area-inter),complete_correspondence_claim=False));ii.append(index);bboxs.append([a,b,a+w,b+h]);merged.append(bool(merge))
            if len(match)>1:
                box=np.array(bboxs);a=int(box[:,0].min());b=int(box[:,1].min());e=int(box[:,2].max());f=int(box[:,3].max());um=np.isin(al[b:f,a:e],[k for k,q in match]).astype(np.uint8);ii.append(add(um,dict(parent_id=r['parent_id'],contrast=contrast,role='split_union_observed_recovery',native_bbox=[a,b,e,f],split=True,merge=any(merged),iou=None,complete_correspondence_claim=False)))
            corr.append(dict(contrast=contrast,missing=False,candidate_indices=ii,split=len(match)>1,merge=any(merged)));indices.extend(ii)
        for value in [.04,-.04]:indices.append(add(slant(mask,value),dict(parent_id=r['parent_id'],contrast=9,role='slant_sensitivity',native_bbox=r['native_bbox'],shear=value,split=False,merge=False,iou=None,complete_correspondence_claim=False)))
        photo_ok=s['source_extent_resolved'];parents.append(dict(parent_id=r['parent_id'],audit_id=r['audit_id'],original_proposal_index=j,caption=r['caption'],corpus='fresh',native_source=r['native_source'],native_bbox=r['native_bbox'],native_crop=r['native_crop'],body_proxy=r['body_proxy'],source_membership=s['membership'],source_parent_status=s['source_parent_status'],source_extent_resolved=photo_ok,full_extent_state='source_resolved' if photo_ok else 'unknown',full_physical_distance_bounded=False,primary_index=primary,candidate_indices=indices,correspondence=corr,full_parent_coordinate=None if not photo_ok else 'observed_candidates_not_pixel_truth',source_family_or_class=None,semantic_features_required=False))
        if j%40==0:print('Fresh frozen-procedure ensembles',j,'/',len(rr),flush=True)
    fresh_n=len(parents);old=read_json(OLD/'source_parent_ensembles.json');oldnative=np.load(OLD/'native_candidate_masks.npz');oldfields=np.load(OLD/'direct_image_fields.npz');old_candidates={r['index']:r for r in old['candidates']};importmap={}
    for r in old['parents']:
        if r['corpus']!='reference':continue
        for i in r['candidate_indices']:
            q=old_candidates[i];meta={k:v for k,v in q.items() if k not in ['candidate_id','index','native_shape']};k=add(oldnative[q['candidate_id']],meta);importmap[i]=k
            for name,arr in [('shape64',shapes),('sdf64',fields),('shape32',small),('shape128',large)]:assert np.array_equal(arr[k],oldfields[name][i]),'Frozen reference encoder differs'
        projected={k:r[k] for k in ['parent_id','audit_id','caption','native_source','native_bbox','native_crop','body_proxy','source_membership','source_parent_status','source_extent_resolved','full_extent_state','full_physical_distance_bounded']};projected.update(corpus='separate_frozen_reference',primary_index=importmap[r['primary_index']],candidate_indices=[importmap[i] for i in r['candidate_indices']],source_family_or_class=None,semantic_features_required=False);parents.append(projected)
    # Source alternatives preserve whole evidence, never choose a union for similarity.
    by={r['audit_id']:r for r in parents[:fresh_n]};alts=[]
    for a in src['extent_alternatives']:
        q=dict(a,observed_union_index=None,full_parent_embedding=None,complete_physical_distance=None)
        if len(a['audit_ids'])>1:
            members=[by[n] for n in a['audit_ids']];box=np.array([m['native_bbox'] for m in members]);x=int(box[:,0].min());y=int(box[:,1].min());c=int(box[:,2].max());d=int(box[:,3].max());um=np.zeros((d-y,c-x),np.uint8)
            for m in members:
                xx,yy,ee,ff=m['native_bbox'];pm=native[candidates[m['primary_index']]['candidate_id']];um[yy-y:ff-y,xx-x:ee-x]|=pm
            q['observed_union_index']=add(um,dict(parent_id='_'.join(a['audit_ids'])+'_extent_alternative',contrast=9,role='partial_source_union_no_invented_bridge',native_bbox=[x,y,c,d],split=True,merge=False,iou=None,complete_correspondence_claim=False))
        alts.append(q)
    np.savez_compressed(D/'native_candidate_masks.npz',**native);np.savez_compressed(D/'direct_image_fields.npz',shape64=np.array(shapes),sdf64=np.array(fields),shape32=np.array(small),shape128=np.array(large));save(D/'source_parent_ensembles.json',dict(created_at_utc=now(),parents=parents,candidates=candidates,fresh_n=fresh_n,reference_n=len(parents)-fresh_n,extent_alternatives=alts,frozen_reference_all_fields_exact=True,Trial1_representation_functions_sha256=sha256(OUT/'src/build_direct_morphology.py'),no_V3_or_feature_labels=True));seal([D/'native_candidate_masks.npz',D/'direct_image_fields.npz',D/'source_parent_ensembles.json',OUT/'src/build_direct_morphology2.py'],D/'SHAPE_SEAL.json');print('Ensembles built; predictions remain unopened',fresh_n,'fresh',len(parents)-fresh_n,'reference',len(candidates),'candidates',flush=True)
if __name__=='__main__':main()
