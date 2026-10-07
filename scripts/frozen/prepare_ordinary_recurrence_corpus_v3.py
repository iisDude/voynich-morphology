"""Native ordinary-row evidence, without class labels or comparison metadata."""
from common import OUT,read_json,write_json,write_csv,sha256
from PIL import Image,ImageDraw
from visual_extract import ink_mask
import numpy as np,cv2

def main(root=None,gallery=None):
    root=root or OUT/'data/observations/recurrence_v3_development';plan=read_json(root/'PLAN.json');gallery=gallery or OUT/'figures/recurrence_v3/source_review';gallery.mkdir(parents=True,exist_ok=True);crops=root/'native_rows';crops.mkdir(exist_ok=True);index=[]
    from recurrence_guard_v3 import require_unfrozen
    require_unfrozen(root)
    for view in plan['selected_views']:
        vid=view['view_id'];im=Image.open(OUT/view['native_source']).convert('RGB');overview=im.copy();overview.thumbnail((900,1300));draw=ImageDraw.Draw(overview);sc=overview.width/im.width;patches=[]
        for i,row in enumerate(sorted(view['rows'],key=lambda r:r['bbox_xyxy'][1])):
            a,b,c,d=row['bbox_xyxy'];body=row['body_height'];box=[max(0,a-75),max(0,int(b-body*.8)),min(im.width,c+75),min(im.height,int(d+body*.8))];patch=im.crop(box);path=crops/f'{vid}_R{i+1:02d}.png';patch.save(path)
            display=patch.copy();display.thumbnail((2000,400));canvas=Image.new('RGB',(2000,display.height+28),'white');canvas.paste(display,(0,28));dr=ImageDraw.Draw(canvas);dr.text((3,3),f'{vid} R{i+1:02d} native {box}; proposed body {row["line_id"]}',fill='black');sx=display.width/(box[2]-box[0]);sy=display.height/(box[3]-box[1]);knots=row['source_line']['baseline_polyline_xy'];dr.line([(max(0,min(1999,(x-box[0])*sx)),28+(y-box[1])*sy) for x,y in knots if box[0]<=x<=box[2]],fill='cyan',width=1);patches.append(canvas);draw.rectangle([a*sc,b*sc,c*sc,d*sc],outline='red',width=1);draw.text((a*sc,b*sc),str(i+1),fill='red')
            index.append(dict(view_id=vid,row_number=i+1,line_id=row['line_id'],native_bbox=box,source_row_bbox=row['bbox_xyxy'],body_height=body,native_crop=path.relative_to(OUT).as_posix(),native_source=view['native_source'],split=view['split'],folio_component=view['folio_component'],body_path_knots=knots,status='pending source review'))
        overview.save(gallery/(vid+'_overview.png'))
        for start in range(0,len(patches),8):
            chosen=patches[start:start+8];sheet=Image.new('RGB',(2000,sum(p.height+5 for p in chosen)),'#cccccc');yy=0
            for patch in chosen:sheet.paste(patch,(0,yy));yy+=patch.height+5
            sheet.save(gallery/f'{vid}_rows_{start+1:02d}_{start+len(chosen):02d}.png')
        print(vid,len(patches),flush=True)
    write_json(root/'native_row_review_index.json',index);write_csv(root/'native_row_review_index.csv',index)
if __name__=='__main__':main()
