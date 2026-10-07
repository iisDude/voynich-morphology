"""Registered positional question, only after the source-only v2 freeze."""
from common import OUT,read_json,write_json,write_csv,sha256
from structural_assays import pair_assay
from collections import Counter
from datetime import datetime,timezone
import sys

DEST=OUT/'tests/adjudicated_currier_B_v2'
def register():
    DEST.mkdir(exist_ok=True)
    if (DEST/'analysis_plan.json').exists():raise ValueError('Already registered')
    write_json(DEST/'analysis_plan.json',dict(registered_at_utc=datetime.now(timezone.utc).isoformat(),question='Do single manuscript-derived unit changes at group edges versus interiors differ in mean position in Currier B?',primary=dict(minimum_frequency=8,edge_width=2,length_min=5),sensitivities=dict(frequencies=[5,8,10,12],edge_widths=[1,2],length_min=5),representations=['visual_fine_units','visual_merged_units','visual_factored_units'],endpoints=['normalized_group_rank','normalized_pixel_center'],cohort='Exact same source-eligible fully admitted group occurrences for both endpoints; all original unknown slots retained in rank and native extent; Currier inherited metadata attached only after freeze',split_cohorts=['all source reviewed, post-exposure diagnostic','train+validation','test captions'],statistics='Existing registered OLS displacement~edge+length+log geometric mean frequency, HC3; connected-family clustered uncertainty only at >=10 clusters; min12 pairs/full design rank; 199 joint caption-block bootstrap and 199 within-line position-slot null when estimable',negative_result_policy='No eligible repeated minimal pairs/design rank => not estimable, not absence of effect. Do not lower thresholds or change segmentation after results.',controls='Previously documented natural-language ordinal controls retained as external reference; no measured-image controls falsely manufactured from ordinal spacing; if native visual primary not estimable, new control calibration cannot validate it',method_limits='Connected raster parent/image family is a visual hypothesis, not certified letter. Row/group extents and split coverage remain partial. Currier labels not independently inferred from source. Heldout figures are diagnostics after prior exposure.'))
    print('Registered before freeze')

def main():
    freeze=OUT/'data/observations/visual_dataset_v2/FREEZE_MANIFEST.json';plan=read_json(DEST/'analysis_plan.json');manifest=read_json(freeze)
    for r in manifest['files']:
        if sha256(OUT/r['path'])!=r['sha256']:raise ValueError('Frozen content changed '+r['path'])
    source=read_json(OUT/'data/observations/visual_dataset_v2/assay_groups_source_only.json')
    # Only page-level metadata copied; no conventional strings used as units or positions.
    inherited=read_json(OUT/'data/comparisons/v11/visual_groups_with_metadata.json');meta={}
    for r in inherited:meta.setdefault(r['view_id'],{k:r.get(k) for k in ['currier','hand','section']})
    attached=[dict(g,**meta.get(g['view_id'],{})) for g in source];write_json(DEST/'groups_with_postfreeze_metadata.json',attached);results=[];primary_pairs=[];coverage=[]
    for rep in plan['representations']:
        rows=[dict(g,units=g[rep]) for g in attached if g['primary_eligible'] and g.get(rep) and g.get('currier')=='B' and g.get('normalized_group_rank') is not None and g.get('normalized_pixel_center') is not None]
        coverage.append(dict(representation=rep,B_groups=len(rows),B_lines=len({g['line_id'] for g in rows}),B_captions=len({g['folio_component'] for g in rows}),splits=dict(Counter(g['split'] for g in rows)),distinct_forms=len({tuple(g['units']) for g in rows})))
        for cohort in ['all','train_validation','test']:
            rr=rows if cohort=='all' else [g for g in rows if g['split'] in (['train','validation'] if cohort=='train_validation' else ['test'])]
            for position in plan['endpoints']:
                for frequency in plan['sensitivities']['frequencies']:
                    for edge in plan['sensitivities']['edge_widths']:
                        result,pairs=pair_assay(rr,position,minimum=frequency,edge_width=edge,length_min=5,iterations=199)
                        result.update(representation=rep,cohort=cohort,groups=len(rr),primary_setting=frequency==8 and edge==2,freeze_sha256=sha256(freeze));results.append(result)
                        if result['primary_setting']:primary_pairs.extend(dict(r,representation=rep,cohort=cohort,position=position) for r in pairs)
    write_json(DEST/'coverage.json',coverage);write_json(DEST/'results.json',results);write_json(DEST/'primary_pairs.json',primary_pairs)
    write_csv(DEST/'results.csv',[{k:r.get(k) for k in ['representation','cohort','position','minimum_frequency','edge_width','length_min','groups','pairs','status','beta','p_hc3','family_cluster_p','primary_setting']} for r in results])
    after=[]
    for r in manifest['files']:
        if sha256(OUT/r['path'])!=r['sha256']:after.append(r['path'])
    write_json(DEST/'run_manifest.json',dict(started_after_source_freeze=True,completed_at_utc=datetime.now(timezone.utc).isoformat(),freeze_sha256=sha256(freeze),source_groups_sha256=sha256(OUT/'data/observations/visual_dataset_v2/assay_groups_source_only.json'),analysis_plan_sha256=sha256(DEST/'analysis_plan.json'),metadata_source='data/comparisons/v11/visual_groups_with_metadata.json; copied Currier/hand/section only',metadata_source_sha256=sha256(OUT/'data/comparisons/v11/visual_groups_with_metadata.json'),same_matched_occurrences_for_both_endpoints=True,assays=len(results),frozen_integrity_failures=after,no_segmentation_retuning=True))
    if after:raise ValueError('Frozen model changed during assay')
    print('Coverage',coverage,'primary',[(r['representation'],r['cohort'],r['position'],r['status'],r['pairs']) for r in results if r['primary_setting']],flush=True)
if __name__=='__main__':register() if '--register' in sys.argv else main()
