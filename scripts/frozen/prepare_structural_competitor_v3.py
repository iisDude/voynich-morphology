"""Train-only coarse source atlas and fresh caption reserve after candidate failure."""
from common import OUT,read_json,read_csv,write_json,sha256,SEED
from fit_source_classes_v3 import pixels
from collections import defaultdict
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA
import numpy as np,cv2,pickle
from PIL import Image,ImageDraw
from datetime import datetime,timezone
ROOT=OUT/'data/observations/recurrence_v3_development';NEXT=OUT/'data/observations/recurrence_v3_structural_candidate'

def main():
    NEXT.mkdir(exist_ok=True)
    if (NEXT/'RESERVE.json').exists():raise ValueError('Reserve already registered')
    oldplan=read_json(ROOT/'PLAN.json');used={v['folio_component'] for v in oldplan['selected_views']};sources=read_csv(OUT/'data/source/yale_native_all_manifest.csv');choices=[]
    for s in sources:
        vid=s['view_id'];o=read_json(OUT/f'data/observations/regional_candidates_v11/{vid}.json');v=o['view']
        if v['split']!='test' or v['folio_component'] in used:continue
        rr=[]
        for line in o['lines']:
            a,b,c,d=line['bbox_xyxy'];body=line['body_height_proxy_px'];n=line['component_count']
            if c-a>=550 and n>=8 and 12<=body<=65:rr.append(dict(view_id=vid,line_id=line['line_id'],bbox_xyxy=line['bbox_xyxy'],body_height=body,source_line=line))
        if len(rr)>=3:choices.append(dict(view_id=vid,split='test',folio_component=v['folio_component'],native_source=s['path'],rows=sorted(rr,key=lambda r:r['bbox_xyxy'][1])))
    fresh=[];usedcap=set()
    for lo,hi in [(4,55),(55,106),(106,157),(157,208)]:
        chosen=sorted([v for v in choices if lo<=int(v['view_id'][2:])<hi],key=lambda v:(-min(len(v['rows']),24),v['view_id']))
        n=0
        for v in chosen:
            if v['folio_component'] in usedcap:continue
            ii=np.unique(np.linspace(0,len(v['rows'])-1,min(24,len(v['rows']))).round().astype(int));v=dict(v,rows=[v['rows'][i] for i in ii]);fresh.append(v);usedcap.add(v['folio_component']);n+=1
            if n==2:break
    reserve=dict(registered_at_utc=datetime.now(timezone.utc).isoformat(),fresh_views=[dict(view_id=v['view_id'],folio_component=v['folio_component'],rows=len(v['rows'])) for v in fresh],criteria=oldplan['freeze_requirements'],previous_test_not_reused=True,reason='First candidate fails source pair agreement and threshold stability; high resolution source atlas revises broad class hypotheses, not thresholds fitted to old test.',class_choice='Train-only image/topology atlas; source structural tags and factor constraints; old test pair judgments cannot define individual merges.')
    write_json(NEXT/'RESERVE.json',reserve);write_json(NEXT/'PLAN.json',dict(oldplan,selected_views=[v for v in oldplan['selected_views'] if v['split']!='test']+fresh,proposed_rows=sum(len(v['rows']) for v in oldplan['selected_views'] if v['split']!='test')+sum(len(v['rows']) for v in fresh),second_candidate_reserve_sha256=sha256(NEXT/'RESERVE.json')))
    rec=read_json(ROOT/'source_parents.json');data=np.load(ROOT/'source_shapes.npz');train=np.array([i for i,r in enumerate(rec) if r['class_eligible'] and r['split']=='train']);px=pixels(data['shapes'][train]);pca=PCA(n_components=24,whiten=False,random_state=SEED).fit(px);z=pca.transform(px);km=MiniBatchKMeans(n_clusters=16,n_init=10,random_state=SEED,batch_size=1024,max_iter=250).fit(z);labs=km.predict(z);dist=km.transform(z)
    gal=OUT/'figures/recurrence_v3/train_structural_atlas';gal.mkdir(parents=True,exist_ok=True);atlas=[]
    for k in range(16):
        ii=np.where(labs==k)[0];ordered=ii[np.argsort(dist[ii,k])];chosen=[];caps=set()
        for j in ordered:
            if rec[train[j]]['folio_component'] in caps:continue
            chosen.append(int(train[j]));caps.add(rec[train[j]]['folio_component'])
            if len(chosen)>=8:break
        atlas.append(dict(cluster=k,training_instances=len(ii),exemplar_indices=chosen,source_crop_paths=[rec[j]['native_crop'] for j in chosen],holes_distribution={str(h):int(sum(data['geometry'][train[ii],4]==h)) for h in sorted(set(data['geometry'][train[ii],4]))}))
    for start in [0,8]:
        canvas=Image.new('RGB',(1600,1600),'white');draw=ImageDraw.Draw(canvas)
        for j,a in enumerate(atlas[start:start+8]):
            yy=j*200;draw.text((5,yy+3),f"Train contour cluster {a['cluster']}; {a['training_instances']} parents; source hypothesis pending",fill='black')
            for col,path in enumerate(a['source_crop_paths']):
                im=Image.open(OUT/path);scale=min(2.5,185/im.width,155/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);canvas.paste(im,(col*200,yy+30))
        canvas.save(gal/f'train_{start:02d}_{start+7:02d}.png')
    (NEXT/'train_contour_model.pkl').write_bytes(pickle.dumps(dict(pca=pca,kmeans=km,train_indices=train,labels=labs,z=z)))
    write_json(NEXT/'train_source_atlas.json',atlas);print(reserve,flush=True)

if __name__=='__main__':main()
