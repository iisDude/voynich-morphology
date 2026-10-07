from dm2_robustness_common import *
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import csr_matrix,vstack
from collections import Counter
import numpy as np

def dyad(r):return tuple(sorted([r['caption_left'],r['caption_right']],key=int))
def select(rows,mode,seed):
    if not rows:return [],dict(maximum_n=0,status='empty')
    if mode=='unrestricted':return [r['pair_id'] for r in rows],dict(maximum_n=len(rows),status='all')
    constraints=[]
    if mode in ['parent','parent_dyad']:
        for p in sorted({p for r in rows for p in [r['left_parent'],r['right_parent']]}):constraints.append([int(p in [r['left_parent'],r['right_parent']]) for r in rows])
    if mode in ['dyad','parent_dyad']:
        for d in sorted({dyad(r) for r in rows}):constraints.append([int(dyad(r)==d) for r in rows])
    n=len(rows);a=csr_matrix(np.array(constraints));limits=LinearConstraint(a,-np.inf,np.ones(len(constraints)));bounds=Bounds(np.zeros(n),np.ones(n));sol=milp(-np.ones(n),integrality=np.ones(n),bounds=bounds,constraints=limits,options={'mip_rel_gap':0.});assert sol.success;maximum=int(round(-sol.fun));priority=np.random.default_rng(seed).permutation(np.arange(1,n+1));aa=vstack([a,csr_matrix(np.ones((1,n)))]);lo=np.r_[np.full(len(constraints),-np.inf),maximum];hi=np.r_[np.ones(len(constraints)),maximum];ss=milp(priority.astype(float),integrality=np.ones(n),bounds=bounds,constraints=LinearConstraint(aa,lo,hi),options={'mip_rel_gap':0.});assert ss.success;ids=[r['pair_id'] for r,z in zip(rows,ss.x) if z>.5];assert len(ids)==maximum
    return ids,dict(maximum_n=maximum,cardinality_objective=-float(sol.fun),priority_objective=float(ss.fun),status='proven optimal',seed=seed,no_category_or_distance_objective=True)
def greedy(rows,mode,seed):
    rng=np.random.default_rng(seed);parents=set();dyads=set();out=[]
    for i in rng.permutation(len(rows)):
        r=rows[int(i)];ps={r['left_parent'],r['right_parent']};d=dyad(r)
        if mode in ['parent','parent_dyad'] and ps&parents:continue
        if mode in ['dyad','parent_dyad'] and d in dyads:continue
        out.append(r['pair_id']);parents|=ps;dyads.add(d)
    return out
def contrast_label(r,name):
    v=r['rating']
    if name=='binary':return int(v==2) if v in [0,2] else None
    if name=='same_vs_partial':return int(v==2) if v in [1,2] else None
    if name=='partial_vs_different':return int(v==1) if v in [0,1] else None
    if name=='partial_as_same':return int(v in [1,2]) if v in [0,1,2] else None
    if name=='partial_as_different':return int(v==2) if v in [0,1,2] else None
    raise ValueError(name)

def inputs():
    loc=read_json(B/'source_location_aids.json')['parents'];key={r['pair_id']:r for r in read_json(B/'pair_pool_hidden_key.json')['pairs']};ratings=read_json(B/'source_similarity_decisions.json')['pairs'];rows=[]
    for r in ratings:
        k=key[r['pair_id']];rows.append(dict(pair_id=r['pair_id'],rating=r['rating'],left_parent=loc[k['left_index']]['parent_id'],right_parent=loc[k['right_index']]['parent_id'],caption_left=k['caption_left'],caption_right=k['caption_right'],sampling_method=k['sampling_method']))
    source={r['parent_id']:r for r in read_json(B/'source_decisions.json')['parents']};ensemble={r['parent_id']:r for r in read_json(B/'source_parent_ensembles.json')['parents']};flags={}
    for pid,s in source.items():
        e=ensemble[pid];why=[name for name in ['possible_join','possible_split','detached_association_unknown','faint_or_insufficient_extent','neighboring_row_contact_possible'] if s[name]];corr=e['correspondence'];extent=s['source_extent_resolved'] and not why;recovery=len(corr)==2 and all(not c['missing'] and not c['split'] and not c['merge'] and len(c['candidate_indices'])==1 for c in corr);flags[pid]=dict(extent_clean=bool(extent),recovery_clean=bool(recovery),field_edge=bool(s['field_edge_location_aid']),source_flags=why,source_extent_resolved=s['source_extent_resolved'],audit_id=s['audit_id'])
    return rows,flags
