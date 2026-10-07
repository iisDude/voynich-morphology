"""Explicit visual outcomes, preserving every sampled admitted candidate."""
from common import OUT,read_json,write_json,write_csv,SEED
import numpy as np

# Crop review is deliberately conservative. Incompatible/multiple-row crops
# count against source precision even when some writing is visible.
FAIL={96:'paint and text coexist; assigned assembly extent incompatible',
      98:'two neighboring rows in crop; single assembly extent incompatible',
      111:'neighboring row/compound extent incompatible',
      114:'neighboring row/compound extent incompatible',
      121:'drawing/texture trace, no unambiguous writing assembly',
      128:'blank/faint texture; no unambiguous writing assembly',
      139:'tiny blank/texture fragment',144:'tiny brown/texture trace without recognizable writing',
      167:'mostly blank extent with isolated tail; incompatible assembly',
      182:'blank texture',183:'large blank/texture extent surrounding low loop',
      195:'blank texture'}
AMBIG={3,6,7,14,16,36,40,41,50,55,68,71,97,123,165,168,169,175,179,194}

def main():
    path=OUT/'data/observations/heldout_source_audit_v4.json';rows=read_json(path)
    for r in rows:
        n=int(r['audit_id'][1:]);r['outcome']='failure' if n in FAIL else 'ambiguous' if n in AMBIG else 'writing_visible'
        r['review_note']=FAIL.get(n,'Faint, fragmented or incompatible with nearest-family identity; source quality uncertain.' if n in AMBIG else
            'Writing is visible; this does not establish atomic-unit identity or validate assigned family homology.')
        r['reviewer']='Codex source-crop visual audit'
    write_json(OUT/'data/observations/heldout_source_audit_v4_reviewed.json',rows)
    results=[];rng=np.random.default_rng(SEED)
    for split in ('validation','test'):
        rr=[r for r in rows if r['split']==split];views=sorted(set(r['view_id'] for r in rr))
        perview=[np.mean([r['outcome']=='writing_visible' for r in rr if r['view_id']==v]) for v in views]
        boot=np.mean(rng.choice(perview,(2000,len(perview)),replace=True),axis=1)
        results.append(dict(split=split,sampled_views=len(views),sampled_instances=len(rr),
            writing_visible=sum(r['outcome']=='writing_visible' for r in rr),
            failures=sum(r['outcome']=='failure' for r in rr),ambiguous=sum(r['outcome']=='ambiguous' for r in rr),
            equal_view_writing_visible_fraction=float(np.mean(perview)),
            view_bootstrap_lower=float(np.quantile(boot,.025)),view_bootstrap_upper=float(np.quantile(boot,.975)),
            status='source gate admits errors; atomic identity not validated'))
    write_csv(OUT/'reports/heldout_source_audit_v4_results.csv',results)
    write_json(OUT/'reports/heldout_source_audit_v4_results.json',dict(results=results,
        limitations=['Single reviewer; no inter-annotator agreement estimate.',
            'Only sampled admitted instances: recall and rejected-writing fraction are not estimable.',
            'Random view selection yielded early manuscript views; later section coverage is not established.',
            'View bootstrap has only 4/6 clusters and is descriptive; bifolio independence unresolved.',
            'No threshold refit using held-out outcomes; all failures retained.']))
    print(results)

if __name__=='__main__':main()
