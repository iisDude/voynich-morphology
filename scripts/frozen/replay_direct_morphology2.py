from direct_morphology2_common import *
from build_direct_morphology import tight,normalize,sdf
from evaluate_direct_morphology import contour_matrix,sdf_matrix,envelopes
import numpy as np
def replay(distances=False):
    verify(); verify_seal(D/'SHAPE_SEAL.json')
    data=read_json(D/'source_parent_ensembles.json'); masks=np.load(D/'native_candidate_masks.npz'); fields=np.load(D/'direct_image_fields.npz'); result={}
    for key,size in [('shape32',32),('shape64',64),('shape128',128)]:
        rebuilt=np.array([normalize(masks[c['candidate_id']],size) for c in data['candidates']]); assert np.array_equal(rebuilt,fields[key]),key; result[key]=len(rebuilt)
    rebuilt=np.array([sdf(s) for s in fields['shape64']]); assert np.array_equal(rebuilt,fields['sdf64']); result['sdf64']=len(rebuilt)
    result['source_unknowns_preserved']=all(p['full_extent_state']=='unknown' and p['full_physical_distance_bounded'] is False for p in data['parents'] if not p['source_extent_resolved']); assert result['source_unknowns_preserved']
    if distances:
        matrices=np.load(D/'direct_distance_matrices.npz'); cc=contour_matrix(fields['shape64']); ss=sdf_matrix(fields['sdf64']); b,l,h=envelopes(data['parents'],cc); sb,sl,sh=envelopes(data['parents'],ss); primary=[p['primary_index'] for p in data['parents']]
        rr=dict(candidate_contour64=cc,candidate_sdf64=ss,primary_contour64=b,observed_contour_low=l,observed_contour_high=h,primary_sdf64=sb,observed_sdf_low=sl,observed_sdf_high=sh,primary_contour32=contour_matrix(fields['shape32'][primary]),primary_contour128=contour_matrix(fields['shape128'][primary]))
        for key,a in rr.items(): assert np.array_equal(a,matrices[key]),key
        result['exact_distance_matrices']=list(rr)
    result.update(checked_at_utc=now(),candidate_n=len(data['candidates']),parent_n=len(data['parents']),not_source_ground_truth=True)
    return result
if __name__=='__main__':
    import sys
    full='--distances' in sys.argv; result=replay(full)
    target=P/'POSTFREEZE_REPLAY.json' if (D/'FREEZE_MANIFEST.json').exists() else T/('DETERMINISTIC_REPLAY.json' if full else 'PRE_REPEAT_REPLAY.json')
    write_json(target,result); print('Exact replay complete',result['candidate_n'],'candidates',flush=True)
