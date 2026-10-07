from direct_morphology2_common import *
from PIL import Image,ImageDraw
def main():
    guard();assert not (D/'SELECTION_SEAL.json').exists();opts=read_json(D/'SOURCE_LAYOUT_OPTIONS.json');chosen=[opts[i] for i in [0,2,5,7,10,12,15,17]];allfields=read_json(OUT/'data/observations/sequence_v4_development/source_rows.json');previews=[]
    for r in chosen:
        cap=str(r['folio_component']);rr=sorted([q for q in allfields if str(q['folio_component'])==cap and q['status']=='triaged_local_writing_field' and q['safe_x'][1]-q['safe_x'][0]>=650],key=lambda q:(q['view_id'],q['row_number']))[:2]
        for q in rr:
            im=Image.open(OUT/q['native_source']).convert('RGB');x,y,c,d=q['source_row_bbox'];b=q['body_height'];box=[max(0,int(q['safe_x'][0]-65)),max(0,int(y-1.3*b)),min(im.width,int(q['safe_x'][1]+65)),min(im.height,int(d+.7*b))];p=G/f"preview_cap{cap}_{q['view_id']}_row{q['row_number']}.png";im.crop(box).save(p);previews.append(dict(caption=cap,view_id=q['view_id'],row_number=q['row_number'],native_source=q['native_source'],preview=p.relative_to(OUT).as_posix(),preview_bbox=box,field={k:q[k] for k in ['view_id','row_number','native_source','source_row_bbox','safe_x','body_height','body_path_knots']}))
    save(D/'PENDING_LAYOUT_SELECTION.json',dict(source_only_candidates=previews,selection_rule='Eight equally spread eligible ordinary-field options at fixed indices0,2,5,7,10,12,15,17; first two qualifying horizontal fields per caption, before any new extraction/distance. Native-RGB clarity audit pending.',morphology_outcomes_not_computed=True));print([(r['caption'],r['view_id'],r['row_number']) for r in previews],flush=True)
if __name__=='__main__':main()
