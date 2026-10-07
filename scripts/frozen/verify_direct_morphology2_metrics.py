from direct_morphology2_common import *
from evaluate_direct_morphology2 import auc
from collections import Counter
import numpy as np
def main():
    verify_seal(D/'DISTANCE_SEAL.json'); sim=read_json(T/'primary_and_secondary_metrics.json'); rr=sim['pairs']; binary=[r for r in rr if r['rating'] in [0,2]]; parents=read_json(D/'source_parent_ensembles.json')['parents']; by={r['parent_id']:i for i,r in enumerate(parents)}; matrices=np.load(D/'direct_distance_matrices.npz'); aspects={r['parent_id']:np.log((r['native_bbox'][2]-r['native_bbox'][0])/(r['native_bbox'][3]-r['native_bbox'][1])) for r in parents}; source={r['pair_id']:r['rating'] for r in read_json(D/'source_similarity_decisions.json')['pairs']}
    for r in rr:
        i=by[r['left_parent']];j=by[r['right_parent']]; assert r['rating']==source[r['pair_id']]; assert r['caption_left']!=r['caption_right'];assert parents[i]['source_extent_resolved'] and parents[j]['source_extent_resolved'];assert abs(r['aspect_only']-abs(aspects[r['left_parent']]-aspects[r['right_parent']]))<1e-12
        for name,key in [('contour64','primary_contour64'),('sdf64','primary_sdf64'),('contour32','primary_contour32'),('contour128','primary_contour128'),('contour_observed_low','observed_contour_low'),('contour_observed_high','observed_contour_high')]:assert r[name]==float(matrices[key][i,j])
    for name in sim['metrics']:assert auc(binary,name)==sim['metrics'][name]['AUROC']
    caps=sorted({c for r in binary for c in [r['caption_left'],r['caption_right']]},key=int); rng=np.random.default_rng(sim['bootstrap_seed']); bb=[];dd=[]
    for _ in range(2000):
        count=Counter(rng.choice(caps,len(caps),replace=True));w=[count[r['caption_left']]*count[r['caption_right']] for r in binary];a=auc(binary,'contour64',w);z=auc(binary,'aspect_only',w)
        if a is not None and z is not None:bb.append(a);dd.append(a-z)
    assert len(bb)==sim['valid_bootstrap_n']; assert np.array_equal(np.percentile(bb,[2.5,97.5]),sim['primary_caption_node_bootstrap95']);assert np.array_equal(np.percentile(dd,[2.5,97.5]),sim['paired_delta_bootstrap95'])
    pool=read_json(D/'pair_pool_hidden_key.json')['pairs']; degree=Counter(i for p in pool for i in [p['left_index'],p['right_index']]);assert max(degree.values())<=12;assert len({tuple(sorted([p['left_index'],p['right_index']])) for p in pool})==len(pool);assert len(rr)==read_json(D/'OPENED_PAIRS.json')['final_used_n'];assert [r['pair_id'] for r in rr]==[p['pair_id'] for p in pool[:len(rr)]]
    # All atlas local image links resolve, and every source has a candidate card.
    import re
    atlas=OUT/'reports/26_direct_contour_morphology_atlas_trial2.html';text=atlas.read_text(encoding='utf-8');links=re.findall(r"src='([^']+)'",text)
    for link in links:assert (atlas.parent/link).resolve().is_file(),link
    assert text.count('<details>')==len(parents)
    result=dict(checked_at_utc=now(),source_ratings_and_pair_order_exact=True,primary_secondary_AUROCs_exact=True,native_aspect_baseline_exact=True,two_endpoint_bootstrap_and_paired_delta_exact=True,unique_pool_n=len(pool),maximum_parent_degree=max(degree.values()),used_pool_prefix_n=len(rr),atlas_cards=len(parents),local_atlas_image_links_checked=len(links),failures=[])
    target=P/'METRIC_REPLAY.json' if (D/'FREEZE_MANIFEST.json').exists() else T/'METRIC_REPLAY.json';write_json(target,result);print('Metric, sampling and atlas replay complete',flush=True)
if __name__=='__main__':main()
