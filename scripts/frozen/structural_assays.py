"""Shared structural assays for frozen visual sequences and later comparisons.

Space-gap groups and transcription tokens are treated as observations, not words.
No statistic here can repair failed image segmentation or prove a decipherment.
"""
from common import OUT,read_json,write_json,write_csv,sha256,SEED
from collections import defaultdict,Counter
from itertools import combinations
import hashlib
import numpy as np
import networkx as nx
from statsmodels.regression.linear_model import OLS
from scipy.stats import pearsonr,spearmanr


def correlation(a,b):
    if len(a)<4 or np.std(a)<1e-10 or np.std(b)<1e-10:return dict(n=len(a),pearson=None,spearman=None,same_direction=None)
    return dict(n=len(a),pearson=float(pearsonr(a,b).statistic),spearman=float(spearmanr(a,b).statistic),same_direction=float(np.mean(np.sign(a)==np.sign(b))))


def regression(x,y,clusters=None):
    if len(y)<max(12,x.shape[1]*3) or np.linalg.matrix_rank(x)<x.shape[1]:
        return dict(status='not_estimable: insufficient observations or design rank',n=len(y),beta=None,p_hc3=None)
    fit=OLS(y,x).fit(cov_type='HC3');result=dict(status='estimated',n=len(y),beta=float(fit.params[1]),p_hc3=float(fit.pvalues[1]),se_hc3=float(fit.bse[1]))
    if clusters is not None:
        ng=len(set(clusters));result['connected_family_clusters']=ng
        result['family_cluster_p']=None
        if ng>=10:
            cf=OLS(y,x).fit(cov_type='cluster',cov_kwds={'groups':clusters},use_t=True)
            result['family_cluster_p']=float(cf.pvalues[1]);result['family_cluster_se']=float(cf.bse[1])
        else:result['family_cluster_limitation']='Fewer than 10 connected-family clusters; inferential p-value withheld.'
    return result


def prepare(rows,position):
    rr=[r for r in rows if r.get('units') and r.get(position) is not None]
    forms=sorted(set(tuple(r['units']) for r in rr));lookup={f:i for i,f in enumerate(forms)}
    ids=np.array([lookup[tuple(r['units'])] for r in rr],np.int32);positions=np.array([r[position] for r in rr],float)
    frequencies=np.bincount(ids,minlength=len(forms));sums=np.bincount(ids,weights=positions,minlength=len(forms))
    means=sums/np.maximum(1,frequencies)
    return rr,forms,ids,positions,frequencies,means


def pairs(forms,frequencies,minimum,length_min):
    buckets=defaultdict(list)
    for i,f in enumerate(forms):
        if frequencies[i]<minimum or len(f)<length_min:continue
        for j in range(len(f)):buckets[(len(f),j,f[:j],f[j+1:])].append(i)
    found=[]
    for key,indexes in buckets.items():
        for a,b in combinations(indexes,2):
            j=key[1];found.append((a,b,j,min(j,len(forms[a])-1-j),len(forms[a])))
    return found


def section_distances(rows,ids,nforms):
    sections=sorted(set(r.get('section') for r in rows if r.get('section') is not None))
    if len(sections)<2:return None
    lookup={s:i for i,s in enumerate(sections)};counts=np.zeros((nforms,len(sections)))
    for r,i in zip(rows,ids):
        if r.get('section') in lookup:counts[i,lookup[r['section']]]+=1
    denom=counts.sum(axis=1);return counts/np.maximum(denom[:,None],1),denom


