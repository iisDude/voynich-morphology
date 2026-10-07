from inventory_v6_common import *
SAME=[2,4,5,7,8,9,12,15,16,18,19,20]
DIFFERENT=[3,13,17]
UNKNOWN=[1,6,10,11,14]
def main():
    guard()
    decisions=[dict(pair_id=f'Q{i:03d}',judgment='same_whole_source_organization' if i in SAME else 'different_whole_source_organization' if i in DIFFERENT else 'unresolved_source_organization',note='Native RGB comparison; cavity/branch/bridge geometry without letters or stroke-order inference.') for i in range(1,21)]
    challenge=[dict(pair_id=f'C{i:03d}',judgment='unresolved_cavity_placement' if i in [7,9] else 'different_whole_source_organization',general_stacked_lobe_resemblance=i in [7,9],note='Compact rings and paired uprights differ from stacked-lobe prototype. Two broadly similar lobe pairs do not establish matching cavity placement from these crops.') for i in range(1,11)]
    save(D/'masked_native_pair_decisions.json',dict(created_at_utc=now(),nonmember_retrieval_pairs=decisions,unaccepted_candidate_challenges=challenge,adjudicator='Same AI source adjudicator; prior image familiarity persists. Randomized pair identities and class suggestions hidden in image. Pair pool types were known from the empty accepted pool; not fully blinded independent validation.',formal_accepted_positive_audit_n=0,formal_false_grouping_denominator=0,diagnostic_not_acceptance_evidence=True))
    seal([D/'masked_native_pair_decisions.json',Path(__file__)],D/'PAIR_DECISION_SEAL.json');print('Source diagnostic comparisons recorded; no accepted-positive audit fabricated',flush=True)
if __name__=='__main__':main()
