"""Source-only train/validation models; seal before assigning test imagery."""
from common import OUT,read_json,write_json,sha256,SEED
import numpy as np,cv2,pickle
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import MiniBatchKMeans
from sklearn.neighbors import NearestNeighbors
from datetime import datetime,timezone
ROOT=OUT/'data/observations/recurrence_v3_development'

def pixels(shapes):
    out=[]
    for s in shapes:
        b=(cv2.resize(s,(24,24),interpolation=cv2.INTER_AREA)>.25).astype(np.uint8)
        # Smoothed proximity encodes relative contour geometry without whitening faint detail.
        dt=cv2.distanceTransform(1-b,cv2.DIST_L2,3)
        out.append(np.exp(-dt/2.0).ravel())
    return np.array(out,np.float32)

def main():
    from recurrence_guard_v3 import require_unfrozen
    require_unfrozen(ROOT)
    rec=read_json(ROOT/'source_parents.json');data=np.load(ROOT/'source_shapes.npz');sh=data['shapes'];g=data['geometry']
    train=np.array([i for i,r in enumerate(rec) if r['class_eligible'] and r['split']=='train']);val=np.array([i for i,r in enumerate(rec) if r['class_eligible'] and r['split']=='validation'])
    protocol=dict(model_inputs='Source-only contour proximity, significant holes, connectivity and geometry; no group recurrence/minimal pairs, transcription, Currier or position',image_preprocessing='24x24 aspect-preserving parent, exponential distance-to-ink field, PCA32 not whitened',candidate_k=[16,24,32,48,64],topology='Classes partitioned by exact threshold-stable significant-hole count; no cross-hole class assignment',geometry_weight=.65,holes_weight=2.,selection='Validation contour quantization loss plus 0.018*log(K), evaluated without test assignments. This unsupervised criterion is not a claim of class validity.',acceptance='Other-caption nearest-neighbor distance calibrated at train 90th percentile per class; >=1.08 alternative-class distance ratio, topology exact. Unknown retained.',pair_audit='Separate native RGB audit of positive and same-topology hard-negative pairs, after sealed model. Unknown pairs count as failures to accept proposed positive.',train_instances=len(train),validation_instances=len(val),test_class_inspection=False,registered_at_utc=datetime.now(timezone.utc).isoformat())
    write_json(ROOT/'class_protocol.json',protocol)
    px=pixels(sh[train]);pca=PCA(n_components=32,whiten=False,random_state=SEED);p=pca.fit_transform(px);scale=max(float(np.sqrt(np.mean((p-p.mean(0))**2))),.01)
    gs=StandardScaler().fit(g[train]);geom=gs.transform(g[train]);geom=np.clip(geom,-4,4);geom[:,4]=g[train,4]*2 # categorical topology remains explicit
    z=np.c_[p/scale/np.sqrt(32),geom*.65/np.sqrt(g.shape[1])];vpx=pixels(sh[val]);vp=pca.transform(vpx);vg=np.clip(gs.transform(g[val]),-4,4);vg[:,4]=g[val,4]*2;vz=np.c_[vp/scale/np.sqrt(32),vg*.65/np.sqrt(g.shape[1])]
    candidates=[];models={}
    for k in protocol['candidate_k']:
        km=MiniBatchKMeans(n_clusters=k,n_init=8,random_state=SEED,batch_size=1024,max_iter=250).fit(z)
        dist=km.transform(vz);loss=float(np.mean(np.min(dist,axis=1)**2));score=loss+.018*np.log(k)
        candidates.append(dict(k=k,validation_contour_geometry_loss=loss,complexity_penalty=float(.018*np.log(k)),selection_score=float(score)));models[k]=km
        print('source-only candidate',k,'validation loss',loss,'score',score,flush=True)
    k=min(candidates,key=lambda r:r['selection_score'])['k'];km=models[k];labs=km.predict(z)
    # The topology subdivision remains a competing structural taxonomy, not an alphabet.
    keys=sorted(set((int(a),int(b)) for a,b in zip(labs,g[train,4])));mapping={key:f'SC{i+1:03d}' for i,key in enumerate(keys)}
    class_ids=np.array([mapping[(int(a),int(b))] for a,b in zip(labs,g[train,4])]);capt=np.array([r['folio_component'] for r in rec]);radii={};core={};nns={}
    for cid in sorted(set(class_ids)):
        idx=np.where(class_ids==cid)[0];nn=NearestNeighbors(n_neighbors=min(25,len(idx))).fit(z[idx]);d,j=nn.kneighbors(z[idx]);other=[]
        for a in range(len(idx)):
            valid=[float(dd) for dd,b in zip(d[a],j[a]) if capt[train[idx[b]]]!=capt[train[idx[a]]]]
            if valid:other.append(min(valid))
        radius=float(np.quantile(other,.90)) if other else 0.
        radii[cid]=radius;core[cid]=dict(training_instances=len(idx),training_captions=len(set(capt[train[idx]])),other_caption_calibration_instances=len(other),radius=radius)
        nns[cid]=dict(train_local_indices=idx.tolist())
    bundle=dict(pca=pca,pca_scale=scale,geometry_scaler=gs,kmeans=km,train_indices=train,class_ids=class_ids,z_train=z,keys=mapping,radii=radii,core=core,protocol=protocol)
    path=ROOT/'sealed_class_model.pkl';path.write_bytes(pickle.dumps(bundle))
    write_json(ROOT/'class_model_selection.json',dict(candidates=candidates,selected_k=k,topology_partition_classes=len(keys),training_class_summary=core,selection_note='Held-out recurrence, pair audit and perturbation gates have not yet been tested. No segmentation freeze.'))
    write_json(ROOT/'MODEL_SEAL.json',dict(sealed_at_utc=datetime.now(timezone.utc).isoformat(),model_sha256=sha256(path),class_protocol_sha256=sha256(ROOT/'class_protocol.json'),source_parents_sha256=sha256(ROOT/'source_parents.json'),shapes_sha256=sha256(ROOT/'source_shapes.npz'),plan_sha256=sha256(ROOT/'PLAN.json'),test_assignments_inspected=False,status='Locked candidate before test classification, not a segmentation freeze'))
    print('MODEL SEALED',k,len(keys),flush=True)

if __name__=='__main__':main()
