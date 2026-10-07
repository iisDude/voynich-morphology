from feature_trial2_common import *
from PIL import Image,ImageDraw
import numpy as np
RATINGS='''1 2 1 1 1 1 2 2 0 0 2 1
2 1 0 1 1 0 0 1 0 0 2 0
2 1 2 0 1 2 0 2 2 0 2 0
1 1 1 0 1 0 2 1 2 1 2 2
0 0 0 2 1 2 1 0 0 1 2 1
2 1 0 1 2 2 1 2 2 2 2 0
1 1 1 1 0 0 2 2 0 0 0 0
0 0 1 1 0 2 1 1 2 0 0 0
1 2 2 2 1 2 2 2 2 2 1 2
1 0 0 2 0 1 1 0 1 0 0 2
1 1 2 0 0 1 0 0 0 0 1 0
1 0 1 1 1 1 0 2 0 1 0 1
0 2 1 1 1 2 0 0 2 2 0 2
1 0 1 0 1 2 0 2 2 1 2 0
1 1 0 0 0 1 0 2 1 1 0 0
0 0 0 1 2'''.split()
def main():
    guard();verify_seal(D/'METRIC_SEAL.json');assert not (D/'RATING_SEAL.json').exists();assert len(RATINGS)==185
    save(D/'similarity_decisions.json',dict(decided_at_utc=now(),pairs=[dict(pair_id=f'Q{i+1:03d}',rating=int(v)) for i,v in enumerate(RATINGS)],all_185_native_RGB_pairs_viewed=True,predictions_V3_and_selector_provenance_not_inspected=True,adjudicator='same AI, not independent human inter-rater',rubric='2 whole visual organization compatible;1 partial organization with visible structural differences;0 different organization;U undecidable. Nearest contours do not determine source judgments. Neighboring ink in padded crops is context, not part of parent where extent was source resolved.',source_images='similarity_01 through16.png',uncertainty='Ink variation/fill allowed for2; open/closed/head or stem-count differences only partial unless source ambiguity makes them undecidable. Ratings are subjective source comparisons, not transitive equivalence classes.'))
    seal([D/'similarity_decisions.json',OUT/'src/adjudicate_feature_trial2_pairs.py'],D/'RATING_SEAL.json')
    # Repeated pair display hides original IDs, ratings and predictions.
    key=read_json(D/'similarity_hidden_key.json')['pairs'];rec=read_json(D/'source_location_aids.json')['parents'];rng=np.random.default_rng(read_json(D/'PLAN.json')['seed']+1);chosen=rng.choice(len(key),12,replace=False);pp=[];canvas=Image.new('RGB',(1440,940),'#eee');dr=ImageDraw.Draw(canvas)
    for j,k in enumerate(chosen):
        q=key[int(k)];idx=q['display_indices'][::-1] if rng.random()<.5 else q['display_indices'];rid=f'R{j+1:03d}';pp.append(dict(repeat_id=rid,original_pair_id=q['pair_id'],indices=idx));x=j%3*480;y=j//3*235;dr.text((x+5,y+4),rid,fill='black')
        for side,i in enumerate(idx):
            im=Image.open(OUT/rec[i]['native_crop']).convert('RGB');sc=min(3,225/im.width,195/im.height);im=im.resize((max(1,round(im.width*sc)),max(1,round(im.height*sc))),Image.Resampling.NEAREST);canvas.paste(im,(x+5+side*235,y+27))
    canvas.save(G/'repeat_similarity.png');save(D/'repeat_hidden_key.json',dict(created_at_utc=now(),pairs=pp,registered_n=12,selection='fixed seed+1; no rating-based selection',separation='Intervening source-feature implementation/replay work; no independent observer or memory washout claim'))
    print('185 source pair judgments sealed; anonymous12 pair repeat prepared',flush=True)
if __name__=='__main__':main()
