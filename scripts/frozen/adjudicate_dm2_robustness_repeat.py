from dm2_robustness_common import *
VALUES='''2 0 2 1 1 1 2 0 1 0 1 1
2 2 1 1 0 1 1 0 1 1 1 0
0 2 2 2 1 0 1 1 2 0 2 0
0 0 1 1 0 0 0 2 1 0 1 2
2 0 0 1 1 0 0 1 0 0 0 0
2 1 1 1 0 0 1 0 1 1 1 0
2 1 0 2 1 2 2 1 0 1 2 1
0 1 1 1 1 1 0 1 0 2 0 0
0 2 0 0 2 0 0 0 0 2 2 0
1 1 1 2 1 1 0 1 0 2 1 1
2 1 0 2 1'''.split()
def main():
    guard();verify_seal(D/'REPEAT_POOL_SEAL.json');verify_seal(D/'SUBSET_SEAL.json');assert not (D/'REPEAT_RATINGS_SEAL.json').exists();assert len(VALUES)==125
    save(D/'repeat_source_ratings.json',dict(rated_at_utc=now(),pairs=[dict(repeat_id=f'J{i+1:03d}',rating=int(v) if v!='U' else 'U') for i,v in enumerate(VALUES)],native_RGB_only=True,prior_ratings_original_IDs_and_distances_hidden_during_review=True,all_11_anonymous_galleries_reviewed=True,old_exposure_not_erased=True,same_AI_not_independent_human=True,separation='Intervening sealed matching/source-integrity preparation; new IDs and shuffled sides. Same-session/conversation memory may persist.'))
    seal([D/'repeat_source_ratings.json',OUT/'src/adjudicate_dm2_robustness_repeat.py'],D/'REPEAT_RATINGS_SEAL.json');print('All125 anonymous source judgments sealed before robustness metrics or prior-label comparison',flush=True)
if __name__=='__main__':main()
