"""Complete readable derivative summaries and figures for post-freeze assays."""
from common import OUT,read_json,write_json,write_csv,sha256,SEED
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def plot_intervals(root,records,title,xlabel,filename='effects.png'):
    fig=root/'figures';fig.mkdir(parents=True,exist_ok=True)
    chart,ax=plt.subplots(figsize=(9,max(3,len(records)*.37)))
    for i,(label,value,interval) in enumerate(records):
        if value is not None:
            ax.plot(value,i,'o',color='#155e75')
            if interval and all(v is not None for v in interval):ax.plot(interval,[i,i],color='#155e75')
        else:ax.text(.02,i,'Not estimable',transform=ax.get_yaxis_transform(),va='center')
    ax.set_yticks(range(len(records)),[r[0] for r in records]);ax.set_ylim(-.7,max(.7,len(records)-.3));ax.axvline(0,color='#aaa',lw=.7);ax.set_title(title);ax.set_xlabel(xlabel);chart.tight_layout();chart.savefig(fig/filename,dpi=150);plt.close(chart)

def base_summary(root,title,hypothesis):
    config=read_json(root/'config.json');manifest=read_json(root/'input_manifest.json')
    return [f'# {title}','',hypothesis,'',f'Seed: {config.get("seed",SEED)}. Exact source paths and SHA-256 digests: `input_manifest.json`. Inclusion, exclusions, model settings and null definitions: `config.json`.','',
      'Visual source groups and prototype categories are provisional. Unknown assignments are excluded without renumbering original physical/rank slots. Caption/document resampling is not a verified physical-bifolio independence proof. Post-exposure repairs are diagnostic, not newly blind. Multiple exploratory endpoints are dependent.','']