def pair_assay(rows,position,minimum=8,edge_width=2,length_min=5,iterations=199):
    rr,forms,ids,pos,freq,means=prepare(rows,position);pp=pairs(forms,freq,minimum,length_min)
    if not pp:return dict(status='not_estimable: no qualifying minimal pairs',pairs=0,position=position,minimum_frequency=minimum,edge_width=edge_width,length_min=length_min),[]
    arr=np.array(pp);aa,bb,edit,depth,length=arr.T;edge=depth<edge_width
    x=np.c_[np.ones(len(pp)),edge.astype(float),length,np.log(np.sqrt(freq[aa]*freq[bb]))]
    graph=nx.Graph();graph.add_edges_from(zip(aa,bb));components={v:i for i,c in enumerate(nx.connected_components(graph)) for v in c}
    clusters=[components[a] for a in aa];y=abs(means[aa]-means[bb]);result=regression(x,y,clusters)
    result.update(pairs=len(pp),position=position,minimum_frequency=minimum,edge_width=edge_width,length_min=length_min,
        outer_pairs=int(sum(depth==0)),near_pairs=int(sum(depth==1)),interior_pairs=int(sum(depth>=2)),
        largest_family_fraction=max(Counter(clusters).values())/len(pp),depth_means={str(d):float(np.mean(y[depth==d])) for d in sorted(set(depth))})
    theme=section_distances(rr,ids,len(forms))
    if theme is not None:
        distributions,denom=theme;p,q=distributions[aa],distributions[bb];keep=(denom[aa]>0)&(denom[bb]>0)
        m=(p+q)/2
        js=.5*(np.sum(p*np.log2(np.maximum(p,1e-20)/np.maximum(m,1e-20)),axis=1)+np.sum(q*np.log2(np.maximum(q,1e-20)/np.maximum(m,1e-20)),axis=1))
        metrics={'TV':.5*abs(p-q).sum(axis=1),'JSD_bits':js,'sqrt_JS':np.sqrt(np.maximum(js,0)),
            'Hellinger':np.sqrt(.5*((np.sqrt(p)-np.sqrt(q))**2).sum(axis=1))}
        result['theme']={name:regression(x[keep],v[keep],np.array(clusters)[keep]) for name,v in metrics.items()}
    else:result['theme_status']='not_estimable: section labels absent or only one class'
    pairrows=[dict(form_a=list(forms[a]),form_b=list(forms[b]),edit_index=int(j),depth=int(d),length=int(l),frequency_a=int(freq[a]),frequency_b=int(freq[b]),
        mean_position_a=float(means[a]),mean_position_b=float(means[b]),absolute_displacement=float(abs(means[a]-means[b])),connected_family=components[a]) for a,b,j,d,l in pp]
    if iterations<=0 or result['beta'] is None:return result,pairrows
    rng=np.random.default_rng(SEED);folios=sorted(set(r['folio_component'] for r in rr));fi={f:i for i,f in enumerate(folios)}
    counts=np.zeros((len(folios),len(forms)));sums=np.zeros_like(counts)
    for r,i,p in zip(rr,ids,pos):counts[fi[r['folio_component']],i]+=1;sums[fi[r['folio_component']],i]+=p
    boot=[];deletions=[]
    for b in range(iterations+len(folios)):
        if b<iterations:weights=np.bincount(rng.integers(len(folios),size=len(folios)),minlength=len(folios))
        else:weights=np.ones(len(folios));weights[b-iterations]=0
        f=weights@counts;means_b=(weights@sums)/np.maximum(f,1);keep=(f[aa]>0)&(f[bb]>0)
        xb=x[keep].copy();xb[:,3]=np.log(np.sqrt(f[aa[keep]]*f[bb[keep]]));yb=abs(means_b[aa[keep]]-means_b[bb[keep]])
        if len(yb)>=12 and np.linalg.matrix_rank(xb)==xb.shape[1]:
            val=float(np.linalg.lstsq(xb,yb,rcond=None)[0][1]);(boot if b<iterations else deletions).append(val)
    result['folio_bootstrap']=dict(requested=iterations,estimable=len(boot),lower=float(np.quantile(boot,.025)) if boot else None,
        upper=float(np.quantile(boot,.975)) if boot else None,estimand='frozen selected vocabulary; joint occurrence resampling by caption/document group; missing forms omit affected pairs')
    result['leave_one_folio_out']=dict(deletions=len(deletions),positive=sum(v>0 for v in deletions),minimum=min(deletions) if deletions else None,maximum=max(deletions) if deletions else None)
    byline=defaultdict(list)
    for i,r in enumerate(rr):byline[r['line_id']].append(i)
    null=[]
    for b in range(iterations):
        shuffled=pos.copy()
        for ix in byline.values():shuffled[ix]=rng.permutation(pos[ix])
        nm=np.bincount(ids,weights=shuffled,minlength=len(forms))/np.maximum(freq,1)
        null.append(float(np.linalg.lstsq(x,abs(nm[aa]-nm[bb]),rcond=None)[0][1]))
    result['within_line_null']=dict(iterations=iterations,mean=float(np.mean(null)),sd=float(np.std(null)),
        two_sided_p=float((1+sum(abs(v)>=abs(result['beta']) for v in null))/(iterations+1)),
        preserves='vocabulary, frequency, retained line membership and retained measured-position slots; unresolved gaps remain')
    return result,pairrows


