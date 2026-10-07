"""Contribution-only numerical replay. Source adjudication remains a fixed observational input."""
from pathlib import Path
import sys,json,collections,os
for _key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ.setdefault(_key,'2')
sys.dont_write_bytecode=True
PKG=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(PKG/'scripts'),str(PKG/'scripts/frozen')]
from evidence import Evidence
import numpy as np
from sklearn.metrics import roc_auc_score,cohen_kappa_score
from build_direct_morphology import normalize,sdf
from evaluate_direct_morphology import contour_matrix,sdf_matrix,envelopes
from evaluate_dm2_robustness import evaluate,agreement
from prepare_dm2_robustness import contrast_label,select,allowed,greedy
def run(full=True):
 e=Evidence();results={}
 for trial in ['direct_morphology_trial1','direct_morphology_trial2']:
  d='data/observations/'+trial+'/';v=e.json(d+'source_parent_ensembles.json');f=e.npz(d+'direct_image_fields.npz');n=e.npz(d+'native_candidate_masks.npz');m=e.npz(d+'direct_distance_matrices.npz')
  for key,size in [('shape32',32),('shape64',64),('shape128',128)]:assert np.array_equal(np.array([normalize(n[c['candidate_id']],size) for c in v['candidates']]),f[key]),(trial,key)
  assert np.array_equal(np.array([sdf(x) for x in f['shape64']]),f['sdf64'])
  assert all(p['full_extent_state']=='unknown' and not p['full_physical_distance_bounded'] for p in v['parents'] if not p['source_extent_resolved'])
  if full:
   cc=contour_matrix(f['shape64']);ss=sdf_matrix(f['sdf64']);b,lo,hi=envelopes(v['parents'],cc);sb,sl,sh=envelopes(v['parents'],ss);idx=[p['primary_index'] for p in v['parents']]
   expected=dict(candidate_contour64=cc,candidate_sdf64=ss,primary_contour64=b,observed_contour_low=lo,observed_contour_high=hi,primary_sdf64=sb,observed_sdf_low=sl,observed_sdf_high=sh,primary_contour32=contour_matrix(f['shape32'][idx]),primary_contour128=contour_matrix(f['shape128'][idx]))
   for k,a in expected.items():assert np.array_equal(a,m[k]),(trial,k)
  results[trial]=dict(candidate_n=len(v['candidates']),parent_n=len(v['parents']),normalized_fields_exact=True,ten_distance_matrices_exact=full,source_unknowns_preserved=True)
  print('Replayed',trial,flush=True)
 # Registered Trial 2 metrics and caption dependence-aware bootstrap.
 d='data/observations/direct_morphology_trial2/';t='tests/direct_morphology_trial2/';v=e.json(d+'source_parent_ensembles.json');parents=v['parents'];by={p['parent_id']:i for i,p in enumerate(parents)};m=e.npz(d+'direct_distance_matrices.npz');out=e.json(t+'primary_and_secondary_metrics.json');rr=out['pairs'];ratings={p['pair_id']:p['rating'] for p in e.json(d+'source_similarity_decisions.json')['pairs']};binary=[r for r in rr if r['rating'] in [0,2]]
 for r in rr:
  i,j=by[r['left_parent']],by[r['right_parent']];assert r['rating']==ratings[r['pair_id']];assert r['caption_left']!=r['caption_right'];assert parents[i]['source_extent_resolved'] and parents[j]['source_extent_resolved'];assert r['contour64']==float(m['primary_contour64'][i,j])
 for key in ['contour64','aspect_only','sdf64','contour32','contour128']:assert roc_auc_score([r['rating']==2 for r in binary],[-r[key] for r in binary])==out['metrics'][key]['AUROC']
 caps=sorted({c for r in binary for c in [r['caption_left'],r['caption_right']]},key=int);rng=np.random.default_rng(out['bootstrap_seed']);b=[];delta=[]
 for _ in range(2000):
  cnt=collections.Counter(rng.choice(caps,len(caps),replace=True));w=np.array([cnt[r['caption_left']]*cnt[r['caption_right']] for r in binary]);y=np.array([r['rating']==2 for r in binary])
  if not (w[y].sum() and w[~y].sum()):continue
  a=roc_auc_score(y,[-r['contour64'] for r in binary],sample_weight=w);z=roc_auc_score(y,[-r['aspect_only'] for r in binary],sample_weight=w);b.append(a);delta.append(a-z)
 assert len(b)==out['valid_bootstrap_n'];assert np.array_equal(np.percentile(b,[2.5,97.5]),out['primary_caption_node_bootstrap95']);assert np.array_equal(np.percentile(delta,[2.5,97.5]),out['paired_delta_bootstrap95'])
 results['trial2_metrics']=dict(AUROC=out['metrics']['contour64']['AUROC'],binary_n=len(binary),caption_bootstrap_exact=True,paired_delta_exact=True)
 # Robustness selection graphs, source filters, 108 conditions and repeatability.
 d='data/observations/direct_morphology_trial2_robustness_v1/';t='tests/direct_morphology_trial2_robustness_v1/';selection=e.json(d+'analysis_selections.json');flags=e.json(d+'source_filter_audit.json')['parents'];spec=e.json(d+'PLAN.json');a=e.npz(d+'caption_bootstrap_draws.npz');cnt=a['counts'];caps=a['captions'].tolist();draws=np.random.default_rng(spec['seed']+2).integers(0,8,(5000,8));assert np.array_equal(cnt,np.stack([(draws==i).sum(1) for i in range(8)],axis=1));meta=selection['source_pair_metadata'];old={r['pair_id']:r for r in rr};rows={r['pair_id']:dict(r,contour64=old[r['pair_id']]['contour64'],aspect_only=old[r['pair_id']]['aspect_only']) for r in meta};expected={r['analysis_id']:r for r in e.json(t+'conservative_analyses.json')['analyses']}
 for s in selection['analyses']:
  eligible=[r for r in meta if allowed(r,flags,s['source_filter']) and (s['stratum']=='pooled' or r['sampling_method']==s['stratum']) and contrast_label(r,s['contrast']) is not None];assert [r['pair_id'] for r in eligible]==s['eligible_pair_ids'];ids,diag=select(eligible,s['dependence'],s['selection_seed']);assert ids==s['selected_pair_ids'];assert diag==s['selection'];rs=[rows[p] for p in ids];labels=[contrast_label(r,s['contrast']) for r in rs];computed=evaluate(rs,labels,cnt,caps)
  for k,val in computed.items():assert val==expected[s['analysis_id']][k],(s['analysis_id'],k)
  if len(set(labels))==2:assert abs(roc_auc_score(labels,[-r['contour64'] for r in rs])-computed['AUROC'])<1e-12
  for g in s['greedy_selection_sensitivity']:assert greedy(eligible,s['dependence'],g['seed'])==g['pair_ids']
 rep=e.json(t+'larger_repeatability.json');ra=np.array([r['original_rating'] for r in rep['pairs']]);rb=np.array([r['repeat_rating'] for r in rep['pairs']]);ag=agreement(ra,rb,np.ones(len(ra)));assert ag==rep['sample_agreement']
 for weights,key in [(None,'unweighted_kappa'),('linear','linear_kappa'),('quadratic','quadratic_kappa')]:assert abs(cohen_kappa_score(ra,rb,weights=weights)-ag[key])<1e-12
 results['robustness']=dict(conditions_exact=len(selection['analyses']),all_selection_and_greedy_sets_exact=True,repeat_n=len(ra),exact_agreement=ag['exact'],all_intervals_exact=True)
 # Feature Trial 2 measurement replay from frozen rasters, without altering its failed gates.
 from measure_feature_trial2 import measure,distances,baselines
 d='data/observations/neutral_feature_trial2/';spec=e.json(d+'PLAN.json');rec=e.json(d+'source_location_aids.json')['parents'];sources={r['parent_id']:r for r in e.json(d+'source_decisions.json')['parents']};old=e.json(d+'feature_profiles.json')['parents'];native=e.npz(d+'native_variants.npz');computed=[measure(r,[native[f'{i}_{j}'] for j in range(3)],spec,sources[r['parent_id']]) for i,r in enumerate(rec)];assert computed==old;dm,ss=distances(computed,spec);ad,ch,co,scale=baselines(e.npz(d+'source_shapes.npz')['shapes'][:,0],computed);prior=e.npz(d+'distances.npz')
 for k,a in [('profile',dm),('shared',ss),('aspect',ad),('contour',ch),('combined',co)]:assert np.array_equal(a,prior[k]),k
 results['feature_trial2']=dict(parents=len(computed),profiles_and_five_matrices_exact=True)
 # Earlier numerical evidence remains accessible and integrity-verified, not retrained.
 seq=e.json('tests/row_benchmark_v5/sequence_completeness.json');assert seq['confirmed_target_parents']==638 and seq['assigned_v3']==311 and seq['complete_structural_rows']==0
 results['v5_conservation']=dict(confirmed_target_parents=638,assigned_v3=311,complete_structural_rows=0)
 print(json.dumps(results,indent=2));return results
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--fields-only',action='store_true');a=ap.parse_args();e=Evidence();p=e.outside(a.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(run(not a.fields_only),indent=2),encoding='utf-8')
