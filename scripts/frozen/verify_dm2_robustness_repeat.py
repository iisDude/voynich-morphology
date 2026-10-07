from dm2_robustness_common import *
from evaluate_dm2_robustness import evaluate,agreement,interval
from collections import Counter
import numpy as np
def verify():
    rep=read_json(T/'larger_repeatability.json');joined=rep['pairs'];a=np.array([r['original_rating'] for r in joined],dtype=object);b=np.array([r['repeat_rating'] for r in joined],dtype=object);base=read_json(B/'source_similarity_decisions.json')['pairs'];frequency=Counter(r['rating'] for r in base);sample=Counter(a.tolist());f=np.array([frequency[int(z)]/sample[int(z)] for z in a]);assert agreement(a,b,f)==rep['original_category_reweighted_agreement'];npz=np.load(D/'caption_bootstrap_draws.npz');counts=npz['counts'];caps=npz['captions'].tolist();w=np.stack([counts[:,caps.index(r['caption_left'])]*counts[:,caps.index(r['caption_right'])] for r in joined],axis=1);known=np.isin(b,[0,1,2]);ordinal=1-abs(a[known].astype(int)-b[known].astype(int))/2
    def ratio(num,den):
        out=np.full(len(den),np.nan);np.divide(num,den,out=out,where=den>0);return out
    assert interval(ratio((w*(a==b)).sum(1),w.sum(1)))==rep['exact_caption_bootstrap95'];assert interval(ratio((w[:,known]*ordinal).sum(1),w[:,known].sum(1)))==rep['linear_ordinal_caption_bootstrap95'];wf=w*f;assert interval(ratio((wf*(a==b)).sum(1),wf.sum(1)))==rep['reweighted_exact_caption_bootstrap95']
    for cat in [0,1,2]:
        mask=a==cat;values=ratio((w[:,mask]*(b[mask]==cat)).sum(1),w[:,mask].sum(1));r=rep['category_stability'][str(cat)];assert interval(values)==r['conditional_caption_bootstrap95'];assert int(np.isfinite(values).sum())==r['valid_bootstrap_n'];assert int((b[mask]==cat).sum())==r['retained_n']
    for stored in read_json(T/'repeat_prediction_sensitivity.json')['results']:
        label=stored['label'];rows=[];y=[];ff=[]
        for i,r in enumerate(joined):
            z=r['original_rating'] if label=='original' else r['repeat_rating']
            if z not in [0,2] or label=='stable_original_repeat' and r['original_rating']!=r['repeat_rating']:continue
            rows.append(dict(r,pair_id=r['original_pair_id']));y.append(int(z==2));ff.append(f[i])
        assert evaluate(rows,y,counts,caps)==stored['unweighted'];assert evaluate(rows,y,counts,caps,ff)==stored['original_category_frequency_reweighted']
    import re
    dashboard=OUT/'reports/28_direct_morphology_trial2_robustness_dashboard.html';text=dashboard.read_text(encoding='utf-8');links=re.findall(r"src='([^']+)'",text)
    for link in links:assert (dashboard.parent/link).resolve().is_file()
    assert text.count("<tr data-source=")==108;assert text.count('<td>J')==125
    return dict(checked_at_utc=now(),repeat_weighted_and_category_uncertainty_exact=True,three_repeat_binary_analyses_unweighted_and_reweighted_exact=True,local_dashboard_image_links_resolve=len(links),all108_condition_rows_and125_repeat_rows_present=True,all_current_repeat_labels_resolved=bool(known.all()),failures=[])
if __name__=='__main__':
    result=verify();write_json(P/'REPEAT_REPLAY.json' if (D/'FREEZE_MANIFEST.json').exists() else T/'REPEAT_REPLAY.json',result);print('Repeat and dashboard exact replay complete',flush=True)
