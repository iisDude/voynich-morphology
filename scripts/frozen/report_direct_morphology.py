from direct_morphology_common import *
from PIL import Image,ImageDraw
import numpy as np,html
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def main():
    guard();verify();verify_seal(D/'DISTANCE_SEAL.json');data=read_json(D/'source_parent_ensembles.json');parents=data['parents'];candidates=data['candidates'];fields=np.load(D/'direct_image_fields.npz');unc=read_json(T/'representation_and_source_uncertainty.json');sim=read_json(T/'source_similarity_and_envelopes.json');ret=read_json(T/'continuous_reference_retrieval.json');diagnosis={r['parent_id']:r for r in unc['parents']};cards=[];thumbs=G/'parent_ensembles';thumbs.mkdir(exist_ok=True)
    for r in parents:
        ids=r['candidate_indices'];ww=150;hh=185;can=Image.new('RGB',(min(6,len(ids))*ww,((len(ids)+5)//6)*hh),'#f4f4f4');dr=ImageDraw.Draw(can)
        for j,k in enumerate(ids):
            x=j%6*ww;y=j//6*hh;im=Image.fromarray((1-fields['shape64'][k])*255).convert('RGB').resize((128,128),Image.Resampling.NEAREST);can.paste(im,(x+8,y+23));meta=candidates[k];dr.text((x+6,y+4),meta['candidate_id']+' c'+str(meta['contrast']),fill='black');role=meta['role'].replace('_',' ');dr.text((x+6,y+155),role[:22],fill='black');dr.text((x+6,y+170),role[22:44],fill='black')
        path=thumbs/(r['audit_id']+'.png');can.save(path);d=diagnosis[r['parent_id']];extent='source-resolved whole extent' if r['source_extent_resolved'] else 'UNKNOWN full extent; observed-part shapes only';cards.append(f"<details><summary>{r['audit_id']} / caption {r['caption']} / {extent}</summary><p>{html.escape(r['parent_id'])}; native bbox {r['native_bbox']}; {r['native_source']}. Candidate count {len(ids)}; split {d['split_contrast']}; merge {d['merge_contrast']}. Primary-to-raster observed spread {d['max_primary_to_raster_candidate']:.4f}. Complete physical distance interval: unknown.</p><img class='source' src='../{r['native_crop']}' alt='Native Yale source parent and context'><p>Observed raster alternatives; fragments and possible contaminated merges are diagnostic recoveries, not source-certified whole-parent shapes.</p><img class='ensemble' src='../{path.relative_to(OUT).as_posix()}'><p>Signed-distance image fields and exact candidate/native mappings are retained in the sealed data. No class assignment, internal unit boundary or writing identity is inferred.</p></details>")
    (OUT/'reports/24_direct_contour_morphology_atlas_trial1.html').write_text("<!doctype html><meta charset='utf-8'><title>Direct source morphology ensembles</title><style>body{font:16px system-ui;max-width:1300px;margin:24px auto}summary{padding:12px;background:#edf2f5;margin:5px 0}.source{max-width:600px;image-rendering:pixelated}.ensemble{max-width:100%}p{max-width:1150px}</style><h1>Direct continuous contour/morphology — source ensembles</h1><p>217 confirmed-writing proposals, 206 with source-resolved whole extent and11 with unknown full extent. A contour/SDF coordinate describes an observed raster hypothesis, not a writing class. Possible fragments/merges and source joins are retained; no highest-similarity candidate settles their physical ownership. Earlier source judgments and feature trials are immutable. This trial reuses earlier imagery and similarity judgments, so it is not fresh confirmation.</p>"+''.join(cards)+"<h2>Unresolved source-join alternative</h2><p>N094/N095: a faint bridge may join the observed parts. Their stored union omits unresolved bridge pixels; full-parent embedding and physical distance remain unknown.</p><img class='source' src='../figures/neutral_feature_trial2/V_112_upper_context_extension.png'>",encoding='utf-8')
    # Illustrate a field, without reducing the actual metric to2D learned coordinates.
    fig,axes=plt.subplots(3,4,figsize=(11,8));examples=['N003','N009','N094'];lookup={r['audit_id']:r for r in parents}
    for row,aid in enumerate(examples):
        r=lookup[aid];idx=r['candidate_indices'];axes[row,0].imshow(Image.open(OUT/r['native_crop']));axes[row,0].set_title(aid+' native source');axes[row,1].imshow(fields['shape64'][r['primary_index']],cmap='gray_r',vmin=0,vmax=1);axes[row,1].set_title('Observed primary mask');axes[row,2].imshow(fields['sdf64'][r['primary_index']],cmap='coolwarm',vmin=-.15,vmax=.15);axes[row,2].set_title('Signed distance field');axes[row,3].imshow(fields['shape64'][idx[1]],cmap='gray_r',vmin=0,vmax=1);axes[row,3].set_title('Alternate recovery')
        for ax in axes[row]:ax.axis('off')
    fig.suptitle('Native source remains primary; N094 full extent is unknown');fig.tight_layout();fig.savefig(G/'direct_shape_examples.png',dpi=140);plt.close(fig)
    mt='\n'.join(f"| {k} | {v['auc']:.3f} | {v['ordinal_spearman']:.3f} |" for k,v in sim['metrics'].items());allunc=unc['all'];f=unc['fresh'];iv=sim['interval_ordering'];ci=sim['primary_contour_caption_bootstrap95']
    report=f'''# Direct continuous contour/morphology space — Trial1

**Yes: an explicit, reproducible image-shape representation can be constructed without discrete classes or a complete named-feature profile.** This separate preregistered feasibility trial represents217 source-confirmed writing proposals as1,124 direct contour/signed-distance image fields.206 have source-resolved whole extents;11 retain **unknown full-parent geometry**. Every observed candidate has coordinates, but an observed-part coordinate is not a certified whole-parent representation.

On121 reused same/different source pairs, fixed primary contour AUROC is **{sim['metrics']['contour64']['auc']:.3f}**. Uncertainty remains consequential: only **{ret['certain_nearest_n']}/118** source-resolved fresh-for-Trial2 parents have a nominal nearest reference that stays certainly nearest across observed raster/slant alternatives. Thus a continuous morphology space supports graded resemblance while often requiring an unresolved set of neighbors.

## Preregistration and scope

[PLAN](../data/observations/direct_morphology_trial1/PLAN.json) and [specification seal](../data/observations/direct_morphology_trial1/SPECIFICATION_SEAL.json) predate this trial's shape/distance outcomes. Trial2's superior contour result was already known and motivated the trial. This is **post-exposure feasibility and sensitivity**, not fresh independent confirmation. Trial1/Trial2 feature packages and V3–V6 remain immutable. No V3 class labels, semantic feature profiles, conventional strings, Currier data, positional/section effects, sequences or decipherment outcomes define the representation or metric.

The corpus reuses Trial2's frozen source adjudication:88 reference proposals and129 fresh-for-Trial2 confirmed-writing proposals from six caption groups. Three unresolved proposals and one nonwriting detection are excluded and enumerated. Native photographs, coordinates and original source judgments remain primary. No breadth expansion or new parent/source ownership decision occurred. Current proposal sampling cannot establish all-writing recall or a complete row/sequence extraction.

## Representation

Each parent record stores the native photo/mask/coordinates, source extent state and an **ensemble of observed recovery candidates**. Each candidate is represented directly by an aspect-preserving64×64 binary image and normalized signed-distance field. Tight envelope dimensions fit within56×56 support, centered, using nearest-neighbor resampling. Orientation/aspect are preserved; overall size and translation are normalized away. Native size/body proxy remain source metadata. There is no rotation, reflection, learned alignment, PCA, class prototype, cluster label or hand-designed completeness requirement. The ambient4,096 pixel-field coordinates are measurements of an image function, not a semantic alphabet.

Primary distance is symmetric contour Chamfer divided by56, using inner and outer **raster** boundaries. Secondary morphology distance is signed-distance-field RMS.32/128px are registered sensitivity resolutions;64px stays primary despite their observed scores. Normalization/resampling can remove or alter fine details, so the native photo/mask remains accessible. Negative space, apparent closure and raster connectivity are not automatically photographically certified cavities or physical joins.

At contrast6/12, every component covering≥5% of primary-mask ink is retained. Multiple matches produce both component candidates and a union preserving native relative placement. Possible merged extents retain contamination flags. These candidates include failed/incomplete recoveries and are **not all source-certified physical whole parents**. Missing matches would retain an explicit absence state; none occurs in this sample. Synthetic±0.04 slants probe nuisance sensitivity only. No connecting ink is fabricated.

Source uncertainty differs from raster variability. A source-resolved extent can still have multiple inadequate raster recoveries. An uncertain extent has provisional observed-part vectors plus an explicit unknown full-parent state. N094/N095 retain the frozen possible faint-bridge join and a partial union; unresolved bridge pixels are omitted, and its full-parent embedding remains absent. Similarity does not decide whether these parts physically connect.

## Coverage and correspondence

Observed primary coordinates are available for217/217 confirmed-writing proposals. Source-resolved whole extents are206/217, including118/129 fresh-for-Trial2 proposals. The other11 are not counted as resolved whole shapes. Availability therefore does not establish source fidelity, writing-unit boundaries or complete extraction.

Across217 parents,18 have split and43 have merge recovery cases(counts overlap);0 have missing threshold matches. Fresh-for-Trial2 counts are14 splits and33 merges. Median candidate count is5. Median maximum primary-to-raster candidate contour spread is{allunc['raster_spread_median']:.4f},95th percentile{allunc['raster_spread95']:.4f}. Median slant spread is{allunc['slant_spread_median']:.4f}. These are normalized geometric sensitivities, not source-rater disagreement or uncertainty probabilities. No threshold was chosen to convert spread into a writing class.

## Reused source-image similarity

The fixed185 pairs previously selected through pooled profile/contour/aspect methods retain54 same whole-organization ratings,64 partial,67 different,0 unresolvable. All121 binary pairs now have observed contour distances and source-resolved extents;64 partials remain reported, not forced into binary labels. The source judgments were made by the same AI with repeated references/anchors. Pair selection and outcomes were already exposed. Scores are conditional descriptive checks, not independent validation.

| Fixed direct metric | AUROC on121 binary pairs | Ordinal association on185 pairs |
|---|---:|---:|
{mt}

Primary contour six-caption bootstrap95% is{ci[0]:.3f}–{ci[1]:.3f}. This does not remove source-judgment dependence, repeated reference reuse or prior outcome exposure. Trial2's reported0.917 contour baseline used a different99-pair common-feature subset and24px normalization; direct comparisons of those values would mix estimands.

## Uncertainty-aware similarity

For each source pair, preserve its primary distance and the minimum/maximum over observed candidate recoveries/slants. These are **observed sensitivity envelopes**, not calibrated posterior intervals, exhaustive physical bounds or a probability of same writing identity. They intentionally include fragmented or contaminated recoveries; a wide envelope can diagnose extraction failure rather than variation of a true parent. Unknown full extent remains unknown regardless of a finite candidate envelope. Complete physical distance intervals are not estimated in any record.

Among3,618 same-vs-different pair comparisons,2,097(58.0%) are correctly ordered for every observed candidate-distance choice,63(1.7%) are reversed for every choice and1,458(40.3%) overlap/tie. The resulting0.580–0.983 sensitivity ordering bounds are **not an AUROC confidence interval**; repeated/correlated candidate choices make them conservative diagnostic envelopes rather than a joint posterior.

All118 source-resolved fresh-for-Trial2 parents were queried against88 reference parents from different captions, without any class labels. Only10(8.5%) have their primary nearest reference certainly nearest under the observed envelopes. Median not-excluded reference set size is7.5. Primary nearest reference is unchanged in93/118 cases at32px and110/118 at128px. These are **image-similarity ranks**, not manuscript token rank or pixel position. A neighbor set is not a discrete class or writing equivalence relation; no source parent boundary was selected to improve a match.

## Interpretation and disposition

The operational feasibility criteria pass: nonempty observed representation, explicit unknown source extents, and no discrete classes or mandatory named-feature vector. The registered descriptive AUROC/sample/caption checks also pass. **Fresh independent generalization remains untested.** The more informative limitation is uncertainty in recovered outlines and nearest matches, which a class-free representation makes visible rather than eliminating.

A defensible record is: native source evidence + extent hypotheses/UNKNOWN + candidate contour/SDF coordinates + provenance + observed distance envelope/abstention. It can describe graded morphology even when a form resists discrete assignment. It cannot establish letters, internal graphemes, pen lifts, stroke order, complete writing membership, physical connection, semantic identity or a usable sequence notation.

The separate [Trial1 freeze](../data/observations/direct_morphology_trial1/FREEZE_MANIFEST.json) preserves the protocol, candidate/native arrays, source alternatives, metrics, uncertainty failures, source atlas and code. [Postfreeze integrity/replay](../tests/direct_morphology_trial1_postfreeze/integrity.json) checks both this package and earlier freezes. No downstream assay is reopened. A later genuinely fresh source-image test must be preregistered before interpreting this as generalizable manuscript morphology.

[Source ensemble atlas](24_direct_contour_morphology_atlas_trial1.html) · [image-field examples](../figures/direct_morphology_trial1/direct_shape_examples.png) · [acceptance distinctions](../tests/direct_morphology_trial1/acceptance_summary.json)
'''
    (OUT/'reports/23_direct_contour_morphology_trial1.md').write_text(report,encoding='utf-8');print('Direct morphology report and217-parent uncertainty atlas written',flush=True)
if __name__=='__main__':main()
