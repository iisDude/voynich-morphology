"""Held-out conditional coding proxy on the SAME native group masks.

Training template predictions, not the original mask, reconstruct each group.
This is a binary assigned-ink coding proxy, not lossless manuscript compression.
"""
from common import OUT,read_json,write_json,write_csv,sha256,SEED
from analyse_native_structure import unpack
from assign_visual_families import MODELS
import numpy as np
import cv2
import joblib


def native_template(prob,h,w):
    scale=44/max(h,w,1);rh,rw=max(1,round(h*scale)),max(1,round(w*scale))
    yy,xx=(48-rh)//2,(48-rw)//2
    return cv2.resize(prob[yy:yy+rh,xx:xx+rw],(w,h),interpolation=cv2.INTER_LINEAR)


def main():
    folder=OUT/'data/observations/regional_candidates_v4';assigned=OUT/'data/observations/assigned_visual_candidates_v4'
    sums={m:np.zeros((128,48,48),np.float64) for m in MODELS};counts={m:np.zeros(128,np.int64) for m in MODELS}
    train_ink=0;train_pixels=0;inputs=[]
    for path in sorted(folder.glob('V_*.json')):
        if not path.stem[2:].isdigit():continue
        obj=read_json(path)
        if obj['view']['split']!='train':continue
        a=read_json(assigned/path.name);arr=np.load(path.with_name(path.stem+'_shapes.npz'))['shapes']
        for r in obj['instances']:
            u=a['units'][r['instance_id']];ci=int(u['nearest_family_id'].split('_')[-1])-1;m=r['model']
            # Atlas eligibility is the frozen training rule; all source-quality
            # failures remain a reported training contamination limitation.
            if r['atlas_eligible']:sums[m][ci]+=arr[r['shape_index']];counts[m][ci]+=1
            if m=='group_only':
                train_ink+=r['features']['ink_area_body2']*r['body_height_proxy_px']**2
                x,y,c,d=r['bbox_xyxy'];train_pixels+=(c-x)*(d-y)
        inputs.append(dict(path=path.relative_to(OUT).as_posix(),sha256=sha256(path)))
    prob={m:np.clip((sums[m]+1)/(counts[m][:,None,None]+2),.02,.98).astype(np.float32) for m in MODELS}
    out=OUT/'tests/visual_reconstruction';out.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(out/'training_templates.npz',**prob)
    base_rate=float(np.clip(train_ink/train_pixels,.02,.98));results=[]
    for path in sorted(folder.glob('V_*.json')):
        if not path.stem[2:].isdigit():continue
        obj=read_json(path)
        if obj['view']['split'] not in ('validation','test'):continue
        a=read_json(assigned/path.name);byid={r['instance_id']:r for r in obj['instances']}
        packed=np.load(path.with_name(path.stem+'_native_masks.npz'))
        for g in a['groups']:
            if not g['primary_assay_eligible']:continue
            x0,y0,x1,y1=g['bbox_xyxy'];gt=unpack(packed,byid[g['models']['group_only'][0]]['shape_index']);h,w=gt.shape
            baseline_bits=float(-(gt*np.log2(base_rate)+(1-gt)*np.log2(1-base_rate)).sum())
            for m in MODELS:
                predicted=np.zeros((h,w),np.float32);ids=g['models'][m]
                for instance in ids:
                    r=byid[instance];u=a['units'][instance];ci=int(u['nearest_family_id'].split('_')[-1])-1
                    xx,yy,xx1,yy1=r['bbox_xyxy'];p=native_template(prob[m][ci],yy1-yy,xx1-xx)
                    tile=predicted[yy-y0:yy1-y0,xx-x0:xx1-x0]
                    if tile.shape!=p.shape:raise ValueError(f'Group/component coordinates disagree: {instance}')
                    tile[:]=1-(1-tile)*(1-p)
                predicted=np.clip(predicted,.02,.98)
                residual=float(-(gt*np.log2(predicted)+(1-gt)*np.log2(1-predicted)).sum())
                bitmap=predicted>=.5;intersection=(bitmap & gt.astype(bool)).sum();union=(bitmap | gt.astype(bool)).sum()
                # Fixed rectangle coordinates cost 64 bits; class code is 7 bits.
                metadata=12+len(ids)*(64+7)
                results.append(dict(group_id=g['group_id'],view_id=path.stem,folio_component=g['folio_component'],split=g['split'],
                    model=m,unit_count=len(ids),native_mask_pixels=h*w,native_mask_ink=int(gt.sum()),
                    template_residual_bits=residual,geometry_and_identity_bits=metadata,total_proxy_bits=residual+metadata,
                    training_constant_rate_bits=baseline_bits+64,native_mask_uncompressed_bits=h*w,
                    template_mask_iou=float(intersection/union) if union else 1.))
        print(path.stem,flush=True)
    write_csv(out/'results.csv',results);rng=np.random.default_rng(SEED);summary=[]
    for split in ('validation','test'):
        for m in MODELS:
            rr=[r for r in results if r['split']==split and r['model']==m];folios=sorted(set(r['folio_component'] for r in rr))
            vals=[np.mean([(r['total_proxy_bits']-r['training_constant_rate_bits'])/r['native_mask_pixels'] for r in rr if r['folio_component']==f]) for f in folios]
            boot=rng.choice(vals,(2000,len(vals)),replace=True).mean(axis=1) if vals else np.array([np.nan])
            summary.append(dict(split=split,model=m,groups=len(rr),folio_components=len(folios),
                equal_folio_excess_bits_per_pixel=float(np.mean(vals)) if vals else None,
                folio_bootstrap_lower=float(np.quantile(boot,.025)),folio_bootstrap_upper=float(np.quantile(boot,.975)),
                mean_template_iou=float(np.mean([r['template_mask_iou'] for r in rr])) if rr else None))
    write_csv(out/'summary.csv',summary)
    write_json(out/'config.json',dict(seed=SEED,training='train only',evaluation='validation and test without template refit',
        models=MODELS,template_probability_floor=.02,rectangle_cost_bits=64,family_cost_bits=7,
        target='exact native assigned group mask, identical across models',selection='primary admitted medium groups only',
        baseline='constant training group ink fraction plus one rectangle',
        limitations=['Binary thresholded assigned ink, not native grayscale evidence or lossless coding.',
            'Coordinates and nearest class are supplied by the encoder and charged fixed proxy costs.',
            'Source-quality gate errors and unresolved neighboring groups persist.',
            'Different partitions can improve geometry prediction without being graphemes.',
            'Folio components are caption groups; bifolio independence unverified.']))
    write_json(out/'input_manifest.json',dict(training=inputs,template_sha256=sha256(out/'training_templates.npz'),
        assignment_protocol_sha256=sha256(OUT/'data/observations/heldout_source_audit_plan.json')))
    (out/'README.md').write_text('# Native assigned-ink reconstruction\n\nRun `run.py` using the project scientific runtime. The target is the same source-coordinate binary group mask under every competing partition. Training templates predict it; copying its constituent masks is not counted as a result. Negative excess bits means improvement over a training constant-rate baseline. This test cannot establish a recovered alphabet.\n',encoding='utf-8')
    (out/'run.py').write_text('from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]/"src"))\nfrom evaluate_visual_reconstruction import main\nmain()\n',encoding='utf-8')
    (out/'summary.md').write_text('# Results\n\nSee `summary.csv` for equal-folio results and descriptive folio bootstrap intervals. Template IoU is measured against held-out native assigned ink. The code-length values are conditional binary-image proxies, not evidence that the manuscript is a cipher or that a partition recovers graphemes.\n',encoding='utf-8')
    print(summary)

if __name__=='__main__':main()
