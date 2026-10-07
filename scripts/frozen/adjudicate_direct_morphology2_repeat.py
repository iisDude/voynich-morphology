from direct_morphology2_common import *
from collections import Counter
from sklearn.metrics import cohen_kappa_score
RATINGS=[0,1,1,2,0,1,0,1,1,0,0,0,1,1,1,0,1,1,1,1]
def main():
    guard(); verify_seal(D/'REPEAT_POOL_SEAL.json'); assert not (D/'REPEAT_SEAL.json').exists()
    save(D/'repeat_source_ratings.json',dict(rated_at_utc=now(),pairs=[dict(repeat_id=f'R{i+1:02d}',rating=r) for i,r in enumerate(RATINGS)],source_RGB_only=True,old_rating_key_and_predictions_hidden_during_rating=True,separation='Intervening 1437 candidate representation replay; same-session memory persists',same_AI_only=True))
    seal([D/'repeat_source_ratings.json'],D/'REPEAT_RATINGS_SEAL.json')
    old={r['pair_id']:r['rating'] for r in read_json(D/'source_similarity_decisions.json')['pairs']}; key=read_json(D/'repeat_hidden_key.json')['pairs']; rows=[dict(**k,first=old[k['original_pair_id']],repeat=RATINGS[i]) for i,k in enumerate(key)]; a=[str(r['first']) for r in rows]; b=[str(r['repeat']) for r in rows]
    save(T/'same_adjudicator_repeatability.json',dict(n=20,exact_agreement_n=sum(x==y for x,y in zip(a,b)),exact_agreement=sum(x==y for x,y in zip(a,b))/20,unweighted_kappa=float(cohen_kappa_score(a,b)),transitions=dict(Counter(f'{x}->{y}' for x,y in zip(a,b))),pairs=rows,independent_interrater_validation=False,independent_human_validation=False,separation_period_seconds=None,limitation='Short same-session separation with hidden prior decisions; memory carryover possible. Twenty pairs are a small repeatability diagnostic; no success gate was assigned.'))
    seal([D/'repeat_source_ratings.json',D/'REPEAT_RATINGS_SEAL.json',T/'same_adjudicator_repeatability.json',OUT/'src/adjudicate_direct_morphology2_repeat.py'],D/'REPEAT_SEAL.json'); print('Repeat ratings sealed; no predictions opened')
if __name__=='__main__':main()
