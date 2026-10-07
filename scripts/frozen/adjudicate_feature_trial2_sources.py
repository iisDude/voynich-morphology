"""Transcribe native RGB judgments made before features/class suggestions."""
from feature_trial2_common import *
A='''2/?/W/Y 0/N/W/? 1/C/S/N 0/N/W/Y 2/U/S/Y ?/?/S/Y 1/L/T/N 2/B/T/N
1/U/T/N 1/U/S/Y 1/U/T/N 0/N/T/N 0/N/T/N 0/N/T/N 2/B/T/N 0/N/T/N
0/N/W/Y 2/B/W/Y 1/L/W/? 2/U/S/Y 1/C/S/N 0/N/T/N ?/?/S/Y 3/C/W/Y
1/C/S/N 0/N/T/N 1/U/T/Y 2/B/T/N ?/?/T/N 0/N/T/N 2/U/S/Y 1/C/S/N
0/N/S/N ?/?/S/? ?/?/S/N 2/?/T/N 0/N/T/N 1/U/T/N 0/N/S/Y 0/N/W/Y
0/N/S/N 0/N/W/N 1/U/T/N ?/?/T/N 2/U/S/Y 2/B/T/N 0/N/T/N 1/C/S/N
0/N/W/Y 0/N/T/N 0/N/S/? 0/N/S/? 0/N/W/N 2/B/T/N 0/N/S/N 0/N/S/N
0/N/T/N 0/N/W/N 1/C/S/N 0/N/W/N 2/B/T/N 0/N/S/N 1/C/W/N ?/?/T/N
1/U/T/Y ?/?/S/N 1/U/T/N 2/B/T/N 0/N/W/Y 1/U/T/Y 1/U/T/N 1/C/S/N
1/U/T/N 1/C/W/N 1/C/W/N 0/N/T/N 0/N/S/Y ?/?/W/Y 1/U/T/N 2/B/W/Y
0/N/S/N 0/N/W/Y 0/N/T/N 0/N/S/N 0/N/T/N 2/B/S/N 1/L/S/N 1/U/T/Y'''.split()
N='''0/N/T/N ?/?/T/N 2/B/T/N 2/B/T/N 2/B/T/N 2/B/T/N ?/?/T/N 0/N/S/N
1/U/T/N 0/N/S/N 1/C/W/Y 1/C/W/N 0/N/S/N 1/C/S/N 0/N/W/Y
2/U/S/Y 0/N/T/N 0/N/S/Y 2/B/T/N 1/U/T/N ?/?/S/? 1/U/S/N ?/?/T/Y
1/C/S/N 0/N/W/Y 0/N/W/Y 1/C/W/N 1/U/T/N 0/N/T/N 0/N/S/N 0/N/S/N
2/U/T/Y 2/U/T/Y ?/?/T/Y 0/N/T/N 0/N/S/? 1/U/W/Y 2/B/T/N 1/U/T/N
0/N/S/N 2/B/T/N 0/N/W/Y 1/C/W/Y 1/U/T/N 1/C/S/N 2/B/T/N 1/C/S/N
1/C/S/N 0/N/S/N 1/U/T/Y
1/U/T/Y 1/U/T/Y 2/U/T/Y ?/?/S/Y ?/?/S/Y 1/U/T/Y ?/?/S/Y 0/N/T/N
0/N/T/N 0/N/S/N 0/N/T/N 0/N/W/N 2/B/T/N 2/B/S/N ?/?/?/? 0/N/T/N
1/C/W/Y 2/U/W/Y 1/U/T/N ?/?/?/? 0/N/S/N 1/U/T/N 0/N/S/N 0/N/S/N
0/N/W/N 1/U/S/N 0/N/W/N 1/U/T/N 0/N/W/N 1/C/T/N ?/?/T/N 1/C/W/?
0/N/T/N 0/N/S/N 0/N/W/Y 0/N/S/N ?/?/?/? ?/?/T/N 0/N/S/N 1/C/S/N
0/N/T/N 1/C/S/N ?/?/?/?
?/?/?/? ?/?/?/? 2/U/T/Y 0/N/T/N 2/B/T/N 1/U/T/N 0/N/S/N 1/C/W/N
0/N/W/Y 1/U/T/N 0/N/W/Y 0/N/T/N 0/N/W/Y 1/C/S/N 1/C/S/N ?/?/S/N
1/U/T/N 1/U/T/N 0/N/S/N 0/N/T/N 1/U/T/Y
?/?/W/Y 3/B/T/Y 2/B/S/Y 2/?/S/Y 1/L/T/N 1/L/T/N 3/B/S/N 1/U/T/N
1/U/T/N 0/N/S/N 2/B/W/Y 1/C/T/N 0/N/S/N ?/?/W/Y 0/N/T/N 0/N/W/Y
0/N/T/N 0/N/S/N 1/U/S/Y'''.split()

