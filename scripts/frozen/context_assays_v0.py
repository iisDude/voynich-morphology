"""Post-freeze context, representation, wrapper and compression comparisons.

All visual inputs remain partial failed raster candidates. These comparisons
cannot certify the row/group layer or recover script signs. Inherited metadata
is attached only after the visual freeze. Same-author controls use supplied UD.
"""
from common import OUT,read_json,write_json,write_csv,sha256,SEED
from run_structural_tests_v2 import load,input_path
from collections import Counter,defaultdict
from itertools import combinations
import argparse,zlib
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from sklearn.metrics import roc_auc_score,adjusted_rand_score

def docs(rows):
    dd=defaultdict(list)
    for r in rows:dd[r['folio_component']].append(r)
    return dd

def features(unit_rows,representation='ngrams'):
    c=Counter()
    for r in unit_rows:
        u=r['units']
        if representation=='ngrams':
            c.update('U|'+v for v in u);c.update('B|'+repr(tuple(u[i:i+2])) for i in range(len(u)-1))
            c['length']+=len(u)
        elif representation=='full':c['F|'+repr(tuple(u))]+=1
        elif representation=='edge':c['L|'+u[0]]+=1;c['R|'+u[-1]]+=1
        elif representation=='core':c['C|'+repr(tuple(u[1:-1]))]+=1
        elif representation=='abstract':
            lookup={};pattern=[]
            for a in u:
                if a not in lookup:lookup[a]=len(lookup)
                pattern.append(lookup[a])
            c['A|'+repr(tuple(pattern))]+=1
    return {key:value/max(len(unit_rows),1) for key,value in c.items()}

def context_prediction(rows,field='section',minimum_train_docs=6,minimum_test_docs=3):
    bydoc=docs(rows);records=[]
    for d,rr in bydoc.items():
        labels={r.get(field) for r in rr};splits={r['split'] for r in rr}
        if len(labels)!=1 or None in labels or len(splits)!=1:continue
        if next(iter(splits))=='calibration':continue
        records.append(dict(document=d,label=next(iter(labels)),split=next(iter(splits)),rows=rr))
    result=[];rng=np.random.default_rng(SEED)
    for a,b in combinations(sorted(set(r['label'] for r in records)),2):
        rr=[r for r in records if r['label'] in (a,b)];tr=[r for r in rr if r['split'] in ('train','validation')];te=[r for r in rr if r['split']=='test']
        cnt=Counter((r['split']=='test',r['label']) for r in rr)
        base=dict(label_a=a,label_b=b,training_documents=len(tr),test_documents=len(te),field=field,train_counts=dict(Counter(r['label'] for r in tr)),test_counts=dict(Counter(r['label'] for r in te)))
        if min((cnt[False,a],cnt[False,b]))<minimum_train_docs or min((cnt[True,a],cnt[True,b]))<minimum_test_docs:
            result.append(dict(base,status='not_estimable: too few independent caption/document blocks'));continue
        vectorizer=DictVectorizer();x=vectorizer.fit_transform(features(r['rows']) for r in tr);xt=vectorizer.transform(features(r['rows']) for r in te)
        y=np.array([r['label']==b for r in tr]);yt=np.array([r['label']==b for r in te])
        fit=LogisticRegression(C=1,max_iter=1000,class_weight='balanced',random_state=SEED).fit(x,y);p=fit.predict_proba(xt)[:,1];auc=float(roc_auc_score(yt,p))
        null=[float(roc_auc_score(rng.permutation(yt),p)) for _ in range(199)];boot=[]
        for _ in range(1000):
            ix=rng.integers(len(te),size=len(te))
            if len(set(yt[ix]))==2:boot.append(float(roc_auc_score(yt[ix],p[ix])))
        result.append(dict(base,status='estimated',heldout_document_auc=auc,bootstrap_interval=np.quantile(boot,[.025,.975]).tolist(),
            test_document_label_null_p=(1+sum(v>=auc for v in null))/200,features=x.shape[1],
            predictions=[dict(document=r['document'],label=r['label'],p_label_b=float(q)) for r,q in zip(te,p)],
            limitation='One averaged unit-ngram vector per caption/document. Fixed trained predictions under held-out document-label null; shared bifolios/authors can reduce independence.'))
    return result

