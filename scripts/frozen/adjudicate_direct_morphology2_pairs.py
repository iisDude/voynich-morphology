from direct_morphology2_common import *
from collections import Counter
INITIAL='''0 1 0 0 2 1 0 0 0 1 1 2
0 2 0 0 1 0 2 1 1 0 0 1
1 0 1 0 0 1 0 1 1 2 0 0
0 1 1 0 1 1 1 2 0 0 1 1
0 1 1 1 1 0 1 0 2 0 0 1
1 0 0 0 1 0 1 2 1 1 0 0
0 0 1 0 0 0 1 0 1 1 0 0
1 0 0 0 0 2 1 0 0 1 1 2
1 1 2 2 1 0 1 1 1 2 0 0
0 1 0 0 1 2 0 2 1 2 0 1
0 1 1 1 1 0 0 0 2 1 0 0
1 1 0 0 2 1 1 0 0 1 0 0
1 0 0 2 1 1 0 0 1 0 1 2
0 1 0 1 1 0 1 0 2 0 1 0
0 2 0 2 0 0 0 0 1 0 0 1
1 0 0 0 0 0 0 0 1 0 1 1
1 0 0 0 1 0 1 0 1 0 1 1
1 2 0 0 0 0 0 2 0 1 0 1
1 1 0 1 0 0 0 0 0 1 0 1
1 0 0 0 0 1 1 1 1 1 0 0'''.split()
def record(batch,values,start):
    guard();verify_seal(D/'PAIR_POOL_SEAL.json');assert not (D/'RATING_SEAL.json').exists();p=D/f'pair_ratings_batch{batch}.json';assert not p.exists();save(p,dict(decided_at_utc=now(),pairs=[dict(pair_id=f'Q{start+i:03d}',rating=int(v) if v!='U' else 'U') for i,v in enumerate(values)],source_RGB_only=True,predictions_and_V3_hidden=True,same_AI_not_independent_interrater=True));seal([p],D/f'RATING_BATCH{batch}_SEAL.json');allrows=[r for p in sorted(D.glob('pair_ratings_batch*.json')) for r in read_json(p)['pairs']];key={r['pair_id']:r for r in read_json(D/'pair_pool_hidden_key.json')['pairs']};counts=Counter(r['rating'] for r in allrows);cats={v:set(c for r in allrows if r['rating']==v for c in [key[r['pair_id']]['caption_left'],key[r['pair_id']]['caption_right']]) for v in [0,2]};support=counts[0]+counts[2]>=120 and counts[0]>=30 and counts[2]>=30 and len(cats[0]|cats[2])>=6 and all(len(cats[v])>=4 for v in [0,2]);opened=read_json(D/'OPENED_PAIRS.json');save(T/f'rating_support_after_batch{batch}.json',dict(ratings_n=len(allrows),counts={str(k):v for k,v in counts.items()},endpoint_caption_counts={str(v):len(cats[v]) for v in [0,2]},sample_support_reached=support,morphology_metrics_unopened=True))
    if support:
        save(D/'source_similarity_decisions.json',dict(sealed_at_utc=now(),pairs=allrows,source_rubric=read_json(D/'PLAN.json')['pair_sampling']['ratings'],predictions_unopened=True,same_AI_not_independent_interrater=True));seal([D/'source_similarity_decisions.json']+list(D.glob('pair_ratings_batch*.json'))+list(D.glob('RATING_BATCH*_SEAL.json')),D/'RATING_SEAL.json');opened['final_used_n']=len(allrows);opened['sample_support_reached']=True;save(D/'OPENED_PAIRS.json',opened);print('Final source ratings sealed',dict(counts),'n',len(allrows),flush=True)
    else:
        pool_n=read_json(D/'PAIR_PROTOCOL.json')['pool_n'];next_n=min(pool_n,len(allrows)+120);opened['extensions'].append(dict(after_batch=batch,source_binary_n=counts[0]+counts[2],same_n=counts[2],different_n=counts[0],next_used_n=next_n,rule='Registered support-only deterministic next120; no morphology results'));opened['used_n']=next_n;save(D/'OPENED_PAIRS.json',opened);print('Registered extension required',dict(counts),'next',len(allrows)+1,'to',next_n,flush=True)
if __name__=='__main__':assert len(INITIAL)==240;record(1,INITIAL,1)
