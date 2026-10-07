"""Training-context comparison mappings; never a visual-unit crosswalk."""
from common import OUT,read_json,write_json,write_csv,sha256,SEED
from run_structural_tests_v2 import load,input_path
from structural_assays import pairs,prepare,correlation,pair_assay
from collections import Counter,defaultdict
import numpy as np

def comparison_mapping(target,source_rows,paired):
    index={r['group_id']:r for r in source_rows};types=defaultdict(Counter);held=[]
    for r in paired:
        source=index.get(r['from_group_id'])
        if r['to_dataset']!=target or not source or source.get('currier')!='B' or not r['from_units'] or not r['to_units']:continue
        a=tuple(r['from_units']);b=tuple(r['to_units'])
        if r['split']=='train':types[a][b]+=1
        elif r['split']=='test':held.append((a,b,r['folio_component']))
    lexical={a:counter.most_common(1)[0][0] for a,counter in types.items() if sum(counter.values())>=3 and counter.most_common(1)[0][1]/sum(counter.values())>=.8}
    forms=sorted(lexical);frequencies=np.array([sum(types[f].values()) for f in forms]);pp=pairs(forms,frequencies,3,2)
    evidence=defaultdict(lambda:defaultdict(set));contrast_records=[]
    for i,j,edit,depth,length in pp:
        a,b=forms[i],forms[j];ta,tb=lexical[a],lexical[b]
        if len(ta)!=len(tb):continue
        dif=[k for k,(u,v) in enumerate(zip(ta,tb)) if u!=v]
        if len(dif)!=1:continue
        k=dif[0];core=a[:edit]+('<?>',)+a[edit+1:]
        evidence[a[edit]][core].add(ta[k]);evidence[b[edit]][core].add(tb[k])
        contrast_records.append(dict(source_unit_a=a[edit],source_unit_b=b[edit],target_unit_a=ta[k],target_unit_b=tb[k],source_core=list(core),target_core=list(ta[:k]+('<?>',)+ta[k+1:])))
    mapping={};records=[]
    for a,cores in evidence.items():
        counts=Counter(next(iter(targets)) for targets in cores.values() if len(targets)==1)
        if not counts:continue
        winner,n=counts.most_common(1)[0];total=sum(counts.values());admitted=n>=5 and n/total>=.9
        records.append(dict(source_unit=a,target_unit=winner,independent_literal_contexts=n,total_unambiguous_contexts=total,agreement=n/total,admitted=admitted,alternatives=dict(counts)))
        if admitted:mapping[a]=winner
    covered=[]
    for a,b,doc in held:
        if all(u in mapping for u in a):covered.append(dict(document=doc,source=list(a),target=list(b),predicted=[mapping[u] for u in a],correct=tuple(mapping[u] for u in a)==b))
    accuracy=float(np.mean([r['correct'] for r in covered])) if covered else None
    return dict(target=target,status='conditional comparison correspondence; no source-image unit validation',mapping=records,contrast_evidence=contrast_records,
        heldout_covered_groups=len(covered),heldout_exact_group_accuracy=accuracy,heldout_predictions=covered,
        global_one_to_one_hypothesis_passed=bool(len(covered)>=30 and accuracy>=.9),
        limitation='Single-edit contexts may create context-specific mappings inside conventionally combined forms. Only a passed held-out complete-group rule permits exploratory graph correspondence.'),mapping

def collapse(u,spans):
    output=[];i=0
    while i<len(u):
        found=next((s for s in spans if tuple(u[i:i+len(s)])==tuple(s)),None)
        if found:output.append('EVA_COMPOUND:'+found);i+=len(found)
        else:output.append(u[i]);i+=1
    return output

