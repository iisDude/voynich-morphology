"""Held-out categorical HMM transfer analogues of ledger test 14.

Units within each admitted group form a sequence; groups restart the HMM.
These are statistical sequence models, not inferred pen or semantic states.
"""
from common import OUT,read_json,write_json,write_csv,sha256,SEED
from run_structural_tests_v2 import load,input_path
from collections import defaultdict,Counter
import argparse,copy,warnings
import numpy as np
from hmmlearn.hmm import CategoricalHMM

def select(rows,name):
    if name=='Latin':return [dict(r,context=r['same_author_work']) for r in rows if r.get('same_author_work')]
    if name=='Finnish':return [dict(r,context=r['section']) for r in rows if r.get('section') in ('b','w')]
    if name=='Turkish':return []
    return [dict(r,context=r['section']) for r in rows if r.get('currier')=='B' and r.get('hand')=='2' and r.get('section') in ('H','B')]

def pack(rows,index):
    seq=[[index.get(u,0) for u in r['units']] for r in rows];lengths=[len(v) for v in seq]
    return np.array([i for v in seq for i in v],np.int32).reshape(-1,1),lengths

def clean(model):
    for field in ('startprob_','transmat_','emissionprob_'):
        value=np.maximum(getattr(model,field),1e-7);value/=value.sum() if value.ndim==1 else value.sum(axis=1,keepdims=True);setattr(model,field,value)

