"""Masked RGB audit for feature semantics; no profile result read in prepare."""
from common import OUT,read_json,write_json,sha256
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image,ImageDraw
import numpy as np
D=OUT/'data/observations/neutral_feature_trial_v1';G=OUT/'figures/neutral_feature_trial_v1'
OLD=OUT/'data/observations/structural_inventory_v6_development'
def prepare():
    if (D/'EVIDENCE_SEAL.json').exists():raise RuntimeError('Trial sealed')
    if (D/'RGB_AUDIT_REGISTRATION.json').exists():raise RuntimeError('Already registered')
    rec=read_json(OLD/'discovery_parents.json');states={r['parent_id']:r['source_state'] for r in read_json(OUT/'data/observations/visual_dataset_v6/expanded_parent_assignments.json')};fresh=read_json(OLD/'fresh_source_reference.json')['parents'];rng=np.random.default_rng(20261014);chosen=[]
    for cap in sorted({r['caption'] for r in rec}):
        for known in [True,False]:
            pool=[r for r in rec if r['caption']==cap and (r['structural_class']!='UNK')==known and states[r['parent_id']] in ['source_resolved_existing_V3','source_confirmed_writing_V3_UNK']]
            chosen.append(pool[int(rng.integers(len(pool)))])
    for cap in ['16','47','94']:
        pool=[r for r in fresh if r['caption']==cap and r['membership']=='confirmed_writing' and r['source_parent_status']=='confirmed_connected_writing_trace'];idx=rng.choice(len(pool),2,replace=False);chosen.extend(pool[int(i)] for i in idx)
    rng.shuffle(chosen);key=[]
    for i,r in enumerate(chosen):key.append(dict(audit_id=f'R{i+1:02d}',parent_id=r['parent_id'],native_source=r['native_source'],native_bbox=r['native_bbox'],native_crop=r['native_crop']))
    write_json(D/'RGB_AUDIT_REGISTRATION.json',dict(registered_at_utc=datetime.now(timezone.utc).isoformat(),n=len(key),selection='One frozen-class-assigned and one source-resolved UNK parent per V5 caption, two resolved parents per V6 validation caption; seeded random. No feature result used.',questions=['clearly visible enclosed cavities: count or unresolved','principal long near-horizontal bridge/run: evident/absent/unresolved','whole-parent photography adequate for these descriptors'],semantics='Count source-visible enclosed light regions, not inferred strokes. Raster descriptors and visual features may differ; unknown means photograph cannot decide.',same_adjudicator=True,prior_image_familiarity=True,independent_interrater=False))
    write_json(D/'RGB_AUDIT_HIDDEN_KEY.json',key)
    for start in range(0,len(key),12):
        can=Image.new('RGB',(1200,((min(12,len(key)-start)+3)//4)*250),'#eee');dr=ImageDraw.Draw(can)
        for j,q in enumerate(key[start:start+12]):
            im=Image.open(OUT/q['native_crop']).convert('RGB');sc=min(3,275/im.width,210/im.height);im=im.resize((round(im.width*sc),round(im.height*sc)),Image.Resampling.NEAREST);x=(j%4)*300;y=(j//4)*250;can.paste(im,(x+10,y+30));dr.text((x+10,y+8),q['audit_id']+' native RGB only',fill='black');a,b,c,d=q['native_bbox'];dr.rectangle((x+10+10*sc,y+30+10*sc,x+10+(c-a+10)*sc,y+30+(d-b+10)*sc),outline='#b26',width=1)
        can.save(G/f'RGB_feature_audit_{start//12+1:02d}.png')
    print('Registered22 masked source feature observations, no numeric suggestions',flush=True)
if __name__=='__main__':prepare()
