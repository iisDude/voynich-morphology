"""Explicit ledger analogues: depth, section ordering, preference and repeats."""
from common import OUT,SEED,read_json,write_json,write_csv,sha256
from run_structural_tests_v2 import load,input_path
from structural_assays import prepare,pairs,section_distances,edge_graph,correlation
from positional_dependence_and_boundaries_v0 import theme_metrics
from context_assays_v0 import context_prediction
from collections import defaultdict,Counter
from itertools import combinations
import argparse
import numpy as np
import networkx as nx
from statsmodels.regression.linear_model import OLS

def depth_assay(rows,position):
    rr,forms,ids,pos,freq,means=prepare(rows,position);pp=pairs(forms,freq,8,5)
    if not pp:return {'status':'not_estimable: no qualifying minimal pairs','pairs':0,'position':position}
    aa,bb,edit,depth,length=np.array(pp).T
    x=np.c_[np.ones(len(pp)),depth==1,depth==0,length,np.log(np.sqrt(freq[aa]*freq[bb]))]
    graph=nx.Graph();graph.add_edges_from(zip(aa,bb));families={v:i for i,c in enumerate(nx.connected_components(graph)) for v in c};clusters=np.array([families[a] for a in aa])
    responses={'position':abs(means[aa]-means[bb])};theme=section_distances(rr,ids,len(forms))
    if theme is not None:
        prob,denom=theme;keep=(denom[aa]>0)&(denom[bb]>0)
        responses.update({k:np.where(keep,v,np.nan) for k,v in theme_metrics(prob[aa],prob[bb]).items()})
    documents=sorted(set(r['folio_component'] for r in rr));lookup={d:i for i,d in enumerate(documents)}
    selected=sorted(set(aa)|set(bb));fi={f:i for i,f in enumerate(selected)};aix=np.array([fi[a] for a in aa]);bix=np.array([fi[b] for b in bb])
    counts=np.zeros((len(documents),len(selected)));sums=np.zeros_like(counts)
    sections=sorted(set(r.get('section') for r in rr if r.get('section') is not None));si={s:i for i,s in enumerate(sections)};sc=np.zeros((len(documents),len(selected),len(sections)))
    for r,i,p in zip(rr,ids,pos):
        if i not in fi:continue
        d,j=lookup[r['folio_component']],fi[i];counts[d,j]+=1;sums[d,j]+=p
        if r.get('section') in si:sc[d,j,si[r['section']]]+=1
    rng=np.random.default_rng(SEED);boots=defaultdict(list)
    for _ in range(199):
        w=np.bincount(rng.integers(len(documents),size=len(documents)),minlength=len(documents));f=w@counts;mu=(w@sums)/np.maximum(f,1)
        keep=(f[aix]>0)&(f[bix]>0);xb=x.copy();xb[:,4]=np.log(np.maximum(np.sqrt(f[aix]*f[bix]),1))
        ys={'position':np.where(keep,abs(mu[aix]-mu[bix]),np.nan)}
        if len(sections)>=2:
            cc=np.tensordot(w,sc,axes=1);n=cc.sum(axis=1);prob=cc/np.maximum(n[:,None],1);valid=(n[aix]>0)&(n[bix]>0)
            ys.update({k:np.where(valid,v,np.nan) for k,v in theme_metrics(prob[aix],prob[bix]).items()})
        for metric,y in ys.items():
            mask=np.isfinite(y)
            if mask.sum()>=15 and np.linalg.matrix_rank(xb[mask])==5:boots[metric].append(np.linalg.lstsq(xb[mask],y[mask],rcond=None)[0][1:3].tolist())
    results=[]
    for metric,y in responses.items():
        finite=np.isfinite(y);result={'metric':metric,'n':int(finite.sum()),'counts':{label:int(np.sum(finite&(depth==d if d>=0 else depth>=2))) for label,d in [('outer',0),('near',1),('interior',-1)]},
            'raw_means':{label:float(np.nanmean(y[depth==d if d>=0 else depth>=2])) if np.any(finite&(depth==d if d>=0 else depth>=2)) else None for label,d in [('outer',0),('near',1),('interior',-1)]}}
        if finite.sum()<15 or np.linalg.matrix_rank(x[finite])<5:result.update(status='not_estimable: insufficient observations or design rank')
        else:
            fit=OLS(y[finite],x[finite]).fit(cov_type='HC3');result.update(status='estimated',near_minus_interior=float(fit.params[1]),outer_minus_interior=float(fit.params[2]),hc3_p_near=float(fit.pvalues[1]),hc3_p_outer=float(fit.pvalues[2]))
            if len(set(clusters[finite]))>=10:
                cf=OLS(y[finite],x[finite]).fit(cov_type='cluster',cov_kwds={'groups':clusters[finite]},use_t=True);result.update(family_cluster_p_near=float(cf.pvalues[1]),family_cluster_p_outer=float(cf.pvalues[2]))
            values=np.array(boots[metric]);result['joint_document_bootstrap']=dict(estimable=len(values),near_interval=np.quantile(values[:,0],[.025,.975]).tolist() if len(values) else None,outer_interval=np.quantile(values[:,1],[.025,.975]).tolist() if len(values) else None)
        results.append(result)
    return dict(status='completed',position=position,pairs=len(pp),connected_families=len(set(clusters)),results=results,
        estimand='Frequency>=8, length>=5. Two indicators near(depth1), outer(depth0); interior(depth>=2) baseline, length and log geometric mean frequency controls. Fixed selected vocabulary; joint caption/document occurrence resampling, missing members omit pairs.')

