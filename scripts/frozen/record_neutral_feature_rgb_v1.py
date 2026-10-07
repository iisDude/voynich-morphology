from common import OUT,read_json,write_json,sha256
from pathlib import Path
from datetime import datetime,timezone
D=OUT/'data/observations/neutral_feature_trial_v1'
CAV={1:1,2:1,4:2,5:0,6:2,8:1,9:1,10:1,11:1,14:0,15:1,17:0,18:0,19:0,20:1,21:0,22:2}
RUN_YES={4,5,7,13,14,15,19,21}
RUN_UNKNOWN={2,9,10,16,18}
def main():
    if (D/'EVIDENCE_SEAL.json').exists() or (D/'RGB_DECISION_SEAL.json').exists():raise RuntimeError('Source decisions sealed')
    records=[]
    for i in range(1,23):
        records.append(dict(audit_id=f'R{i:02d}',source_visible_cavities=CAV.get(i),cavity_status='resolved_source_visible' if i in CAV else 'unresolved_source_visibility_or_ownership',principal_horizontal_span='evident' if i in RUN_YES else 'unresolved' if i in RUN_UNKNOWN else 'absent',photography='partial_or_insufficient' if i in [3,7,16] else 'adequate_for_some_descriptors',note='Source RGB only, previous numeric profile/class suggestion concealed. Count visible enclosed light regions belonging to the located parent; neighboring partial ink does not automatically belong. Faint closures and complex ownership retain unknown.'))
    write_json(D/'RGB_source_feature_decisions.json',dict(recorded_at_utc=datetime.now(timezone.utc).isoformat(),observations=records,previous_numeric_profiles_read=False,same_AI_adjudicator=True,independent_rater=False,prior_photograph_exposure=True,semantics='Source-visible cavities and principal horizontal span are coarse audit observations, not strokes/characters. Scalar horizontal-run ratio is not equivalent to a bench/frame judgment.'))
    paths=[D/'RGB_source_feature_decisions.json',D/'RGB_AUDIT_REGISTRATION.json',D/'RGB_AUDIT_HIDDEN_KEY.json',Path(__file__)]
    write_json(D/'RGB_DECISION_SEAL.json',dict(sealed_at_utc=datetime.now(timezone.utc).isoformat(),files=[dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p)) for p in paths]));print('Sealed22 source observations before numeric comparison;17 resolved cavity counts',flush=True)
if __name__=='__main__':main()
