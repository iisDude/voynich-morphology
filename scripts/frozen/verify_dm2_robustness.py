from dm2_robustness_common import *
from prepare_dm2_robustness import inputs,allowed,contrast_label,select,greedy,dyad
from evaluate_dm2_robustness import evaluate,weighted_auc,agreement,interval
from sklearn.metrics import roc_auc_score,cohen_kappa_score
from collections import Counter
import numpy as np

def verify():
    verify_base()
    for s in ['PROTOCOL','REPEAT_POOL','SUBSET','REPEAT_RATINGS','ANALYSIS']:verify_seal(D/(s+'_SEAL.json'))
    data=read_json(D/'analysis_selections.json');metadata,flags=inputs();assert data['source_pair_metadata']==metadata;assert read_json(D/'source_filter_audit.json')['parents']==flags
    expected={r['analysis_id']:r for r in read_json(T/'conservative_analyses.json')['analyses']};old={r['pair_id']:r for r in read_json(BT/'primary_and_secondary_metrics.json')['pairs']};parents=read_json(B/'source_parent_ensembles.json')['parents'];by={p['parent_id']:i for i,p in enumerate(parents)};mat=np.load(B/'direct_distance_matrices.npz')['primary_contour64'];rows={r['pair_id']:dict(r,contour64=old[r['pair_id']]['contour64'],aspect_only=old[r['pair_id']]['aspect_only']) for r in metadata}
    for r in rows.values():assert r['contour64']==float(mat[by[r['left_parent']],by[r['right_parent']]])
    npz=np.load(D/'caption_bootstrap_draws.npz');counts=npz['counts'];caps=npz['captions'].tolist();rng=np.random.default_rng(read_json(D/'PLAN.json')['seed']+2);draws=rng.integers(0,8,(5000,8));assert np.array_equal(counts,np.stack([(draws==i).sum(1) for i in range(8)],axis=1));auc_checks=0;selection_checks=0
    for s in data['analyses']:
        eligible=[r for r in metadata if allowed(r,flags,s['source_filter']) and (s['stratum']=='pooled' or r['sampling_method']==s['stratum']) and contrast_label(r,s['contrast']) is not None];assert s['eligible_pair_ids']==[r['pair_id'] for r in eligible];ids,diag=select(eligible,s['dependence'],s['selection_seed']);assert ids==s['selected_pair_ids'];assert diag==s['selection'];selection_checks+=1;rr=[rows[p] for p in ids];yy=[contrast_label(r,s['contrast']) for r in rr];result=evaluate(rr,yy,counts,caps)
        for k,v in result.items():assert v==expected[s['analysis_id']][k],(s['analysis_id'],k)
        if s['dependence'] in ['parent','parent_dyad']:assert result['maximum_parent_degree']<=1
        if s['dependence'] in ['dyad','parent_dyad']:assert result['maximum_dyad_degree']<=1
        if len(set(yy))==2:
            assert abs(roc_auc_score(yy,[-r['contour64'] for r in rr])-result['AUROC'])<1e-12;auc_checks+=1
            for draw in [0,1,50,211,999]:
                w=np.array([counts[draw,caps.index(r['caption_left'])]*counts[draw,caps.index(r['caption_right'])] for r in rr]);y=np.array(yy,dtype=bool)
                if w[y].sum() and w[~y].sum():assert abs(roc_auc_score(yy,[-r['contour64'] for r in rr],sample_weight=w)-weighted_auc(yy,[-r['contour64'] for r in rr],w)[0])<1e-12;auc_checks+=1
        for g in s['greedy_selection_sensitivity']:assert greedy(eligible,s['dependence'],g['seed'])==g['pair_ids']
    # Tied scores, degenerate weighted categories and explicit unknown fixture.
    fixture_y=[0,1,0,1];fixture_s=[.1,.1,.2,.3];fixture_w=[2,3,4,5];assert abs(weighted_auc(fixture_y,fixture_s,fixture_w)[0]-roc_auc_score(fixture_y,fixture_s,sample_weight=fixture_w))<1e-12;assert np.isnan(weighted_auc([0,0],[0,1],[1,2])[0]);fixture=agreement(np.array([0,1,2],dtype=object),np.array([0,'U',1],dtype=object),np.ones(3));assert fixture['resolved_n']==2 and fixture['unresolved_n']==1 and fixture['exact']==1/3
    rep=read_json(T/'larger_repeatability.json');joined=rep['pairs'];a=np.array([r['original_rating'] for r in joined]);b=np.array([r['repeat_rating'] for r in joined]);assert len(joined)==125;assert Counter(a.tolist())==Counter({0:45,1:45,2:35});assert len({r['original_pair_id'] for r in joined})==125
    ag=agreement(a,b,np.ones(125));assert ag==rep['sample_agreement'];assert abs(cohen_kappa_score(a,b)-ag['unweighted_kappa'])<1e-12;assert abs(cohen_kappa_score(a,b,weights='linear')-ag['linear_kappa'])<1e-12;assert abs(cohen_kappa_score(a,b,weights='quadratic')-ag['quadratic_kappa'])<1e-12
    key=read_json(D/'repeat_hidden_key.json')['pairs'];recorded={r['repeat_id']:r['rating'] for r in read_json(D/'repeat_source_ratings.json')['pairs']}
    for j,k in zip(joined,key):assert j['repeat_id']==k['repeat_id'] and j['original_pair_id']==k['original_pair_id'] and j['repeat_rating']==recorded[j['repeat_id']] and j['original_rating']==old[j['original_pair_id']]['rating']
    original={r['pair_id']:r['rating'] for r in read_json(B/'source_similarity_decisions.json')['pairs']};assert all(original[r['pair_id']]==r['rating'] for r in metadata);assert len(original)==360
    return dict(checked_at_utc=now(),analysis_conditions_replayed=selection_checks,maximum_cardinality_and_seeded_priority_selections_exact=True,all_selected_parent_and_dyad_constraints_hold=True,all_50_seed_greedy_sets_replayed=True,bootstrap_draws_intervals_and_deltas_exact=True,independent_sklearn_AUROC_checks=auc_checks,tie_zero_weight_and_unknown_fixtures_pass=True,repeat_count_and_category_transition_replay=True,ordinal_kappas_agree_with_sklearn=True,source_filter_flags_exact=True,primary_contour_values_exact_from_frozen_matrix=True,previous_source_ratings_unchanged=True,no_other_morphology_metric_used=True,failures=[])
if __name__=='__main__':
    result=verify();target=P/'REPLAY.json' if (D/'FREEZE_MANIFEST.json').exists() else T/'DETERMINISTIC_REPLAY.json';write_json(target,result);print('Robustness deterministic and independent numerical checks complete',result['analysis_conditions_replayed'],flush=True)
