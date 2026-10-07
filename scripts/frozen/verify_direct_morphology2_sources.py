from direct_morphology2_common import *
from benchmark_membership_v5 import page_features
from build_direct_morphology import tight,slant
from PIL import Image
import numpy as np
def main():
    verify(); verify_seal(D/'SOURCE_SEAL.json'); verify_seal(D/'SHAPE_SEAL.json'); data=read_json(D/'source_parent_ensembles.json'); masks=np.load(D/'native_candidate_masks.npz'); loc=read_json(D/'source_location_aids.json')['parents']; parent={r['parent_id']:r for r in data['parents']}; cache=None; view=None; checked=0
    for r in loc:
        if view!=r['native_source']:cache=page_features(r);view=r['native_source']
        rgb,delta,cc=cache; x,y,e,f=r['native_bbox']; primary=(cc[0][1][y:f,x:e]==r['cc_label']).astype(np.uint8); assert np.array_equal(primary,(np.asarray(Image.open(OUT/r['mask_path']))>0).astype(np.uint8)); a,b=r['crop_origin']; crop=np.asarray(Image.open(OUT/r['native_crop'])); assert np.array_equal(crop,rgb[b:b+crop.shape[0],a:a+crop.shape[1]]); p=parent[r['parent_id']]; n=primary.sum()
        for idx in p['candidate_indices']:
            q=data['candidates'][idx]; z=masks[q['candidate_id']]; bx,by,be,bf=q['native_bbox']
            if q['role']=='primary_source_located_raster':expected=primary
            elif q['role']=='slant_sensitivity':expected=slant(primary,q['shear'])
            else:
                vi={6:1,12:2}[q['contrast']]; labels=cc[vi][1]; ids,cnt=np.unique(labels[y:f,x:e][primary>0],return_counts=True); matches=[int(k) for k,c in zip(ids,cnt) if k and c>=n*.05]
                if q['role']=='split_union_observed_recovery':expected=np.isin(labels[by:bf,bx:be],matches).astype(np.uint8)
                else:
                    candidates=[k for k in matches if list(map(int,cc[vi][2][k,:4]))==[bx,by,be-bx,bf-by]]; assert len(candidates)==1; expected=(labels[by:bf,bx:be]==candidates[0]).astype(np.uint8)
            assert np.array_equal(tight(expected),z),q['candidate_id'];checked+=1
    old=read_json(OLD/'source_parent_ensembles.json'); oldby={r['parent_id']:r for r in old['parents']}; oldfields=np.load(OLD/'direct_image_fields.npz'); fields=np.load(D/'direct_image_fields.npz'); refs=0
    for p in data['parents']:
        if p['corpus']!='separate_frozen_reference':continue
        oldp=oldby[p['parent_id']]; assert len(p['candidate_indices'])==len(oldp['candidate_indices'])
        for i,j in zip(p['candidate_indices'],oldp['candidate_indices']):
            for name in ['shape32','shape64','shape128','sdf64']:assert np.array_equal(fields[name][i],oldfields[name][j])
            refs+=1
    result=dict(checked_at_utc=now(),fresh_native_RGB_crops_exact=len(loc),fresh_primary_masks_exact=len(loc),fresh_candidate_native_recovery_exact=checked,frozen_reference_fields_exact=refs,source_adjudication_not_independently_validated=True,failures=[])
    target=P/'SOURCE_REPLAY.json' if (D/'FREEZE_MANIFEST.json').exists() else T/'SOURCE_REPLAY.json';write_json(target,result); print('Native RGB and raster correspondence replay complete',checked,'fresh candidates',flush=True)
if __name__=='__main__':main()
