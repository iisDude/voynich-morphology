"""Calibrate local writing windows; mixed whole-page rows are not negatives."""
from common import OUT,read_json,write_json,write_csv,SEED
from visual_extract import detect_lines
from calibrate_path_gate import features,transfer
import numpy as np
import cv2
from PIL import Image,ImageDraw
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix


def local_window(line,cc,center,width=None):
    body=max(1,line['body_height']); width=width or 12*body
    left,right=center-width/2,center+width/2
    members=[c for c in cc.values() if left<=c['cx']<=right and c['area']>=12
             and c['height']<=4*body and abs(c['y1']-1-line['slope']*(c['cx']-line['xref'])-line['baseline'])<=.8*body]
    if len(members)<4:return None
    local=dict(line)
    local.update(x0=min(c['x0'] for c in members),x1=max(c['x1'] for c in members),
                 y0=min(c['y0'] for c in members),y1=max(c['y1'] for c in members),
                 component_labels=[c['label'] for c in members],component_count=len(members),
                 multiline_component_count=sum(c.get('multiline_contact',False) for c in members))
    return local


def main():
    anchor_data=read_json(OUT/'data/observations/calibration_path_anchors.json')
    gate=read_json(OUT/'reports/path_gate_calibration.json')
    rows=[];cards=[]
    for view in anchor_data['anchors_xy']:
        obj=read_json(OUT/f'data/observations/pilot_native_global_proposals/{view}.json')
        image=Image.open(OUT/obj['view']['image_path']).convert('RGB')
        mask=(np.asarray(Image.open(OUT/f'data/observations/pilot_native_global_proposals/{view}_mask.png'))>0).astype(np.uint8)
        cc={c['label']:c for c in obj['components']}
        for anchor in gate['anchors']:
            if anchor['view_id']!=view or not anchor['matched']:continue
            line=next(l for l in obj['lines'] if l['line_id']==anchor['line_id'])
            local=local_window(line,cc,anchor['x'])
            if local:rows.append(dict(view_id=view,label=1,kind='anchor_window',bbox=[local[k] for k in ('x0','y0','x1','y1')],**features(local,cc,mask)))
        matrix=np.array(obj['view']['pdf_to_native_matrix'])
        for ri,(x0,y0,x1,y1) in enumerate(anchor_data['non_target_regions_xyxy'][view]):
            pts=transfer([[x0,y0],[x1,y1]],matrix).round().astype(int)
            (x0,y0),(x1,y1)=pts
            patch=mask[y0:y1,x0:x1]
            config=dict(obj['effective_config']);config.update(page_margin_fraction=0,minimum_line_component_count=4,minimum_line_width_px=min(100,patch.shape[1]*.6),line_horizontal_break_px=100)
            neg_lines,neg_cc,_=detect_lines(patch,config)
            neg_cc={c['label']:c for c in neg_cc}
            for line in neg_lines:
                for center in np.arange(line['x0'],line['x1'],max(40,6*line['body_height'])):
                    local=local_window(line,neg_cc,center)
                    if local:
                        bbox=[int(local['x0']+x0),int(local['y0']+y0),int(local['x1']+x0),int(local['y1']+y0)]
                        rows.append(dict(view_id=view,label=0,kind=f'explicit_negative_region_{ri}',bbox=bbox,**features(local,neg_cc,patch)))
        for row in [r for r in rows if r['view_id']==view]:
            crop=image.crop(row['bbox']);crop.thumbnail((460,150))
            card=Image.new('RGB',(480,180),'white');card.paste(crop,(10,25))
            ImageDraw.Draw(card).text((10,5),f'{view} label={row["label"]} {row["kind"]}',fill='black');cards.append(card)
    names=[k for k in rows[0] if k not in ('view_id','label','kind','bbox')]
    x=np.array([[r[k] for k in names] for r in rows]);y=np.array([r['label'] for r in rows]);groups=np.array([r['view_id'] for r in rows])
    pred=np.full(len(rows),np.nan)
    for view in sorted(set(groups)):
        train=groups!=view;test=~train
        if len(set(y[train]))<2:continue
        model=RandomForestClassifier(n_estimators=500,max_depth=4,min_samples_leaf=3,class_weight='balanced',random_state=SEED,n_jobs=2)
        model.fit(x[train],y[train]);pred[test]=model.predict_proba(x[test])[:,1]
    valid=np.isfinite(pred);metrics={}
    for t in (.5,.7,.85):
        cm=confusion_matrix(y[valid],pred[valid]>=t,labels=[0,1]);tn,fp,fn,tp=cm.ravel()
        metrics[str(t)]=dict(tn=int(tn),fp=int(fp),fn=int(fn),tp=int(tp),precision=float(tp/max(1,tp+fp)),recall=float(tp/max(1,tp+fn)))
    for row,p in zip(rows,pred):row['leave_one_view_out_probability']=float(p) if np.isfinite(p) else None
    model=RandomForestClassifier(n_estimators=500,max_depth=4,min_samples_leaf=3,class_weight='balanced',random_state=SEED,n_jobs=2).fit(x,y)
    joblib.dump(dict(model=model,feature_names=names),OUT/'data/observations/window_gate_calibration.joblib')
    write_json(OUT/'data/observations/window_gate_calibration_labels.json',rows)
    write_json(OUT/'reports/window_gate_calibration.json',dict(status='triage_only',positives=int(y.sum()),negatives=int((1-y).sum()),evaluated=int(valid.sum()),leave_one_view_out=metrics,limitations=['Approximate anchor-window positives; negative windows are inside explicit drawing/margin regions.','No estimate of complete writing-path recall.','Curved and radial writing not covered.','Window samples on a view are dependent; leave-one-view-out evaluation is descriptive, not independent-window significance.']))
    folder=OUT/'figures/window_gate_audit';folder.mkdir(parents=True,exist_ok=True)
    for start in range(0,len(cards),16):
        sheet=Image.new('RGB',(1920,720),'#ddd')
        for i,card in enumerate(cards[start:start+16]):sheet.paste(card,((i%4)*480,(i//4)*180))
        sheet.save(folder/f'labels_{start:03d}.png')
    print(dict(positives=int(y.sum()),negatives=int((1-y).sum()),metrics=metrics),flush=True)


if __name__=='__main__':main()
