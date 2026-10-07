"""Post-freeze geometry variation inside neutral source-family hypotheses."""
from common import OUT,read_json,write_json,write_csv,sha256,SEED
from collections import defaultdict,Counter
from itertools import combinations
import numpy as np

FEATURES=['height_ratio','width_ratio','upper_extent_ratio','lower_extent_ratio','raster_loops','skeleton_branch_clusters']

def main():
    metadata={r['group_id']:r for r in read_json(OUT/'data/comparisons/v2/visual_groups_with_metadata.json')};review={r['family_id']:r for r in read_json(OUT/'data/observations/fine_family_source_review_v4.json')['records']}
    samples=[]
    for path in sorted((OUT/'data/observations/regional_candidates_v4').glob('V_*.json')):
        if not path.stem[2:].isdigit():continue
        obj=read_json(path);assign=read_json(OUT/f'data/observations/assigned_visual_candidates_v4/{path.name}')
        for r in obj['instances']:
            if r['model']!='fine_components':continue
            u=assign['units'][r['instance_id']];source_review=review[u['nearest_family_id']]
            if not u['recognized_within_training_radius'] or not source_review['prototype_gate_eligible']:continue
            m=metadata[r['group_id']];samples.append(dict(document=r['folio_component'],view_id=r['view_id'],split=r['split'],family=u['nearest_family_id'],structure=source_review['visual_structure_merge_hypothesis'],
                currier=m.get('currier'),hand=m.get('hand'),section=m.get('section'),rank=m['normalized_group_rank'],pixel_x=m['normalized_pixel_center'],features={k:r['features'][k] for k in FEATURES}))
    grouped=defaultdict(list)
    for r in samples:grouped[r['document'],r['family']].append(r)
    documents=[]
    for (document,family),rr in grouped.items():
        if len(rr)<5:continue
        record=dict(document=document,family=family,structure=rr[0]['structure'],instances=len(rr),features={k:float(np.median([r['features'][k] for r in rr])) for k in FEATURES})
        for k in ('split','currier','hand','section'):
            values={r[k] for r in rr};record[k]=next(iter(values)) if len(values)==1 else None
        documents.append(record)
    contexts=[('currier','all_hands_sections',documents)]
    for currier,hand in sorted(set((r['currier'],r['hand']) for r in documents if r['currier'] and r['hand'])):
        contexts.append(('section',f'currier_{currier}_hand_{hand}',[r for r in documents if r['currier']==currier and r['hand']==hand]))
    for currier,section in sorted(set((r['currier'],r['section']) for r in documents if r['currier'] and r['section'])):
        contexts.append(('hand',f'currier_{currier}_section_{section}',[r for r in documents if r['currier']==currier and r['section']==section]))
    rng=np.random.default_rng(SEED);results=[]
    for field,stratum,rr in contexts:
        for a,b in combinations(sorted(set(r[field] for r in rr if r.get(field))),2):
            for family in sorted(set(r['family'] for r in rr)):
                train={s:{r['document'] for r in rr if r['family']==family and r[field]==s and r['split'] in ('train','validation')} for s in (a,b)}
                # Candidate comparisons selected by training coverage only.
                if min(len(train[a]),len(train[b]))<4:continue
                test={s:[r for r in rr if r['family']==family and r[field]==s and r['split']=='test'] for s in (a,b)}
                base=dict(field=field,stratum=stratum,label_a=a,label_b=b,family=family,training_docs_a=len(train[a]),training_docs_b=len(train[b]),test_docs_a=len(test[a]),test_docs_b=len(test[b]))
                if min(len(test[a]),len(test[b]))<3:results.append(dict(base,status='not_estimable: fewer than three test caption blocks per class'));continue
                for feature in FEATURES:
                    av=np.array([r['features'][feature] for r in test[a]]);bv=np.array([r['features'][feature] for r in test[b]]);effect=float(bv.mean()-av.mean());pooled=np.r_[av,bv];null=[]
                    for _ in range(199):
                        p=rng.permutation(pooled);null.append(float(p[len(av):].mean()-p[:len(av)].mean()))
                    boot=rng.choice(bv,(1000,len(bv)),replace=True).mean(axis=1)-rng.choice(av,(1000,len(av)),replace=True).mean(axis=1)
                    results.append(dict(base,feature=feature,status='estimated exploratory conditional-family geometry',mean_b_minus_a=effect,caption_bootstrap_interval=np.quantile(boot,[.025,.975]).tolist(),p_document_label_null=(1+sum(abs(v)>=abs(effect) for v in null))/200))
    estimated=[r for r in results if r.get('p_document_label_null') is not None];order=sorted(estimated,key=lambda r:r['p_document_label_null']);q=1.
    for i in range(len(order)-1,-1,-1):q=min(q,order[i]['p_document_label_null']*len(order)/(i+1));order[i]['bh_q_exploratory']=q
    # Within-caption matched contextual variation, with ordinal and pixel bins separate.
    variation=[]
    for coordinate in ('rank','pixel_x'):
        buckets=defaultdict(lambda:defaultdict(list))
        for r in samples:
            if r['split']!='test':continue
            band='early' if r[coordinate]<.25 else 'late' if r[coordinate]>.75 else None
            if band:buckets[r['family'],r['document']][band].append(r)
        families=defaultdict(list)
        for (family,document),bands in buckets.items():
            if min(len(bands['early']),len(bands['late']))<3:continue
            delta={k:float(np.median([r['features'][k] for r in bands['late']])-np.median([r['features'][k] for r in bands['early']])) for k in FEATURES};families[family].append((document,delta))
        for family,records in families.items():
            for feature in FEATURES:
                values=np.array([r[1][feature] for r in records]);record=dict(family=family,coordinate=coordinate,feature=feature,paired_test_caption_blocks=len(values),late_minus_early=float(values.mean()),status='estimated exploratory paired geometry' if len(values)>=6 else 'descriptive: fewer than six paired caption blocks')
                if len(values)>=6:
                    boot=rng.choice(values,(1000,len(values)),replace=True).mean(axis=1);null=(values*rng.choice([-1,1],(999,len(values)))).mean(axis=1);record.update(caption_bootstrap_interval=np.quantile(boot,[.025,.975]).tolist(),p_caption_sign_null=(1+sum(abs(v)>=abs(values.mean()) for v in null))/1000)
                variation.append(record)
    root=OUT/'tests/visual_family_stability_v1';root.mkdir(parents=True,exist_ok=True);write_json(root/'results.json',dict(samples=len(samples),document_family_records=len(documents),context_geometry=results,within_caption_context=variation));write_json(root/'document_family_measurements.json',documents)
    write_csv(root/'results.csv',[dict(stratum=r['stratum'],family=r['family'],feature=r.get('feature'),status=r['status'],effect=r.get('mean_b_minus_a'),ci=r.get('caption_bootstrap_interval'),p=r.get('p_document_label_null'),q=r.get('bh_q_exploratory')) for r in results] or [dict(stratum='all',family=None,feature=None,status='not_estimable: training context coverage absent',effect=None,ci=None,p=None,q=None)])
    write_json(root/'config.json',dict(seed=SEED,features=FEATURES,minimum_family_instances_per_caption=5,minimum_training_caption_blocks_per_class=4,minimum_test_caption_blocks_per_class=3,document_null=199,bootstrap=1000,
        restrictions=['Units, geometry and admission gates from original pre-comparison freeze; metadata attached afterward.', 'Conditional raw prototype family is a visual hypothesis, not a known same grapheme.', 'Height/baseline proxies and mask errors can produce apparent variation.', 'Caption blocks are not verified independent physical bifolios; broad Currier contrasts confound hands, sections and source quality.', 'Exploratory multiplicity adjustment only for estimable context-geometry tests; no confirmatory or semantic claims.']))
    write_json(root/'input_manifest.json',dict(visual_freeze_sha256=sha256(OUT/'data/observations/visual_dataset_v0/FREEZE_MANIFEST.json'),postfreeze_metadata_sha256=sha256(OUT/'data/comparisons/v2/visual_groups_with_metadata.json'),source_sha256=sha256(OUT/'src/visual_family_stability_v1.py')))
    (root/'run.py').write_text('from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]/"src"))\nfrom visual_family_stability_v1 import main\nmain()\n',encoding='utf-8')
    (root/'README.md').write_text('# Source-family geometry stability\n\nRun `run.py`. Conditional raw-family median geometry uses one record per caption block. Same-hand section and same-section hand comparisons retain power failures. Ordinal rank and measured line-pixel context are tested separately.\n',encoding='utf-8')
    (root/'summary.md').write_text('# Contextual visual variation\n\nThese tests measure source-derived shape proxies within fixed image-family hypotheses. They do not establish allographs or count historical scribes. Test-only document differences, label/sign nulls and uncertainty are reported, with explicit coverage failures and confounds.\n',encoding='utf-8')
    print('Visual stability',len(samples),'instances',len(results),'context results',len(variation),'paired results',flush=True)

if __name__=='__main__':main()
