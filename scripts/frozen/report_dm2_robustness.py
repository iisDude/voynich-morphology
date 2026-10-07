from dm2_robustness_common import *
import html,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def fmt(v):return 'not estimable' if v is None else f'{v:.3f}'
def ci(r):return 'not estimable' if r['caption_bootstrap95'] is None else '–'.join(fmt(v) for v in r['caption_bootstrap95'])
def table(rr):
    return '\n'.join(f"| {name} | {r['n']} ({r['positive_n']}/{r['negative_n']}) | {fmt(r['AUROC'])} | {ci(r)} | {fmt(r['aspect_AUROC'])} | {'yes' if r['adequate_conditional_uncertainty'] else 'limited'} |" for name,r in rr)
def main():
    guard();verify_seal(D/'ANALYSIS_SEAL.json');records=read_json(T/'conservative_analyses.json')['analyses'];by={r['analysis_id']:r for r in records};repeat=read_json(T/'larger_repeatability.json');prediction=read_json(T/'repeat_prediction_sensitivity.json')['results'];disp=read_json(T/'DISPOSITION.json');b=by['all__pooled__binary__unrestricted'];mainrows=[('Original binary pairs',b),('Each parent once',by['all__pooled__binary__parent']),('Each caption-dyad once',by['all__pooled__binary__dyad']),('Each parent and dyad once',by['all__pooled__binary__parent_dyad']),('Extent + recovery clean',by['extent_and_recovery_clean__pooled__binary__unrestricted']),('Clean, each parent once',by['extent_and_recovery_clean__pooled__binary__parent']),('Clean, parent + dyad once',by['extent_and_recovery_clean__pooled__binary__parent_dyad']),('Clean, field-edge aids excluded',by['field_edge_sensitivity__pooled__binary__unrestricted'])];targetrows=[(c.replace('_',' '),by['all__pooled__'+c+'__unrestricted']) for c in ['same_vs_partial','partial_vs_different','partial_as_same','partial_as_different']];stratarows=[(s.replace('_',' '),by['all__'+s+'__binary__'+m]) for s in ['broad_random','aspect_matched'] for m in ['unrestricted','parent','parent_dyad']];header='| Condition | Pairs (positive/negative) | Contour64 AUROC | Caption-node 95% | Aspect AUROC | Conditional support |\n|---|---:|---:|---|---:|---|\n'
    fig,ax=plt.subplots(2,2,figsize=(14,10))
    def forest(axis,rr,title):
        for i,(name,r) in enumerate(rr):
            yy=len(rr)-i-1;color='#246b9b' if r['adequate_conditional_uncertainty'] else '#888';interval=r['caption_bootstrap95']
            if interval:axis.plot(interval,[yy,yy],color=color,lw=2)
            if r['AUROC'] is not None:axis.plot(r['AUROC'],yy,'o',color=color)
            if r['aspect_AUROC'] is not None:axis.plot(r['aspect_AUROC'],yy,'^',color='#a35c22',ms=5)
        axis.set_yticks(range(len(rr)),[name for name,r in rr][::-1]);axis.set_xlim(.1,1.02);axis.axvline(.5,color='#777',ls=':');axis.set_xlabel('Contour64 AUROC (circle); aspect baseline (triangle)');axis.set_title(title)
    forest(ax[0,0],mainrows[:6],'Fixed binary labels and conservative subsets');forest(ax[0,1],targetrows,'Changing the target: partial remains ambiguous');forest(ax[1,0],[(s.replace('_',' '),by['all__'+s+'__binary__unrestricted']) for s in ['broad_random','aspect_matched']],'Sampling strata analyzed separately');matrix=np.array(repeat['sample_agreement']['transition_weights']);im=ax[1,1].imshow(matrix,cmap='Blues',vmin=0);ax[1,1].set_xticks(range(3),['different (0)','partial (1)','same (2)']);ax[1,1].set_yticks(range(3),['different (0)','partial (1)','same (2)']);ax[1,1].set_xlabel('Anonymous repeat judgment');ax[1,1].set_ylabel('Frozen original judgment');ax[1,1].set_title('Same-AI repeat transitions (125 pairs)')
    for i in range(3):
        for j in range(3):ax[1,1].text(j,i,str(int(matrix[i,j])),ha='center',va='center',color='white' if matrix[i,j]>20 else 'black')
    fig.suptitle('Postfreeze robustness: fixed contour64, fixed source evidence',fontsize=15);fig.tight_layout();fig.savefig(G/'robustness_summary.png',dpi=150);plt.close(fig)
    category='\n'.join(f"| {name} | {repeat['category_stability'][str(k)]['retained_n']}/{repeat['category_stability'][str(k)]['original_n']} | {repeat['category_stability'][str(k)]['retention']:.1%} | {'–'.join(fmt(z) for z in repeat['category_stability'][str(k)]['conditional_caption_bootstrap95'])} |" for k,name in [(2,'same'),(1,'partial'),(0,'different')]);sample=repeat['sample_agreement'];weighted=repeat['original_category_reweighted_agreement'];rerows=[(a['label'].replace('_',' '),a['unweighted']) for a in prediction];greedy='\n'.join(f"| {r['dependence']} | {r['n']} | {' / '.join(fmt(x) for x in r['greedy_selection_sensitivity']['AUROC_min_median_max'])} |" for r in records if r['source_filter']=='all' and r['stratum']=='pooled' and r['contrast']=='binary' and r['dependence']!='unrestricted');recovery=by['extent_and_recovery_clean__pooled__binary__unrestricted'];originalall=next(r for r in records if r['analysis_id']=='all__pooled__partial_as_same__unrestricted');cleanall=by['extent_and_recovery_clean__pooled__partial_as_same__unrestricted']
    report=f'''# Direct Morphology Trial2 — postfreeze robustness investigation v1

**Classification: {disp['classification']}.** A substantial same/different morphology signal remains. Its strongest interpretation depends on the binary target, the sampling mixture and a limited set of repeated source parents. Conservative disjoint-parent analysis loses precision and the pooled advantage over aspect alone. Flagged raster recovery does not explain away the signal: removing those cases strengthens the original binary result.

Direct Morphology Trial2 remains immutable and supported within its registered sample. This investigation is a separate sensitivity analysis, **not another validation pass**. It uses only frozen contour64, frozen source judgments and the original360 reviewed pairs. No unused evaluation pairs, new pages, structural classes or downstream information are opened. SDF64, contour32/128 and learned representations are not substituted.

## Dependence and ambiguous recovery

{header}{table(mainrows)}

Original binary eligibility already excludes all27 source-unknown whole extents, and the frozen extent/contact flags exclude **zero additional evaluated pairs**. Extent-clean unrestricted results therefore equal the original result. Recovery-clean excludes missing, split or merged contrast6/12 correspondence, using existing flags and no new numeric morphology cutoff.61/211 binary pairs are removed:8 same and53 different. Across all360 reviewed pairs,99 are removed, leaving261. Connected-compound description alone does not discard a source-resolved whole parent. Field-edge exclusion is a separate sensitivity to a location aid, not a retrospective claim of unresolved physical extent.

Each-parent-once selection gives63 binary pairs,14 same and49 different, with126 distinct parents. Its contour64 AUROC0.805 has conditional95%0.496–1.000 and ties aspect-only AUROC0.805. This does not establish a disappearance of morphology discrimination; it removes the previously precise evidence for its superiority to aspect on this particular subset. Shared captions and source-adjudicator bias remain.

The28-parent-and-dyad-constrained selection has only3 same pairs and3,793/5,000 valid resamples. Its0.840 point estimate is descriptive. Broad-random dyad selection is even sparser; a0.370 score from one positive is **not treated as an adequately supported reversal**. Perfect1.000 scores and degenerate1.000–1.000 empirical intervals in other small selections likewise cannot establish perfect population discrimination. Resampling cannot introduce errors absent from a tiny selected sample.

Maximum-cardinality selections use parent≤1 and/or caption-dyad≤1 constraints, with seeded secondary priorities after count is maximized. Same/different category balance and distances are never objectives. All eligible dyads can be represented once where shown; some resulting category support is weak. The point estimates are conditional on the stored graph selections.

**Identical filtered populations can have different matched subsets.** Each analysis has its preregistered seed: extent-clean and original pools are identical, while recovery-clean and combined-clean pools are identical among eligible pairs. Differences between their matched scores reflect tie-breaking, not source exclusion. Reported unrestricted filter comparisons avoid that confounding. No seed was chosen to rescue a score.

Fifty additional seeded greedy admissible selections per binary constrained condition expose selection variability. They are supplementary to maximum-cardinality primary selections and may retain fewer pairs. Their min/median/max AUROCs are **selection ranges, not confidence intervals**:

| Constraint | Primary maximal pairs | Greedy AUROC min / median / max |
|---|---:|---|
{greedy}

The strong variation among dyad selections shows why one favorable subset cannot support a universal robustness claim. All50 selections and category counts are preserved.

## Target sensitivity and the partial boundary

{header}{table(targetrows)}

Contour64 separates **same from partial** reasonably well(AUROC0.824), while **partial from different** is weaker(AUROC0.623). Reclassifying every partial as same lowers pooled AUROC to0.672, a0.207 drop. Reclassifying every partial as different yields0.853. The0.672–0.853 range is an envelope of the **two uniform recoding scenarios**; it is not a sharp bound over all possible mixed assignments, a statement of true labels or permission to overwrite partial judgments.

Both scenarios change the binary question. A related organization is not established as the same whole organization. These calculations explain which distinction the frozen contour signal supports, without selecting a preferred recoding. Recovery cleaning leaves this asymmetry: same/partial AUROC0.886, partial/different0.626, partial-as-same0.688 and partial-as-different0.915. Disjoint-parent versions and both sampling strata are retained among all108 conditions.

## Sampling mixture

{header}{table(stratarows)}

The broad-random subset gives contour0.798 versus aspect0.812; its10 same judgments provide limited precision. The aspect-matched subset gives contour0.907 versus aspect0.655, with25 same judgments. After parent-disjoint selection, aspect-matched contour remains0.855 versus aspect0.602. Broad-random disjoint estimates are less precise and do not establish contour superiority. The registered pooled mixture supplies a real conditional result, but its advantage over aspect is concentrated in geometric hard comparisons rather than demonstrated uniformly across both strata.

## Larger anonymous same-adjudicator repeat

The sealed125-pair sample contains all35 original same judgments, plus seeded uniform45 partial and45 different judgments. It is6.25 times the earlier20-pair repeat. New IDs, shuffled sides and randomized order hid original ratings/categories, source identities, strata and contour scores during nativeRGB review. Sealed subset preparation intervened. Prior image exposure and same-session conversational memory persist. This is **same-AI repeatability**, not independent human or inter-rater validation.

Exact agreement is **101/125(80.8%)**, conditional caption-node95%70.4–90.0%. Linear ordinal agreement, defined1−|original−repeat|/2, is **90.4%**; quadratic agreement is95.2%. Chance-corrected kappas are0.708 unweighted,0.772 linear and0.841 quadratic. All24 disagreements are adjacent:15 partial↔different,8 same→partial and1 partial→same. No direct same↔different flips occurred. The unstable boundary therefore includes both edges of the partial category.

| Original category | Retained | Retention | Conditional caption-node95% |
|---|---:|---:|---|
{category}

Same retention is27/35(77.1%), partial36/45(80.0%), and different38/45(84.4%). Precision is limited by eight captions and the35 available same cases. Because same pairs are oversampled, original-category-frequency reweighted exact agreement is81.9%, linear agreement90.9%; these accompany the raw balanced-repeat sample rather than replacing it. Reweighting addresses original-category sampling proportions, not adjudicator bias or a fresh manuscript population.

Rerated binary comparisons are separately recorded:

{header}{table(rerows)}

Original ratings on this selected repeat corpus yield80 binary pairs/AUROC0.888; repeat ratings yield74/AUROC0.911. Their memberships differ because partials enter/leave the binary analysis. The65 unchanged binary pairs give0.907, a diagnostic conditioned on agreement. Strong binary discrimination persists after this repeat, despite category instability. None of these scores overwrites the frozen211-pair evaluation or constitutes independent confirmation. Original-category-frequency weighted versions are also preserved.

## Conditional uncertainty and reproducibility

All108 conditions use the same preregistered5,000 draws of the original eight-caption node bootstrap, with pair weights=count(left caption)×count(right caption); paired aspect deltas use identical weights. A weighted Mann–Whitney implementation gives half credit to distance ties and agrees with independent sklearn checks. Parent reuse is removed in constrained source samples; caption resampling still weights caption-shared observations. These are conditional empirical intervals, not complete uncertainty over source truth, rating bias or alternative matching choices.

Both categories,≥5 pairs/category,≥3 caption endpoints/category,≥4 captions overall and≥4,500 valid draws are required for the registered descriptive-support flag. This robustness flag is **not Trial2's validation criterion**. Every available point score and conditional interval is shown, including weaker cases. Single-category or zero-weight comparisons remain not estimable. Sparse subsets are not rescued by another metric, seed, label interpretation or sample substitution.

The5,000-draw pooled robustness interval0.762–1.000 differs slightly from Trial2's sealed2,000-draw0.767–1.000 interval because the registered robustness seed and draw count differ. The frozen point metric and its original interval remain unchanged.

Source filters, maximum-cardinality solutions, selected pair IDs,50-seed alternatives, all bootstrap counts, anonymous repeat ratings, category transitions and metric outputs are frozen in the separate package. Deterministic replay checks all108 conditions, constraint limits and sampling; independent weighted AUROC/kappa calculations verify numerical implementation. Earlier freezes, the full Trial2 manifest and its prior postfreeze evidence are checked without editing them. No source/raster/representation decision is retuned.

## Disposition

The pre-outcome robustness rubric identifies sensitivity to sampling mixture, partial recoding and same-category repeat retention. The core same/different result is **not classified as unsupported under conservative analysis**: recovery-clean and disjoint-parent subsets retain substantial signal. Exact graph selection and reduced information budgets limit claims of uniform dependence-free precision. The defensible statement is that frozen contour64 discriminates selected whole-organization same/different judgments, while broader “related morphology” discrimination and unique source-rater labeling remain less stable.

This investigates visible morphology only. It establishes no letters, graphemes, writing identities, allographs, boundaries, sequences, physical stroke order, pen lifts or meaning. Conventional transcription, Currier, position, sequence and decipherment analyses remain sealed.

[All-condition dashboard](28_direct_morphology_trial2_robustness_dashboard.html) · [Separate protocol](../data/observations/direct_morphology_trial2_robustness_v1/PLAN.json) · [All108 analyses](../tests/direct_morphology_trial2_robustness_v1/conservative_analyses.json) · [Repeat judgments and transitions](../tests/direct_morphology_trial2_robustness_v1/larger_repeatability.json) · [Separate freeze](../data/observations/direct_morphology_trial2_robustness_v1/FREEZE_MANIFEST.json) · [Postfreeze integrity](../tests/direct_morphology_trial2_robustness_v1_postfreeze/INTEGRITY.json)

![Robustness summary](../figures/direct_morphology_trial2_robustness_v1/robustness_summary.png)
'''
    reportpath=OUT/'reports/27_direct_morphology_trial2_robustness.md';assert not reportpath.exists();reportpath.write_text(report,encoding='utf-8')
    dashboard_records=[{k:r[k] for k in ['analysis_id','source_filter','stratum','contrast','dependence','n','positive_n','negative_n','unique_parent_n','maximum_parent_degree','maximum_dyad_degree','AUROC','aspect_AUROC','caption_bootstrap95','paired_delta_bootstrap95','valid_bootstrap_n','adequate_conditional_uncertainty','pair_ids']} for r in records];rows=''.join(f"<tr data-source='{r['source_filter']}' data-stratum='{r['stratum']}' data-contrast='{r['contrast']}' data-dependence='{r['dependence']}'><td>{r['source_filter']}</td><td>{r['stratum']}</td><td>{r['contrast']}</td><td>{r['dependence']}</td><td>{r['n']} ({r['positive_n']}/{r['negative_n']})</td><td>{fmt(r['AUROC'])}</td><td>{ci(r)}</td><td>{fmt(r['aspect_AUROC'])}</td><td>{r['valid_bootstrap_n']}/5000</td><td>{'conditional' if r['adequate_conditional_uncertainty'] else 'limited'}</td><td><details><summary>IDs</summary>{' '.join(r['pair_ids'])}</details></td></tr>" for r in records);controls=''.join(f"<label>{name} <select data-key='{name}'><option value=''>All</option>"+''.join(f"<option>{html.escape(v)}</option>" for v in sorted({r[field] for r in records}))+"</select></label>" for name,field in [('source','source_filter'),('stratum','stratum'),('contrast','contrast'),('dependence','dependence')]);repeatrows=''.join(f"<tr><td>{r['repeat_id']}</td><td>{r['original_pair_id']}</td><td>{r['original_rating']}</td><td>{r['repeat_rating']}</td><td>{r['contour64']:.4f}</td></tr>" for r in repeat['pairs']);galleries=''.join(f"<details><summary>Anonymous source sheet{i:02d}</summary><img src='../figures/direct_morphology_trial2_robustness_v1/anonymous_repeat_{i:02d}.png'></details>" for i in range(1,12))
    page="""<!doctype html><meta charset='utf-8'><title>Frozen Trial2 robustness dashboard</title><style>body{font:15px system-ui;margin:24px;color:#18242b}h1{font-size:25px}label{display:inline-block;margin:8px}select{padding:6px}table{border-collapse:collapse;width:100%}th,td{padding:7px;text-align:left;border-bottom:1px solid #ddd}thead{position:sticky;top:0;background:#e9f0f4}tr:nth-child(even){background:#f6f8fa}details{max-width:480px}img{max-width:100%}.overview{max-width:1200px}p{max-width:1100px}</style><h1>Postfreeze contour64 robustness</h1><p><b>Sensitive to one or more evaluation assumptions.</b> Frozen Trial2 remains unchanged. These are source-conditioned sensitivity analyses, not a new validation pass. Only contour64 is evaluated; aspect is a baseline. Scores for tiny or perfectly separated subsets can have misleadingly narrow empirical intervals. Filter and inspect counts/support together.</p><img class='overview' src='../figures/direct_morphology_trial2_robustness_v1/robustness_summary.png'><h2>All108 preselected conditions</h2>"""+controls+"<p id='count'></p><table id='analyses'><thead><tr><th>Source filter</th><th>Stratum</th><th>Target</th><th>Constraint</th><th>n (+/−)</th><th>Contour64</th><th>Conditional95%</th><th>Aspect</th><th>Valid draws</th><th>Support</th><th>Selected pairs</th></tr></thead><tbody>"+rows+"</tbody></table><h2>Repeat audit — labels opened after source review seal</h2><p>These125 nativeRGB pairs were reviewed under anonymous J IDs with prior labels and scores hidden. The following key is disclosed only after the repeat ratings were sealed. Source sampling is35 original same,45 partial and45 different. Same-AI memory carryover persists; this is not independent human validation.</p><table><thead><tr><th>Anonymous ID</th><th>Original pair</th><th>Frozen rating</th><th>Repeat rating</th><th>Contour64 distance</th></tr></thead><tbody>"+repeatrows+"</tbody></table>"+galleries+"<script>function filter(){let controls=[...document.querySelectorAll('select[data-key]')];let n=0;document.querySelectorAll('#analyses tbody tr').forEach(row=>{let ok=controls.every(c=>!c.value||row.dataset[c.dataset.key]===c.value);row.hidden=!ok;if(ok)n++});document.getElementById('count').textContent=n+' /108 conditions shown'}document.querySelectorAll('select').forEach(c=>c.addEventListener('change',filter));filter();</script>"
    dashboard=OUT/'reports/28_direct_morphology_trial2_robustness_dashboard.html';assert not dashboard.exists();dashboard.write_text(page,encoding='utf-8');save(T/'REPORT_CHECKS.json',dict(report_table_rows=len(records),repeat_rows=len(repeat['pairs']),no_modified_prior_reports=True,figures_are_direct_metric_summaries_not_embeddings=True,scope='Dashboard keys expose prior/repeat ratings only after repeat seal.'))
    print('Separate robustness report and108-condition dashboard written',flush=True)
if __name__=='__main__':main()
