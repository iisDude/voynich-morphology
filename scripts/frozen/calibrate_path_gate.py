"""Image-derived writing-path triage, evaluated by leave-one-view-out calibration.

Only explicitly anchored positives and explicit drawing/margin negatives are
labeled. Unannotated proposals are not negative examples.
"""
from common import OUT, read_json, write_json, write_csv, SEED
import numpy as np
import cv2
from PIL import Image, ImageDraw
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, balanced_accuracy_score
import joblib
import argparse


def features(line, components, mask):
    cc = [components[i] for i in line['component_labels']]
    x0,y0,x1,y1 = [line[k] for k in ('x0','y0','x1','y1')]
    body = max(1.,line['body_height'])
    width = max(1,x1-x0)
    crop = mask[y0:y1,x0:x1]
    heights = np.array([c['height']/body for c in cc])
    areas = np.array([c['area']/body**2 for c in cc])
    bottoms = np.array([c['y1']-1-line['slope']*(c['cx']-line['xref'])-line['baseline'] for c in cc])/body
    occupied = np.zeros(width,bool)
    for c in cc:
        occupied[max(0,c['x0']-x0):min(width,c['x1']-x0)] = True
    vector = dict(ink_fraction=float(crop.mean()), width_body=width/body,
                  bbox_height_body=(y1-y0)/body, count_per_body=len(cc)*body/width,
                  occupied_fraction=float(occupied.mean()), area_per_body_width=float(areas.sum()*body/width),
                  largest_area_fraction=float(areas.max()/max(areas.sum(),1e-9)),
                  baseline_mad_body=line['baseline_mad']/body,
                  multiline_fraction=line['multiline_component_count']/len(cc),
                  bottom_near_fraction=float((abs(bottoms)<.3).mean()),
                  tiny_fraction=float((areas<.12).mean()))
    for name,values in [('height',heights),('area',areas),('abs_bottom',abs(bottoms))]:
        for q in (25,50,75,90):
            vector[f'{name}_q{q}'] = float(np.percentile(values,q))
    return vector