def edge_graph(rows,position,side='left',minimum=5,minimum_cores=2,bucket=None):
    rr,forms,ids,pos,freq,means=prepare(rows,position);cores=defaultdict(dict)
    for i,f in enumerate(forms):
        if len(f)<2 or freq[i]<minimum:continue
        core=f[1:] if side=='left' else f[:-1];symbol=f[0] if side=='left' else f[-1]
        if bucket is not None and int(hashlib.sha256(repr(core).encode()).hexdigest(),16)%3!=bucket:continue
        cores[core][symbol]=i
    differences=defaultdict(list)
    for core,variants in cores.items():
        for a,b in combinations(sorted(variants),2):
            i,j=variants[a],variants[b];differences[(a,b)].append((means[j]-means[i],core,int(freq[i]+freq[j])))
    edges={key:dict(delta=float(np.mean([v[0] for v in values])),matched_cores=len(values),
        occurrence_weighted_delta=float(np.average([v[0] for v in values],weights=[v[2] for v in values])),
        core_details=[dict(core=list(v[1]),delta=float(v[0]),combined_frequency=v[2]) for v in values])
        for key,values in differences.items() if len(values)>=minimum_cores}
    return edges


def oriented(edges,a,b):
    key=tuple(sorted((a,b)));edge=edges.get(key)
    return None if edge is None else edge['delta']*(1 if a<b else -1)


def alternate_prediction(edges,a,c):
    target=tuple(sorted((a,c)));gg=nx.Graph();gg.add_edges_from(k for k in edges if k!=target)
    if a not in gg or c not in gg or not nx.has_path(gg,a,c):return None
    nodes=sorted(nx.node_connected_component(gg,a));index={v:i for i,v in enumerate(nodes)};eq=[];deltas=[];weights=[]
    for (u,v),r in edges.items():
        if (u,v)==target or u not in index or v not in index:continue
        row=np.zeros(len(nodes));row[index[v]]=1;row[index[u]]=-1;eq.append(row);deltas.append(r['delta']);weights.append(np.sqrt(r['matched_cores']))
    eq=np.array(eq);ww=np.array(weights);p=np.linalg.lstsq(eq*ww[:,None],np.array(deltas)*ww,rcond=None)[0]
    return float(p[index[c]]-p[index[a]])