def main():
    guard();verify_seal(D/'SPECIFICATION_SEAL.json')
    assert not (D/'SOURCE_SEAL.json').exists()
    assert len(A)==88 and len(N)==133,(len(A),len(N))
    rr=read_json(D/'source_location_aids.json')['parents'];out=[]
    for r in rr:
        code=(A if r['audit_id'][0]=='A' else N)[int(r['audit_id'][1:])-1]
        k,p,a,s=code.split('/');n=int(r['audit_id'][1:]);fresh=r['corpus']=='fresh'
        membership='confirmed_writing';status='resolved_whole_parent';note='Native RGB, padded parent and whole field inspected; no numeric features or V3 suggestion displayed.'
        if fresh and n in [65,70,87]:membership='unresolved';status='insufficient_photo';note='Faint fragment: writing/texture and association not photographically resolved.'
        if fresh and n==93:membership='confirmed_nonwriting';status='nonwriting';note='Blue/grey substrate contrast without ordinary brown writing trace.'
        if fresh and n in [11,21,23,66,82,94,95,105,106,111,113]:
            status='possible_contact_or_parent_extent';note='Writing confirmed; full connected-parent extent/ownership not resolved. Keep profile diagnostic only.'
        if fresh and n in [94,95]:note='Extended native context shows faint horizontal bridge between N094/N095; observed source-join alternative spans x357:740 y396:542. Raster parts cannot be treated as complete separate parents. Physical closure of bridge attachment remains uncertain; no gap filling.'
        out.append(dict(parent_id=r['parent_id'],audit_id=r['audit_id'],caption=r['caption'],corpus=r['corpus'],membership=membership,source_parent_status=status,source_cavity_count=None if k=='?' else int(k),source_cavity_placement={'U':'upper','L':'lower','B':'both','N':'none','C':'midpoint_uncertain','?':'unknown'}[p],source_aspect={'T':'taller','W':'wide','S':'near_square','?':'unknown'}[a],source_horizontal_span={'Y':'evident','N':'absent','?':'unknown'}[s],native_source=r['native_source'],native_bbox=r['native_bbox'],note=note))
    save(D/'source_decisions.json',dict(decided_at_utc=now(),parents=out,source_visible_only=True,same_AI_not_independent_interrater=True,aspect_bbox_aided=True,limitations='Cavity counts refer to visible cavities regardless of numerical area cutoff; source aspect is coarse and bbox-aided. Proposal sampling cannot estimate all-writing recall. Possible-source-join cases are alternatives, not separate accepted whole parents.',source_alternatives=[dict(audit_ids=['N094','N095'],relation='possible_faint_horizontal_source_join',native_bbox=[357,396,740,542],context='figures/neutral_feature_trial2/V_112_upper_context_extension.png',context_native_bbox=[250,200,1150,560])]))
    paths=[D/'source_decisions.json',D/'source_location_aids.json',D/'fresh_source_contexts.json',D/'source_shapes.npz',OUT/'src/adjudicate_feature_trial2_sources.py',OUT/'src/prepare_feature_trial2_sources.py']+list((D/'parent_masks').glob('*.png'))+list(G.glob('*.png'))+list((G/'native_parents').glob('*.png'))
    seal(paths,D/'SOURCE_SEAL.json')
    from collections import Counter
    print(Counter((r['corpus'],r['membership'],r['source_parent_status']) for r in out),flush=True)
if __name__=='__main__':main()
