from common import OUT,read_json,write_json,sha256
from neutral_feature_trial_v1 import D,T,G,DEFS,verify
from datetime import datetime,timezone
from pathlib import Path
from html import escape
import numpy as np,cv2,re
from PIL import Image

def main():
    if (D/'EVIDENCE_SEAL.json').exists():raise RuntimeError('Trial sealed')
    verify();profiles=read_json(D/'parent_feature_profiles.json')['parents'];lookup={r['parent_id']:r for r in profiles};key={r['audit_id']:r for r in read_json(D/'RGB_AUDIT_HIDDEN_KEY.json')};obs=read_json(D/'RGB_source_feature_decisions.json')['observations'];comparisons=[]
    for r in obs:
        p=lookup[key[r['audit_id']]['parent_id']];c=p['features']['significant_cavity_count'];comparisons.append(dict(audit_id=r['audit_id'],parent_id=p['parent_id'],source_cavity_count=r['source_visible_cavities'],raster_primary_count=c['primary'],raster_status=c['status'],primary_count_agrees=r['source_visible_cavities'] is not None and r['source_visible_cavities']==c['primary'],semantic_uncertainty='Source-visible cavity counts lack the raster significance-area cutoff; differences need not be model/source-adjudicator error.',source_horizontal_observation=r['principal_horizontal_span'],raster_horizontal_run=p['features']['horizontal_run_fraction'],source_photography=r['photography']))
    resolved=[r for r in comparisons if r['source_cavity_count'] is not None];stable=[r for r in resolved if r['raster_status']=='stable'];unresolved=[r for r in comparisons if r['source_cavity_count'] is None]
    audit=dict(created_at_utc=datetime.now(timezone.utc).isoformat(),observations=comparisons,resolved_cavity_counts=len(resolved),primary_count_agreement=sum(r['primary_count_agrees'] for r in resolved),stable_resolved_cavity_counts=len(stable),stable_count_agreement=sum(r['primary_count_agrees'] for r in stable),source_unknown_cavity_cases=len(unresolved),numerically_stable_source_unknown=sum(r['raster_status']=='stable' for r in unresolved),same_adjudicator_only=True,independent_feature_accuracy_not_established=True)
    write_json(T/'source_feature_audit.json',audit)
    # Preserve raw repeatability measurements. Attach feature-specific semantic
    # caution instead of re-fitting the numeric descriptor to visual judgments.
    qualified=[];byobs={r['parent_id']:r for r in comparisons}
    for p in profiles:
        source=byobs.get(p['parent_id']);caution='not_individually_source_audited' if source is None else 'source_photographic_unknown' if source['source_cavity_count'] is None else 'source_definition_discordance' if not source['primary_count_agrees'] else 'source_coarse_count_agrees'
        qualified.append(dict(parent_id=p['parent_id'],source_state=p['source_state'],native_source=p['native_source'],native_bbox=p['native_bbox'],usable_partial_numeric_profile=p['usable_partial_profile'],cavity_semantic_status=caution,features={k:dict(primary=v['primary'],range=v['range'],numerical_status=v['status'],source_semantic_status=caution if DEFS[k][0]=='cavity' else 'raster_geometry_measurement_not_stroke_or_unit_claim') for k,v in p['features'].items()}))
    write_json(D/'source_qualified_profiles.json',qualified);write_json(T/'variant_value_key.json',dict(values_in_order=['native_contrast9','native_contrast6','native_contrast12','native_shear_plus0.04','native_shear_minus0.04','body_proxy_times0.90','body_proxy_times1.10'],native_parent_alternatives='Largest overlapping whole-parent raster; split/merge/IoU uncertainty retained.'))
    # Diagnose the discrepant count without changing the significant-hole rule.
    pid=next((r['parent_id'] for r in resolved if not r['primary_count_agrees']),None)
    if pid:
        source={r['parent_id']:r for r in read_json(OUT/'data/observations/structural_inventory_v6_development/discovery_parents.json')}[pid];mask=(np.asarray(Image.open(OUT/source['mask_path']))>0).astype(np.uint8);n,lab,stats,cent=cv2.connectedComponentsWithStats(1-np.pad(mask,1),8);areas=[int(s[4]) for s in stats[2:]];write_json(T/'cavity_definition_discrepancy.json',dict(parent_id=pid,enclosed_primary_background_areas_px=areas,significant_area_cutoff=max(8,int(mask.sum())*.012),source_count=byobs[pid]['source_cavity_count'],raster_count=byobs[pid]['raster_primary_count'],interpretation='Definitions differ: small or threshold-open light spaces may be visible to an adjudicator but absent from significant raster cavities. No cutoff retuning.'))
    s=read_json(T/'feature_repeatability.json');keys=['log_aspect','ink_density','ink_centroid_x','ink_centroid_y','significant_cavity_count','cavity_upper_count','skeleton_endpoint_count','skeleton_branch_cluster_count','horizontal_run_fraction','vertical_run_fraction'];labels=['Aspect','Ink density','Ink centroid x','Ink centroid y','Significant cavities','Upper cavity count','Skeleton endpoints','Skeleton branches','Horizontal run','Vertical run']
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(10,6));y=np.arange(len(keys));width=.35
    for off,name,color,label in [(-width/2,'V5_UNK','#bd733b','V5 UNK (327 parents)'),(width/2,'validation','#367986','Reused validation (66 writing parents)')]:
        group=s['strata'][name];values=[group['by_feature'][k]['stable']/group['parents']*100 for k in keys];ax.barh(y+off,values,width,color=color,label=label)
    ax.set_yticks(y,labels);ax.invert_yaxis();ax.set_xlim(0,100);ax.set_xlabel('Descriptor stable across registered perturbations (%)');ax.set_title('Repeatable geometry and distribution; unstable skeleton counts');ax.legend(loc='lower left',bbox_to_anchor=(0,-.25),ncols=2);ax.grid(axis='x',alpha=.25);ax.set_axisbelow(True);fig.tight_layout();fig.savefig(G/'feature_repeatability.png',dpi=160,bbox_inches='tight');plt.close(fig)
    example=next(p for p in profiles if p['parent_id']=='B001_O121');write_json(T/'example_partial_profile.json',dict(parent_id=example['parent_id'],native_source=example['native_source'],native_bbox=example['native_bbox'],profile={k:example['features'][k] for k in ['log_aspect','ink_density','ink_centroid_x','ink_centroid_y','significant_cavity_count','cavity_centroid_y','skeleton_branch_cluster_count','horizontal_run_fraction','vertical_run_fraction']},interpretation='One source-traceable vector of properties, not a decomposition into internal writing units.'))
    md=f'''# Neutral structural feature profiles: feasibility trial1

**Yes, partially. Confirmed writing parents can carry reproducible combinations of neutral numeric properties even while remaining unassigned to a discrete class.** This trial supports partial measurement profiles, not a validated compositional notation or recovered grapheme system. Its reused-validation support gate failed:45/57 source-resolved parents (78.9%) versus the registered80% minimum. V3–V6 remain immutable; no sequences or downstream tests were opened.

The [protocol](../data/observations/neutral_feature_trial_v1/PLAN.json) fixed34 descriptors, tolerances and a usable-profile criterion before results. It used638 V5 confirmed writing parents and66 confirmed parents from the three V6 validation captions. Those images and source decisions were previously exposed; this is a reserved region generalization check for a new feature specification, not globally fresh imagery or independent source annotation.

## Representation

A parent is an uncertain feature vector: geometry + ink distribution + raster cavity/connectivity + graph/run measurements. It retains its whole source parent, native coordinates, primary values, perturbation ranges, and `stable`, `unknown_variant_sensitive`, `unknown_presence` or `not_applicable` states. Cavity-centroid absence is not a coordinate value of zero. Source contact/photographic ambiguity remains separate from numeric stability.

Features include relative aspect, ink density, ink centroid/spread, thirds and3×3 ink fractions, enclosed negative-space count/position/area, connected-component count, skeleton endpoint/branch counts and longest horizontal/vertical ink runs. These are neutral measurements. Skeleton endpoints are not pen lifts; branches are not graphemes; a horizontal run is not automatically a bench/frame. Features can coexist in one vector without asserting detachable subunits or stroke order.

Contrast6/9/12, native±0.04 slant and body-proxy±10% perturbations test operational repeatability. Counts require exact equality; continuous features have preregistered range tolerances. A usable partial profile requires resolved source parent evidence, whole-parent raster correspondence, at least eight stable applicable descriptors, and geometry/distribution plus a third substantive family. Connectivity count alone does not satisfy the third family. Correlated ink fractions are not independent pieces of evidence.

## Coverage

| Corpus | Usable partial profiles | Source-resolved denominator | Rate |
|---|---:|---:|---:|
| V5 confirmed writing | 513 | 589 | 87.1% |
| V5 parents with existing class | 300 | 301 | 99.7% |
| V5 class-unknown parents | 213 | 288 | 74.0% |
| Reused validation regions | 45 | 57 | 78.9% |

Among all327 V5 unknowns,213 (65.1%) have a usable numeric profile after source/correspondence exclusions. The remaining cases retain partial descriptor measurements plus unknown/source-hypothesis flags; they are not forced into profile usability. Forty-one source contacts and eight insufficient-morphology V5 parents remain outside the resolved-parent denominator. Seven contacts and two insufficient-evidence validation parents likewise remain excluded.

Validation-caption rates are12/15 (caption16),16/22 (47),17/20 (94). Each passes the70% per-caption minimum; the pooled80% minimum fails. Caption-bootstrap95% intervals: discovery84.4–89.7%, validation72.7–85.0%. These do not include adjudicator error. No tolerance was relaxed after observing the failure.

## Which properties survive

![Feature perturbation repeatability](../figures/neutral_feature_trial_v1/feature_repeatability.png)

For the327 V5 unknowns, aspect is stable in249, density in288, ink centroid x/y in309/318, significant raster cavity count in245, and horizontal/vertical runs in226/240. Skeleton endpoints and branch clusters are stable in only54/57. Median stable descriptor count is28/34, but many distribution descriptors are correlated.

Height/body and width/body fail the registered range tolerance in every parent **by construction**: a±10% body-proxy interval alone spans log(1.1/0.9)≈0.2007, exceeding the0.18 limit. This is normalization-reference uncertainty, not universal inability to measure native height/width. Native coordinate envelopes remain available; normalized dimensions are retained as intervals. The tolerance and perturbation were not adjusted to improve coverage. A complete34-feature point vector is therefore unsupported.

## Source-visible meaning versus raster repeatability

A preregistered22-parent anonymous RGB audit hid previous numeric values and class suggestions. It sampled an assigned and unknown resolved parent in each V5 caption plus two resolved validation parents per caption. This is the same AI adjudicator with prior photograph familiarity, not independent human-rater validation.

Seventeen source-visible cavity counts were resolved: primary raster counts agree in16/17. Among fifteen numerically stable resolved counts, fourteen agree. Five photographic cavity counts remain unresolved, and three of those still have stable numeric raster counts. **Repeatable numbers can describe a thresholded image without establishing the corresponding source-visible feature.** Cavity statuses in [source-qualified profiles](../data/observations/neutral_feature_trial_v1/source_qualified_profiles.json) therefore retain source uncertainty and definition discordance instead of promoting raster stability into visual truth.

The discrepant B006_O144 has small/enclosed background details affected by the significant-area definition. Source-visible cavities and significant raster cavities are not identical quantities; the cutoff was not retuned. The principal-horizontal-span audit remains descriptive because a straight-row run ratio is not equivalent to a qualitative bridge/frame judgment.

## What this supports

The [B001_O121 example](../tests/neutral_feature_trial_v1/example_partial_profile.json) remains class-unknown but carries stable aspect, density, ink-location, significant-cavity and run measurements with source coordinates. Its single significant cavity has vertical centroid0.677–0.681 of the parent height from the top; source RGB also supports one cavity. Skeleton branch count varies3–4 and remains unknown. A neutral description can retain the lower cavity and other reproducible properties while abstaining on branch count. This demonstrates the advantage of feature-specific uncertainty: one unstable count need not erase the rest of the parent description.

This representation can support source-traceable similarity research and uncertainty diagnosis. It has not established reusable internal components, source-certified feature truth for every parent, unique reconstruction of the shape, an alphabet, complete row membership, or sequence recurrence. The same feature vector can describe several different forms. Source-window ownership and raster-correspondence problems remain limiting cases.

The trial is an evidence package, **not a V7 segmentation freeze**. Existing writing membership, V3 classes and V6 inventory stay unchanged. Neither Currier, native pixel-x, EVA/RF/v101, minimal-pair nor decipherment tests were reopened.
'''
    report=OUT/'reports/19_neutral_structural_feature_profiles_trial1.md';report.write_text(md,encoding='utf-8');examplekeys=['log_aspect','ink_density','ink_centroid_x','ink_centroid_y','significant_cavity_count','cavity_centroid_y','skeleton_branch_cluster_count','horizontal_run_fraction','vertical_run_fraction'];cards=[];qlookup={r['parent_id']:r for r in qualified}
    for p in profiles:
        if p['parent_id'] not in {'B001_O121','B006_O144','B012_O031','B004_O063','V_094_P012544','V_170_P006718'}:continue
        table=''.join(f'<tr><td>{escape(k)}</td><td>{escape(str(p["features"][k]["primary"]))}</td><td>{escape(str(p["features"][k]["range"]))}</td><td>{escape(p["features"][k]["status"])}</td></tr>' for k in examplekeys);cards.append(f'<article><h2>{escape(p["parent_id"])}</h2><img src="../{p["native_crop"]}"><p>Native bbox {p["native_bbox"]}; source {escape(p["source_state"])}. Class reporting: {escape(p["old_class_reporting_only"])}</p><p><strong>Cavity source qualification: {escape(qlookup[p["parent_id"]]["cavity_semantic_status"])}</strong></p><table><tr><th>Descriptor</th><th>Primary</th><th>Range</th><th>Status</th></tr>{table}</table></article>')
    html='<!doctype html><html><head><meta charset="utf-8"><title>Neutral feature examples</title><style>body{font:15px system-ui;margin:24px;background:#f2f0ec}article{background:white;padding:20px;margin:16px 0}img{max-width:400px;max-height:240px}table{border-collapse:collapse}td,th{padding:6px;border:1px solid #ccc;text-align:left}td{font-size:13px}</style></head><body><h1>Source parents with partial neutral feature vectors</h1><p>Numeric raster stability and source-visible certainty are separate. Whole parents remain primary; no internal unit or pen-lift claim. Primary values are never silently substituted for unknown features.</p>'+''.join(cards)+'</body></html>'
    atlas=OUT/'reports/20_neutral_feature_profile_examples_trial1.html';atlas.write_text(html,encoding='utf-8')
    for src in re.findall('src="([^"]+)"',html):assert (atlas.parent/src).resolve().exists(),src
    write_json(T/'artifact_validation.json',dict(profile_parents=len(profiles),descriptors=len(DEFS),all_example_images_exist=True,source_audit_count=len(obs),numeric_source_disagreements_retained=True,no_classes_fit=True,no_sequence_assay=True));print('Feature report19/20; audit16/17 primary,14/15 stable agreement,3 stable/source-unknown cases retained',flush=True)
if __name__=='__main__':main()