def section_order(rows,position):
    strata=[('all_hands',rows)]+[('hand_'+h,[r for r in rows if r.get('hand')==h]) for h in sorted(set(r.get('hand') for r in rows if r.get('hand')))]
    results=[]
    for stratum,rr in strata:
        sections=sorted(set(r.get('section') for r in rr if r.get('section')))
        for side in ('left','right'):
            graphs={s:edge_graph([r for r in rr if r.get('section')==s],position,side,5,2) for s in sections}
            for a,b in combinations(sections,2):
                ga,gb=graphs[a],graphs[b];common=sorted(set(ga)&set(gb));cr=correlation([ga[k]['delta'] for k in common],[gb[k]['delta'] for k in common])
                result=dict(stratum=stratum,position=position,side=side,section_a=a,section_b=b,relations_a=len(ga),relations_b=len(gb),agreement=cr,status='estimated exploratory pooled-section comparison' if cr['pearson'] is not None else 'not_estimable: fewer than four variable shared relations')
                if cr['pearson'] is not None:
                    rng=np.random.default_rng(SEED);null=[];subset=[r for r in rr if r.get('section') in (a,b) and r.get(position) is not None];lines=defaultdict(list)
                    for i,r in enumerate(subset):lines[r['line_id']].append(i)
                    for _ in range(99):
                        shuffled=[dict(r) for r in subset]
                        for indexes in lines.values():
                            values=rng.permutation([subset[i][position] for i in indexes])
                            for i,p in zip(indexes,values):shuffled[i][position]=float(p)
                        ng={s:edge_graph([r for r in shuffled if r.get('section')==s],position,side,5,2) for s in (a,b)}
                        v=correlation([ng[a][k]['delta'] for k in common],[ng[b][k]['delta'] for k in common])['pearson']
                        if v is not None:null.append(v)
                    result['within_line_null']=dict(iterations=len(null),p=(1+sum(abs(v)>=abs(cr['pearson']) for v in null))/(1+len(null)),mean=float(np.mean(null)) if null else None)
                result['limitation']='Pooled sections with shared graph units/cores; relations are dependent, no edge-independent confidence interval or held-out generalization claim.';results.append(result)
    return results

def ordinary_preference(rows,position,root):
    output=[]
    for side in ('left','right'):
        edges=edge_graph(rows,position,side,5,2);graph=nx.Graph();graph.add_edges_from(edges);potentials={};preferences={}
        for component in nx.connected_components(graph):
            nodes=sorted(component);index={u:i for i,u in enumerate(nodes)};xx=[];yy=[]
            for (a,b),edge in edges.items():
                if a not in component:continue
                equation=np.zeros(len(nodes));equation[index[b]]=1;equation[index[a]]=-1;xx.append(equation);yy.append(edge['delta'])
            p=np.linalg.lstsq(xx,yy,rcond=None)[0]
            q=np.array([np.mean([r[position] for r in rows if r.get(position) is not None and (r['units'][0] if side=='left' else r['units'][-1])==u]) for u in nodes]);q-=q.mean()
            potentials.update(zip(nodes,p));preferences.update(zip(nodes,q))
        shared=sorted(potentials);pooled=correlation([potentials[u] for u in shared],[preferences[u] for u in shared]);predictions=[]
        for frequency in (5,8):
            path=root/f'prediction_{position}_{side}_freq{frequency}.json'
            if not path.exists():continue
            records=[r for r in read_json(path) if r.get('ordinary_unit_preference_prediction') is not None]
            alt=np.array([r['alternate_training_prediction'] for r in records]);ordinary=np.array([r['ordinary_unit_preference_prediction'] for r in records]);observed=np.array([r['heldout_direct_delta'] for r in records])
            predictions.append(dict(frequency=frequency,n=len(records),alternate_rmse=float(np.sqrt(np.mean((alt-observed)**2))) if len(records) else None,ordinary_rmse=float(np.sqrt(np.mean((ordinary-observed)**2))) if len(records) else None,
                ordinary_prediction_correlation=correlation(ordinary,observed),mean_alternate_minus_ordinary_squared_error=float(np.mean((alt-observed)**2-(ordinary-observed)**2)) if len(records) else None,
                limitations='Identical held-out edges, direct training edge and all its training matched cores removed. Shared edges/cores make edge-naive uncertainty invalid; small-n comparisons descriptive.'))
        output.append(dict(side=side,position=position,pooled_component_centered_potential_vs_preference=pooled,heldout_comparison=predictions))
    return output

