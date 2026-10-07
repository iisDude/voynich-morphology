from common import OUT,read_json,write_json,write_csv,SEED
import numpy as np

FAIL={30:'tiny blank/texture fragment',36:'tiny blank/texture fragment',57:'blank/texture strip',82:'paint/texture fragment',105:'tiny blank/texture fragment',113:'multiple neighboring rows; incompatible single assembly extent'}
AMBIG={5,35,39,40,44,52,62,63,64,68,75,77,100,102,118,127}
MERGE_MISMATCH={6,18,49,99,100,113,114,119}

def main():
    root=OUT/'data/observations/visual_dataset_v0';rows=read_json(root/'fine_source_audit.json')
    for r in rows:
        n=int(r['audit_id'][1:]);r['outcome']='failure' if n in FAIL else 'ambiguous' if n in AMBIG else 'writing_visible'
        r['review_note']=FAIL.get(n,'Faint or small fragment, incomplete shape or unclear assigned extent.' if n in AMBIG else 'Writing visible; raster/atomic boundary remains unverified.')
        r['merge_hypothesis_outcome']='visibly_incompatible' if n in MERGE_MISMATCH else 'not_resolved' if r['outcome']!='writing_visible' else 'compatible_at_broad_shape_level_only'
    write_json(root/'fine_source_audit_reviewed.json',rows)
    views=sorted(set(r['view_id'] for r in rows));rates=[np.mean([r['outcome']=='writing_visible' for r in rows if r['view_id']==v]) for v in views]
    rng=np.random.default_rng(SEED);boot=rng.choice(rates,(2000,len(rates)),replace=True).mean(axis=1)
    result=dict(test_views=len(views),instances=len(rows),writing_visible=sum(r['outcome']=='writing_visible' for r in rows),
        failures=len(FAIL),ambiguous=len(AMBIG),visibly_incompatible_merge_assignments=len(MERGE_MISMATCH),
        equal_view_writing_visible_fraction=float(np.mean(rates)),view_bootstrap_interval=[float(np.quantile(boot,.025)),float(np.quantile(boot,.975))],
        status='source gate and homology assignments admit errors; no recovered alphabet',
        limitations=['One reviewer; moderate sample; no recall or boundary-accuracy ground truth.',
            'Raw bins and proposed merges can both misclassify unfamiliar shapes.',
            'Source crops show surrounding ink as well as the assigned component.',
            'Caption grouping does not settle physical panel or bifolio independence.'])
    write_json(root/'fine_source_audit_summary.json',result);print(result)

if __name__=='__main__':main()
