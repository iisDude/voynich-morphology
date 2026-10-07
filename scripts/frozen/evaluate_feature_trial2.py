"""Fixed diagnostic tests after source/metric/rating seals. Never fit features."""
from feature_trial2_common import *
from measure_feature_trial2 import distances
from evaluate_source_classes_v3 import transform,assign
from sklearn.metrics import roc_auc_score
from scipy.stats import spearmanr
from collections import Counter
import numpy as np,cv2,pickle

def labels(records,rows):
    old={r['parent_id']:r['structural_class'] for r in read_json(OLD/'discovery_parents.json')}
    v6={r['parent_id']:r['retained_v3_class'] for r in read_json(OUT/'data/observations/visual_dataset_v6/expanded_parent_assignments.json')}
    for k,v in v6.items():assert old[k]==v,'Frozen old label projection mismatch'
    old.update({r['parent_id']:r['v3_class'] for r in read_json(OLD/'fresh_assignments.json')})
    data=np.load(D/'source_shapes.npz');model=pickle.loads(MODEL.read_bytes());sh=data['shapes'];gg=data['geometry'];base=assign(transform(sh[:,0],gg[:,0],model),gg[:,0],model);alt=[]
    for vi in [1,2]:
        g=gg[:,0].copy();g[:,:3]=gg[:,vi,:3];alt.append(assign(transform(sh[:,vi],g,model),g,model))
    nuisance=np.array([cv2.warpAffine(s,np.float32([[1,.04,-1],[0,1,1]]),(48,48),flags=cv2.INTER_LINEAR,borderValue=0) for s in sh[:,0]]);nu=assign(transform(nuisance,gg[:,0],model),gg[:,0],model);out=[]
    for i,(r,f) in enumerate(zip(records,rows)):
        a,b,c,d=r['native_bbox'];body=r['body_proxy'];mask=np.asarray(__import__('PIL').Image.open(OUT/r['mask_path']))>0;connected=cv2.connectedComponents(mask.astype(np.uint8),8)[0]-1
        eligible=mask.sum()>=35 and d-b>=.32*body and c-a>=4 and d-b<=3.8*body and c-a<=12*body and connected==1
        cid=str(base['classes'][i]);stable=all(q['accepted'][i] and str(q['classes'][i])==cid for q in alt+[nu]);ok=eligible and r['photo_raster_stable'] and base['accepted'][i] and stable and cid!='ST09' and f['source_resolved']
        label=old.get(r['parent_id'],'UNK') if r['corpus']=='reference' else cid if ok else 'UNK'
        out.append(dict(parent_id=r['parent_id'],class_reporting_only=label,fresh_frozen_inference=bool(ok) if r['corpus']=='fresh' else None))
    return out

def stats(rr):
    writing=[r for r in rr if r['membership']=='confirmed_writing'];res=[r for r in writing if r['source_resolved']];usable=sum(r['usable_partial_profile'] for r in writing)
    return dict(proposals=len(rr),confirmed=len(writing),resolved=len(res),usable=usable,overall_rate=usable/len(writing) if writing else None,resolved_rate=usable/len(res) if res else None,unknown_source=sum(not r['source_resolved'] for r in writing))

