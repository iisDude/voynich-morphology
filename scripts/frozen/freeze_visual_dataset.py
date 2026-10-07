"""Freeze a failure-aware candidate snapshot BEFORE reading transcriptions."""
from common import OUT,read_json,write_json,write_csv,sha256
from datetime import datetime,timezone
from jsonschema import Draft202012Validator


def main():
    root=OUT/'data/observations/visual_dataset_v0';freeze=root/'FREEZE_MANIFEST.json'
    if freeze.exists():raise ValueError('Snapshot already frozen; do not overwrite. Create a new version for changes.')
    files=sorted(p for p in root.glob('V_*.json') if p.stem[2:].isdigit())
    if len(files)!=204:raise ValueError('Full-view dataset incomplete')
    if not (root/'fine_source_audit_summary.json').exists():raise ValueError('Held-out source audit not recorded')
    validator=Draft202012Validator(read_json(OUT/'data/observations/annotation_schema.json'))
    for path in files:
        obj=read_json(path);obj['status']='frozen';validator.validate(obj);write_json(path,obj)
    patterns=['data/observations/visual_dataset_v0/*.json','data/observations/visual_dataset_v0/*.csv',
        'data/observations/regional_candidates_v4/V_*.json','data/observations/regional_candidates_v4/V_*_shapes.npz',
        'data/observations/regional_candidates_v4/V_*_native_masks.npz','data/observations/native_structure_v4/V_*.json',
        'data/observations/visual_family_models_v4/*','data/observations/curved_path_candidates_v2/V_*.json',
        'data/observations/*family_source_review_v4.json','data/observations/visual_structure_merge_hypotheses_v0.json',
        'data/observations/annotation_schema.json','data/observations/visual_family_analysis_plan.json',
        'data/observations/regional_candidate_protocol_snapshot_v4.json','data/observations/region_review_protocol.json',
        'data/observations/layout_regions_fractional.json','data/observations/calibration_regions.json',
        'data/observations/heldout_source_audit*.json','data/source/all_view_manifest.csv',
        'data/source/yale_native_all_manifest.csv','data/source/yale_registration_all.json',
        'data/source/visual_split_manifest.json','tests/visual_reconstruction/*','tests/visual_structure/*',
        'src/*.py']
    evidence=sorted(set(p for pattern in patterns for p in OUT.glob(pattern) if p.is_file()))
    items=[dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p),bytes=p.stat().st_size) for p in evidence]
    manifest=dict(snapshot_id='visual_candidate_v0',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
        status='frozen candidate segmentation and ambiguity record; recovered manuscript alphabet NOT established',
        comparison_transcription_contents_opened=False,source_derivation='physical images and geometry only; prior chat examples disclosed',
        views=204,canonical_grapheme_claim=False,files=items,
        partitions=['fine raster components','medium gap assemblies','coarser compounds','space-gap groups','sparse skeleton internal cuts'],
        identity_hypotheses=['training-only raw prototype bins','21 broad visual structure merges','six proposed compound factorizations'],
        primary_assay_rule='Raw fine, merged fine, factored fine and medium sequences reported separately; only fully admitted groups supply identities; all original rank/pixel slots retained.',
        unresolved_coverage=['Circular/irregular paths remain separately registered hypotheses; do not enter horizontal assays.',
            'Sparse labels, rotated writing, incomplete faint marks and crossing drawings remain unresolved.',
            'Physical panel/bifolio map is unverified; repeated view deduplication not established.',
            'Majority of source groups lack complete admitted unit sequences; exclusion is not proof that the source contains no writing.',
            'Source quality audits find false admissions and incompatible broad shape assignments.',
            'No positive pen-lift or stroke-order evidence established.'],
        interpretation='This freeze permits an honest comparison of a reproducible failed/partial candidate model. It does not certify that the requested complete writing-unit inventory has been recovered.')
    write_json(freeze,manifest)
    # Complete neutral atlas: each candidate has source crops, recurrence, context,
    # variants, confidence and alternative boundaries, including rejected families.
    report=['# Visual unit atlas v0','',
        'This is a frozen, manuscript-derived candidate atlas with substantial unresolved coverage. It is not a recovered alphabet. Source imagery defines the candidates; EVA, RF and v101 contents remained unopened until this snapshot.',
        '', '## Evidence and model comparison','',
        'All 204 folio-captioned views have native Yale images and reversible registration. The twelve-view pilot calibrated the extraction; candidate analysis then expanded across all views. Captions are not verified physical panel maps.',
        '', 'Four partitions compete on the same held-out native assigned-ink masks. Training template mean IoU on 1,824 test groups is 0.621 for fine components, 0.538 for medium assemblies, 0.458 for coarse compounds and 0.415 for whole groups. This favors finer geometry within the admitted subset, not graphemes. Rectangle costs and binary residuals are coding proxies, not lossless source compression.',
        '', 'The medium source audit found clear writing in 100/120 test crops, 12 failures and 8 ambiguous cases. A fresh stratified fine audit found clear writing in 106/128 crops, 6 failures and 16 ambiguous cases; 8 broad-structure assignments were visibly incompatible. Neither audit estimates recall or boundary accuracy. No threshold was retuned on these outcomes.',
        '', 'About 31% of held-out sampled crops changed component count across contrast thresholds; about 32% changed connectivity under a two-pixel erosion probe. Disconnection cannot be promoted to pen-lift evidence.',
        '', 'Height remains continuous. A two-component training mixture modestly improves validation log density, but this can reflect different assemblies, detector truncation and scribal variation. Tall-form thresholds do not establish a sign class.',
        '', '## Boundaries and structural hypotheses','',
        'Fine components are threshold-connected raster objects. Medium and coarse models join objects by geometric gaps; whole-group models preserve space-gap assemblies. Native skeleton valleys add candidate internal cuts without declaring an alphabet. Every group retains alternative partitions and native coordinates.',
        '', 'Long upright and horizontal segments, end supports, above-bar ink, repeated column ridges and erosion sensitivity are explicit geometric measurements in `native_structure_v4`. Frames and insertions remain hypotheses; the simple frame detector is sparse and not validated as a complete bench inventory. Upper and lower extents use a provisional local baseline/body estimate. Raster endpoints are not stroke ends.',
        '', 'Twenty-one broad structure merges and six compound analogies are alternate interpretations, not canonical graphemes. Similar rounded loops recur in many prototype bins; merging can remove allographic duplication or conflate different structures. Tall structures occur alongside or connected to lower traces, but photographs and masks do not establish stroke order.',
        '', 'Circular text has orientation-preserving unwrapping proposals in 17 views. Approximate ellipses leave curved/sinusoidal rows and fragment paths; these remain unresolved and excluded from horizontal position statistics. Sparse and rotated labels are not silently converted into linear rows.',
        '', 'Section and attributed-hand labels were withheld from family fitting and are used only after this freeze for stability comparisons. They are inherited annotations, not independent physical hand identifications.',
        '', '## Candidate families','']
    for name in ['fine','medium']:
        reviewed=read_json(OUT/f'data/observations/{name}_family_source_review_v4.json')['records']
        report.extend([f'### {name.capitalize()} partition',''])
        for r in reviewed:
            report.extend([f'#### {r["family_id"]}','',r['visual_description'],'',
                f'- Source review: {r["review_category"]}; confidence: {r["confidence"]}.',
                f'- Recurrence: {r["training_instances"]} training instances across {r["training_folio_components"]} caption-connected folio components.',
                f'- Context: {r["contexts"]}.',f'- Variants: {r["observed_variants"]}.',
                '- Competing segmentations: '+', '.join(r['segmentation_alternatives'])+'.',
                '- Pen lift and atomic identity: unresolved.',
                f'- Source examples: [gallery](../{r["gallery"]}).',''])
    report.extend(['## Freeze and reproducibility','',
        'The machine-readable schema-conforming per-view dataset is in `data/observations/visual_dataset_v0`. `FREEZE_MANIFEST.json` hashes source-derived candidates, native masks, unit hypotheses, protocols, model artifacts, scripts and visual test results before comparison transcriptions are opened. The freeze preserves failed and unknown assignments rather than forcing a single alphabet.'])
    (OUT/'reports/02_visual_unit_atlas_v0.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    print('Frozen',len(items),'files',sha256(freeze))

if __name__=='__main__':main()
