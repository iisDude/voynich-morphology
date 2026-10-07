"""Repeat native RGB decisions, anonymous labels recorded before decoding."""
from common import write_json,sha256
from register_row_benchmark_v5 import D
from datetime import datetime,timezone
DECISIONS={
'R01':dict(target=[4,6,7,14,18,20,22,23,24,32],neighbor=[10,12,21],unknown=[2,3,8,9,13,15,16,17,19,26,28,30],physical_start_interval=[397,407],physical_end_interval=[2016,2026],note='Selected sloping third row. Narrow coherent curves and compound traces recur visually, but minor fragments near them cannot be assigned from the RGB alone. Fourth-row curves belong to the neighbor.'),
'R02':dict(target=[4,14,15,18,25,31],neighbor=[10,12],unknown=[9,21,22,23,24,26,28,29,32],physical_start_interval=[743,753],physical_end_interval=[2640,2655],note='First ordinary row. Small green/gray margin detections and bright grain are nonwriting. Minor marks near brown traces remain unknown. Native curved terminal ends well before the right photo edge.'),
'R03':dict(target=[21,22,23,28,29],neighbor=[27],unknown=[19,24,26],mixed=[24],physical_start_interval=[309,320],physical_end_interval=[1990,2005],note='Fourth row. The diffuse brown object contains recognizable ink along with unresolved substrate/neighbor contact. Source after the actual endpoint is bare textured parchment; tiny dark point R03_26 is undecidable.'),
'R04':dict(target=[7,10,11,13,14,15,20,22,29,30],neighbor=[2,3,4,6,9,16,18,23,24,31],unknown=[27],physical_start_interval=[463,474],physical_end_interval=[2435,2447],note='Selected row near y670. The upper-row curves/tall structures have separate body roots. The small upper curve fragment R04_11 is writing but continuity with its lower curve is ambiguous. Tiny bright ridge detections in the surrounding parchment are nonwriting.'),
}
def main():
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen(source_stage=True)
    result=[]
    for group,note in DECISIONS.items():
        for n in range(1,33):
            owner='target' if n in note['target'] else 'neighbor' if n in note['neighbor'] else 'unknown' if n in note['unknown'] else 'outside_row'
            membership='mixed_writing_and_unresolved' if n in note.get('mixed',[]) else 'confirmed_writing' if owner in ['target','neighbor'] else 'unresolved' if owner=='unknown' else 'confirmed_nonwriting'
            result.append(dict(anonymous_id=f'{group}_{n:02d}',membership=membership,owner=owner,connected_parent='unknown' if owner=='unknown' or (group,n)==('R04',11) else 'connected_trace' if membership=='confirmed_writing' else 'not_writing_parent'))
    write_json(D/'repeat_blind_decisions.json',dict(sealed_at_utc=datetime.now(timezone.utc).isoformat(),labels_prior_to_mapping_decode=True,rows=DECISIONS,objects=result,disclaimer='Same adjudicator after intervening work. Prior labels hidden; source familiarity and visual memory remain. Not independent human inter-rater validation.'))
    write_json(D/'REPEAT_DECISION_SEAL.json',dict(sha256=sha256(D/'repeat_blind_decisions.json'),path='repeat_blind_decisions.json'))
    print('Sealed128 anonymous repeat decisions before decoding',flush=True)
if __name__=='__main__':main()