def repetitions(rows,name):
    descriptive=[]
    for key,rr in __import__('context_assays_v0').docs(rows).items():
        count2=sum(any(r['units'][i]==r['units'][i+1] for i in range(len(r['units'])-1)) for r in rr)
        count3=sum(any(r['units'][i]==r['units'][i+1]==r['units'][i+2] for i in range(len(r['units'])-2)) for r in rr)
        literal2=sum(any(r['units'][i:i+2]==['e','e'] for i in range(len(r['units'])-1)) for r in rr) if name in ('ZL_EVA','RF') else None
        literal3=sum(any(r['units'][i:i+3]==['e','e','e'] for i in range(len(r['units'])-2)) for r in rr) if name in ('ZL_EVA','RF') else None
        descriptive.append(dict(document=key,split=rr[0]['split'],sections=sorted(set(r.get('section') for r in rr if r.get('section'))),hands=sorted(set(r.get('hand') for r in rr if r.get('hand'))),curriers=sorted(set(r.get('currier') for r in rr if r.get('currier'))),groups=len(rr),any_double=count2,any_triple=count3,literal_ee=literal2,literal_eee=literal3))
    return descriptive

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--dataset',required=True);args=ap.parse_args();name=args.dataset;rows=load(name);root=OUT/'tests/depth_order_repetition'/name;root.mkdir(parents=True,exist_ok=True)
    subsets={'all':rows}
    if name not in ('Finnish','Turkish','Latin'):subsets.update({s:[r for r in rows if r.get('currier')==s] for s in ('A','B')})
    positions=['normalized_group_rank']+(['normalized_pixel_center'] if name.startswith('visual_') else [])
    depth=[]
    for subset,rr in subsets.items():
        for position in positions:depth.append(dict(dataset=name,subset=subset,**depth_assay(rr,position)));print(name,subset,position,'depth complete',flush=True)
    primary=rows if name in ('Finnish','Turkish','Latin') else subsets['B'];ordering=[];ordinary=[]
    for position in positions:
        ordering.extend(section_order(primary,position));ordinary.extend(ordinary_preference(primary,position,OUT/'tests/structural'/name));print(name,position,'order complete',flush=True)
    repeats=repetitions(rows,name);write_json(root/'depth_results.json',depth);write_json(root/'section_order_results.json',ordering);write_json(root/'ordinary_preference_results.json',ordinary);write_json(root/'repetition_documents.json',repeats)
    flat=[]
    for d in depth:
        for r in d.get('results',[]):flat.append(dict(subset=d['subset'],position=d['position'],metric=r['metric'],status=r['status'],pairs=d['pairs'],near_beta=r.get('near_minus_interior'),outer_beta=r.get('outer_minus_interior'),near_ci=r.get('joint_document_bootstrap',{}).get('near_interval'),outer_ci=r.get('joint_document_bootstrap',{}).get('outer_interval')))
        if not d.get('results'):flat.append(dict(subset=d['subset'],position=d['position'],metric='all',status=d['status'],pairs=d['pairs'],near_beta=None,outer_beta=None,near_ci=None,outer_ci=None))
    write_csv(root/'results.csv',flat);write_json(root/'config.json',dict(seed=SEED,depth_frequency=8,depth_min_length=5,depth_bootstraps=199,section_order_frequency=5,section_order_cores=2,section_null=99,comparison_scope='Exploratory specified ledger analogues; conventional symbols and source prototype categories not equivalent alphabets.',failure='Frozen v4 writing rows/groups have demonstrated defects. No inferred writing-unit claim follows.'))
    write_json(root/'input_manifest.json',dict(path=input_path(name).relative_to(OUT).as_posix(),sha256=sha256(input_path(name)),source_sha256=sha256(OUT/'src/finish_depth_order_repetition_v1.py')))
    (root/'run.py').write_text(f'from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[3]/"src"))\nsys.argv=[sys.argv[0],"--dataset","{name}"]\nfrom finish_depth_order_repetition_v1 import main\nmain()\n',encoding='utf-8')
    (root/'README.md').write_text('# Depth, ordering and repetitions\n\nRun `run.py`. Raw and adjusted depth contrasts, shared-section relations, ordinary positional preferences and document-level repetition counts are retained. Unit repeats are not measured minim strokes; literal EVA ee/eee is stored only for EVA comparison datasets.\n',encoding='utf-8')
    (root/'summary.md').write_text('# Ledger analogues 5, 9, 25, 26\n\nDepth indicators separate outer from near; intervals jointly resample caption/document occurrences. Section ordering uses shared relations with within-line nulls; pooled relation correlations are exploratory and dependent. Held-out alternate and ordinary preference predictions are compared on identical edges, without direct training cores. Source repeats, codepoint repeats and physical minim repetitions remain distinct observations. Non-estimable outcomes retain their denominators.\n',encoding='utf-8')

if __name__=='__main__':main()
