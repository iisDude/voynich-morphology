from common import OUT,read_json,write_json
from PIL import Image
ROOT=OUT/'data/observations/recurrence_v3_structural_candidate'
FRESH={
 'V_045':dict(safe_overview_x=[260,360],note='All marked fields inspected in overview. Writing left of overlapping green leaves and upper large flower, conservative left field retained.'),
 'V_030':dict(safe_overview_x=[145,270],note='All marked fields inspected in overview. Uncolored radial upper flower, blue/green central stalk and thin branching stem excluded; clear left writing over blue show-through retained.'),
 'V_102':dict(safe_overview_x=[150,300],note='All marked fields inspected in overview. Red/outlined flower heads and lower leaves interrupt middle/right; narrow left writing field retained.'),
 'V_089':dict(safe_overview_x=[310,550],note='All marked fields inspected in overview. Upper ordinary paragraph with outlined flowers at lower right; conservative central-left writing excludes flowers and leaves.'),
 'V_154':dict(safe_overview_x=[160,650],exclude_rows=[1],row_safe_overview_x={str(i):[450,650] for i in [14,16,18,20,21,22,23,24]}|{str(i):[150,370] for i in [13,15,17,19]},note='All marked fields inspected in overview. First proposal crosses painted basin boundary and is excluded. Main upper ordinary block; lower-left and lower-right fields mapped separately around bathing figures. Panel and physical reading order unknown.'),
 'V_120':dict(safe_overview_x=[135,650],note='All marked fields inspected in overview. Ordinary paragraphs with detached left margin labels and lower isolated human figure/marks; retain body field only.'),
 'V_202':dict(safe_overview_x=[145,650],note='All marked fields inspected in overview. Ordinary paragraphs clear of detached stars and marginal numbering; lower crease/damaged substrate requires local contact abstention.'),
}

def main():
    from recurrence_guard_v3 import require_unfrozen
    require_unfrozen(ROOT)
    old=read_json(OUT/'data/observations/recurrence_v3_development/ordinary_source_reviews.json');plan=read_json(ROOT/'PLAN.json');wanted={v['view_id'] for v in plan['selected_views']};records=[r for r in old if r['view_id'] in wanted]
    for v in plan['selected_views']:
        vid=v['view_id']
        if vid not in FRESH:continue
        r=dict(FRESH[vid]);width=Image.open(OUT/v['native_source']).width;ow=Image.open(OUT/'figures/recurrence_v3/structural_source_review'/f'{vid}_overview.png').width
        r['safe_x']=[round(x*width/ow) for x in r['safe_overview_x']];r['row_safe_x']={k:[round(x*width/ow) for x in p] for k,p in r.get('row_safe_overview_x',{}).items()}
        records.append(dict(view_id=vid,**r,reviewed_row_numbers=list(range(1,len(v['rows'])+1)),review_mode='overview_membership_triage',source_basis='Native-source overview; all selected field locations. Contact/class validation uses native RGB parents separately',complete_physical_line=False,pen_lifts='unknown',safe_field_status='Visible source writing field, local contact uncertainty still required'))
    write_json(ROOT/'ordinary_source_reviews.json',records);print(len(records),'views reviewed',sum(len(r['reviewed_row_numbers']) for r in records),'fields',flush=True)

if __name__=='__main__':main()
