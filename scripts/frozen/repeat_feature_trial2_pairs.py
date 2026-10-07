from feature_trial2_common import *
def main():
    guard();assert not (D/'REPEAT_SEAL.json').exists();verify_seal(D/'RATING_SEAL.json')
    ratings=[0,0,2,1,2,2,2,1,2,0,1,1]
    save(D/'repeat_decisions.json',dict(decided_at_utc=now(),pairs=[dict(repeat_id=f'R{i+1:03d}',rating=v) for i,v in enumerate(ratings)],source_gallery='figures/neutral_feature_trial2/repeat_similarity.png',prior_pair_ids_and_ratings_not_displayed=True,separation='Intervening measurement replay and source/metric invariant checks; short same-session separation. Prior conversational exposure cannot be erased.',independent_interrater=False,adjudicator='Same AI, not independent human rater'))
    seal([D/'repeat_decisions.json',D/'repeat_hidden_key.json',G/'repeat_similarity.png',OUT/'src/repeat_feature_trial2_pairs.py'],D/'REPEAT_SEAL.json')
if __name__=='__main__':main()
