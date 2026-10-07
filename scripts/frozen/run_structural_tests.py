"""Reproduce positional/graph assays after the visual snapshot has frozen."""
from common import OUT,read_json,write_json,write_csv,sha256,SEED
from structural_assays import pair_assay,graph_assay,sequence_assay
from collections import defaultdict
import argparse
import numpy as np


def load(name):
    if name in ('ZL_EVA','RF','v101'):
        rows=read_json(OUT/f'data/comparisons/{name}_groups_with_metadata.json')
        return [r for r in rows if r.get('units') and r.get('locus_kind')=='P']
    if name in ('Finnish','Turkish','Latin'):
        return read_json(OUT/f'data/controls/{name.lower()}_sentence_groups.json')
    source=read_json(OUT/'data/comparisons/visual_groups_with_metadata.json')
    field={'visual_fine':'visual_fine_units','visual_merged':'visual_merged_units','visual_factored':'visual_factored_units','visual_medium':'primary_candidate_units'}[name]
    return [dict(r,units=r[field]) for r in source if r.get(field)]


def budget_controls(rows,budget,replicate=0):
    rng=np.random.default_rng(SEED+replicate);bydoc=defaultdict(list)
    for r in rows:bydoc[r['folio_component']].append(r)
    docs=list(bydoc);rng.shuffle(docs);out=[]
    for doc in docs:
        byline=defaultdict(list)
        for r in bydoc[doc]:byline[r['line_id']].append(r)
        for line in byline.values():
            if len(out)+len(line)>budget:return out
            out.extend(line)
    return out


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--dataset',required=True);ap.add_argument('--iterations',type=int,default=199);ap.add_argument('--graphs-only',action='store_true');args=ap.parse_args()
    freeze=OUT/'data/observations/visual_dataset_v0/FREEZE_MANIFEST.json'
    if not freeze.exists():raise ValueError('Visual snapshot has not frozen')
    rows=load(args.dataset);root=OUT/'tests/structural'/args.dataset;root.mkdir(parents=True,exist_ok=True)
    iscontrol=args.dataset in ('Finnish','Turkish','Latin');groups={'all':rows}
    if not iscontrol:
        groups.update({lang:[r for r in rows if r.get('currier')==lang] for lang in ('A','B')})
    positions=['normalized_group_rank']
    if args.dataset.startswith('visual_'):positions+=['normalized_pixel_center','source_pixel_center_x','source_pixel_x_page_fraction']
    minimal=[];graph_results=[];sequence=[]
    if not args.graphs_only:
        for subset,data in groups.items():
            for position in positions:
                for minimum in (5,8,10,12):
                    for width in (1,2):
                        # Full dependence/null work is the registered primary
                        # frequency-8, two-unit-edge, length>=5 specification.
                        primary=minimum==8 and width==2
                        result,pairs=pair_assay(data,position,minimum,width,3 if width==1 else 5,args.iterations if primary else 0)
                        result.update(dataset=args.dataset,subset=subset);minimal.append(result)
                        if primary:
                            write_json(root/f'minimal_pairs_{subset}_{position}.json',pairs)
                            # Historical assays included short forms: retained as
                            # a separate reconstruction, never silently pooled.
                            legacy,_=pair_assay(data,position,minimum,width,1,0);legacy.update(dataset=args.dataset,subset=subset,specification='legacy all lengths');minimal.append(legacy)
                        print(args.dataset,subset,position,minimum,width,result.get('pairs'),result.get('beta'),flush=True)
                # One-unit edge with strict >=5 forms is also preserved.
                strict,_=pair_assay(data,position,8,1,5,0);strict.update(dataset=args.dataset,subset=subset,specification='one-unit edge strict length>=5');minimal.append(strict)
        write_json(root/'minimal_pair_results.json',minimal)
    graph_data=rows if iscontrol else groups['B']
    # Physical pixel x is source-scale dependent. Use normalized measured line x
    # as the primary pixel graph endpoint; absolute pixel regression stays above.
    graph_positions=['normalized_group_rank']+(['normalized_pixel_center'] if args.dataset.startswith('visual_') else [])
    for position in graph_positions:
        for minimum in (5,8):
            for side in ('left','right'):
                result,edges,predictions,triangles=graph_assay(graph_data,position,side,minimum,2,min(99,args.iterations))
                result.update(dataset=args.dataset,subset='all' if iscontrol else 'B');graph_results.append(result)
                stem=f'{position}_{side}_freq{minimum}';write_json(root/f'graph_{stem}.json',edges);write_json(root/f'prediction_{stem}.json',predictions);write_json(root/f'triangles_{stem}.json',triangles)
                print(args.dataset,stem,result['full_relations'],result['direct_edge_removed_prediction'],flush=True)
        seq=sequence_assay(graph_data,position,min(99,args.iterations));seq.update(dataset=args.dataset);sequence.append(seq)
    write_json(root/'directional_graph_results.json',graph_results);write_json(root/'sequence_results.json',sequence)
    # Predeclared independent folio half-splits, retaining captions/doc blocks.
    rng=np.random.default_rng(SEED);folios=sorted(set(r['folio_component'] for r in graph_data));halves=[]
    from structural_assays import edge_graph,correlation
    for repeat in range(30):
        order=rng.permutation(folios);left=set(order[:len(order)//2]);a=[r for r in graph_data if r['folio_component'] in left];b=[r for r in graph_data if r['folio_component'] not in left]
        for side in ('left','right'):
            aa=edge_graph(a,'normalized_group_rank',side,5,2);bb=edge_graph(b,'normalized_group_rank',side,5,2);common=sorted(set(aa)&set(bb))
            halves.append(dict(replicate=repeat,side=side,**correlation([aa[k]['delta'] for k in common],[bb[k]['delta'] for k in common])))
    write_csv(root/'independent_folio_halves.csv',halves)
    if iscontrol:
        # Budget uses observed conventional Currier B, not the historical chat count.
        comparison=load('ZL_EVA');budget=sum(r.get('currier')=='B' for r in comparison);budget_results=[]
        for replicate in range(5):
            sample=budget_controls(rows,budget,replicate)
            mp,_=pair_assay(sample,'normalized_group_rank',8,2,5,0)
            for side in ('left','right'):
                gr,_,_,_=graph_assay(sample,'normalized_group_rank',side,5,2,0)
                budget_results.append(dict(replicate=replicate,sample_groups=len(sample),target_budget=budget,side=side,
                    minimal_pairs=mp.get('pairs'),edge_beta=mp.get('beta'),left_or_right_relations=gr['full_relations'],triangles=gr['context_disjoint_triangles'],
                    alternate_prediction=gr['direct_edge_removed_prediction']))
        write_json(root/'voynich_budget_control_results.json',budget_results)
    write_json(root/'config.json',dict(seed=SEED,dataset=args.dataset,primary=dict(minimum_frequency=8,edge_width=2,length_min=5),
        sensitivity=dict(frequencies=[5,8,10,12],edges=[1,2],legacy_all_lengths=True),position_endpoints=positions,
        bootstrap_iterations=args.iterations,null_iterations=min(99,args.iterations),independent_half_splits=30,
        source='frozen visual sequences or post-freeze literal conventional codepoints; no redefinition from effect sizes',
        controls=['length','log geometric mean pair frequency','connected-family clustering when at least 10 clusters','joint folio occurrence bootstrap','within-line measured-position shuffle'],
        graph_rules=['at least two matched cores; equal-core delta primary; occurrence weighting recorded',
            'train/validation edges compared to test; direct training edge AND its matched cores removed for alternate prediction',
            'triangle edges use disjoint hashed core buckets; common-mean identity excluded',
            'adjacency only between consecutive original source ranks; gaps reset accumulators'],
        limitations=['Source gate and boundaries are uncertain; conditioning on admitted groups can bias outcomes.',
            'Folio components are caption/document blocks, not verified independent bifolios/authors.',
            'Absolute native pixel x depends on scan scale and page layout; normalized measured line x is separate.',
            'Control position is UD sentence ordinal rank; no natural-language manuscript pixel control exists.',
            'Multiple exploratory specifications are not independent confirmations; no uniqueness/decipherment inference.',
            'Exact prior connected-family bootstrap specification was not recovered; these tests do not claim that exact reproduction.']))
    write_json(root/'input_manifest.json',dict(visual_freeze_sha256=sha256(freeze),rows=len(rows),
        source_path='data/comparisons/visual_groups_with_metadata.json' if args.dataset.startswith('visual_') else
            f'data/controls/{args.dataset.lower()}_sentence_groups.json' if iscontrol else f'data/comparisons/{args.dataset}_groups_with_metadata.json'))
    (root/'README.md').write_text(f'# {args.dataset} structural tests\n\nRun `run.py`. Results retain every primary, sensitivity and non-estimable outcome. Ordinal token rank is not measured pixel position. See configuration for dependence and null models.\n',encoding='utf-8')
    (root/'run.py').write_text(f'from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[3]/"src"))\nsys.argv=[sys.argv[0],"--dataset","{args.dataset}"]\nfrom run_structural_tests import main\nmain()\n',encoding='utf-8')
    (root/'summary.md').write_text('# Reproduction outputs\n\nSee minimal-pair, graph, independent-half and sequence result files. Non-estimable cases are substantive coverage/power limitations, not zero effects. No source-unit inventory is certified by these statistics.\n',encoding='utf-8')

if __name__=='__main__':main()
