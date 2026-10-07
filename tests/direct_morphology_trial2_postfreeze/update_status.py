import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
from direct_morphology2_common import *

verify_seal(D/'FREEZE_MANIFEST.json')
assert read_json(P/'DISPOSITION.json')['status']=='supported'
protected=set()
manifests=[OUT/f'data/observations/visual_dataset_{v}/FREEZE_MANIFEST.json' for v in ['v0','v11','v2','v3','v4','v5','v6']]+[OUT/'data/observations/neutral_feature_trial_v1/EVIDENCE_SEAL.json',OUT/'data/observations/neutral_feature_trial2/FREEZE_MANIFEST.json',OLD/'FREEZE_MANIFEST.json',D/'FREEZE_MANIFEST.json']
for manifest in manifests:
    protected.update((OUT/r['path']).resolve() for r in read_json(manifest)['files'])
digest=sha256(D/'FREEZE_MANIFEST.json')
updates={
    OUT/'README.md':'''\n\n## Latest completed trial: Direct Morphology Trial2 (2026-10-07)

The frozen64px class-free contour representation meets the preregistered fresh-caption validation gates:211 binary source judgments from eight caption groups, AUROC0.879 versus aspect0.737. This is qualified support for visible morphology in the selected source-resolved sample, with same-AI source ratings,70% short-session repeat agreement and consequential raster uncertainty. Earlier overview exposure remains.27 whole-parent extents stay unknown. Trial1 and all earlier freezes are unchanged; no downstream assay is reopened.

[Postfreeze interpretation](tests/direct_morphology_trial2_postfreeze/SUMMARY.md) · [Evidence report](reports/25_direct_contour_morphology_trial2.md) · [Source atlas](reports/26_direct_contour_morphology_atlas_trial2.html)
''',
    OUT/'reports/08_investigation_status.md':'''\n\n## Current state after Direct Morphology Trial2 — 2026-10-07

The fresh-caption direct morphology validation is complete and frozen.192 confirmed-writing proposals from eight qualified fresh captions include165 source-resolved whole extents and27 unknown extents.360 anonymous RGB judgments yield35 same,176 different and149 partial;211 binary pairs evaluate the unchanged contour64 metric. AUROC0.879, caption-node bootstrap95%0.767–1.000; aspect-only0.737, paired improvement0.141 with95%0.020–0.261. All registered support gates pass.

Support is conditional on the registered random/aspect mixture and same-AI source targets. Random-subset superiority over aspect is not established. Repeat agreement14/20 and kappa0.388 limits source-label reliability. Only24/165 queries keep a unique nearest reference across all observed alternatives; median not-excluded set is6. Unknown physical geometry remains unknown. No alphabet, segmentation, semantic identity or complete transcription is established, and no downstream test is reopened.

[Postfreeze interpretation](../tests/direct_morphology_trial2_postfreeze/SUMMARY.md) · [Frozen evidence report](25_direct_contour_morphology_trial2.md) · [Source atlas](26_direct_contour_morphology_atlas_trial2.html) · [Integrity](../tests/direct_morphology_trial2_postfreeze/INTEGRITY.json)
''',
    OUT/'reports/WORK_LOG.md':f'''\n\n## 2026-10-07 — Direct Continuous Contour/Morphology Trial2 completed

Preserved Trial1 exactly. Audited102 caption groups using source identifiers;45 eligible and0 unresolved prior source-pair references after correcting the initial incomplete mapping before selection freeze. Selected eight captions/16 horizontal fields by source layout.192 nativeRGB proposals source-adjudicated before predictions:165 resolved whole extents,27 unknown. Frozen source judgments then applied exact Trial1 candidate/normalization/distance procedure;1,437 image fields for192 fresh and88 separate reference parents.

Sealed deterministic600-pair pool before anonymous source ratings. Initial240 had25 same, so registered next120 extension was used with predictions unopened. Final360:35 same,176 different,149 partial. Repeat20 under changed IDs/sides after representation replay:14 agreement, kappa0.388; same-AI only. Ratings sealed before predictions. Contour64 AUROC0.879, source-caption bootstrap95%0.767–1.000; aspect0.737, paired delta0.141 [0.020,0.261],1,993 valid draws. SDF64 secondary0.895; contour32/1280.877/0.871. No metric, source decision or threshold retuned.

Uncertainty:24/165 uniquely stable nearest across all observed alternatives; median not-excluded set6;81 query-recovery changes. All27 unknown full extents retained. Random stratum contour0.798/aspect0.812 and modest repeatability reported as limitations. Freeze943 files, SHA256 `{digest}`. Exact1,437 candidate fields, ten distance matrices, nativeRGB/mask/candidate correspondences, sampling, aspect and bootstrap replay.27,050 earlier visual-frozen checks, both feature trials, DirectTrial1 and14 originals preserved. Postfreeze disposition: supported within qualified fresh-caption/source-resolved sample; no independent human validation or global image blindness, writing identities or complete transcription. No conventional/linguistic/downstream assay opened.

[Summary](../tests/direct_morphology_trial2_postfreeze/SUMMARY.md) · [Report25](25_direct_contour_morphology_trial2.md) · [Atlas26](26_direct_contour_morphology_atlas_trial2.html).
'''
}
for path,text in updates.items():
    assert path.resolve() not in protected,path
    with path.open('a',encoding='utf-8') as f:f.write(text)
verify_seal(D/'FREEZE_MANIFEST.json')
write_json(P/'STATUS_UPDATE.json',dict(updated_at_utc=now(),paths=[p.relative_to(OUT).as_posix() for p in updates],all_targets_outside_prior_and_current_freezes=True,current_freeze_unchanged=True))
print('Unfrozen project navigation/status updated; frozen evidence unchanged')
