"""Show exactly assigned ink, separating crop context from row membership."""
from common import OUT,read_json,write_json
from analyse_native_structure import unpack
import numpy as np
from PIL import Image,ImageDraw,ImageFont

def main():
    audit=read_json(OUT/'data/comparisons/v2/visual_row_alignment_source_audit.json');folder=OUT/'figures/crosswalk_mask_audit_v0';folder.mkdir(parents=True,exist_ok=True)
    font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
    for number,r in enumerate(audit,1):
        vid=r['view_id'];obj=read_json(OUT/f'data/observations/regional_candidates_v4/{vid}.json');instances={i['instance_id']:i for i in obj['instances']};groups={g['group_id']:g for g in obj['groups']};data=np.load(OUT/f'data/observations/regional_candidates_v4/{vid}_native_masks.npz')
        bounds=r['visual_bboxes'];x0=min(b[0] for b in bounds)-10;y0=min(b[1] for b in bounds)-10;x1=max(b[2] for b in bounds)+10;y1=max(b[3] for b in bounds)+10
        with Image.open(OUT/obj['native_source']) as source:rgb=np.array(source.crop((x0,y0,x1,y1)).convert('RGB'))
        mask=np.zeros(rgb.shape[:2],np.uint8)
        for groupid in r['visual_groups']:
            group=groups[groupid]
            for instanceid in group['models']['group_only']:
                rec=instances[instanceid];b=rec['bbox_xyxy'];piece=unpack(data,rec['shape_index']);mask[b[1]-y0:b[3]-y0,b[0]-x0:b[2]-x0]|=piece
        overlay=rgb.copy();overlay[mask>0]=np.round(.3*rgb[mask>0]+.7*np.array([255,0,180])).astype(np.uint8)
        source=Image.fromarray(rgb);highlight=Image.fromarray(overlay);binary=Image.fromarray(255-mask*255).convert('RGB')
        for pic in (source,highlight,binary):pic.thumbnail((1800,500))
        canvas=Image.new('RGB',(max(1000,source.width),sum(pic.height for pic in (source,highlight,binary))+120),'white');draw=ImageDraw.Draw(canvas)
        draw.text((8,5),f'{number:02d} {vid} {r["visual_line_id"]}: source / assigned ink in magenta / exact assigned mask',fill='black',font=font)
        y=35
        for pic in (source,highlight,binary):canvas.paste(pic,(0,y));y+=pic.height+10
        draw.text((8,y+5),'Other ink visible in the source is context, not automatically assigned. No comparison strings shown.',fill='black',font=font)
        canvas.save(folder/f'audit_{number:02d}.png');r['membership_overlay']=(folder/f'audit_{number:02d}.png').relative_to(OUT).as_posix()
    write_json(OUT/'data/comparisons/v2/visual_membership_overlay_audit_plan.json',audit)

if __name__=='__main__':main()