def main():
    root=OUT/'tests/conventional_crossgraph';root.mkdir(parents=True,exist_ok=True);source=load('ZL_EVA')
    paired=read_json(OUT/'data/comparisons/v2/conventional_group_crosswalk.json');mapping_results=[];graph_results=[]
    for target in ('RF','v101'):
        result,mapping=comparison_mapping(target,source,paired);mapping_results.append(result)
        for minimum in (5,8):
            for side in ('left','right'):
                filename=f'graph_normalized_group_rank_{side}_freq{minimum}.json'
                aa=read_json(OUT/'tests/structural/ZL_EVA'/filename);bb=read_json(OUT/'tests/structural'/target/filename)
                bg={(r['from_unit'],r['to_unit']):r['delta'] for r in bb};a_values=[];b_values=[];matched=[];seen=set()
                if result['global_one_to_one_hypothesis_passed']:
                    for edge in aa:
                        a,b=edge['from_unit'],edge['to_unit']
                        if a not in mapping or b not in mapping or mapping[a]==mapping[b]:continue
                        key=tuple(sorted((mapping[a],mapping[b])))
                        if key not in bg or key in seen:continue
                        seen.add(key);value=bg[key]*(1 if mapping[a]<mapping[b] else -1)
                        a_values.append(edge['delta']);b_values.append(value);matched.append(dict(source_pair=[a,b],target_pair=[mapping[a],mapping[b]],source_delta=edge['delta'],target_oriented_delta=value))
                graph_results.append(dict(target=target,side=side,minimum_frequency=minimum,status='exploratory literal-unit comparison' if result['global_one_to_one_hypothesis_passed'] else 'not_estimable: global unit-mapping hypothesis failed held-out coverage/accuracy',
                    **correlation(a_values,b_values),matched_relations=matched,independence='RF is derived from ZL/GC; convention agreement is not independent manuscript replication.'))
    stress=[]
    for name,spans in [('literal_codepoints',[]),('ch_sh',['ch','sh']),('bench_sequences',['cth','cph','cfh','ckh','ch','sh'])]:
        transformed=[dict(r,units=collapse(r['units'],spans)) for r in source]
        for currier in ('A','B'):
            rr=[r for r in transformed if r.get('currier')==currier]
            result,_=pair_assay(rr,'normalized_group_rank',8,2,5,199)
            result.update(partition=name,currier=currier,compound_sequences=spans);stress.append(result)
            print(name,currier,result.get('pairs'),result.get('beta'),flush=True)
    write_json(root/'mapping_results.json',mapping_results);write_json(root/'graph_correspondence_results.json',graph_results);write_json(root/'grapheme_stress_results.json',stress)
    write_csv(root/'results.csv',[dict(test='grapheme_stress',dataset=r['partition'],subset=r['currier'],status=r['status'],effect=r.get('beta'),pairs=r.get('pairs')) for r in stress]+[
        dict(test='crossgraph',dataset=r['target'],subset=f"{r['side']}:{r['minimum_frequency']}",status=r['status'],effect=r.get('pearson'),pairs=r.get('n')) for r in graph_results])
    write_json(root/'config.json',dict(seed=SEED,mapping='train-only paired paragraph groups at same physical locus and count; dominant complete-form pairs >=3 occurrences and 80%; single-edit context unit hypothesis >=5 distinct contexts and 90%; held-out >=30 completely covered groups and >=90% exact agreement',
        grapheme_stress='literal codepoints, ch/sh collapse, longer bench-sequence collapse; longest match first; not visual alphabet hypotheses',
        registered_primary='frequency 8, edge width 2, length >=5, joint caption bootstrap 199 and within-line rank null 199',
        no_visual_crosswalk='All 18 audited geometric row matches failed; zero accepted manuscript-unit correspondences.',
        prior_art='No novelty claimed. Standardized comparison analogue, not exact unpublished historical mapping.'))
    write_json(root/'input_manifest.json',dict(sources=[dict(dataset=n,path=input_path(n).relative_to(OUT).as_posix(),sha256=sha256(input_path(n))) for n in ('ZL_EVA','RF','v101')],source_sha256=sha256(OUT/'src/conventional_crossgraph_v0.py'),visual_freeze_sha256=sha256(OUT/'data/observations/visual_dataset_v0/FREEZE_MANIFEST.json')))
    (root/'README.md').write_text('# Comparison mappings and grapheme stress\n\nRun `run.py`. These mappings are hypotheses about conventional encoding systems. They do not define, repair or validate the frozen image-unit inventory. Failed mapping and statistical cases are retained.\n',encoding='utf-8')
    (root/'run.py').write_text('from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]/"src"))\nfrom conventional_crossgraph_v0 import main\nmain()\n',encoding='utf-8')
    (root/'summary.md').write_text('# Conventional mapping and boundary stress\n\nTrain-only context correspondences must pass complete held-out group prediction before graph comparison. This tests the convention-level mapping assumption rather than assuming equal string lengths define unit correspondences. The EVA compounds change comparison segmentation only. Positional outcomes are ordinal source ranks; native writing positions remain unmapped. No decoded units or meanings are asserted.\n',encoding='utf-8')

if __name__=='__main__':main()
