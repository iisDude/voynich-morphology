"""Source-atlas structural tags; training-only choices, separate fresh test."""
from common import OUT,read_json,write_json,sha256,SEED
from fit_source_classes_v3 import pixels
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import pickle,numpy as np
from datetime import datetime,timezone
ROOT=OUT/'data/observations/recurrence_v3_structural_candidate';PREV=OUT/'data/observations/recurrence_v3_development'

# This table follows inspection of train_00_07 and train_08_15 RGB source atlas only.
TAGS={0:'paired_uprights_bridge',6:'paired_uprights_bridge',1:'horizontal_arch_bridge',2:'upper_curve_lower_terminal',10:'upper_curve_lower_terminal',14:'upper_curve_lower_terminal',3:'vertical_loop_pair',4:'compact_ring',13:'compact_ring',5:'compact_loop_upper_right_trace',7:'vertical_loop_pair_left_appendage',9:'single_upright_lateral_bridge',11:'open_compact_hook',12:'short_oblique_terminal',15:'upper_loop_oblique_lower_branch'}
ALLOWED={'paired_uprights_bridge':[1,2],'horizontal_arch_bridge':[0,1],'upper_curve_lower_terminal':[0,1],'vertical_loop_pair':[2],'compact_ring':[1],'compact_loop_upper_right_trace':[1],'vertical_loop_pair_left_appendage':[2],'single_upright_lateral_bridge':[1,2],'open_compact_hook':[0],'short_oblique_terminal':[0],'upper_loop_oblique_lower_branch':[1]}

def main():
    from recurrence_guard_v3 import require_unfrozen
    require_unfrozen(ROOT)
    if (ROOT/'MODEL_SEAL.json').exists():raise ValueError('Model already sealed')
    protocol=dict(registered_at_utc=datetime.now(timezone.utc).isoformat(),source_basis='Train-only RGB atlas 16 contour clusters, eight examples from distinct captions per cluster; no test pairs used to select individual merges',tags=TAGS,allowed_topologies=ALLOWED,
     rejected_cluster=8,rejection_reason='Train examples mix inter-row contacts/stacked parents and compounds; no single reusable structural class asserted',
     grouping='Whole parent, contour organization and stable hole count. Width/slant/ink density and small proportion variation are nuisance dimensions; extra upright, branch, bridge or appended lower trace are competing classes. Open/closed variants remain separate topology hypotheses.',
     geometry='Relative native aspect/height and skeleton geometry weakly weighted (0.25) for matching; topology exact. Pixel x and row ordinal excluded.',
     factor_criteria='Upper/lower spatial contour signatures, hole centroids, uprights/bridge organization. Factors are measurements, not internal grapheme boundaries or asserted pen strokes.',
     acceptance='Training class 90th-percentile cross-caption nearest-neighbor radius and alternative-class distance ratio 1.08; threshold connectivity/topology unstable parents remain unknown',
     validation='Registered original freeze gates unchanged, tested on fresh reserved caption groups. Source pair judgments before key, caption bootstrap and topology-matched nulls.',
     model_inputs='Source pixels, topology, connectivity, relative geometry only; no transcription, inherited hand/section, Currier, positional assay or minimal pairs',
     pca_components=24,geometry_weight=.25,model_status='Source-atlas competitor, not segmentation freeze')
    write_json(ROOT/'class_protocol.json',protocol)
    source_model=pickle.loads((ROOT/'train_contour_model.pkl').read_bytes());oldrec=read_json(PREV/'source_parents.json');rec=read_json(ROOT/'source_parents.json');oldindex={r['parent_id']:i for i,r in enumerate(oldrec)};newindex={r['parent_id']:i for i,r in enumerate(rec)}
    data=np.load(ROOT/'source_shapes.npz');g=data['geometry'];pca=source_model['pca'];km=source_model['kmeans'];idx=np.array([newindex[oldrec[i]['parent_id']] for i in source_model['train_indices']]);labels=source_model['labels']
    keep=np.array([int(l) in TAGS and int(g[i,4]) in ALLOWED[TAGS[int(l)]] for i,l in zip(idx,labels)])
    train=idx[keep];labels=labels[keep];rawkeys=[(TAGS[int(l)],int(g[i,4])) for i,l in zip(train,labels)];keys=sorted(set(rawkeys));mapping={key:f'ST{i+1:02d}' for i,key in enumerate(keys)};class_ids=np.array([mapping[key] for key in rawkeys]);p=pca.transform(pixels(data['shapes'][train]));scale=max(float(np.sqrt(np.mean((p-p.mean(0))**2))),.01)
    gs=StandardScaler().fit(g[train]);geo=np.clip(gs.transform(g[train]),-4,4);geo[:,4]=g[train,4]*2;z=np.c_[p/scale/np.sqrt(24),geo*.25/np.sqrt(g.shape[1])]
    caps=np.array([r['folio_component'] for r in rec]);radii={};core={}
    for cid in sorted(set(class_ids)):
        ii=np.where(class_ids==cid)[0];nn=NearestNeighbors(n_neighbors=min(40,len(ii))).fit(z[ii]);d,j=nn.kneighbors(z[ii]);other=[]
        for a in range(len(ii)):
            dd=[float(dd) for dd,b in zip(d[a],j[a]) if caps[train[ii[b]]]!=caps[train[ii[a]]]]
            if dd:other.append(min(dd))
        rad=float(np.quantile(other,.9)) if other else 0.;radii[cid]=rad;key=[key for key,c in mapping.items() if c==cid][0]
        core[cid]=dict(source_structure=key[0],significant_holes=key[1],training_instances=len(ii),training_captions=len(set(caps[train[ii]])),radius=rad,other_caption_calibration_instances=len(other))
    bundle=dict(pca=pca,pca_scale=scale,geometry_scaler=gs,kmeans=km,train_indices=train,class_ids=class_ids,z_train=z,keys=mapping,radii=radii,core=core,protocol=protocol,pca_components=24,geometry_weight=.25,audit_pairs_per_class=3)
    path=ROOT/'sealed_class_model.pkl';path.write_bytes(pickle.dumps(bundle));write_json(ROOT/'class_model_selection.json',dict(source_atlas_tag_system=TAGS,structural_classes=core,training_retained=len(train),training_abstained=len(idx)-len(train),competing_system='178-class prior sealed source candidate preserved; no one-to-one claim',class_system_size=len(mapping)))
    write_json(ROOT/'MODEL_SEAL.json',dict(sealed_at_utc=datetime.now(timezone.utc).isoformat(),model_sha256=sha256(path),class_protocol_sha256=sha256(ROOT/'class_protocol.json'),source_parents_sha256=sha256(ROOT/'source_parents.json'),shapes_sha256=sha256(ROOT/'source_shapes.npz'),reserve_sha256=sha256(ROOT/'RESERVE.json'),test_assignments_inspected=False,status='Source-only candidate sealed before fresh test assignments; not segmentation freeze'))
    print('SEALED source structural classes',len(mapping),'retained train',len(train),flush=True)

if __name__=='__main__':main()