def coverage(rows,labels,sources,spec):
    fresh=[r for r in rows if r['corpus']=='fresh'];lab={r['parent_id']:r['class_reporting_only'] for r in labels};summary={c:stats([r for r in rows if r['corpus']==c]) for c in ['fresh','reference']};bycap={c:stats([r for r in fresh if r['caption']==c]) for c in CAPTIONS};unknown=stats([r for r in fresh if lab[r['parent_id']]=='UNK']);summary['fresh_V3_UNKNOWN']=unknown
    feature_stats={}
    for k in spec['features']:
        feature_stats[k]={c:dict(raster_status_counts=dict(Counter(r['features'][k]['raster_status'] for r in rows if r['corpus']==c)),source_qualified_counts=dict(Counter(r['features'][k]['source_qualified_status'] for r in rows if r['corpus']==c))) for c in ['reference','fresh']}
    source_by_id={r['parent_id']:r for r in sources};agreement={}
    for corpus in ['reference','fresh']:
        ss=[r for r in rows if r['corpus']==corpus and r['source_resolved']];cavity=[r for r in ss if source_by_id[r['parent_id']]['source_cavity_count'] is not None];aspect=[r for r in ss if source_by_id[r['parent_id']]['source_aspect']!='unknown'];asp_pred=lambda r:'taller' if np.exp(r['features']['log_aspect']['primary'])<.8 else 'wide' if np.exp(r['features']['log_aspect']['primary'])>1.25 else 'near_square'
        agreement[corpus]=dict(source_resolved_n=len(ss),cavity_adjudicable_n=len(cavity),cavity_primary_agreement=sum(r['source_cavity_compatible'] for r in cavity)/len(cavity) if cavity else None,cavity_stable_and_source_agree=sum(r['source_cavity_compatible'] and r['features']['significant_cavity_count']['raster_status']=='stable' for r in cavity),source_cavity_unknown_n=sum(source_by_id[r['parent_id']]['source_cavity_count'] is None for r in ss),aspect_adjudicable_n=len(aspect),aspect_primary_agreement=sum(source_by_id[r['parent_id']]['source_aspect']==asp_pred(r) for r in aspect)/len(aspect) if aspect else None)
    gates=spec['validation_gates'];sf=summary['fresh'];aa=agreement['fresh'];passed=dict(sample_n=sf['confirmed']>=gates['fresh_confirmed_n_min'],caption_n=len(bycap)>=6,overall=sf['overall_rate']>=gates['overall_usable_confirmed_min'],resolved=sf['resolved_rate']>=gates['resolved_usable_min'],every_caption=all(r['overall_rate']>=gates['each_caption_overall_min'] for r in bycap.values()),unknown=unknown['overall_rate']>=gates['V3_unknown_usable_confirmed_min'],cavity_n=aa['cavity_adjudicable_n']>=gates['source_cavity_adjudicable_n_min'],cavity_agreement=aa['cavity_primary_agreement']>=gates['source_cavity_numeric_agreement_min'],aspect=aa['aspect_primary_agreement']>=gates['source_aspect_agreement_min'])
    rng=np.random.default_rng(spec['seed']);rates=[]
    for _ in range(2000):rates.append(stats([r for c in rng.choice(CAPTIONS,6,replace=True) for r in fresh if r['caption']==c])['overall_rate'])
    return dict(summary=summary,by_fresh_caption=bycap,features=feature_stats,source_agreement=agreement,gates=passed,coverage_source_gate_pass=all(passed.values()),fresh_overall_caption_bootstrap95=np.percentile(rates,[2.5,97.5]).tolist(),source_agreement_scope='Same-adjudicator, source-count qualification. Coarse aspect bbox-aided; not independent physical ground truth. Span evidence retained alongside run raster measures without equating a run cutoff with a bench. All unresolved parent extent cases block usability.')