def allowed(r,flags,name):
    ff=[flags[r['left_parent']],flags[r['right_parent']]]
    if name=='all':return True
    if name=='extent_clean':return all(f['extent_clean'] for f in ff)
    if name=='recovery_clean':return all(f['recovery_clean'] for f in ff)
    if name=='extent_and_recovery_clean':return all(f['extent_clean'] and f['recovery_clean'] for f in ff)
    if name=='field_edge_sensitivity':return all(f['extent_clean'] and f['recovery_clean'] and not f['field_edge'] for f in ff)
    raise ValueError(name)
def main():
    guard();verify_base();verify_seal(D/'PROTOCOL_SEAL.json');assert not (D/'SUBSET_SEAL.json').exists();rows,flags=inputs();analyses=[];seed=read_json(D/'PLAN.json')['seed'];filters=['all','extent_clean','recovery_clean','extent_and_recovery_clean','field_edge_sensitivity'];strata=['pooled','broad_random','aspect_matched']
    def add(f,s,c,mode):
        eligible=[r for r in rows if allowed(r,flags,f) and (s=='pooled' or r['sampling_method']==s) and contrast_label(r,c) is not None];index=len(analyses);selection_seed=seed+100+index;ids,diagnosis=select(eligible,mode,selection_seed);replicates=[dict(seed=seed+10000+index*100+j,pair_ids=greedy(eligible,mode,seed+10000+index*100+j)) for j in range(50)] if c=='binary' and mode!='unrestricted' else [];analyses.append(dict(analysis_id=f'{f}__{s}__{c}__{mode}',source_filter=f,stratum=s,contrast=c,dependence=mode,selection_seed=selection_seed,eligible_pair_ids=[r['pair_id'] for r in eligible],selected_pair_ids=ids,selection=diagnosis,greedy_selection_sensitivity=replicates))
    for f in filters:
        for s in strata:
            for mode in ['unrestricted','parent','dyad','parent_dyad']:add(f,s,'binary',mode)
        print('Sealed-rule selections prepared',f,flush=True)
    for f in ['all','recovery_clean','extent_and_recovery_clean']:
        for s in strata:
            for c in ['same_vs_partial','partial_vs_different','partial_as_same','partial_as_different']:add(f,s,c,'unrestricted')
        for c in ['same_vs_partial','partial_vs_different','partial_as_same','partial_as_different']:add(f,'pooled',c,'parent')
    save(D/'source_filter_audit.json',dict(parents=flags,source_resolved_parent_n=sum(f['source_extent_resolved'] for f in flags.values()),extent_clean_n=sum(f['extent_clean'] for f in flags.values()),recovery_clean_n=sum(f['recovery_clean'] for f in flags.values()),eligible_population_note='Includes192 source proposals for filter audit, but evaluation remains frozen360 reviewed pairs among165 source-resolved parents. Unknown extent never newly imputed.'))
    save(D/'analysis_selections.json',dict(prepared_at_utc=now(),source_pair_metadata=rows,analyses=analyses,contour_scores_not_used_in_selection=True));seal([D/'source_filter_audit.json',D/'analysis_selections.json',OUT/'src/prepare_dm2_robustness.py'],D/'SUBSET_SEAL.json');print('All conservative subsets frozen before repeat review/new robustness outcomes',len(analyses),flush=True)
if __name__=='__main__':main()
