"""Source factor validation, coverage accounting and reversible group hypotheses."""
from common import OUT,read_json,write_json,write_csv,sha256,SEED
from evaluate_source_classes_v3 import transform,assign,chamfer
from fit_source_classes_v3 import pixels
from sklearn.decomposition import NMF
from collections import Counter,defaultdict
import pickle,numpy as np,cv2
from PIL import Image,ImageDraw
ROOT=OUT/'data/observations/recurrence_v3_structural_candidate';TEST=OUT/'tests/recurrence_v3_development'

def recurrence(seqs):
    freq=Counter(tuple(s) for s in seqs if s);n=sum(freq.values())
    return dict(occurrences=n,distinct=len(freq),singleton_types=sum(v==1 for v in freq.values()),repeated_occurrence_fraction=sum(v for v in freq.values() if v>=2)/max(1,n),maximum_frequency=max(freq.values(),default=0))

def source_factors(shape):
    # Three horizontal bands and three vertical bands describe source geometry only.
    s=cv2.resize(shape,(24,24));regions=[s[a:a+8,:] for a in [0,8,16]]+[s[:,a:a+8] for a in [0,8,16]]
    return np.array([v.mean() for v in regions]+[s[:12,:12].mean(),s[:12,12:].mean(),s[12:,:12].mean(),s[12:,12:].mean()])