def coherence(rows,lab,dm,spec):
    labels=np.array([r['class_reporting_only'] for r in lab]);caps=np.array([r['caption'] for r in rows]);good=np.array([r['usable_partial_profile'] for r in rows]);eligible={c for c in set(labels) if c!='UNK' and sum((labels==c)&good)>=5 and len(set(caps[(labels==c)&good]))>=3};idx=np.where(good&np.isin(labels,list(eligible)))[0];rng=np.random.default_rng(spec['seed']);out={}
    def within(c,ll):
        q=(ll==c)&good;mask=q[:,None]&q[None,:]&(caps[:,None]!=caps[None,:])&np.isfinite(dm)&np.triu(np.ones(dm.shape,bool),1);return float(np.mean(dm[mask])) if mask.any() else None
    for c in sorted(eligible):
        obs=within(c,labels);null=[]
        for _ in range(999):
            ll=labels.copy()
            for cap in set(caps):q=np.where((caps==cap)&good&(labels!='UNK'))[0];ll[q]=rng.permutation(ll[q])
            z=within(c,ll)
            if z is not None:null.append(z)
        out[c]=dict(parents=int(sum((labels==c)&good)),captions=len(set(caps[(labels==c)&good])),crosscaption_mean_distance=obs,null999_median=float(np.median(null)) if null else None,p_lower=(1+sum(v<=obs for v in null))/(1+len(null)) if null and obs is not None else None)
    nearest=[]
    for i in idx:
        candidates=idx[(caps[idx]!=caps[i])&np.isfinite(dm[i,idx])]
        if len(candidates):j=candidates[np.argmin(dm[i,candidates])];nearest.append(dict(parent_id=rows[i]['parent_id'],correct=bool(labels[i]==labels[j]),class_id=str(labels[i])))
    return dict(classes=out,leave_caption_nearest_n=len(nearest),leave_caption_accuracy=sum(r['correct'] for r in nearest)/len(nearest) if nearest else None,parent_retrieval=nearest,class_labels_used_only_after_metric_seal=True,null='999 within-caption known-label permutations preserving frequencies/missing profiles; cross-caption distances. Unadjusted exploratory p-values; class/sample/repeated-parent dependence limits inference.')

def unknown_neighborhoods(rows,lab,dist,spec):
    labels=np.array([r['class_reporting_only'] for r in lab]);caps=np.array([r['caption'] for r in rows]);good=np.array([r['usable_partial_profile'] for r in rows]);idx=np.where(good&(labels=='UNK'))[0];rng=np.random.default_rng(spec['seed'])
    def counts(dd):
        out=[]
        for i in idx:
            neighbors=idx[(dd[i,idx]<=.25)&(caps[idx]!=caps[i])];support=set(caps[neighbors]);out.append(dict(parent_id=rows[i]['parent_id'],caption=rows[i]['caption'],corpus=rows[i]['corpus'],cross_caption_neighbors=len(neighbors),caption_support_including_self=1+len(support),reference_transport=bool(any(rows[j]['corpus']=='reference' for j in neighbors))))
        return out
    obs=counts(dist);null=[];families=['geometry','distribution','run','cavity'];original={fam:[{k:r['features'][k] for k in spec['core_features'] if spec['features'][k]['family']==fam} for r in rows] for fam in families}
    # Conditional unknown corpus null: whole-family vectors independently permuted inside each caption.
    import copy
    perm=copy.deepcopy(rows)
    for rep in range(999):
        for fam in families:
            for cap in set(caps[idx]):
                q=idx[caps[idx]==cap];p=rng.permutation(q)
                for i,j in zip(q,p):perm[i]['features'].update(original[fam][j])
        nd,_=distances(perm,spec);rr=counts(nd);null.append(sum(r['caption_support_including_self']>=3 for r in rr))
    observed=sum(r['caption_support_including_self']>=3 for r in obs)
    return dict(usable_unknown_n=len(idx),source_confirmed_unknown_n=sum(labels[i]=='UNK' and rows[i]['membership']=='confirmed_writing' for i in range(len(rows))),crosscaption_neighbor_n=sum(r['cross_caption_neighbors']>0 for r in obs),three_caption_support_n=observed,fresh_reference_transport_n=sum(r['corpus']=='fresh' and r['reference_transport'] for r in obs),parents=obs,null999_threecaption_mean=float(np.mean(null)),null999_threecaption95=np.percentile(null,[2.5,97.5]).tolist(),p_upper=(1+sum(v>=observed for v in null))/1000,interpretation='Continuous neighborhoods only; similarity is not transitive and these are not new classes, factors, tokens or ordered sequences. Family-vector permutations preserve caption/marginal missingness but are an exploratory composite-morphology null, not a language test.')