def same_hand(rows):
    result=[]
    for currier,hand in sorted(set((r.get('currier'),r.get('hand')) for r in rows if r.get('currier') and r.get('hand'))):
        rr=[r for r in rows if r.get('currier')==currier and r.get('hand')==hand and r.get('section')]
        for r in context_prediction(rr):r.update(currier=currier,hand=hand);result.append(r)
    return result

def clustering(rows):
    # Equal group count for each document; labels are used only to set class
    # count and compute ARI. Feature dictionaries are fitted on training docs.
    documents=[]
    for d,rr in docs(rows).items():
        lab={r.get('section') for r in rr};splits={r['split'] for r in rr}
        if len(rr)<40 or len(lab)!=1 or None in lab or len(splits)!=1 or 'calibration' in splits:continue
        documents.append((d,next(iter(lab)),next(iter(splits)),rr))
    labels=Counter(r[1] for r in documents);good={k for k,v in labels.items() if v>=6}
    documents=[r for r in documents if r[1] in good];tr=[r for r in documents if r[2] in ('train','validation')];te=[r for r in documents if r[2]=='test']
    if len(good)<2 or len(tr)<len(good)*2 or len(te)<6:return [dict(status='not_estimable: document/context coverage insufficient')]
    budget=min(200,min(len(r[3]) for r in documents));results=[]
    for rep in range(10):
        rng=np.random.default_rng(SEED+rep);sample={d:[rr[i] for i in rng.choice(len(rr),budget,replace=False)] for d,_,_,rr in documents}
        for representation in ('full','edge','core','abstract','ngrams'):
            dv=DictVectorizer();x=dv.fit_transform(features(sample[r[0]],representation) for r in tr);xt=dv.transform(features(sample[r[0]],representation) for r in te)
            x=normalize(x);xt=normalize(xt)
            model=KMeans(n_clusters=len(good),n_init=10,random_state=SEED+rep).fit(x);pred=model.predict(xt);y=[r[1] for r in te]
            observed=float(adjusted_rand_score(y,pred));null=[float(adjusted_rand_score(rng.permutation(y),pred)) for _ in range(99)]
            results.append(dict(replicate=rep,representation=representation,groups_per_document=budget,train_documents=len(tr),test_documents=len(te),classes=len(good),
                training_ari=float(adjusted_rand_score([r[1] for r in tr],model.labels_)),heldout_ari=observed,heldout_label_null_p=(1+sum(v>=observed for v in null))/100,
                limitation='Abstract pattern is within-group first-occurrence identity, not a paleographic shape transcription. Visual group boundaries are unvalidated.'))
    return results