def graph_assay(rows,position,side='left',minimum=5,minimum_cores=2,iterations=99):
    train=[r for r in rows if r['split'] in ('train','validation')];test=[r for r in rows if r['split']=='test']
    full=edge_graph(rows,position,side,minimum,minimum_cores);tr=edge_graph(train,position,side,minimum,minimum_cores);te=edge_graph(test,position,side,minimum,minimum_cores)
    common=sorted(set(tr)&set(te));repro=correlation([tr[k]['delta'] for k in common],[te[k]['delta'] for k in common]);predictions=[]
    for a,c in common:
        excluded={tuple(v['core']) for v in tr[(a,c)]['core_details']}
        context_train=[r for r in train if tuple(r['units'][1:] if side=='left' else r['units'][:-1]) not in excluded]
        context_edges=edge_graph(context_train,position,side,minimum,minimum_cores)
        predicted=alternate_prediction(context_edges,a,c)
        # Ordinary context-independent positional preference is a competing
        # explanation, estimated without the direct training matched cores.
        pref={u:np.mean([r[position] for r in context_train if r.get(position) is not None and
            (r['units'][0] if side=='left' else r['units'][-1])==u]) for u in (a,c)}
        baseline=float(pref[c]-pref[a]) if np.isfinite(pref[a]) and np.isfinite(pref[c]) else None
        if predicted is not None:predictions.append(dict(from_unit=a,to_unit=c,alternate_training_prediction=predicted,
            ordinary_unit_preference_prediction=baseline,excluded_direct_training_cores=len(excluded),heldout_direct_delta=te[(a,c)]['delta']))
    prediction=correlation([r['alternate_training_prediction'] for r in predictions],[r['heldout_direct_delta'] for r in predictions])
    # Edge-role contexts are disjoint by hashed core, avoiding shared-mean algebra.
    buckets=[edge_graph(train,position,side,minimum,minimum_cores,bucket=b) for b in range(3)];nodes=sorted(set(v for k in full for v in k));triangles=[]
    for a,b,c in combinations(nodes,3):
        ab=oriented(buckets[0],a,b);bc=oriented(buckets[1],b,c);ac=oriented(buckets[2],a,c)
        if ab is None or bc is None or ac is None:continue
        closure=ab+bc-ac;scale=np.sqrt(ab*ab+bc*bc+ac*ac)
        triangles.append(dict(a=a,b=b,c=c,ab=ab,bc=bc,ac=ac,closure=closure,normalized_absolute_closure=abs(closure)/max(scale,1e-10)))
    result=dict(status='estimated' if full else 'not_estimable: no qualifying directional relations',position=position,side=side,minimum_frequency=minimum,minimum_matched_cores=minimum_cores,
        full_relations=len(full),train_relations=len(tr),test_relations=len(te),heldout_reproducibility=repro,
        direct_edge_removed_prediction=prediction,context_disjoint_triangles=len(triangles),
        median_normalized_triangle_closure=float(np.median([r['normalized_absolute_closure'] for r in triangles])) if triangles else None,
        triangle_warning='Common form-mean triangle closure is algebraic and is not counted; here core buckets for AB, BC, AC are disjoint.')
    rng=np.random.default_rng(SEED);validrows=[r for r in rows if r.get(position) is not None];byline=defaultdict(list)
    for i,r in enumerate(validrows):byline[r['line_id']].append(i)
    nullrepro=[];nullprediction=[];nullclosure=[]
    if iterations and (len(common)>=4 or triangles):
        for _ in range(iterations):
            shuffled=[dict(r) for r in validrows]
            for ix in byline.values():
                values=rng.permutation([validrows[i][position] for i in ix])
                for i,v in zip(ix,values):shuffled[i][position]=float(v)
            nt=[r for r in shuffled if r['split'] in ('train','validation')];ne=[r for r in shuffled if r['split']=='test']
            ng=edge_graph(nt,position,side,minimum,minimum_cores);nh=edge_graph(ne,position,side,minimum,minimum_cores)
            cr=correlation([ng[k]['delta'] for k in common],[nh[k]['delta'] for k in common])
            if cr['pearson'] is not None:nullrepro.append(cr['pearson'])
            pr=[]
            for r in predictions:
                key=tuple(sorted((r['from_unit'],r['to_unit'])));excluded={tuple(v['core']) for v in tr[key]['core_details']}
                context_nt=[v for v in nt if tuple(v['units'][1:] if side=='left' else v['units'][:-1]) not in excluded]
                context_ng=edge_graph(context_nt,position,side,minimum,minimum_cores)
                pr.append((alternate_prediction(context_ng,r['from_unit'],r['to_unit']),nh[key]['delta']))
            pc=correlation([v[0] for v in pr if v[0] is not None],[v[1] for v in pr if v[0] is not None])
            if pc['pearson'] is not None:nullprediction.append(pc['pearson'])
            nb=[edge_graph(nt,position,side,minimum,minimum_cores,bucket=b) for b in range(3)];cl=[]
            for tri in triangles:
                a,b,c=tri['a'],tri['b'],tri['c'];ab=oriented(nb[0],a,b);bc=oriented(nb[1],b,c);ac=oriented(nb[2],a,c)
                cl.append(abs(ab+bc-ac)/max(np.sqrt(ab*ab+bc*bc+ac*ac),1e-10))
            if cl:nullclosure.append(float(np.median(cl)))
    for name,values,observed in [('reproducibility',nullrepro,repro['pearson']),('alternate_prediction',nullprediction,prediction['pearson']),
        ('triangle_closure',nullclosure,result['median_normalized_triangle_closure'])]:
        result[name+'_null']=dict(iterations=len(values),mean=float(np.mean(values)) if values else None,
            p=float((1+sum(v<=observed if name=='triangle_closure' else abs(v)>=abs(observed) for v in values))/(len(values)+1)) if values and observed is not None else None)
    edges=[dict(from_unit=k[0],to_unit=k[1],**r) for k,r in full.items()]
    return result,edges,predictions,triangles


