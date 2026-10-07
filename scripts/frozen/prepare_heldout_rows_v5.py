"""Heldout native source review after membership rules have been sealed."""
from common import OUT,read_json,write_json,sha256
from register_row_benchmark_v5 import D,G
from prepare_row_objects_v5 import objects,atlas,compact,locator
from seal_membership_rules_v5 import function_hashes
from datetime import datetime,timezone
GEOMETRY={
'B003':([930,2565],[[930,561],[1400,565],[1950,578],[2565,588]]),
'B004':([935,2570],[[935,792],[1450,790],[2000,779],[2570,786]]),
'B013':([490,2460],[[490,283],[1000,273],[1500,244],[2100,263],[2460,270]]),
'B014':([465,2450],[[465,696],[1050,692],[1500,678],[2100,679],[2450,681]])}

def main():
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen(source_stage=True)
    seal=read_json(D/'MEMBERSHIP_RULE_SEAL.json');assert seal['function_hashes']==function_hashes()
    index=[]
    for r in read_json(D/'PLAN.json')['rows']:
        if r['row_id'] not in GEOMETRY:continue
        rgb,cc,ps=objects(r,GEOMETRY[r['row_id']]);rr=dict(**r,provisional_scope=GEOMETRY[r['row_id']][0],provisional_body_path=GEOMETRY[r['row_id']][1],objects=ps);atlas(rr,rgb,cc,ps);compact(rr,rgb,ps);locator(rr,rgb,ps);index.append(rr);print(r['row_id'],len(ps),flush=True)
    write_json(D/'heldout_object_location_aids.json',dict(created_at_utc=datetime.now(timezone.utc).isoformat(),membership_rules_seal_sha256=sha256(D/'MEMBERSHIP_RULE_SEAL.json'),rows=index,status='Native source aids only, no rule predictions, class labels or conventional strings'))
if __name__=='__main__':main()
