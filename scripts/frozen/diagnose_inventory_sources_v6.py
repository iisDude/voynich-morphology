from inventory_v6_common import *
from evaluate_source_classes_v3 import transform,chamfer
from collections import Counter
import numpy as np,pickle
from scipy.spatial.distance import cdist
from prepare_structural_inventory_v6 import gallery

# Observations from all seven327-parent native RGB mosaics. These are physical
# descriptors, not newly proven classes or claims about internal units.
FRAME=['B002_O075','B005_O185','B011_O016','B012_O040','B003_O065','B014_O028','B014_O053','B014_O071']
REPEAT=['B001_O014','B001_O053','B002_O047','B002_O059','B006_O138','B007_O189','B008_O135','B009_O060','B010_O092','B015_O048','B015_O061','B016_O041','B004_O034','B004_O041','B014_O049']
APPEND=['B001_O121','B002_O114','B005_O122','B005_O138','B006_O155','B006_O157','B007_O158','B011_O039','B011_O044','B012_O032','B015_O011','B015_O024','B016_O051','B004_O075','B013_O106','B013_O107','B014_O106','B014_O111']
FAINT=['B001_O012','B001_O019','B005_O151','B005_O170','B007_O048','B007_O071','B007_O087','B007_O094','B007_O096','B009_O062','B013_O032','B014_O036','B014_O080','B014_O082']
def main():
    guard();rec=read_json(D/'discovery_parents.json');data=np.load(D/'discovery_shapes.npz');sh=data['shapes'][:,0];g=data['geometry'][:,0];model=pickle.loads(MODEL.read_bytes());z=transform(sh,g,model);known=np.array([i for i,r in enumerate(rec) if r['structural_class']!='UNK']);diag=[];examples=[]
    for i,r in enumerate(rec):
        if r['structural_class']!='UNK':continue
        idx=known[g[known,4]==g[i,4]];nearest=int(idx[np.argmin(cdist(z[i:i+1],z[idx])[0])]) if len(idx) else None
        ch=chamfer(sh[i],sh[nearest]) if nearest is not None else None
        family=bool(nearest is not None and ch<=.08 and abs(g[i,2]-g[nearest,2])<=.5)
        tags=[];pid=r['parent_id']
        if family:tags.append('likely_V3_family_variant_similarity_hypothesis')
        if not r['photo_raster_stable']:tags.append('topology_connectivity_or_threshold_instability')
        if pid in FRAME:tags.extend(['frame_insertion_or_added_upright_candidate','connected_compound_candidate'])
        if pid in REPEAT:tags.append('repeated_structural_element_candidate')
        if pid in APPEND:tags.extend(['loop_branch_or_appendix_candidate','connected_compound_candidate'])
        if pid in FAINT:tags.append('insufficient_photographic_morphology')
        if r['parent_boundary_status']=='competing_join':tags.extend(['source_contact_ambiguity','detached_or_neighbor_association'])
        if not tags:tags.append('different_structure_or_unmatched_variant_not_decided')
        if 'likely_V3_family_variant_similarity_hypothesis' in tags and len(examples)<24:examples.extend([r,rec[nearest]])
        diag.append(dict(parent_id=pid,caption=r['caption'],exclusive_stage=r['diagnosis_stage'],overlapping_hypotheses=tags,nearest_confirmed_V3_parent=rec[nearest]['parent_id'] if nearest is not None else None,nearest_confirmed_V3_class=rec[nearest]['structural_class'] if nearest is not None else None,symmetric_chamfer=ch,source_note='Whole native RGB mosaics reviewed. Similarity is a diagnostic hypothesis, not assignment, merge or new class. Contact/faint cases may overlap raster categories.'))
    save(D/'source_unknown_diagnosis.json',dict(created_at_utc=now(),parents=diag,exclusive_raster_categories=dict(Counter(r['exclusive_stage'] for r in diag)),overlapping_hypothesis_counts=dict(Counter(t for r in diag for t in r['overlapping_hypotheses'])),genuinely_new_recurrent_classes_established_at_this_stage=0,diagnostic_similarity_rule='Closest same-hole confirmed V5 V3 parent, symmetric Chamfer<=.08 and log aspect difference<=.5; does not define class membership',all_unknown_RGB_atlases_reviewed=True))
    gallery(examples,'family_variant_comparison');seal([D/'source_unknown_diagnosis.json',D/'discovery_parents.json',D/'discovery_shapes.npz',T/'preclass_diagnosis.json',Path(__file__)],D/'DIAGNOSIS_SEAL.json')
    print(Counter(t for r in diag for t in r['overlapping_hypotheses']),flush=True)
if __name__=='__main__':main()
