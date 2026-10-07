from inventory_v6_common import *
from html import escape
import json,re
REPORT=OUT/'reports/17_confirmed_unknown_structures_v6.md'
ATLAS=OUT/'reports/18_confirmed_unknown_source_atlas_v6.html'
def main():
    guard();s=read_json(T/'structural_coverage.json');rec=read_json(D/'discovery_parents.json');lookup={r['parent_id']:r for r in rec};diag=read_json(D/'source_unknown_diagnosis.json');q=read_json(D/'source_diagnosis_qualification.json');model=read_json(F/'structural_inventory.json')
    md='''# V6 confirmed-writing structural inventory investigation

**No additional structural or compositional class passed the source-only validation protocol.** V6 freezes a negative inventory result with failed candidates and unresolved interpretations. It does not establish that all unknowns are different forms, nor that further source-only representation methods cannot succeed. V3, V4 and V5 remain unchanged.

Discovery used all **638 source-confirmed V5 target-writing parents**, without unresolved writing-membership objects, conventional transcription labels, Currier metadata, positional outcomes or sequence objectives. The 311 prior V3 assignments remain intact; 327 remain `UNK`. Source confirmation establishes visible writing membership, not chemical ink identity, atomicity, pen lifts, graphemes or drawing order.

## What the source-confirmed unknowns represent

The preclass diagnostic separates the 327 V3 unknowns into mutually exclusive raster/source categories:

| Primary diagnostic stage | Parents |
|---|---:|
| Stable whole-parent raster awaiting morphology/class explanation | 168 |
| Topology/connectivity instability across native contrasts | 127 |
| Unresolved parent contact / competing photographic join | 31 |
| Confirmed photographic join disconnected in primary raster | 1 |

The old V3 failure flags overlap: 207 nominal fit/radius/margin abstentions, 139 old raster-stability failures, 274 threshold-class failures, 234 fixed-slant class failures and 11 geometry/connectivity exclusions. These are not additive populations. The V6 raster check adds explicit significant-hole/component checks for geometry-excluded parents; it explains why its127 topology/contact-instability count differs from old V5 raster flags.

All seven unknown-parent native RGB mosaics were inspected. Source descriptors record eight frame/insertion or extra-upright candidates, eighteen loop/branch/appendix candidates and fifteen repeated-element candidates. These overlap; twenty-six have a possible connected-compound interpretation. An extended frame or repeated arch is a whole connected parent first. No descriptor decomposes it into characters or asserts execution order.

Thirty-three directly inspected examples retain ordinary ring, paired-upright/upper-loop or hooked-curve organization with proportion/slant differences. They are **likely family-variant hypotheses**, not accepted V3 labels or established allographs. A broader automatic same-hole Chamfer/aspect screen flagged304 cases but failed native inspection: its first twelve comparisons yielded two same-organization judgments, seven different and three unresolved. That permissive screen is preserved as a failure and cannot justify merging304 parents.

Across all638 parents, a separate source-priority partition gives **301 resolved existing-V3 parents, 288 confirmed-writing V3 unknowns, 41 unresolved compound/contact parents and eight insufficient-morphology parents**. Ten of those41 contacts already had frozen V3 labels. Their labels are retained while their whole-parent certainty remains conditional. This partition does not overwrite V5 membership or class judgments.

## Compositional explanations before more classes

The whole parent remains primary. A preregistered outside-band search removed20/30/40% of parent width or height on each side, retained15–45% residual ink, required actual source-mask contact and tested the remaining base against frozen V3. Competing fits were retained. This is a morphology measurement, not evidence of a detachable appendix or internal writing unit.

On the168 initially stable unknowns, 87 had at least one primary-mask fit. Three generic descriptions reached training recurrence: `ST03 + upper residual` (10 parents), `ST11 + left residual` (25), and `ST11 + right residual` (16). Native source review rejected all three as reusable composite classes: the same removal family cut through lobes, ordinary uprights and bridges with no consistent appendix or insertion geometry. The lower-frame/upper-trace descriptions of B012_O040 and B014_O071 remain plausible individual interpretations, insufficient to validate a reusable compositional model.

The broader diagnostic tested all confirmed parents, including unstable/contact cases, plus controls:

| Corpus | Primary base/residual fits | Same explanation across6/9/12 | Orientation-reversed control fits |
|---|---:|---:|---:|
| Already V3-assigned | 261/311 | 205/311 | 141/311 |
| V3 unknown | 176/327 | 75/327 | 101/327 |
| Fresh confirmed writing | 50/66 | 26/66 | 30/66 |

These high fit rates show **truncation-match promiscuity**. Rotation retains silhouette topology/scale but is a diagnostic control, not a claim about manuscript writing or an independent null sample. Even threshold-stable base fits require coherent residual geometry and native source validation. Validated compositional coverage is zero; raw factor fits never become sequence tokens.

## Separate whole-parent candidates and fresh validation

The [original registration](../data/observations/structural_inventory_v6_development/PLAN.json) predates class suggestions. It requires eight discovery instances from three captions, five stable fresh instances from three fresh captions, ten accepted-positive native pairs with agreement≥0.85, a class-specific negative audit of at least twenty with false grouping≤0.10, and threshold/alignment stability≥0.90. Contacts, insufficient images, inconsistent topology, failed margins and source-incoherent candidate groups abstain.

The initial complete-link distance0.35 attempt formed162 clusters from163 eligible unknowns and qualified none. A documented **training-only amendment**, before test assignments, calibrated the scale using already accepted discovery V3 examples: twice their90th-percentile cross-caption nearest distance, giving diameter1.214822. The original failed attempt remains sealed. No validation gate, V3 radius, test outcome or sequence criterion selected this scale.

Five groups qualified by discovery counts: NC01(15 parents/eight captions), NC02(10/six), NC03(9/four), NC04(8/six), NC05(8/four). Native inspection rejected NC01/03/04/05 for mixed whole-parent organization, rather than removing inconvenient examples. NC02 retained a provisional vertically stacked-lobe description with one significant raster hole and a bulky upper region. It may be a V3-family/compound variant, not a novel alphabetic unit.

Its model and radius were sealed before fresh inference. The radius is0.647643; the closest fresh source-resolved parent is0.711685. **No nominal fresh NC02 assignment is accepted**, so no stable assignment exists. Accepted-positive agreement, class-specific false-grouping rate and conditional accepted-assignment stability are **not estimable**, rather than zero error. The minimum-support gates fail. The radius was not enlarged after this result.

Fresh validation used first ordinary local source fields in captions16,47,94 (viewsV_032,V_094,V_170), chosen before candidate assignments. All seventy primary location-aid parents were inspected in native RGB and full context before suggestions:66 confirmed writing, two drawing/paint, two unresolved membership. Of the66 writing parents,57 have resolved whole-parent evidence, seven have possible contacts and two insufficient morphology. Two clear neighboring-row writing parents remain identified as neighbors. Field-edge parents were viewed whole in padded source, rather than clipped. These are local parent-validation fields, not another exhaustive row-truth benchmark.

The captions were unused to define V6 classes but already had V4 source/geometry exposure; source pixels are not globally unseen. Fresh source review occurred before class suggestions, but prior image familiarity and a single AI adjudicator prevent independent-rater or fully blind claims.

Twenty masked nonmember-to-nonmember retrieval comparisons yielded twelve same-organization, three different and five unresolved judgments. They are a **failure diagnostic for similarity pools**, not candidate false-grouping measurements. A separate balanced ten-pair nearest-NC02 challenge has no accepted prediction: eight different organizations and two unresolved cavity-placement comparisons. Neither challenge supplies the missing accepted-positive audit or permits radius retuning. Pair identities/class suggestions were hidden in the displayed RGB; the empty accepted pool was known.

## Coverage and inventory status

| Metric | V3 only | V3 + validated V6 additions |
|---|---:|---:|
| V5 confirmed-parent assignment | 311/638 (48.7%) | 311/638 (48.7%) |
| V5 unknown confirmed parents | 327/638 (51.3%) | 327/638 (51.3%) |
| Fresh confirmed-writing assignment | 29/66 (43.9%) | 29/66 (43.9%) |
| Validated compositional assignment | — | 0 |

Discovery coverage is in-sample use of a fixed model, not fresh validation. Eight-caption bootstrap95% coverage interval is43.7–54.7%; it does not account for source-adjudicator error. Contact and insufficient-photography rates are separate from class coverage. The unchanged source membership remains a hard limit even if a future structural inventory improves.

The [source atlas](18_confirmed_unknown_source_atlas_v6.html), [per-parent diagnosis](../data/observations/structural_inventory_v6_development/source_unknown_diagnosis.json), [source qualification](../data/observations/structural_inventory_v6_development/source_diagnosis_qualification.json), [candidate gate results](../tests/structural_inventory_v6/candidate_validation.json) and [factor controls](../tests/structural_inventory_v6/composition_robustness_and_controls.json) preserve evidence, alternatives and failures.

V6 freezes this inventory assessment **before constructing sequences**. Its expanded inventory adds no validated class, so unknown confirmed parents remain unknown. A separate postfreeze application must reuse the V5 rows, source judgments, whole parents and0.35/0.55/0.75 partitions without retuning. No Currier, pixel-x, conventional crosswalk, minimal-pair or decipherment test was run.

The negative result is conditional on this representation and candidate procedure. Native hole placement and filled/faint lobes, contact uncertainty, width/slant variation, limited fresh caption support and arbitrary truncation matching explain substantial failure. More new labels would currently obscure those uncertainties rather than establish a defensible inventory.
'''
    REPORT.write_text(md,encoding='utf-8')
    cards=[]
    byid={r['parent_id']:r for r in diag['parents']};states={r['parent_id']:r['source_state'] for r in read_json(F/'expanded_parent_assignments.json')}
    for r in rec:
        if r['structural_class']!='UNK':continue
        d=byid[r['parent_id']];tags='; '.join(d['overlapping_hypotheses']);text=f"{r['parent_id']} caption {r['caption']} {r['diagnosis_stage']} {tags}";cards.append(f'<article data-search="{escape(text.lower())}"><h3>{escape(r["parent_id"])} · caption {r["caption"]}</h3><a href="../{r["native_source"]}"><img src="../{r["native_crop"]}" alt="Native source crop"></a><p>Native bbox {r["native_bbox"]}; {escape(states[r["parent_id"]])}</p><p>{escape(r["diagnosis_stage"])}<br>{escape(tags)}</p><p>V3: UNK · validated new class: none</p></article>')
    gallerylinks=' '.join(f'<a href="../figures/structural_inventory_v6/{c["candidate_id"]}_candidate_01.png">{c["candidate_id"]}: {c["source_decision"]}</a>' for c in model['candidates'])
    html='''<!doctype html><html><head><meta charset="utf-8"><title>V6 confirmed unknown source atlas</title><style>body{font:15px system-ui;background:#f3f1ed;color:#242424;margin:24px}header{max-width:1050px}input{padding:10px;width:75%;font:inherit}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:16px}article{background:white;padding:12px;border:1px solid #ccc}img{max-width:100%;max-height:240px;image-rendering:auto}h3{font-size:16px}p{overflow-wrap:anywhere}a{color:#235b78}nav a{display:inline-block;margin:8px}small{color:#666}</style></head><body><header><h1>V6 source-confirmed unknown parents</h1><p>327 writing parents; no validated additional class. Native RGB, source coordinates and competing descriptors. Whole parent is primary; no letter, word, pen-lift or stroke-order claim. Prior V3/V4/V5 remain immutable.</p><p>Images may contain nearby independent ink in the padded crop. The source bbox locates the reviewed parent; it is not an ink-pixel or grapheme mask.</p><p><a href="17_confirmed_unknown_structures_v6.md">Inventory report</a></p><nav>'''+gallerylinks+'''</nav><label>Filter parent/caption/diagnostic description <input id="filter" placeholder="e.g. B014, topology, frame"></label><p id="count"></p></header><main class="grid">'''+''.join(cards)+'''</main><script>const cards=[...document.querySelectorAll('article')];function filter(){const s=document.querySelector('#filter').value.toLowerCase();let n=0;for(const c of cards){c.hidden=!c.dataset.search.includes(s);if(!c.hidden)n++}document.querySelector('#count').textContent=n+' of '+cards.length+' confirmed-writing unknown parents'}document.querySelector('#filter').addEventListener('input',filter);filter();</script></body></html>'''
    ATLAS.write_text(html,encoding='utf-8');missing=[]
    for p in re.findall(r'(?:src|href)="([^"#]+)"',html):
        if not (ATLAS.parent/p).resolve().exists():missing.append(p)
    assert not missing,missing;save(T/'artifact_validation.json',dict(atlas_parents=len(cards),missing_links=missing,report_exists=REPORT.exists(),candidate_galleries=5,inventory_before_sequences=True));print('Reports17/18 ready;327 native unknown cards, links valid',flush=True)
if __name__=='__main__':main()