def main():
    from recurrence_guard_v3 import require_unfrozen
    require_unfrozen(ROOT)
    model=pickle.loads((ROOT/'sealed_class_model.pkl').read_bytes());rec=read_json(ROOT/'source_parents.json');data=np.load(ROOT/'source_shapes.npz');sh=data['shapes'];g=data['geometry'];idx=np.array([i for i,r in enumerate(rec) if r['class_eligible']]);z=transform(sh[idx],g[idx],model);base=assign(z,g[idx],model)
    variant=[]
    for name in ['low','high']:
        vg=g[idx].copy()
        for j,i in enumerate(idx):
            alt=rec[i]['competing_rasters'][0 if name=='low' else 1]['native_bbox'];a,b,c,d=alt;body=rec[i]['body_height_proxy'];vg[j,:3]=[np.log((d-b)/body),np.log((c-a)/body),np.log((c-a)/(d-b))]
        variant.append(assign(transform(data[name][idx],vg,model),vg,model))
    nuisance=np.array([cv2.warpAffine(s,np.float32([[1,.04,-1],[0,1,1]]),(48,48),flags=cv2.INTER_LINEAR,borderValue=0) for s in sh[idx]])
    align=assign(transform(nuisance,g[idx],model),g[idx],model)
    core=read_json(ROOT/'heldout_class_metrics.json')['recurring_core_classes'];pairkey=read_json(ROOT/'pair_audit_key.json');judgment={r['pair_id']:r['judgment'] for r in read_json(ROOT/'pair_source_judgments_before_key.json')};audit_unknown=set()
    # Case-level source disagreements are unknown, not relabeled to an alternative class.
    for p in pairkey:
        if p['kind']=='positive' and judgment[p['pair_id']]!='same_structural_hypothesis':audit_unknown.add(p['left_index'])
    raw= model['kmeans'].predict(model['pca'].transform(pixels(sh[model['train_indices']])))
    raw_by_global={int(i):int(l) for i,l in zip(model['train_indices'],raw)};assignments={};parent_records=[]
    for local,i in enumerate(idx):
        cid=str(base['classes'][local]);stable=all(v['accepted'][local] and v['classes'][local]==cid for v in variant);aligned=align['accepted'][local] and align['classes'][local]==cid
        accepted=bool(base['accepted'][local] and stable and aligned and cid in core and i not in audit_unknown);nearest=int(base['nearest'][local]);rawkey=f"CT{raw_by_global.get(nearest,-1):02d}_H{int(g[i,4])}"
        r=dict(rec[i],structural_class=cid if accepted else None,proposed_class=cid if base['accepted'][local] else None,competing_class=str(base['alternatives'][local]) if np.isfinite(base['alternative_distance'][local]) else None,threshold_class_stable=bool(stable),alignment_class_stable=bool(aligned),source_audit_case_status='unknown' if i in audit_unknown else 'not individually audited',class_status='corroborated_structural_candidate' if accepted else 'unknown',premerge_contour_subclass=rawkey if accepted else None,class_atomicity='unknown',source_factor_signature=source_factors(sh[i]).tolist())
        parent_records.append(r);assignments[r['parent_id']]=r
    # All unstable/unclassified writing candidates retain their coordinates and unknown class.
    present={r['parent_id'] for r in parent_records}
    parent_records += [dict(r,structural_class=None,class_status='unknown',proposed_class=None,class_atomicity='unknown') for r in rec if r['parent_id'] not in present]
    write_json(ROOT/'corroborated_parent_assignments.json',parent_records)
    groups=[];rows=read_json(ROOT/'source_rows.json');byrow=defaultdict(list)
    for r in parent_records:byrow[(r['view_id'],r['row_number'])].append(r)
    for row in rows:
        if row['status']!='reviewed_local_writing_field':continue
        parts=sorted(byrow[(row['view_id'],row['row_number'])],key=lambda r:r['native_bbox'][0]);body=row['body_height']
        for gap in [.35,.55,.75]:
            chunks=[]
            for p in parts:
                if not chunks or p['native_bbox'][0]-max(x['native_bbox'][2] for x in chunks[-1])>=body*gap:chunks.append([p])
                else:chunks[-1].append(p)
            for j,chunk in enumerate(chunks):
                a=min(p['native_bbox'][0] for p in chunk);c=max(p['native_bbox'][2] for p in chunk);b=min(p['native_bbox'][1] for p in chunk);d=max(p['native_bbox'][3] for p in chunk)
                known=all(p['structural_class'] and p['row_ownership']!='unknown' for p in chunk) and a-row['safe_x'][0]>=body*.25 and row['safe_x'][1]-c>=body*.25
                groups.append(dict(group_id=f"{row['line_id']}_GAP{gap}_{j:03d}",view_id=row['view_id'],folio_component=row['folio_component'],split=row['split'],row_number=row['row_number'],gap_body=gap,native_bbox=[a,b,c,d],parent_ids=[p['parent_id'] for p in chunk],structural_units=[p['structural_class'] for p in chunk] if known else None,premerge_contour_units=[p.get('premerge_contour_subclass') for p in chunk] if known else None,local_sequence_status='complete_retained_parent_list' if known else 'unknown',boundary_status='competing source-visible gap hypothesis; detached small ink and full-row extent unresolved',wordhood='unknown',complete_physical_line=False))
    write_json(ROOT/'competing_group_hypotheses.json',groups)
    # Source-only factor model is a validation competitor, never a segmentation boundary rule.
    train=model['train_indices'];raw_images=np.array([cv2.resize(s,(24,24)).ravel() for s in sh[train]],np.float32)
    nmf=NMF(n_components=12,init='nndsvda',random_state=SEED,max_iter=350,tol=.002);trf=nmf.fit_transform(raw_images);factors=nmf.components_;np.savez_compressed(ROOT/'component_factor_model.npz',factors=factors,training_scores=trf)
    facgal=OUT/'figures/recurrence_v3/source_factors.png';canvas=Image.new('RGB',(1200,260),'white');draw=ImageDraw.Draw(canvas)
    for i,f in enumerate(factors):
        arr=f.reshape(24,24);arr=255-(arr/max(arr.max(),1e-9)*255).astype(np.uint8);im=Image.fromarray(arr).convert('RGB').resize((90,90));xx=(i%6)*200;yy=(i//6)*130;canvas.paste(im,(xx,yy+20));draw.text((xx,yy),f'Geometric factor {i+1}',fill='black')
    canvas.save(facgal)
    # Held-out factor signatures compared against topology/relative-aspect-matched other classes.
    rng=np.random.default_rng(SEED);test=[(j,int(i)) for j,i in enumerate(idx) if rec[i]['split']=='test' and base['accepted'][j]];factor_test=nmf.transform(np.array([cv2.resize(sh[i],(24,24)).ravel() for j,i in test],np.float32));means={c:trf[model['class_ids']==c].mean(0) for c in set(model['class_ids'])};factor_scale=np.std(trf,axis=0)+.01;metrics=[]
    for t,(j,i) in enumerate(test):
        cid=str(base['classes'][j]);nearest=int(base['nearest'][j]);pool=[int(k) for k,c in zip(train,model['class_ids']) if c!=cid and g[k,4]==g[i,4] and abs(g[k,2]-g[i,2])<=.35]
        if not pool:continue
        neg=int(rng.choice(pool));negcid=str(model['class_ids'][np.where(train==neg)[0][0]])
        positive=chamfer(sh[i],sh[nearest]);negative=chamfer(sh[i],sh[neg]);goodfac=float(np.mean(((factor_test[t]-means[cid])/factor_scale)**2));badfac=float(np.mean(((factor_test[t]-means[negcid])/factor_scale)**2))
        metrics.append(dict(parent_id=rec[i]['parent_id'],folio_component=rec[i]['folio_component'],class_id=cid,positive_chamfer=positive,matched_null_chamfer=negative,contour_difference=negative-positive,own_class_factor_error=goodfac,matched_null_factor_error=badfac,factor_difference=badfac-goodfac))
    bycap=defaultdict(list)
    for m in metrics:bycap[m['folio_component']].append(m)
    caprows=[dict(caption=c,instances=len(mm),mean_contour_difference=float(np.mean([m['contour_difference'] for m in mm])),mean_factor_difference=float(np.mean([m['factor_difference'] for m in mm]))) for c,mm in bycap.items()]
    cis={}
    for col in ['mean_contour_difference','mean_factor_difference']:
        vals=np.array([r[col] for r in caprows]);boot=np.array([rng.choice(vals,len(vals),replace=True).mean() for _ in range(2000)]);cis[col]=dict(caption_mean=float(vals.mean()),caption_bootstrap_interval=np.quantile(boot,[.025,.975]).tolist(),caption_groups=len(vals))
    write_json(ROOT/'factor_validation.json',dict(source_basis='Raw native-parent shape bands and 12-factor NMF trained on train parents only; no grapheme interpretation',heldout_instances=len(metrics),caption_block_metrics=caprows,intervals=cis,null='Other-class training instance matched on significant-hole count and log-aspect within .35, sampled by fixed seed',limitation='Contour matching is related to the fitted image representation. NMF factor coherence corroborates shape organization but is not independent linguistic evidence. Caption groups are not certified physical bifolios. Small caption count and nonrandom fields limit manuscript population inference.'))
    write_csv(TEST/'heldout_factor_source_controls.csv',metrics)
    # Pure class-specificity comparison: same retained pixels, groups, admission and nearest source exemplars.
    summaries={}
    for gap in [.35,.55,.75]:
        gg=[p for p in groups if p['gap_body']==gap and p['structural_units']];summaries[str(gap)]=dict(complete_retained_group_candidates=len(gg),premerge=recurrence([p['premerge_contour_units'] for p in gg]),structural=recurrence([p['structural_units'] for p in gg]),groups_at_least_three_parents=dict(premerge=recurrence([p['premerge_contour_units'] for p in gg if len(p['parent_ids'])>=3]),structural=recurrence([p['structural_units'] for p in gg if len(p['parent_ids'])>=3])))
    # Coverage/sample-size curves on the same classifier: caption subsampling without replacement.
    gg=[p for p in groups if p['gap_body']==.55 and p['structural_units'] and len(p['parent_ids'])>=3];caps=sorted(set(p['folio_component'] for p in gg));curves=[]
    for ncap in [3,6,12,len(caps)]:
        if ncap>len(caps):continue
        vals=[]
        for _ in range(300):
            chosen=set(rng.choice(caps,ncap,replace=False));subset=[p for p in gg if p['folio_component'] in chosen];pre=recurrence([p['premerge_contour_units'] for p in subset]);coarse=recurrence([p['structural_units'] for p in subset]);vals.append([len(subset),pre['repeated_occurrence_fraction'],coarse['repeated_occurrence_fraction']])
        vals=np.array(vals);curves.append(dict(captions=ncap,mean_groups=float(vals[:,0].mean()),mean_premerge_repeated_fraction=float(vals[:,1].mean()),mean_structural_repeated_fraction=float(vals[:,2].mean()),subsampling_90pct_range=np.quantile(vals[:,1:],[.05,.95],axis=0).tolist()))
    write_json(TEST/'expanded_coverage_specificity.json',dict(matched_class_comparison=summaries,caption_subsampling_without_replacement=curves,interpretation='Matched unit/group lists isolate source-atlas label specificity. Increasing caption coverage with fixed classifier separately shows finite-sample recurrence. Neither curve estimates unobserved writing recall or a causal percentage of manuscript sparsity.',group_status='Descriptive recurrence of retained parent-list gap hypotheses; not words, independently certified full groups, minimal pairs or a downstream positional assay.',unknown_groups=sum(p['gap_body']==.55 and not p['structural_units'] for p in groups),known_groups=sum(p['gap_body']==.55 and bool(p['structural_units']) for p in groups)))
    # Explicit fresh-test reproducibility, same sealed model, run independently a second time.
    ti=np.array([j for j,i in enumerate(idx) if rec[i]['split']=='test']);again=assign(transform(sh[idx[ti]],g[idx[ti]],model),g[idx[ti]],model)
    same=bool(np.array_equal(again['classes'],base['classes'][ti]) and np.array_equal(again['accepted'],base['accepted'][ti]))
    write_json(ROOT/'computational_reproducibility.json',dict(same_test_classes_and_abstentions=same,test_instances=len(ti),sealed_model_sha256=sha256(ROOT/'sealed_class_model.pkl'),model_unchanged=sha256(ROOT/'sealed_class_model.pkl')==read_json(ROOT/'MODEL_SEAL.json')['model_sha256'],independent_human_raters=1,meaning='Deterministic re-execution and held-out image recurrence/perturbation evidence; does not establish independent-rater paleographic reproducibility.'))
    print('source factors',cis,'known .55 groups',sum(p['gap_body']==.55 and bool(p['structural_units']) for p in groups),'reproducible',same,flush=True)

if __name__=='__main__':main()
