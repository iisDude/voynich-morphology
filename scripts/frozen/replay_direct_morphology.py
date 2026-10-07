from direct_morphology_common import *
from build_direct_morphology import normalize,sdf
from evaluate_direct_morphology import contour_matrix,sdf_matrix,envelopes
import numpy as np
def run(target):
    verify();verify_seal(D/'SHAPE_SEAL.json');verify_seal(D/'DISTANCE_SEAL.json');data=read_json(D/'source_parent_ensembles.json');fields=np.load(D/'direct_image_fields.npz');native=np.load(D/'native_candidate_masks.npz')
    for r in data['candidates']:
        m=native[r['candidate_id']];i=r['index'];q=normalize(m);assert np.array_equal(q,fields['shape64'][i]);assert np.array_equal(sdf(q),fields['sdf64'][i]);assert np.array_equal(normalize(m,32),fields['shape32'][i]);assert np.array_equal(normalize(m,128),fields['shape128'][i])
    mat=np.load(D/'direct_distance_matrices.npz');cc=contour_matrix(fields['shape64']);ss=sdf_matrix(fields['sdf64']);assert np.array_equal(cc,mat['candidate_contour64']);assert np.array_equal(ss,mat['candidate_sdf64']);bb,lo,hi=envelopes(data['parents'],cc);sb,sl,sh=envelopes(data['parents'],ss)
    for k,v in [('primary_contour64',bb),('observed_contour_low',lo),('observed_contour_high',hi),('primary_sdf64',sb),('observed_sdf_low',sl),('observed_sdf_high',sh)]:assert np.array_equal(v,mat[k]),k
    primary=np.array([r['primary_index'] for r in data['parents']])
    for size in [32,128]:assert np.array_equal(contour_matrix(fields[f'shape{size}'][primary]),mat[f'primary_contour{size}'])
    assert np.all(lo<=bb) and np.all(bb<=hi);assert np.allclose(cc,cc.T);assert np.allclose(ss,ss.T)
    assert all(r['full_extent_state']=='unknown' and r['full_physical_distance_bounded'] is False for r in data['parents'] if not r['source_extent_resolved']);assert data['extent_alternatives'][0]['full_parent_embedding'] is None
    # Formula check without matrix multiplication; computational fixture, not source validation.
    rng=np.random.default_rng(20261017)
    for i,j in rng.integers(0,len(cc),size=(20,2)):
        def edge(s):return s.astype(bool)&~__import__('cv2').erode(s,np.ones((3,3),np.uint8)).astype(bool)
        a=edge(fields['shape64'][i]);b=edge(fields['shape64'][j]);cv2=__import__('cv2');da=cv2.distanceTransform((~a).astype(np.uint8),cv2.DIST_L2,3);db=cv2.distanceTransform((~b).astype(np.uint8),cv2.DIST_L2,3);direct=(da[b].mean()+db[a].mean())/112;assert np.isclose(direct,cc[i,j],atol=1e-7)
    try:contour_matrix(np.zeros((1,64,64),np.uint8))
    except AssertionError:missing_refused=True
    else:missing_refused=False
    assert missing_refused
    write_json(target,dict(checked_at_utc=now(),native_candidate_masks=len(data['candidates']),parents=len(data['parents']),normalized_shapes_all_three_resolutions_exact=True,SDF_fields_exact=True,ten_distance_matrices_exact=True,envelope_symmetry_and_containment=True,unknown_extent_preserved=True,missing_shape_cannot_receive_zero_distance=True,twenty_direct_formula_checks=True,source_semantics_not_independently_validated=True,failures=[]));print('Direct image-field and distance replay pass',len(data['candidates']),flush=True)
if __name__=='__main__':guard();run(T/'deterministic_replay.json')
