"""Training-only amendment: preserve failed grouping and qualify similarity."""
from inventory_v6_common import *
import numpy as np
from scipy.spatial.distance import cdist
VARIANTS=['B001_O076','B001_O118','B002_O023','B002_O053','B005_O131','B006_O081','B008_O162','B010_O074','B011_O020','B012_O031','B004_O047','B013_O018','B013_O027','B014_O038','B014_O094','B001_O127','B002_O055','B006_O123','B007_O149','B008_O055','B008_O065','B009_O024','B010_O040','B010_O057','B013_O054','B013_O099','B014_O062','B006_O151','B007_O164','B008_O139','B008_O151','B010_O093','B014_O120']
def main():
    guard()
    assert not (D/'fresh_assignments.json').exists()
    if (D/'DEVELOPMENT_AMENDMENT.json').exists():raise RuntimeError('Amendment already recorded')
    rec=read_json(D/'discovery_parents.json');embedding=np.load(D/'whole_candidate_embedding.npz');z=embedding['z'];g=embedding['g'];known=[i for i,r in enumerate(rec) if r['structural_class']!='UNK'];nn=[]
    for i in known:
        jj=[j for j in known if rec[j]['caption']!=rec[i]['caption'] and rec[j]['structural_class']==rec[i]['structural_class']]
        if jj:nn.append(float(cdist(z[i:i+1],z[jj]).min()))
    scale=float(np.quantile(nn,.9));threshold=2*scale
    # Preserve the complete original attempt, do not overwrite its seal/plan.
    save(D/'source_diagnosis_qualification.json',dict(created_at_utc=now(),native_likely_V3_family_variants=VARIANTS,count=len(VARIANTS),interpretation='33 direct RGB examples retain ordinary ring, upright/upper-loop or hooked-curve organization with width/slant/proportion variation. This is a family hypothesis, not V3 acceptance. The earlier304 automated near-family flags are a permissive similarity screen, not304 established allographs.',permissive_match_native_audit=dict(pairs=12,same_organization=2,different_organization=7,unresolved=3,positive_agreement=2/12,examples='family_variant_comparison_01.png; pairs in consecutive cells',warning='Small Chamfer plus broad aspect tolerance can match a bench to paired obliques or a hook to a frame. Do not use this screen to choose class merges.'),new_classes_established=0))
    save(D/'DEVELOPMENT_AMENDMENT.json',dict(registered_at_utc=now(),before_test_assignments=True,original_plan_unchanged=True,failed_attempt='whole_candidate_discovery.json: fixed distance0.35 yields162 clusters from163 source-resolved parents and no8-instance3-caption class',reason='The initial numeric distance is below typical even established source-family distances in the frozen embedding. Source-only training calibration is needed before heldout testing; no test labels or sequence outcome used.',calibration='Twice90th percentile cross-caption nearest distance among311 already accepted V5 V3 instances within the same frozen class. Complete-link diameter uses this calibrated scale. Radius remains leave-caption-out90th percentile; alternative margin1.08; exact topology. No merge with a V3 class.',calibration_instances=len(nn),cross_caption_nearest_q90=scale,grouping_diameter=threshold,new_radius_cap=threshold,other_gates_unchanged=True,negative_result_preserved=True))
    seal([D/'DEVELOPMENT_AMENDMENT.json',D/'source_diagnosis_qualification.json',D/'whole_candidate_discovery.json',D/'composition_discovery.json',Path(__file__)],D/'DEVELOPMENT_AMENDMENT_SEAL.json');print('Training-only grouping diameter',threshold,'native family candidates',len(VARIANTS),flush=True)
if __name__=='__main__':main()
