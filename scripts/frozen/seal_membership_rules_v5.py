"""Seal development-only rules before opening held-out row pixels."""
from common import OUT,read_json,write_json,sha256
from register_row_benchmark_v5 import D,T
from benchmark_membership_v5 import features,strong,track,predict
from datetime import datetime,timezone
import inspect,hashlib

def function_hashes():return {f.__name__:hashlib.sha256(inspect.getsource(f).encode()).hexdigest() for f in [features,strong,track,predict]}

def main():
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen(source_stage=False)
    if (D/'MEMBERSHIP_RULE_SEAL.json').exists():raise RuntimeError('Rules already sealed')
    plan=read_json(D/'PLAN.json')
    seal=dict(sealed_at_utc=datetime.now(timezone.utc).isoformat(),stage='Before heldout row RGB review or heldout object labels; no V3 class input',development_reference_sha256=sha256(D/'development_source_reference.json'),development_predictions_sha256=sha256(D/'development_rule_predictions_final.json'),function_hashes=function_hashes(),
       source_rules=[
         'Membership and row ownership are separate. Connected raster masks are location aids; mixed source contacts stay unknown.',
         'Strong source writing candidate: area>=35 px, height>=0.20 body, width>=0.075 body, height<=4.5 body, width<=12 body, raw local gray contrast 90th percentile>=50 and median>=25 against sigma25 background. The larger height allowance concerns membership only; frozen V3 eligibility is unchanged.',
         'Small weak source detections: area<35 and raw contrast90<45 become texture candidates, retained in the ledger. This is an algorithm prediction, not permission to overwrite source-unresolved truth.',
         'Remaining faint/large/unstable detections are unknown. No low-to-primary bridge is automatically joined; preserve connected-compound and detached alternatives.',
         'Fully automatic localized-field path uses source pixel density, compact coherent components, anchor-minus0.3body seed and bidirectional96px windows, maximum12px shift per window. It receives no reference membership or endpoint boxes.',
         'Target-owner candidate requires>=8 source pixels in body core(-.95,+.25 body), and whole component bottom between-.8 and+.9body of path. Long tails may therefore abstain. Wrong/mixed row-root outcomes remain failure evidence.',
         'A second diagnostic supplies the source-adjudicated body path but no object labels or endpoint boxes. It is layout-assisted, not automatic row recovery.',
         'An endpoint estimate is the first/last accepted source object, not a validated physical line end. Unresolved nearby traces remain in the source reference.'
       ],
       development_rationale='RGB audits distinguish coherent brown traces, diffuse substrate connections, drawing contours and dark marginal writing. The initial contrast18 rule admitted raised surface texture; development contrasts gave writing contrast90 median80.45 versus substrate median33.76. Conservative contrast50/median25 thresholds keep weak writing unknown. Source-visible short minims motivate height0.20; ordinary long descenders motivate owner allowance0.90. No recurrence, structural class suggestion or conventional outcome used.',
       limitations=['Same adjudicator; mask-assisted reference dependence; candidate enumeration within source-localized contexts, not page-discovery certification','Two heldout caption clusters only; source photographs previously overview-seen; heldout for new rule development','Raster contrast is not chemistry, actual stroke boundaries, pen lifts or glyph truth','Failed gates will not be retuned on heldout'],
       unchanged_v3_v4=plan['immutable_dependencies'],parameters_frozen=True,heldout_captions=plan['heldout_captions'])
    write_json(D/'MEMBERSHIP_RULE_SEAL.json',seal);write_json(T/'RULES_SEAL_SHA256.json',dict(path=str((D/'MEMBERSHIP_RULE_SEAL.json').relative_to(OUT)),sha256=sha256(D/'MEMBERSHIP_RULE_SEAL.json')))
    print('Sealed source-only membership rules before heldout review',flush=True)
if __name__=='__main__':main()