def wrapper_transfer(rows,field='section'):
    rr=[r for r in rows if r.get(field) and len(r['units'])>=3 and r['split']!='calibration'];classes=sorted(set(r[field] for r in rr))
    if len(classes)<2:return dict(status='not_estimable: fewer than two contexts')
    index={v:i for i,v in enumerate(classes)};tr=[r for r in rr if r['split'] in ('train','validation')];te=[r for r in rr if r['split']=='test']
    core_counts=defaultdict(lambda:np.ones(len(classes)));wrap_counts=defaultdict(lambda:np.ones(len(classes)));prior=np.ones(len(classes));observations=Counter()
    for r in tr:
        u=r['units'];c=tuple(u[1:-1]);w=(u[0],u[-1]);j=index[r[field]];core_counts[c][j]+=1;wrap_counts[w][j]+=1;prior[j]+=1;observations[c]+=1
    prior/=prior.sum();scores=[];eligible=[]
    for r in te:
        u=r['units'];c=tuple(u[1:-1]);w=(u[0],u[-1]);j=index[r[field]]
        if observations[c]<5 or w not in wrap_counts:continue
        p=core_counts[c]/core_counts[c].sum();q=p*(wrap_counts[w]/wrap_counts[w].sum())/prior;q/=q.sum()
        scores.append((r['folio_component'],float(-np.log2(q[j])+np.log2(p[j]))));eligible.append((r,c,w,j))
    folios=sorted(set(f for f,e in scores));equal=[np.mean([e for f,e in scores if f==d]) for d in folios]
    if len(folios)<4:return dict(status='not_estimable: fewer than four eligible test document blocks',test_groups=len(scores))
    rng=np.random.default_rng(SEED);boot=rng.choice(equal,(1000,len(equal)),replace=True).mean(axis=1);bycore=defaultdict(list)
    for i,(r,c,w,j) in enumerate(eligible):bycore[c].append(i)
    null=[]
    for _ in range(99):
        wrappers=[w for r,c,w,j in eligible]
        for ix in bycore.values():
            order=rng.permutation(ix)
            for i,k in zip(ix,order):wrappers[i]=eligible[k][2]
        values=defaultdict(list)
        for (r,c,w,j),permuted in zip(eligible,wrappers):
            p=core_counts[c]/core_counts[c].sum();q=p*(wrap_counts[permuted]/wrap_counts[permuted].sum())/prior;q/=q.sum();values[r['folio_component']].append(float(-np.log2(q[j])+np.log2(p[j])))
        null.append(float(np.mean([np.mean(v) for v in values.values()])))
    return dict(status='estimated',context_field=field,contexts=classes,test_groups=len(scores),test_documents=len(folios),
        equal_document_wrapper_excess_bits_over_core=float(np.mean(equal)),bootstrap_interval=np.quantile(boot,[.025,.975]).tolist(),
        within_core_test_wrapper_null_p=(1+sum(v<=np.mean(equal) for v in null))/100,
        null_movable_groups=sum(len(ix) for ix in bycore.values() if len(set(eligible[i][2] for i in ix))>1),
        limitation='Held-out context prediction, conditioned on training core recurrence. Boundary wrappers need not be semantic operators; ordinary morphology is a direct control.')