def similarity(spec):
    key=read_json(D/'similarity_hidden_key.json')['pairs'];ratings={r['pair_id']:r['rating'] for r in read_json(D/'similarity_decisions.json')['pairs']};rr=[dict(k,rating=ratings[k['pair_id']]) for k in key];metrics={};primary=[r for r in rr if r['rating'] in [0,2] and r['profile_distance'] is not None];rng=np.random.default_rng(spec['seed']);deltas={k:[] for k in ['aspect','contour','combined']}
    def auc(pp,k):return float(roc_auc_score([r['rating']==2 for r in pp],[-r[k+'_distance'] for r in pp])) if len({r['rating'] for r in pp})==2 else None
    for k in ['profile','aspect','contour','combined']:
        ordinal=[r for r in rr if r['rating'] in [0,1,2] and r['profile_distance'] is not None];s=spearmanr([r['rating'] for r in ordinal],[-r[k+'_distance'] for r in ordinal]);metrics[k]=dict(auc=auc(primary,k),spearman=float(s.statistic) if np.isfinite(s.statistic) else None)
    for _ in range(2000):
        pp=[r for c in rng.choice(CAPTIONS,6,replace=True) for r in primary if r['caption']==c];aa=auc(pp,'profile')
        if aa is not None:
            for k in deltas:deltas[k].append(aa-auc(pp,k))
    gaps={k:dict(delta=metrics['profile']['auc']-metrics[k]['auc'],paired_caption_bootstrap95=np.percentile(v,[2.5,97.5]).tolist()) for k,v in deltas.items()};gate=dict(auc=metrics['profile']['auc']>=.75,pairs=len(primary)>=120,positive=sum(r['rating']==2 for r in primary)>=30,negative=sum(r['rating']==0 for r in primary)>=30,six_captions=len({r['caption'] for r in primary})==6,all_baselines=all(v['delta']>=.05 and v['paired_caption_bootstrap95'][0]>0 for v in gaps.values()))
    repeat=read_json(D/'repeat_decisions.json')['pairs'];rkey=read_json(D/'repeat_hidden_key.json')['pairs'];lookup={r['repeat_id']:r['original_pair_id'] for r in rkey};exact=sum(r['rating']==ratings[lookup[r['repeat_id']]] for r in repeat)
    return dict(all_ratings=dict(Counter(str(r['rating']) for r in rr)),all_pairs=len(rr),primary_scored_pairs=len(primary),excluded_partial_or_unresolved=sum(r['rating'] in [1,'U'] for r in rr),profile_unavailable_n=sum(r['profile_distance'] is None for r in rr),primary_by_caption=dict(Counter(r['caption'] for r in primary)),metrics=metrics,paired_differences=gaps,gates=gate,similarity_superiority_gate_pass=all(gate.values()),repeat=dict(n=len(repeat),exact=exact,exact_rate=exact/len(repeat),same_AI_adjudicator=True,independent_interrater=False,confusion=dict(Counter(str(ratings[lookup[r['repeat_id']]])+'->'+str(r['rating']) for r in repeat))),limitations='Selected pooled nearest/reference hard pairs, not random-pair population. Reference and anchor reuse plus six captions limit generalization. Pair judgment same AI and source crops previously viewed. Unknown/partial excluded explicitly; no training on these ratings.')

def main():
    guard();verify_dependencies();verify_seal(D/'METRIC_SEAL.json');verify_seal(D/'RATING_SEAL.json');verify_seal(D/'REPEAT_SEAL.json');spec=read_json(D/'PLAN.json');rec=read_json(D/'source_location_aids.json')['parents'];rows=read_json(D/'feature_profiles.json')['parents'];sources=read_json(D/'source_decisions.json')['parents'];lab=labels(rec,rows);save(D/'V3_reporting_labels.json',lab);dm=np.load(D/'distances.npz')['profile'];save(T/'coverage_and_source_agreement.json',coverage(rows,lab,sources,spec));save(T/'V3_feature_coherence.json',coherence(rows,lab,dm,spec));print('Coverage, source agreement, V3 diagnostics computed; unknown null next',flush=True);save(T/'unknown_continuous_recurrence.json',unknown_neighborhoods(rows,lab,dm,spec));save(T/'heldout_source_similarity.json',similarity(spec));print('All registered Trial2 tests finished',flush=True)
if __name__=='__main__':main()