def transfer(points,matrix):
    return cv2.perspectiveTransform(np.array([points],np.float32),matrix)[0]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pdf',action='store_true');args=ap.parse_args()
    suffix='_pdf' if args.pdf else ''
    proposal_folder='pilot_global_proposals' if args.pdf else 'pilot_native_global_proposals'
    anchors = read_json(OUT/'data/observations/calibration_path_anchors.json')
    rows,anchor_results = [],[]
    cards = []
    for view,points in anchors['anchors_xy'].items():
        obj=read_json(OUT/f'data/observations/{proposal_folder}/{view}.json')
        matrix=np.eye(3) if args.pdf else np.array(obj['view']['pdf_to_native_matrix'])
        scale=np.sqrt(np.linalg.det(matrix[:2,:2]))
        xy=transfer(points,matrix)
        mask=(np.asarray(Image.open(OUT/f'data/observations/{proposal_folder}/{view}_mask.png'))>0).astype(np.uint8)
        components={c['label']:c for c in obj['components']}
        positives=set()
        for a,(x,y) in enumerate(xy):
            candidates=[]
            for line in obj['lines']:
                if line['x0']<=x<=line['x1']:
                    baseline=line['baseline']+line['slope']*(x-line['xref'])
                    # Anchors locate body, not its precise baseline.
                    distance=abs(y-(baseline-.45*line['body_height']))
                    candidates.append((distance,line['line_id']))
            best=min(candidates) if candidates else (1e9,None)
            matched=best[0]<=max(anchors['uncertainty_pdf_px']*scale, .75*next((l['body_height'] for l in obj['lines'] if l['line_id']==best[1]),1))
            if matched: positives.add(best[1])
            anchor_results.append(dict(view_id=view,anchor=a+1,x=float(x),y=float(y),matched=bool(matched),line_id=best[1] if matched else None,distance_px=float(best[0])))
        negatives=[]
        for box in anchors['non_target_regions_xyxy'][view]:
            x0,y0,x1,y1=box
            pts=transfer([[x0,y0],[x1,y1]],matrix)
            negatives.append([*pts[0],*pts[1]])
        image=Image.open(OUT/obj['view']['image_path']).convert('RGB')
        for line in obj['lines']:
            label=None
            if line['line_id'] in positives: label=1
            elif any(x0<=line['x0'] and line['x1']<=x1 and y0<=line['y0'] and line['y1']<=y1 for x0,y0,x1,y1 in negatives): label=0
            feat=features(line,components,mask)
            rows.append(dict(view_id=view,line_id=line['line_id'],label=label,**feat))
            if label is not None:
                crop=image.crop((line['x0'],max(0,line['y0']-10),line['x1'],line['y1']+10))
                crop.thumbnail((900,130))
                card=Image.new('RGB',(930,160),'white')
                card.paste(crop,(10,25)); ImageDraw.Draw(card).text((10,5),f'{view} {line["line_id"]} label={label}',fill='black')
                cards.append(card)
    labeled=[r for r in rows if r['label'] is not None]
    names=[k for k in rows[0] if k not in ('view_id','line_id','label')]
    x=np.array([[r[k] for k in names] for r in labeled]); y=np.array([r['label'] for r in labeled])
    groups=np.array([r['view_id'] for r in labeled]); pred=np.full(len(y),np.nan)
    for group in sorted(set(groups)):
        train=groups!=group; test=~train
        if len(set(y[train]))<2: continue
        model=RandomForestClassifier(n_estimators=400,max_depth=4,min_samples_leaf=3,class_weight='balanced',random_state=SEED,n_jobs=2)
        model.fit(x[train],y[train]); pred[test]=model.predict_proba(x[test])[:,1]
    valid=np.isfinite(pred)
    for row,p in zip(labeled,pred): row['leave_one_view_out_probability']=float(p) if np.isfinite(p) else None
    metrics={}
    for threshold in (.5,.7,.85):
        decision=pred[valid]>=threshold
        cm=confusion_matrix(y[valid],decision,labels=[0,1])
        metrics[str(threshold)]={'confusion_matrix_tn_fp_fn_tp':cm.tolist(),'balanced_accuracy':float(balanced_accuracy_score(y[valid],decision))}
    model=RandomForestClassifier(n_estimators=400,max_depth=4,min_samples_leaf=3,class_weight='balanced',random_state=SEED,n_jobs=2).fit(x,y)
    allpred=model.predict_proba(np.array([[r[k] for k in names] for r in rows]))[:,1]
    for row,p in zip(rows,allpred): row['calibration_fit_probability']=float(p)
    artifact=OUT/f'data/observations/path_gate_calibration{suffix}.joblib'
    joblib.dump(dict(model=model,feature_names=names),artifact)
    write_json(OUT/f'reports/path_gate_calibration{suffix}.json',dict(status='triage_only_not_visual_acceptance',anchors=anchor_results,labeled_count=len(labeled),positives=int(y.sum()),negatives=int((1-y).sum()),leave_one_view_out=metrics,limitations=['Sparse approximate anchors; classifier evaluates proposal recognition, not complete line recall.','Unlabeled proposals do not contribute negative labels.','Writing on curved paths excluded from straight-path calibration; require separate audit.']))
    write_csv(OUT/f'data/observations/path_gate_calibration{suffix}.csv',rows,fields=list(rows[0])+['leave_one_view_out_probability'] if 'leave_one_view_out_probability' not in rows[0] else list(rows[0]))
    folder=OUT/f'figures/path_gate_audit{suffix}';folder.mkdir(parents=True,exist_ok=True)
    for start in range(0,len(cards),12):
        sheet=Image.new('RGB',(1860,960),'#dddddd')
        for i,card in enumerate(cards[start:start+12]): sheet.paste(card,((i%2)*930,(i//2)*160))
        sheet.save(folder/f'labels_{start:03d}.png')
    print({'labeled':len(labeled),'matched_anchors':sum(r['matched'] for r in anchor_results),'metrics':metrics})


if __name__=='__main__': main()
