"""Readable result tables and scientific plots; does not change test inputs."""
from common import OUT,read_json,write_csv,write_json,sha256
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

NAMES=['ZL_EVA','RF','v101','visual_fine','visual_merged','visual_factored','visual_medium','Finnish','Turkish','Latin','visual_v11_fine','visual_v11_merged','visual_v11_factored','visual_v11_medium']

def finite(x):return x is not None and np.isfinite(x)

def main():
    aggregate=[]
    for name in NAMES:
        root=OUT/'tests/structural'/name
        if not (root/'sequence_results.json').exists():continue
        mp=read_json(root/'minimal_pair_results.json');graphs=read_json(root/'directional_graph_results.json');seq=read_json(root/'sequence_results.json');flat=[]
        for r in mp:
            boot=r.get('folio_bootstrap',{});flat.append(dict(test='minimal_pair',subset=r['subset'],position=r['position'],variant=r.get('specification',f'freq{r["minimum_frequency"]}_edge{r["edge_width"]}_minlen{r["length_min"]}'),status=r['status'],n=r['pairs'],effect=r.get('beta'),ci_low=boot.get('lower'),ci_high=boot.get('upper'),null_p=r.get('within_line_null',{}).get('two_sided_p')))
        for r in graphs:
            for endpoint,key in [('reproducibility','heldout_reproducibility'),('alternate_prediction','direct_edge_removed_prediction')]:
                q=r[key];flat.append(dict(test=endpoint,subset=r['subset'],position=r['position'],variant=f'{r["side"]}_freq{r["minimum_frequency"]}',status='estimated' if q['pearson'] is not None else 'not_estimable: inadequate shared relations',n=q['n'],effect=q['pearson'],ci_low=None,ci_high=None,null_p=r[endpoint+'_null']['p']))
            flat.append(dict(test='triangle_closure',subset=r['subset'],position=r['position'],variant=f'{r["side"]}_freq{r["minimum_frequency"]}',status='estimated' if r['context_disjoint_triangles'] else 'not_estimable: no context-disjoint triangles',n=r['context_disjoint_triangles'],effect=r['median_normalized_triangle_closure'],ci_low=None,ci_high=None,null_p=r['triangle_closure_null']['p']))
        write_csv(root/'results.csv',flat);fig=root/'figures';fig.mkdir(parents=True,exist_ok=True)
        primary=[r for r in mp if r.get('minimum_frequency')==8 and r.get('edge_width')==2 and r.get('length_min')==5 and not r.get('specification')]
        plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
        chart,ax=plt.subplots(figsize=(8,max(3,len(primary)*.4)))
        for y,r in enumerate(primary):
            beta=r.get('beta');boot=r.get('folio_bootstrap',{});label=r['subset']+' | '+r['position']
            if finite(beta):
                ax.plot(beta,y,'o',color='#155e75')
                if finite(boot.get('lower')) and finite(boot.get('upper')):ax.plot([boot['lower'],boot['upper']],[y,y],color='#155e75')
            else:ax.text(.02,y,f"Not estimable ({r['pairs']} pairs)",transform=ax.get_yaxis_transform(),va='center')
        ax.set_yticks(range(len(primary)),[r['subset']+' | '+r['position'] for r in primary]);ax.set_ylim(-.7,len(primary)-.3);ax.axvline(0,color='#888',lw=.8);ax.set_xlabel('Adjusted edge minus interior displacement; caption bootstrap interval');ax.set_title(name+' — frequency 8, two-unit edge, length ≥5');chart.tight_layout();chart.savefig(fig/'primary_position.png',dpi=160);plt.close(chart)
        chart,axes=plt.subplots(1,2,figsize=(9,4))
        for ax,side in zip(axes,['left','right']):
            p=root/f'prediction_normalized_group_rank_{side}_freq5.json';rr=read_json(p)
            if rr:
                ax.scatter([r['heldout_direct_delta'] for r in rr],[r['alternate_training_prediction'] for r in rr],label='Alternate graph',s=25)
                baseline=[r for r in rr if r.get('ordinary_unit_preference_prediction') is not None]
                if baseline:ax.scatter([r['heldout_direct_delta'] for r in baseline],[r['ordinary_unit_preference_prediction'] for r in baseline],label='Ordinary preference',marker='x',s=25)
                ax.legend(fontsize=8)
            else:ax.text(.5,.5,'No qualifying alternate predictions',ha='center',transform=ax.transAxes)
            ax.set_title(side+' edge; n='+str(len(rr)));ax.axhline(0,color='#aaa',lw=.5);ax.axvline(0,color='#aaa',lw=.5);ax.set_xlabel('Held-out direct delta');ax.set_ylabel('Training prediction')
        chart.suptitle(name+' — direct edge AND its matched cores excluded');chart.tight_layout();chart.savefig(fig/'heldout_predictions.png',dpi=160);plt.close(chart)
        lines=[f'# {name}: structural reproduction','',f"Primary tests use {read_json(root/'input_manifest.json')['rows']:,} admitted rows/groups as defined in the source manifest; groups are not presumed words.",'','| Subset / position | Qualifying pairs | Edge effect | Caption bootstrap 95% interval |','|---|---:|---:|---|']
        for r in primary:
            beta=r.get('beta');b=r.get('folio_bootstrap',{});interval=f"[{b['lower']:.5f}, {b['upper']:.5f}]" if finite(b.get('lower')) else 'Not estimable';lines.append(f"| {r['subset']} / {r['position']} | {r['pairs']} | {beta:.5f}"+' | '+interval+' |' if finite(beta) else f"| {r['subset']} / {r['position']} | {r['pairs']} | Not estimable | {interval} |")
        lines.extend(['','Frequency 8, edge width 2, minimum length 5 are primary. Frequency 5/10/12, one-unit edges, and legacy short forms are retained sensitivity specifications. Effects adjust for group length and log geometric-mean pair frequency. Caption/document occurrence bootstrap, connected-family inference where supported, leave-one-caption deletion and within-line slot shuffles have separate interpretations. Normalized ordinal rank is separate from measured native pixel x; conventional coordinates remain unknown.', '', 'Graphs report equal-core signed deltas, independent caption half-splits, train/test reproducibility, alternate predictions after removing the direct edge and every one of its training cores, and triangles with disjoint core buckets. Shared edges/cores are dependent; relation-naive confidence intervals are not supplied. Source masks and group boundaries are unvalidated, and known extraction failures prevent treating visual results as recovered writing-unit evidence.', '', 'Sequence tests retain gap resets and increasing/decreasing physical x hypotheses. The ordinal-rank running-state outcome is already exactly predictable from its rank baseline and is therefore not independently estimable. Pixel running-state tests use an additional trained state predictor with held-out caption losses and shuffled increments.', '', 'Null draws (99 graph/sequence; 199 primary pair bootstraps/shuffles) give coarse Monte Carlo resolution. Threshold sweeps are not independent confirmations. Exact undocumented historical settings are not claimed. Prior positional analysis predates this investigation; see the primary-source collision report.', '', 'Figures: `figures/primary_position.png`, `figures/heldout_predictions.png`. Full machine-readable results retain all non-estimable cases.'])
        (root/'summary.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
        for r in primary:
            if r['subset']==('all' if name in ['Finnish','Turkish','Latin'] else 'B') and r['position']=='normalized_group_rank':aggregate.append(dict(dataset=name,pairs=r['pairs'],beta=r.get('beta'),lower=r.get('folio_bootstrap',{}).get('lower'),upper=r.get('folio_bootstrap',{}).get('upper')))
        cr=OUT/'tests/context'/name
        if (cr/'results.json').exists():
            c=read_json(cr/'results.json');figure=cr/'figures';figure.mkdir(parents=True,exist_ok=True);chart,axes=plt.subplots(1,2,figsize=(9,3.8));w=c['wrappers'];compression=c['compression']
            if w.get('status')=='estimated':
                b=w['bootstrap_interval'];axes[0].plot(b,[0,0],lw=2);axes[0].plot(w['equal_document_wrapper_excess_bits_over_core'],0,'o');axes[0].axvline(0,color='#888');axes[0].set_yticks([])
            else:axes[0].text(.5,.5,w['status'],ha='center',wrap=True,transform=axes[0].transAxes)
            axes[0].set_xlabel('Wrapper minus core context loss (bits/group)');axes[0].set_title('Held-out equal-document loss')
            if compression.get('status')=='estimated':
                keys=['baseline_bits_per_original_unit','deleted_bits_per_original_unit','matched_null_mean'];axes[1].bar(['Unchanged','Declared deletion','Matched deletion'],[compression[k] for k in keys],color=['#777','#155e75','#a16207']);axes[1].set_ylabel('Bits per original encoded unit')
            else:axes[1].text(.5,.5,compression['status'],ha='center',wrap=True,transform=axes[1].transAxes)
            axes[1].set_title('Byte codec; approximate frequency controls');chart.suptitle(name);chart.tight_layout();chart.savefig(figure/'wrapper_and_deletion.png',dpi=160);plt.close(chart)
    report=OUT/'tests/reporting_v1';report.mkdir(parents=True,exist_ok=True);write_csv(report/'primary_comparison.csv',aggregate)
    chart,ax=plt.subplots(figsize=(9,5))
    for i,r in enumerate(aggregate):
        if finite(r['beta']):
            ax.plot(r['beta'],i,'o',color='#155e75');ax.plot([r['lower'],r['upper']],[i,i],color='#155e75')
        else:ax.text(.01,i,'Not estimable: '+str(r['pairs'])+' qualifying pairs',va='center')
    ax.axvline(0,color='#888');ax.set_yticks(range(len(aggregate)),[r['dataset'] for r in aggregate]);ax.set_xlabel('Adjusted edge minus interior difference in mean ordinal position');ax.set_title('Conventional B, frozen visual B and natural-language controls\nFrequency ≥8, length ≥5; document/caption bootstrap');chart.tight_layout();chart.savefig(report/'primary_comparison.png',dpi=180);plt.close(chart)
    write_json(report/'input_manifest.json',dict(sources=[dict(dataset=n,path=f'tests/structural/{n}/minimal_pair_results.json',sha256=sha256(OUT/f'tests/structural/{n}/minimal_pair_results.json')) for n in NAMES if (OUT/f'tests/structural/{n}/minimal_pair_results.json').exists()],source_sha256=sha256(OUT/'src/render_reproduction_reports_v1.py')))
    print('Rendered',len(aggregate),'dataset summaries and comparisons',flush=True)

if __name__=='__main__':main()
