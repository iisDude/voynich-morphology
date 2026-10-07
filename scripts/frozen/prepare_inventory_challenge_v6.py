"""Post-inference retrieval diagnostic; never accepted assignment evidence."""
from inventory_v6_common import *
from validate_inventory_candidates_v6 import pair_gallery
from collections import defaultdict
import numpy as np
def main():
    guard();aa=read_json(D/'fresh_assignments.json');train=read_json(D/'discovery_parents.json');by=defaultdict(list)
    for r in aa:
        if r['source_resolved'] and r['distance'] is not None:by[r['caption']].append(r)
    pairs=[]
    for cap in ['16','47','94']:
        chosen=sorted(by[cap],key=lambda r:(r['distance'],r['parent_id']))[:4 if cap=='47' else 3]
        for r in chosen:pairs.append(dict(kind='unaccepted_nearest_candidate_challenge',candidate=r['candidate'],left=r['parent_id'],right=train[r['nearest_training_index']]['parent_id'],distance=r['distance']))
    rng=np.random.default_rng(20261012);rng.shuffle(pairs)
    for i,p in enumerate(pairs):p['pair_id']=f'C{i+1:03d}'
    # Reuse image layout while keeping prior galleries unchanged.
    gallery=G/'heldout_pairs_01.png';original=gallery.read_bytes();pair_gallery(pairs,train);(G/'unaccepted_candidate_challenge.png').write_bytes(gallery.read_bytes());gallery.write_bytes(original)
    save(D/'unaccepted_candidate_challenge_key.json',dict(created_at_utc=now(),pairs=pairs,registered_acceptance_audit=False,reason='No nominal accepted fresh NC02 parent exists. Balanced nearest retrieval is a source-form failure diagnostic only; cannot manufacture10 accepted positives or enlarge model radius.'))
if __name__=='__main__':main()
