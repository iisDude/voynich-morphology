"""Qualify source classes, make neutral atlas and audit immutability before V3 freeze."""
from common import OUT,ROOT,read_json,read_csv,write_json,write_csv,sha256
from collections import defaultdict
from PIL import Image,ImageDraw
from datetime import datetime,timezone
import html
BASE=OUT/'data/observations/recurrence_v3_structural_candidate';DEST=OUT/'data/observations/visual_dataset_v3';TEST=OUT/'tests/recurrence_v3_development'

def main():
    if (DEST/'FREEZE_MANIFEST.json').exists():raise ValueError('V3 already frozen')
    old_checks=[]
    for ver in ['v0','v11','v2']:
        path=OUT/f'data/observations/visual_dataset_{ver}/FREEZE_MANIFEST.json';m=read_json(path);bad=[r['path'] for r in m['files'] if sha256(OUT/r['path'])!=r['sha256']]
        old_checks.append(dict(version=ver,files_checked=len(m['files']),failures=bad,manifest_sha256=sha256(path)))
        assert not bad,(ver,bad[:5])
    evidence=read_csv(OUT/'data/source/evidence_manifest.csv');bad=[r['path'] for r in evidence if sha256(ROOT/r['path'])!=r['sha256']];assert not bad,bad
    integrity=dict(time_utc=datetime.now(timezone.utc).isoformat(),older_freezes=old_checks,original_files_checked=len(evidence),original_failures=bad)
    write_json(TEST/'pre_v3_integrity.json',integrity)
    plan=read_json(BASE/'PLAN.json');req=plan['freeze_requirements'];ext=read_json(BASE/'extraction_summary.json');metrics=read_json(BASE/'heldout_class_metrics.json')['metrics']['test'];audit=read_json(BASE/'pair_audit_results.json');reprun=read_json(BASE/'computational_reproducibility.json');model=read_json(BASE/'class_model_selection.json');parents=read_json(BASE/'corroborated_parent_assignments.json')
    byclass=defaultdict(list)
    for r in parents:
        if r['structural_class']:byclass[r['structural_class']].append(r)
    core={}
    for cid,rr in byclass.items():
        tt=[r for r in rr if r['split']=='test'];caps=set(r['folio_component'] for r in tt)
        if len(tt)>=req['each_core_class_test_instances_at_least'] and len(caps)>=req['each_core_class_test_captions_at_least'] and model['structural_classes'][cid]['training_captions']>=req['each_core_class_training_captions_at_least']:
            core[cid]=dict(**model['structural_classes'][cid],corroborated_test_instances=len(tt),corroborated_test_captions=len(caps),corroborated_total_instances=len(rr))
    coverage=sum(r['split']=='test' and bool(r['structural_class']) for r in parents)/metrics['clear_components']
    gates=dict(source_rows=ext['row_proposals']>=req['source_rows_reviewed_at_least'],source_views=ext['reviewed_views']>=req['source_views_at_least'],fresh_test_captions=metrics['caption_groups']>=req['test_caption_groups_at_least'],recurring_core_classes=len(core)>=req['stable_recurring_structural_classes_at_least'],source_pair_agreement=audit['positive_agreement']>=req['source_pair_audit_positive_agreement_at_least'],source_judged_negative_false_acceptance=audit['false_acceptance_among_source_judged_different_pairs']<=req['hard_negative_false_acceptance_at_most'],threshold_assignment_stability=metrics['threshold_assignment_stability']>=req['threshold_assignment_stability_at_least'],corroborated_test_coverage=coverage>=req['clear_test_component_assignment_coverage_at_least'],computational_reproducibility=reprun['same_test_classes_and_abstentions'] and reprun['model_unchanged'])
    assert all(gates.values()),gates
    # Split independence uses source caption grouping, not inherited language/hand metadata.
    capsplit={s:set(v['folio_component'] for v in plan['selected_views'] if v['split']==s) for s in ['train','validation','test']}
    assert not(capsplit['train']&capsplit['test'] or capsplit['validation']&capsplit['test'] or capsplit['train']&capsplit['validation'])
    assert len({r['parent_id'] for r in parents})==len(parents)
    qualification=dict(time_utc=datetime.now(timezone.utc).isoformat(),gates=gates,registered_requirements=req,corroborated_test_coverage=coverage,core_classes=core,heldout_point_metrics=metrics,pair_point_metrics=audit,caption_split_counts={s:len(c) for s,c in capsplit.items()},qualification_scope='Reproducible image-derived structural candidates on selected ordinary fields. Not an alphabet, word segmentation, full writing recall, independent-rater consensus or positional replication.',row_review_scope='918 source row proposals received writing-field triage; fine contacts judged via native parents/perturbations and sampled native RGB pairs, not exhaustive adjudication of every full row.',negative_definition='True negatives are source-judged different pairs; classifier-different near neighbors cannot serve as their own ground truth. Point criteria apply; small-caption confidence intervals remain broad.')
    write_json(TEST/'freeze_qualification_v3.json',qualification)
    DEST.mkdir(exist_ok=True)
    atlas=[];gal=OUT/'figures/recurrence_v3/neutral_atlas';gal.mkdir(parents=True,exist_ok=True)
    for cid,info in sorted(model['structural_classes'].items()):
        rr=byclass.get(cid,[]) or [r for r in parents if r.get('proposed_class')==cid];examples=[]
        for split,quota in [('train',5),('validation',2),('test',5)]:
            seen=set()
            for r in rr:
                if r['split']!=split or r['folio_component'] in seen:continue
                examples.append(r);seen.add(r['folio_component'])
                if len(seen)>=quota:break
        canvas=Image.new('RGB',(1800,520),'white');draw=ImageDraw.Draw(canvas);draw.text((8,5),f"{cid}: {info['source_structure']} | stable raster holes={info['significant_holes']} | {'held-out recurring core' if cid in core else 'experimental / primary unknown'}",fill='black')
        for j,r in enumerate(examples):
            xx=(j%6)*300;yy=(j//6)*235+40;im=Image.open(OUT/r['native_crop']);sc=min(3.,285/im.width,175/im.height);im=im.resize((round(im.width*sc),round(im.height*sc)),Image.Resampling.NEAREST);canvas.paste(im,(xx,yy));draw.text((xx,yy+185),f"{r['split']} {r['view_id']} caption {r['folio_component']}",fill='black')
        path=gal/f'{cid}.png';canvas.save(path)
        atlas.append(dict(class_id=cid,**info,primary_status='heldout_recurring_structural_core' if cid in core else 'experimental_unknown',examples=[dict(parent_id=r['parent_id'],native_source=r['native_source'],native_bbox=r['native_bbox'],native_crop=r['native_crop'],split=r['split'],folio_component=r['folio_component']) for r in examples],figure=path.relative_to(OUT).as_posix(),atomicity='unknown',pen_lifts='unknown',compounds='Whole parent; lower/upper factor descriptors do not establish internal grapheme cuts',allography='Visual nuisance hypothesis only; no linguistic equivalence asserted'))
    write_json(DEST/'neutral_structural_atlas.json',atlas)
    contract=dict(version='V3 source-only recurrence model',v2_immutable=True,unit_definition='Whole native connected raster parent, source-field writing candidate, contrast/topology/connectivity corroboration, neutral structural class or unknown',source_basis='204 highest-available Yale native captures indexed; V3 ordinary corpus 49 captures, 918 row proposals, 899 retained local writing fields, 20037 unique proposed parents. Across both candidate stages, 61 captures/1184 proposals received field triage.',classes='15 source-atlas classes with 14 held-out recurring core classes; one experimental class remains unknown for primary assignment. Prior 178-class candidate and all ambiguity preserved.',recurrence='Training-only class definitions sealed before fresh seven-caption test assignments. Qualification uses held-out image recurrence, native pair judgments, perturbation stability, factor coherence and deterministic re-execution.',group_boundaries='0.35/0.55/0.75 body-gap competing hypotheses. Complete retained parent list does not certify a complete physical writing group; detached tiny marks and omissions remain possible. Space-delimited groups are not assumed words.',parent_atomicity='unknown: a connected parent may be a compound or ligature; detached attachments, stroke order and pen lifts unresolved',row_extent='unknown: safe writing fields are local source coverage, not actual line endpoints; no normalized rank/pixel position included in this version',physical_identity='Caption/capture grouping only, not certified physical panels/bifolios. Unresolved wide capture and curved/rotated writing remain unknown.',source_ownership='Field writing candidate; many full-row/drawing contacts remain unknown. Source-only visual-unit work has not recovered complete writing recall.',forbidden_inputs='No EVA/RF/v101, Currier, inherited hand/section, positional outcomes or minimal-pair existence used to define classes. Root comparison files integrity-hashed only.',downstream='No positional rerun. This freeze qualifies local structural recurrence; downstream assays still require adequate complete group/line coverage.',validation_limits='Single source adjudicator. Broad caption bootstrap intervals; registered point gates passed. No inter-rater or manuscript-population accuracy claim.')
    write_json(DEST/'model_contract.json',contract);write_json(DEST/'source_parent_segmentation.json',parents);write_json(DEST/'competing_group_hypotheses.json',read_json(BASE/'competing_group_hypotheses.json'));write_json(DEST/'source_row_fields.json',read_json(BASE/'source_rows.json'));write_json(DEST/'freeze_qualification.json',qualification)
    sources=read_csv(OUT/'data/source/yale_native_all_manifest.csv');present={v['view_id'] for v in plan['selected_views']};write_json(DEST/'all_capture_index.json',[dict(view_id=s['view_id'],native_source=s['path'],writing_model_status='V3 selected ordinary fields; other writing unknown' if s['view_id'] in present else 'V3 writing membership/unit classification unknown; immutable V2 source evidence retained separately') for s in sources])
    htmltext='<!doctype html><html><meta charset="utf-8"><title>V3 neutral structural atlas</title><style>body{font:17px system-ui;max-width:1400px;margin:30px auto;color:#252525}img{max-width:100%}article{border-top:1px solid #ccc;padding:24px 0}</style><h1>V3 neutral structural atlas</h1><p>Source-derived whole-parent hypotheses. Fourteen classes recur on fresh held-out imagery. No letters, wordhood, pen lifts or internal grapheme cuts are asserted. Width/slant/ink density may vary; topology and added connected traces preserve competing classes. Experimental and unresolved instances remain unknown.</p>'
    for a in atlas:htmltext+=f"<article><h2>{a['class_id']} — {html.escape(a['source_structure'])}</h2><p>{a['primary_status']}; raster holes {a['significant_holes']}; train captions {a['training_captions']}</p><img src='../figures/recurrence_v3/neutral_atlas/{a['class_id']}.png'></article>"
    (OUT/'reports/12_neutral_structural_atlas_v3.html').write_text(htmltext+'</html>',encoding='utf-8')
    print('Qualification passed',len(core),'core classes; corroborated test coverage',coverage,'older freezes/originals unchanged',flush=True)

if __name__=='__main__':main()
