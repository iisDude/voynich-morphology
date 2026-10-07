"""Prior-label-hidden same-adjudicator photographic repeat sample."""
from common import OUT,read_json,write_json,sha256,SEED
from register_row_benchmark_v5 import D,T,G
from datetime import datetime,timezone
from PIL import Image,ImageDraw
import numpy as np

def main():
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen(source_stage=True)
    if (D/'REPEAT_REGISTRATION.json').exists():raise RuntimeError('Already registered')
    rows=read_json(D/'development_source_reference.json')['rows']+read_json(D/'heldout_source_reference.json')['rows'];lookup={r['row_id']:r for r in rows};rng=np.random.default_rng(SEED+5);mapping=[]
    for n,rid in enumerate(read_json(D/'PLAN.json')['repeatability']['rows']):
        r=lookup[rid];pick=rng.choice(len(r['objects']),size=min(32,len(r['objects'])),replace=False);rng.shuffle(pick);raw=Image.open(OUT/r['native_source']).convert('RGB');group=f'R{n+1:02d}'
        context=next(x for x in read_json(D/'CONTEXT_EXTENSION.json')['rows'] if x['row_id']==rid)['review_context_bbox'];raw.crop(context).save(G/f'{group}_repeat_context.png')
        can=Image.new('RGB',(1600,4*180),'#eee');dr=ImageDraw.Draw(can)
        for j,index in enumerate(pick):
            p=r['objects'][index];x,y,c,d=p['native_bbox'];anon=f'{group}_{j+1:02d}';mapping.append(dict(anonymous_id=anon,row_id=rid,object_id=p['object_id'],native_bbox=p['native_bbox']))
            box=[max(0,x-12),max(0,y-12),min(raw.width,c+12),min(raw.height,d+12)];im=raw.crop(box);sc=min(4,190/im.width,130/im.height);im=im.resize((max(1,round(im.width*sc)),max(1,round(im.height*sc))),Image.Resampling.NEAREST);a=(j%8)*200;b=(j//8)*180;can.paste(im,(a+3,b+20));dr.text((a+3,b+3),anon,fill='black');dr.rectangle((a+3+(x-box[0])*sc,b+20+(y-box[1])*sc,a+3+(c-box[0])*sc,b+20+(d-box[1])*sc),outline='#b40b78');dr.text((a+3,b+155),f'x{x}:{c} y{y}:{d}',fill='black')
        can.save(G/f'{group}_repeat_objects.png')
    write_json(D/'repeat_hidden_mapping.json',mapping)
    write_json(D/'REPEAT_REGISTRATION.json',dict(registered_at_utc=datetime.now(timezone.utc).isoformat(),registered_rows=read_json(D/'PLAN.json')['repeatability']['rows'],selection='32 objects per preregistered row, uniform without replacement from source-only coordinate ledger; seed originally registered, anonymous random order; no class/membership stratification',seed=SEED+5,n=len(mapping),mapping_sha256=sha256(D/'repeat_hidden_mapping.json'),masking='Prior source membership/owner suggestions, row body paths, V3 classes and previous parent decisions absent. Only RGB and source boxes/coordinates. Full unlabeled context available. Original source exposure/memory cannot be erased.',separation='Development source review/rule diagnosis and all heldout reference adjudication intervened; timestamps in source-reference files. Same adjudicator, no independent inter-rater inference.'))
    print('Registered128 anonymous repeat objects across4 preregistered rows',flush=True)
if __name__=='__main__':main()