def compression(rows,name):
    rr=[r for r in rows if r.get('currier')=='B'] if name.startswith(('ZL','RF','v101','visual')) else rows
    tr=[r for r in rr if r['split']=='train'];te=[r for r in rr if r['split']=='test']
    counts=Counter(u for r in tr for u in r['units']);vocab=sorted(counts)
    if len(vocab)<6 or len(vocab)>253:return dict(status='not_estimable: vocabulary outside byte coding or insufficient units')
    mapping={v:i for i,v in enumerate(vocab)}
    targets=list('aeioy') if name in ('ZL_EVA','RF') else list('aeiou') if name in ('Finnish','Turkish','Latin') else [v for v,n in counts.most_common(5)]
    if any(v not in counts for v in targets):return dict(status='not_estimable: declared deletion set absent')
    target=sum(counts[v] for v in targets);rng=np.random.default_rng(SEED);candidates={}
    for _ in range(15000):
        k=tuple(sorted(rng.choice(vocab,5,replace=False)));distance=abs(sum(counts[v] for v in k)-target)/max(target,1)
        candidates[k]=distance
    selected=sorted(candidates,key=candidates.get)[:99]
    def score(remove):
        values=defaultdict(list)
        for r in te:
            values[r['folio_component']].extend(mapping.get(u,254) for u in r['units'] if u not in remove);values[r['folio_component']].append(255)
        original=Counter()
        for r in te:original[r['folio_component']]+=len(r['units'])
        b=[8*len(zlib.compress(bytes(value),level=9))/max(original[f],1) for f,value in values.items()]
        return float(np.mean(b)) if b else None
    observed=score(set(targets));null=[score(set(k)) for k in selected];base=score(set())
    return dict(status='estimated' if observed is not None else 'not_estimable: no test blocks',declared_deletion_set=targets,
        set_meaning='EVA-designated vowels' if name in ('ZL_EVA','RF') else 'ordinary-language vowel codepoints' if name in ('Finnish','Turkish','Latin') else 'five most common training categories; neutral deletion analogy',
        baseline_bits_per_original_unit=base,deleted_bits_per_original_unit=observed,matched_set_count=len(null),
        matched_null_mean=float(np.mean(null)) if null else None,matched_null_interval=np.quantile(null,[.025,.975]).tolist() if null else None,
        frequency_matching_max_relative_difference=max(candidates[k] for k in selected),
        lower_tail_rank_p=(1+sum(v<=observed for v in null))/100 if observed is not None else None,
        codec='zlib level 9; training literal-unit byte dictionary, 254 unknown, 255 gap marker; separate held-out caption/document streams; equal-document average',
        limitation='Deletion necessarily changes information content. Byte compression cannot identify phonetic vowels or compare native image explanation. Frequency matching is approximate and recorded.')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--dataset',required=True);args=ap.parse_args();rows=load(args.dataset)
    root=OUT/'tests/context'/args.dataset;root.mkdir(parents=True,exist_ok=True)
    result=dict(dataset=args.dataset,same_hand_context=same_hand(rows),context_prediction=context_prediction(rows),representation_clustering=clustering(rows),
        wrappers=wrapper_transfer(rows),compression=compression(rows,args.dataset))
    if args.dataset=='Latin':
        c=[r for r in rows if r.get('same_author_work')];result['same_author_Cicero_wrappers']=wrapper_transfer(c,'same_author_work');result['same_author_Cicero_prediction']=context_prediction(c,'same_author_work')
    if args.dataset in ('ZL_EVA','RF'):
        literal=[]
        for currier,hand in [('B','2'),('B','3')]:
            rr=[r for r in rows if r.get('currier')==currier and r.get('hand')==hand];dd=docs(rr)
            for d,v in dd.items():
                f=[''.join(r['units']) for r in v];literal.append(dict(document=d,currier=currier,hand=hand,section=v[0].get('section'),groups=len(v),
                    containing_ee=sum('ee' in s for s in f),containing_eee=sum('eee' in s for s in f),total_e=sum(s.count('e') for s in f)))
        result['literal_e_repeat_document_counts']=literal
    write_json(root/'results.json',result)
    write_json(root/'config.json',dict(seed=SEED,context_feature='averaged per-document unit uni/bigrams and length; training vocabulary only',
        heldout='frozen caption/document split; calibration excluded',cluster_replicates=10,cluster_group_budget='same per document, minimum 40 and maximum 200',
        nulls=['199 held-out document-label permutations for AUC','99 held-out label permutations for ARI','99 within-core held-out wrapper permutations','99 approximately frequency-matched deletion sets'],
        bootstrap='1000 caption/document resamples',uncertainty='Shared physical bifolios or authors can reduce independence; no independent decipherment inference.',
        prior_art='No novelty claimed; standardized analogue of ledger tests 8–13. Exact historical implementation absent.'))
    write_json(root/'input_manifest.json',dict(path=input_path(args.dataset).relative_to(OUT).as_posix(),sha256=sha256(input_path(args.dataset)),
        source_sha256=sha256(OUT/'src/context_assays_v0.py'),visual_freeze_sha256=sha256(OUT/'data/observations/visual_dataset_v0/FREEZE_MANIFEST.json')))
    write_csv(root/'results.csv',[dict(test='same_hand_context',stratum=f"{r['currier']}:{r['hand']}:{r['label_a']}:{r['label_b']}",status=r['status'],effect=r.get('heldout_document_auc')) for r in result['same_hand_context']]+[
        dict(test='wrappers',stratum='all',status=result['wrappers']['status'],effect=result['wrappers'].get('equal_document_wrapper_excess_bits_over_core')),
        dict(test='compression',stratum='all',status=result['compression']['status'],effect=result['compression'].get('deleted_bits_per_original_unit'))])
    (root/'README.md').write_text('# Context comparisons\n\nRun `run.py`. Visual inputs are unvalidated raster-group candidates; section or hand predictability does not certify an alphabet. Context and ordinary morphology controls remain explicit.\n',encoding='utf-8')
    (root/'run.py').write_text(f'from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[3]/"src"))\nsys.argv=[sys.argv[0],"--dataset","{args.dataset}"]\nfrom context_assays_v0 import main\nmain()\n',encoding='utf-8')
    (root/'summary.md').write_text('# Context, wrappers, clustering and deletion\n\nResults contain held-out document effects, resampling uncertainty, explicit non-estimable cases and compression frequency-matching quality. Context labels are inherited after the visual freeze. Negative excess bits favor the wrapper model, but ordinary morphology is a competing explanation. Pixel positions do not enter these tests. No novelty or meanings are asserted.\n',encoding='utf-8')
    print(args.dataset,'context complete',flush=True)

if __name__=='__main__':main()
