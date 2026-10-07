"""Boundary hypotheses and progressively broader dependence blocks."""
from common import OUT,read_json,write_json,write_csv,sha256,SEED
from run_structural_tests_v2 import load,input_path
from structural_assays import pair_assay,graph_assay,prepare,pairs,section_distances
from collections import Counter,defaultdict
import numpy as np
from scipy.sparse import coo_matrix
import networkx as nx

def theme_metrics(p,q):
    m=(p+q)/2;js=.5*((p*np.log2(np.maximum(p,1e-20)/np.maximum(m,1e-20))).sum(axis=1)+(q*np.log2(np.maximum(q,1e-20)/np.maximum(m,1e-20))).sum(axis=1))
    return {'TV':.5*abs(p-q).sum(axis=1),'JSD_bits':js,'sqrt_JS':np.sqrt(np.maximum(js,0)),'Hellinger':np.sqrt(.5*((np.sqrt(p)-np.sqrt(q))**2).sum(axis=1))}

def family_theme_bootstrap(rows,iterations=199):
    rr,forms,ids,pos,freq,means=prepare(rows,'normalized_group_rank');pp=pairs(forms,freq,8,5)
    if not pp:return dict(status='not_estimable: no qualifying minimal pairs')
    arr=np.array(pp);aa,bb,edit,depth,length=arr.T;x=np.c_[np.ones(len(pp)),(depth<2).astype(float),length,np.log(np.sqrt(freq[aa]*freq[bb]))]
    graph=nx.Graph();graph.add_edges_from(zip(aa,bb));lookup={v:i for i,c in enumerate(nx.connected_components(graph)) for v in c};cluster=np.array([lookup[a] for a in aa]);classes=sorted(set(cluster));rng=np.random.default_rng(SEED)
    responses={'position':abs(means[aa]-means[bb])};theme=section_distances(rr,ids,len(forms))
    if theme is not None:
        distributions,denom=theme;mask=(denom[aa]>0)&(denom[bb]>0);responses.update({k:np.where(mask,v,np.nan) for k,v in theme_metrics(distributions[aa],distributions[bb]).items()})
    family_results=[]
    for metric,y in responses.items():
        finite=np.isfinite(y);values=[];observed=np.linalg.lstsq(x[finite],y[finite],rcond=None)[0][1] if np.linalg.matrix_rank(x[finite])==4 else None
        for _ in range(iterations):
            selected=rng.choice(classes,len(classes),replace=True);indexes=np.concatenate([np.where(cluster==c)[0] for c in selected]);indexes=indexes[np.isfinite(y[indexes])]
            if len(indexes)>=12 and np.linalg.matrix_rank(x[indexes])==4:values.append(float(np.linalg.lstsq(x[indexes],y[indexes],rcond=None)[0][1]))
        family_results.append(dict(metric=metric,beta=float(observed) if observed is not None else None,connected_families=len(classes),estimable_bootstraps=len(values),
            interval=np.quantile(values,[.025,.975]).tolist() if values else None,largest_family_fraction=max(Counter(cluster).values())/len(pp),
            caution='Few connected components or one dominant component can make family resampling unstable; these are dependent lexical families, not independent biological samples.'))
    # Joint context occurrence resampling by document; restrict matrices to the
    # forms actually in registered pairs to avoid a corpus-sized dense tensor.
    sections=sorted(set(r.get('section') for r in rr if r.get('section') is not None));doclist=sorted(set(r['folio_component'] for r in rr));docindex={d:i for i,d in enumerate(doclist)}
    selected_forms=sorted(set(aa)|set(bb));formindex={f:i for i,f in enumerate(selected_forms)};ai=np.array([formindex[a] for a in aa]);bi=np.array([formindex[b] for b in bb])
    matrices=[]
    for section in sections:
        coords=[(docindex[r['folio_component']],formindex[i]) for r,i in zip(rr,ids) if i in formindex and r.get('section')==section]
        matrix=coo_matrix((np.ones(len(coords)),tuple(zip(*coords))),shape=(len(doclist),len(selected_forms))).tocsr() if coords else coo_matrix((len(doclist),len(selected_forms))).tocsr();matrices.append(matrix)
    bootvalues=defaultdict(list)
    if len(sections)>=2:
        for _ in range(iterations):
            weights=np.bincount(rng.integers(len(doclist),size=len(doclist)),minlength=len(doclist));counts=np.stack([np.asarray(weights@m).ravel() for m in matrices],axis=1);total=counts.sum(axis=1);prob=counts/np.maximum(total[:,None],1)
            keep=(total[ai]>0)&(total[bi]>0)
            for metric,y in theme_metrics(prob[ai],prob[bi]).items():
                xx=x[keep].copy();xx[:,3]=np.log(np.sqrt(total[ai[keep]]*total[bi[keep]]))
                if len(xx)>=12 and np.linalg.matrix_rank(xx)==4:bootvalues[metric].append(float(np.linalg.lstsq(xx,y[keep],rcond=None)[0][1]))
    return dict(status='estimated',pairs=len(pp),family_bootstrap=family_results,
        theme_document_bootstrap=[dict(metric=k,estimable_bootstraps=len(v),interval=np.quantile(v,[.025,.975]).tolist()) for k,v in bootvalues.items()],
        theme_document_estimand='Selected pair vocabulary fixed; jointly resample context occurrences by caption/document block; omit pairs missing one member.',
        exact_historical_connected_family_bootstrap='Not reconstructed; this is an explicitly defined analogue.')