def score_docs(model,rows,index):
    dd=defaultdict(list)
    for r in rows:dd[r['folio_component']].append(r)
    result=[]
    for doc,rr in dd.items():
        x,lengths=pack(rr,index);result.append(dict(document=doc,groups=len(rr),units=len(x),bits_per_unit=float(-model.score(x,lengths)/np.log(2)/len(x))))
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--dataset',required=True);args=ap.parse_args();rows=select(load(args.dataset),args.dataset)
    root=OUT/'tests/hmm_transfer'/args.dataset;root.mkdir(parents=True,exist_ok=True);rng=np.random.default_rng(SEED)
    blocks=defaultdict(list)
    for r in rows:
        if r['split']!='calibration':blocks[(r['context'],r['folio_component'],r['split'])].append(r)
    selected=[]
    for key,rr in sorted(blocks.items()):selected.extend(rr[i] for i in rng.permutation(len(rr))[:200])
    classes=sorted(set(r['context'] for r in selected));counts=Counter((context,split) for context,doc,split in blocks)
    results=[];models=[]
    enough=len(classes)==2 and all(counts[c,'train']>=4 and counts[c,'test']>=2 for c in classes)
    if not enough:results=[dict(status='not_estimable: requires two contexts, at least four train and two test document blocks per context',block_counts=[dict(context=c,split=s,count=n) for (c,s),n in counts.items()])]
    else:
        tr=[r for r in selected if r['split']=='train'];val=[r for r in selected if r['split']=='validation'];te=[r for r in selected if r['split']=='test']
        vocabulary=sorted(set(u for r in tr for u in r['units']));index={u:i+1 for i,u in enumerate(vocabulary)};x,lengths=pack(tr,index)
        for states in (4,5):
            candidates=[]
            for restart in range(2):
                model=CategoricalHMM(n_components=states,n_features=len(index)+1,n_iter=30,tol=.001,random_state=SEED+restart,
                    startprob_prior=1.01,transmat_prior=1.01,emissionprob_prior=1.01,implementation='scaling')
                with warnings.catch_warnings(record=True) as warning_records:
                    warnings.simplefilter('always');model.fit(x,lengths);clean(model)
                validation=score_docs(model,val,index) if val else []
                value=np.mean([r['bits_per_unit'] for r in validation]) if validation else -model.score(x,lengths)/len(x)/np.log(2)
                candidates.append((value,model,restart,[str(w.message) for w in warning_records]))
            value,pool,restart,poolwarnings=min(candidates,key=lambda r:r[0])
            models.append(dict(states=states,chosen_restart=restart,validation_score=float(value),selection='equal validation document bits/unit; training score fallback only if no validation blocks',
                train_groups=len(tr),train_units=len(x),vocabulary=vocabulary,warnings=poolwarnings,training_iterations=pool.monitor_.iter,
                start_probability=pool.startprob_.tolist(),transition_matrix=pool.transmat_.tolist(),emission_matrix=pool.emissionprob_.tolist()))
            for context in classes:
                ctr=[r for r in tr if r['context']==context];cte=[r for r in te if r['context']==context];cx,cl=pack(ctr,index)
                baseline=score_docs(pool,cte,index);base={r['document']:r['bits_per_unit'] for r in baseline}
                for method,params in [('frozen_both',''),('fixed_transitions','e'),('fixed_emissions','t'),('adapt_both','te')]:
                    model=copy.deepcopy(pool);model.init_params='';model.params=params;model.n_iter=30
                    with warnings.catch_warnings(record=True) as warning_records:
                        warnings.simplefilter('always')
                        if params:model.fit(cx,cl);clean(model)
                    scores=score_docs(model,cte,index);delta=[r['bits_per_unit']-base[r['document']] for r in scores]
                    boot=rng.choice(delta,(1000,len(delta)),replace=True).mean(axis=1)
                    history=list(model.monitor_.history)
                    results.append(dict(status='estimated',states=states,context=context,adaptation=method,trained_parameters=params or 'none',start_distribution='fixed pooled in every adaptation',
                        train_groups=len(ctr),test_groups=sum(r['groups'] for r in scores),test_documents=len(scores),
                        heldout_equal_document_bits_per_unit=float(np.mean([r['bits_per_unit'] for r in scores])),excess_bits_over_frozen_both=float(np.mean(delta)),
                        bootstrap_interval=np.quantile(boot,[.025,.975]).tolist(),document_scores=scores,warnings=[str(w.message) for w in warning_records],
                        iterations=model.monitor_.iter if params else 0,last_likelihood_change=float(history[-1]-history[-2]) if params and len(history)>1 else None,
                        optimization_status='iteration limit or convergence are not evidence that hidden states are uniquely identified',
                        transition_matrix=model.transmat_.tolist(),emission_matrix=model.emissionprob_.tolist()))
            print(args.dataset,states,'HMM transfer complete',flush=True)
    write_json(root/'results.json',results);write_json(root/'models.json',models)
    write_csv(root/'results.csv',[dict(status=r['status'],states=r.get('states'),context=r.get('context'),adaptation=r.get('adaptation'),bits_per_unit=r.get('heldout_equal_document_bits_per_unit'),excess_bits=r.get('excess_bits_over_frozen_both')) for r in results])
    write_json(root/'config.json',dict(seed=SEED,states=[4,5],pooled_restarts=2,iterations=30,group_budget_per_document=200,
        sequence='literal/frozen units within one admitted group, restart at group boundary; not a line-state mechanism',
        context='same Currier B/hand 2 herbal versus biological; Latin same-author Cicero works; Finnish source partitions b/w',
        null='frozen-both transfer baseline plus fixed-emission/fixed-transition competing models; no random-label null run here',
        heldout='frozen document/caption split; calibration excluded',bootstrap=1000,
        failures=['Unvalidated visual group boundaries prevent manuscript-writing interpretation.','Hidden-state identities are exchangeable and can be non-identifiable.','Training-only priors and validation restarts; held-out scores cannot retune model count.',
            'Same hand reduces one confound but does not isolate subject matter from page layout, source quality or scribal phase.','Not an exact reproduction of undocumented historical HMM settings.'],dependency='hmmlearn 0.3.3, installed only under project .tools/python'))
    write_json(root/'input_manifest.json',dict(path=input_path(args.dataset).relative_to(OUT).as_posix(),sha256=sha256(input_path(args.dataset)),source_sha256=sha256(OUT/'src/hmm_transfer_v0.py'),visual_freeze_sha256=sha256(OUT/'data/observations/visual_dataset_v0/FREEZE_MANIFEST.json')))
    (root/'README.md').write_text('# HMM context transfer\n\nRun `run.py`. These are within-group sequence models, not decoded states. See held-out document scores and explicit coverage or optimization failures.\n',encoding='utf-8')
    (root/'run.py').write_text(f'from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[3]/"src"))\nsys.argv=[sys.argv[0],"--dataset","{args.dataset}"]\nfrom hmm_transfer_v0 import main\nmain()\n',encoding='utf-8')
    (root/'summary.md').write_text('# Hidden-state transfer\n\nThe frozen-both model is compared to section-specific emission adaptation, transition adaptation and joint adaptation under four and five states. Lower held-out bits/unit favor the model. Confidence intervals resample caption/document blocks; state labels have no semantic meaning. All iterations, warnings, matrices and non-estimable cases are preserved. No novelty or exact historical replication is claimed.\n',encoding='utf-8')

if __name__=='__main__':main()
