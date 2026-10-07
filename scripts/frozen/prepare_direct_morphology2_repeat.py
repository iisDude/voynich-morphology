from direct_morphology2_common import *
from prepare_direct_morphology2_pairs import gallery
import numpy as np
def main():
    guard(); verify_seal(D/'RATING_SEAL.json'); assert not (D/'REPEAT_POOL_SEAL.json').exists()
    n=read_json(D/'OPENED_PAIRS.json')['final_used_n']; rng=np.random.default_rng(read_json(D/'PLAN.json')['seed']+1)
    pool=read_json(D/'pair_pool_hidden_key.json')['pairs']; selected=rng.choice(n,20,replace=False); rows=[]; key=[]
    for k,i in enumerate(selected):
        p=pool[int(i)]; sides=[p['left_index'],p['right_index']]; rng.shuffle(sides)
        rows.append(dict(pair_id=f'R{k+1:02d}',display_indices=sides))
        key.append(dict(repeat_id=f'R{k+1:02d}',original_pair_id=p['pair_id']))
    gallery(rows,read_json(D/'source_location_aids.json')['parents'],'blind_repeat')
    save(D/'repeat_hidden_key.json',dict(pairs=key,selection='Uniform seeded20 from all opened pairs, including partial and unresolved; no outcome filter',same_AI=True,global_memory_blinding_not_claimed=True))
    seal([D/'repeat_hidden_key.json',OUT/'src/prepare_direct_morphology2_repeat.py']+list(G.glob('blind_repeat_*.png')),D/'REPEAT_POOL_SEAL.json')
    print('Anonymous repeat set prepared without opening predictions')
if __name__=='__main__':main()