def main():
    root=OUT/'tests/dependence_boundaries';root.mkdir(parents=True,exist_ok=True);results=[];leakage=[];theme=[];purged=[]
    for name in ('ZL_EVA','RF','v101'):
        allrows=load(name);rows=[r for r in allrows if r.get('currier')=='B'];theme.append(dict(dataset=name,**family_theme_bootstrap(rows)))
        for field in ('folio_component','inherited_bifolio_block','quire'):
            valid=[r for r in rows if r.get(field)];clone=[dict(r,folio_component=str(r[field])) for r in valid]
            result,_=pair_assay(clone,'normalized_group_rank',8,2,5,199);result.update(dataset=name,subset='B',variant=field,groups=len(clone),dependency_blocks=len(set(r['folio_component'] for r in clone)));results.append(result)
        for boundary in ('comma_join','exclude_uncertain_space_rows'):
            source=read_json(OUT/f'data/comparisons/v2/{name}_comma_join_groups.json') if boundary=='comma_join' else allrows
            rr=[r for r in source if r.get('currier')=='B' and r.get('locus_kind')=='P' and r.get('units') and (boundary!='exclude_uncertain_space_rows' or not r['line_contains_uncertain_spaces'])]
            result,_=pair_assay(rr,'normalized_group_rank',8,2,5,199);result.update(dataset=name,subset='B',variant=boundary,groups=len(rr));results.append(result)
        blocks=defaultdict(set)
        for r in allrows:
            if r.get('inherited_bifolio_block'):blocks[r['inherited_bifolio_block']].add(r['split'])
        overlap=sorted(d for d,s in blocks.items() if 'test' in s and ('train' in s or 'validation' in s))
        leakage.append(dict(dataset=name,inherited_bifolio_blocks=len(blocks),test_train_shared_blocks=overlap,shared_count=len(overlap),
            limitation='Q/B fields are inherited after freeze; physical-panel mapping not independently verified. They diagnose possible dependence, not a source-image unit definition.'))
        testblocks={r['inherited_bifolio_block'] for r in rows if r['split']=='test' and r.get('inherited_bifolio_block')}
        retained=[r for r in rows if r['split']=='test' or (r['split'] in ('train','validation') and r.get('inherited_bifolio_block') and r['inherited_bifolio_block'] not in testblocks)]
        for side in ('left','right'):
            result,edges,predictions,triangles=graph_assay(retained,'normalized_group_rank',side,5,2,99)
            result.update(dataset=name,subset='B',variant='purge every inherited test bifolio from training/validation',rows=len(retained));purged.append(result)
        print(name,'dependence and boundary sensitivities complete',flush=True)
    write_json(root/'positional_results.json',results);write_json(root/'family_and_theme_results.json',theme);write_json(root/'bifolio_split_audit.json',leakage);write_json(root/'purged_graph_results.json',purged)
    write_csv(root/'results.csv',[dict(dataset=r['dataset'],variant=r['variant'],status=r['status'],pairs=r.get('pairs'),beta=r.get('beta'),lower=r.get('folio_bootstrap',{}).get('lower'),upper=r.get('folio_bootstrap',{}).get('upper')) for r in results])
    write_json(root/'config.json',dict(seed=SEED,minimum_frequency=8,edge_width=2,length_min=5,iterations=199,purged_graph_null_iterations=99,
        primary='caption-block, uncertain-comma-split convention retained as registered; all broader blocks and boundary variants are sensitivities',
        limitations=['Inherited bifolio and quire fields are conditional dependence proxies, not independently verified physical-panel reconstruction.','Uncertain boundaries affect both token frequency and ordinal position.','Purging comparison rows cannot retroactively remove possible bifolio dependence from already frozen image-family training.','No native conventional pixels are known; all conventional outcomes here are ranks.']))
    write_json(root/'input_manifest.json',dict(sources=[dict(dataset=n,path=input_path(n).relative_to(OUT).as_posix(),sha256=sha256(input_path(n))) for n in ('ZL_EVA','RF','v101')],source_sha256=sha256(OUT/'src/positional_dependence_and_boundaries_v0.py'),visual_freeze_sha256=sha256(OUT/'data/observations/visual_dataset_v0/FREEZE_MANIFEST.json')))
    (root/'README.md').write_text('# Dependence and uncertain boundaries\n\nRun `run.py`. This tests caption, inherited bifolio and quire dependence, uncertain comma alternatives, connected-family resampling, contextual document resampling and purged held-out graphs. It does not redefine visual writing units.\n',encoding='utf-8')
    (root/'run.py').write_text('from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]/"src"))\nfrom positional_dependence_and_boundaries_v0 import main\nmain()\n',encoding='utf-8')
    (root/'summary.md').write_text('# Dependence and boundary sensitivities\n\nThe primary rank specification is retained unchanged. Sensitivities use alternative uncertain-space boundaries and increasingly broad resampling blocks. Purged graph training excludes test bifolios under inherited metadata. Exact historical bootstrap settings remain unavailable. These tests cannot repair the failed native writing-group crosswalk.\n',encoding='utf-8')

if __name__=='__main__':main()