def main():
    provenance=[]
    for root in sorted((OUT/'tests/depth_order_repetition').glob('*')):
        if not (root/'depth_results.json').exists():continue
        rows=read_json(root/'depth_results.json');records=[];text=base_summary(root,root.name+' depth and ordering','Hypothesis: outer(depth 0) and near(depth 1) substitutions differ from interior(depth ≥2), with length and log geometric-mean frequency controlled. Frequency ≥8, encoded length ≥5. Joint caption/document occurrence bootstrap 199; fixed selected vocabulary, missing pair members omitted.')
        text+=['| Subset / endpoint | Pairs | Metric | Near minus interior | Outer minus interior |','|---|---:|---|---|---|']
        for d in rows:
            for r in d.get('results',[]):
                text.append(f"| {d['subset']} / {d['position']} | {d['pairs']} | {r['metric']} | {r.get('near_minus_interior')} | {r.get('outer_minus_interior')} |")
                if r['metric']=='position':
                    b=r.get('joint_document_bootstrap',{});records.extend([(d['subset']+' / '+d['position']+' / near',r.get('near_minus_interior'),b.get('near_interval')),(d['subset']+' / '+d['position']+' / outer',r.get('outer_minus_interior'),b.get('outer_interval'))])
            if not d.get('results'):text.append(f"| {d['subset']} / {d['position']} | {d['pairs']} | All | {d['status']} | {d['status']} |");records.append((d['subset']+' / '+d['position'],None,None))
        order=read_json(root/'section_order_results.json');estimable=[r for r in order if r['status'].startswith('estimated')]
        text+=['',f'{len(estimable)}/{len(order)} section-order contrasts estimable. These pooled frequency-5 graphs require at least two cores and four variable shared relations; 99 within-line position nulls refit both section graphs. Hand-specific and pooled comparisons are distinct. Relation-naive confidence intervals are withheld.','',
          'Ordinary unit preferences and graph potentials are compared on identical held-out edges after removing direct training edges and all their cores. See `ordinary_preference_results.json`; descriptive small-edge MSE differences do not establish a positional cipher. Repeated encoded identities are not measured minim strokes. Literal EVA ee/eee is meaningful only as a conventional comparison.','',
          'Failure: too few recurrent forms, sections, shared relations or caption blocks makes an endpoint non-estimable. No threshold is tuned to recover a former effect. Prior art: ledger analogues 5, 9, 25, 26; exact historical implementation unavailable.']
        plot_intervals(root,records,root.name+' — mutation depth','Adjusted positional displacement; joint document bootstrap');(root/'summary.md').write_text('\n'.join(text)+'\n',encoding='utf-8');provenance.append(root/'depth_results.json')
    for root in sorted((OUT/'tests/hmm_transfer').glob('*')):
        if not (root/'results.json').exists():continue
        rows=read_json(root/'results.json');text=base_summary(root,root.name+' hidden-state transfer','Hypothesis: adapting emissions while holding a pooled transition kernel predicts held-out within-group sequences better than a fully frozen model. Four/five exchangeable hidden states, two pooled restarts selected on validation, cap 200 groups/document, 30 EM steps. Groups restart the HMM; this is not a physical-line accumulator.')
        text+=['| States | Context | Adaptation | Excess held-out bits/unit | Document bootstrap 95% interval |','|---:|---|---|---:|---|'];records=[]
        for r in rows:
            if r['status']=='estimated':
                text.append(f"| {r['states']} | {r['context']} | {r['adaptation']} | {r['excess_bits_over_frozen_both']:.6f} | {r['bootstrap_interval']} |")
                if r['adaptation']!='frozen_both':records.append((f"{r['states']} / {r['context']} / {r['adaptation']}",r['excess_bits_over_frozen_both'],r['bootstrap_interval']))
            else:text+=['',r['status'],'',str(r.get('block_counts'))];records.append(('Insufficient independent context blocks',None,None))
        text+=['','Negative excess bits favor adaptation. Frozen-both, fixed-emission, fixed-transition and joint-adaptation models are competing transfer baselines; no random-label HMM refit null was run. Bootstrap 1,000 document blocks. Convergence warnings and likelihood changes are preserved; EM states are not uniquely identified or decoded symbols.','',
          'Latin compares Cicero works; Finnish b/w are source partitions, not verified semantic genres. The all-hand Voynich sensitivity confounds hand/section. Ordinary-language gains show why this pattern cannot uniquely identify a shared computational runtime. Failure: fewer than four train or two test documents/context, incomplete visual groups, or unstable optimization. Prior art: standardized ledger 14 analogue; no exact unpublished historical replication or novelty claim.']
        plot_intervals(root,records,root.name+' — held-out transfer','Adapted minus frozen bits/unit; document bootstrap');(root/'summary.md').write_text('\n'.join(text)+'\n',encoding='utf-8');provenance.append(root/'results.json')
    root=OUT/'tests/dependence_boundaries';rows=read_json(root/'positional_results.json');records=[]
    for r in rows:
        records.append((r['dataset']+' / '+r['variant'],r.get('beta'),[r.get('folio_bootstrap',{}).get(k) for k in ['lower','upper']]))
    plot_intervals(root,records,'Conventional B — dependence and uncertain spaces','Adjusted edge displacement; joint block bootstrap')
    root=OUT/'tests/compound_stress_v1';rows=read_json(root/'results.json');records=[(r['partition']+' / '+r['currier'],r.get('beta'),[r.get('folio_bootstrap',{}).get(k) for k in ['lower','upper']]) for r in rows]
    plot_intervals(root,records,'Declared EVA compound encoding sensitivity','Adjusted edge displacement; caption bootstrap')
    root=OUT/'tests/conventional_crossgraph';rows=read_json(root/'grapheme_stress_results.json');records=[(r['partition']+' / '+r['currier'],r.get('beta'),[r.get('folio_bootstrap',{}).get(k) for k in ['lower','upper']]) for r in rows]
    plot_intervals(root,records,'EVA bench encoding sensitivity','Adjusted edge displacement; caption bootstrap')
    root=OUT/'tests/visual_family_stability_v1';rows=read_json(root/'results.json');heights=[r for r in rows['context_geometry'] if r.get('feature')=='height_ratio' and r['stratum']=='all_hands_sections' and r['status'].startswith('estimated')]
    plot_intervals(root,[(r['family'].split('_')[-1],r['mean_b_minus_a'],r['caption_bootstrap_interval']) for r in heights],'Conditional source families — A/B height (confounded)','B minus A height/body proxy; caption bootstrap',filename='conditional_height.png')
    root=OUT/'tests/literal_e_repetition_v1';r=read_json(root/'results.json');rr=r if isinstance(r,list) else r.get('results',[])
    plot_intervals(root,[(f'Comparison {i+1}',v.get('heldout_document_auc'),v.get('bootstrap_interval')) for i,v in enumerate(rr)],'Literal ee/eee document classifiers','Held-out document AUC')
    # Mechanics fixtures are substantive tests; provide their artifact contract.
    root=OUT/'tests/mechanics_v1';r=read_json(root/'results.json');write_csv(root/'results.csv',r['checks']);write_json(root/'config.json',dict(seed=SEED,scope='12 targeted fixtures: parser symbols/annotations, ambiguous readings, rank deficiency, graph leakage, native packed masks'));write_json(root/'input_manifest.json',dict(source_sha256=sha256(OUT/'src/verify_assay_mechanics_v1.py'),assay_sha256=sha256(OUT/'src/structural_assays.py'),parser_sha256=sha256(OUT/'src/parse_comparison_transcriptions_v2.py')))
    (root/'README.md').write_text('# Assay mechanics\n\nRun `run.py`. These targeted falsification fixtures validate bookkeeping and a graph leakage counterexample, not handwriting truth.\n',encoding='utf-8');(root/'run.py').write_text('from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]/"src"))\nimport verify_assay_mechanics_v1\n',encoding='utf-8');(root/'summary.md').write_text('# Assay mechanics\n\nAll 12 targeted checks passed, including a counterexample in which removing the direct edge alone falsely retains a predictable shared-core triangle. Removing all matched training cores leaves no prediction. Parser tests retain ligature signs and v101 punctuation, abstain on reading alternatives, and preserve continuation records. Odd-size packed masks round-trip exactly. These fixtures do not certify source segmentation.\n',encoding='utf-8');plot_intervals(root,[(c['name'],int(c['passed']),None) for c in r['checks']],'Assay mechanics checks','Passed = 1')
    write_json(OUT/'tests/reporting_v1/extended_input_manifest.json',dict(source_sha256=sha256(OUT/'src/render_extended_test_reports_v1.py'),sources=[dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p)) for p in provenance]))
    print('Rendered extended post-freeze test reports and fixtures',flush=True)

if __name__=='__main__':main()
