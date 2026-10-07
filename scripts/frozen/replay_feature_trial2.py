from feature_trial2_common import *
from measure_feature_trial2 import measure,distances,baselines
import numpy as np
def main():
    guard();verify_dependencies();verify_seal(D/'SOURCE_SEAL.json');verify_seal(D/'METRIC_SEAL.json');spec=read_json(D/'PLAN.json');rec=read_json(D/'source_location_aids.json')['parents'];sources={r['parent_id']:r for r in read_json(D/'source_decisions.json')['parents']};old=read_json(D/'feature_profiles.json')['parents'];native=np.load(D/'native_variants.npz');computed=[]
    for i,r in enumerate(rec):computed.append(measure(r,[native[f'{i}_{j}'] for j in range(3)],spec,sources[r['parent_id']]))
    assert computed==old;dm,ss=distances(computed,spec);ad,ch,co,scale=baselines(np.load(D/'source_shapes.npz')['shapes'][:,0],computed);prior=np.load(D/'distances.npz')
    for k,v in [('profile',dm),('shared',ss),('aspect',ad),('contour',ch),('combined',co)]:assert np.array_equal(v,prior[k]),k
    # Source-unknown cavities cannot silently enter usable fields.
    for r in computed:
        if sources[r['parent_id']]['source_cavity_count'] is None:assert all(f['source_qualified_status']!='stable' for f in r['features'].values() if f['family']=='cavity')
        if not r['source_resolved']:assert not r['usable_partial_profile']
    save(T/'deterministic_replay.json',dict(checked_at_utc=now(),parents=len(old),descriptors=36,variant_measurements=7,feature_profiles_exact=True,five_distance_matrices_exact=True,source_uncertainty_preserved=True,scope='Measurement/distance replay from sealed matched native rasters; source semantics not independently validated.'))
    print('221 feature profiles and5 distance matrices exactly replayed',flush=True)
if __name__=='__main__':main()