def sequence_assay(rows,position,iterations=99):
    """Held-out adjacency and cumulative-state prediction with line resets.

    Physical x order is tested in both directions; these are predictive scores,
    not evidence of logical reading direction, causality or pen sequence.
    """
    train=[r for r in rows if r['split'] in ('train','validation') and r.get(position) is not None]
    test=[r for r in rows if r['split']=='test' and r.get(position) is not None]
    if not train or not test:return dict(status='not_estimable: held-out observations absent')
    result=dict(status='exploratory predictive test',position=position,physical_direction='increasing stored group x/rank; not assumed linguistic direction');scores=[]
    for reverse in (False,True):
        # Outer visual/conventional unit category as next-state target.
        classes=sorted(set(r['units'][0] for r in train if r['units']));index={v:i for i,v in enumerate(classes)}
        counts=np.ones(len(classes));trans=np.ones((len(classes),len(classes)));position_counts=np.ones((20,len(classes)))
        def position_length_bin(r):
            lb=0 if len(r['units'])<=2 else 1 if len(r['units'])<=4 else 2 if len(r['units'])<=7 else 3
            return min(4,int(r['normalized_group_rank']*5))*4+lb
        def lineset(rr):
            ll=defaultdict(list)
            for r in rr:ll[r['line_id']].append(r)
            return [sorted(v,key=lambda r:r['normalized_group_rank'],reverse=reverse) for v in ll.values()]
        for line in lineset(train):
            for i,r in enumerate(line):
                unit=r['units'][0];j=index[unit];counts[j]+=1;position_counts[position_length_bin(r),j]+=1
                if i and abs(r['group_rank']-line[i-1]['group_rank'])==1 and line[i-1]['units'][0] in index:trans[index[line[i-1]['units'][0]],j]+=1
        prior=counts/counts.sum();conditional=trans/trans.sum(axis=1,keepdims=True);pbin=position_counts/position_counts.sum(axis=1,keepdims=True)
        losses=[];transition_records=[]
        for line in lineset(test):
            for i,r in enumerate(line):
                if not i or r['units'][0] not in index or line[i-1]['units'][0] not in index:continue
                if abs(r['group_rank']-line[i-1]['group_rank'])!=1:continue
                j=index[r['units'][0]];previous=index[line[i-1]['units'][0]];b=position_length_bin(r)
                # Product model adds adjacency to positional prior, normalized.
                combined=conditional[previous]*pbin[b]/prior;combined/=combined.sum()
                losses.append((r['folio_component'],-np.log2(prior[j]),-np.log2(pbin[b,j]),-np.log2(combined[j])))
                transition_records.append((r['line_id'],r['folio_component'],j,previous,b))
        folios=sorted(set(v[0] for v in losses));equal=[np.mean([v[3]-v[2] for v in losses if v[0]==f]) for f in folios]
        score=dict(direction='decreasing_physical_x' if reverse else 'increasing_physical_x',transitions=len(losses),folio_components=len(folios),
            equal_folio_adjacency_excess_bits_over_position=float(np.mean(equal)) if equal else None,
            limitation='Only consecutive original group ranks count as adjacent; coarse positional baseline can miss other dependencies.')
        rng=np.random.default_rng(SEED);null=[];byline=defaultdict(list)
        for i,v in enumerate(transition_records):byline[v[0]].append(i)
        for _ in range(iterations if equal else 0):
            previous=np.array([v[3] for v in transition_records])
            for ix in byline.values():previous[ix]=rng.permutation(previous[ix])
            perfolio=defaultdict(list)
            for (_,f,j,old,b),p in zip(transition_records,previous):
                combined=conditional[p]*pbin[b]/prior;combined/=combined.sum()
                perfolio[f].append(float(-np.log2(combined[j])+np.log2(pbin[b,j])))
            null.append(float(np.mean([np.mean(v) for v in perfolio.values()])))
        score['conditional_previous_state_null']=dict(iterations=len(null),mean=float(np.mean(null)) if null else None,
            p=float((1+sum(v<=np.mean(equal) for v in null))/(len(null)+1)) if null else None,
            preserves='heldout target, positional baseline, within-line multiset of preceding categories; tests preceding-category pairing')
        scores.append(score)
    result['direction_scores']=scores
    # Train symbol potentials from signed left-edge graph. No test refit.
    edges=edge_graph(train,position,'left',5,2);graph=nx.Graph();graph.add_edges_from(edges)
    potentials={}
    for comp in nx.connected_components(graph):
        nodes=sorted(comp);lookup={v:i for i,v in enumerate(nodes)};eq=[];yy=[]
        for (a,b),edge in edges.items():
            if a not in lookup:continue
            row=np.zeros(len(nodes));row[lookup[b]]=1;row[lookup[a]]=-1;eq.append(row);yy.append(edge['delta'])
        values=np.linalg.lstsq(np.array(eq),np.array(yy),rcond=None)[0];potentials.update(zip(nodes,values))
    def state_design(rr):
        ll=defaultdict(list)
        for r in rr:ll[r['line_id']].append(r)
        xx=[];yy=[];folios=[]
        for line in ll.values():
            state=0.;previous=None
            for r in sorted(line,key=lambda r:r['normalized_group_rank']):
                if previous is not None and r['group_rank']-previous!=1:state=0.
                n=len(r['units']);xx.append([1.,r['normalized_group_rank'],n,state]);yy.append(r[position]);folios.append(r['folio_component'])
                state+=sum(potentials.get(u,0.) for u in r['units'])
                previous=r['group_rank']
        return np.array(xx),np.array(yy),folios
    x,y,_=state_design(train);xt,yt,folios=state_design(test)
    if position=='normalized_group_rank':
        result['running_state']=dict(status='not independently estimable: ordinal rank outcome is already the baseline rank predictor',
            warning='A rank accumulator coefficient cannot establish added prediction when rank is known.')
    elif potentials and len(y)>20 and np.linalg.matrix_rank(x)==4:
        base=np.linalg.lstsq(x[:,:3],y,rcond=None)[0];full=np.linalg.lstsq(x,y,rcond=None)[0]
        e0=(yt-xt[:,:3]@base)**2;e1=(yt-xt@full)**2
        perfolio=[float(np.mean(e1[np.array(folios)==f]-e0[np.array(folios)==f])) for f in sorted(set(folios))]
        result['running_state']=dict(status='estimated',training_potential_units=len(potentials),heldout_groups=len(yt),
            equal_folio_mse_difference=float(np.mean(perfolio)),
            caveat='Group ordinal rank in baseline makes rank outcome exactly predictable; rank accumulator gain is not independently meaningful. Pixel outcome is separate; cumulative state can proxy length/layout.')
        rng=np.random.default_rng(SEED);bootstrap=rng.choice(perfolio,(1000,len(perfolio)),replace=True).mean(axis=1)
        result['running_state']['folio_bootstrap_interval']=[float(np.quantile(bootstrap,.025)),float(np.quantile(bootstrap,.975))]
        def null_state(rr):
            ll=defaultdict(list)
            for r in rr:ll[r['line_id']].append(r)
            xx=[];yy=[];ff=[]
            for line in ll.values():
                line=sorted(line,key=lambda r:r['normalized_group_rank']);increments=rng.permutation([sum(potentials.get(u,0.) for u in r['units']) for r in line]);state=0.;previous=None
                for r,inc in zip(line,increments):
                    if previous is not None and r['group_rank']-previous!=1:state=0.
                    xx.append([1.,r['normalized_group_rank'],len(r['units']),state]);yy.append(r[position]);ff.append(r['folio_component']);state+=inc;previous=r['group_rank']
            return np.array(xx),np.array(yy),np.array(ff)
        null=[]
        for _ in range(iterations):
            xn,yn,_=null_state(train);xnt,ynt,fn=null_state(test);beta=np.linalg.lstsq(xn,yn,rcond=None)[0]
            error=(ynt-xnt@beta)**2-e0
            null.append(float(np.mean([np.mean(error[fn==f]) for f in sorted(set(fn))])))
        result['running_state']['within_line_increment_null']=dict(iterations=len(null),mean=float(np.mean(null)),
            p=float((1+sum(v<=np.mean(perfolio) for v in null))/(len(null)+1)),
            rule='shuffle training/test potential increments within original lines, preserve lengths and outcome positions, refit training coefficients, reset at unresolved gaps')
    else:result['running_state']=dict(status='not_estimable: insufficient connected training graph or design rank')
    return result
