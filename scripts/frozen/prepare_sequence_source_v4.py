from common import OUT,read_json,write_json
from register_sequence_v4 import D,T
from PIL import Image,ImageDraw
import numpy as np
G=OUT/'figures/sequence_v4';G.mkdir(exist_ok=True)
def sheet(rows,path,width=1900):
    tiles=[]
    for label,im in rows:
        p=im.copy();p.thumbnail((width,400));t=Image.new('RGB',(width,p.height+28),'white');t.paste(p,(0,28));ImageDraw.Draw(t).text((5,4),label,fill='black');tiles.append(t)
    canvas=Image.new('RGB',(width,sum(t.height+8 for t in tiles)),'#ddd');y=0
    for t in tiles:canvas.paste(t,(0,y));y+=t.height+8
    canvas.save(path)
def main():
    if (D/'native_row_index.json').exists():raise RuntimeError('Prepared already')
    plan=read_json(D/'PLAN.json');index=[];thumbs=[]
    for v in plan['selected_views']:
        im=Image.open(OUT/v['native_source']).convert('RGB');ov=im.copy();ov.thumbnail((590,780));dr=ImageDraw.Draw(ov);scale=ov.width/im.width
        for rn,r in enumerate(v['rows'],1):
            a,b,c,d=r['bbox_xyxy'];body=r['body_height'];box=[max(0,a-75),max(0,int(b-.8*body)),min(im.width,c+75),min(im.height,int(d+.8*body))]
            dr.rectangle([a*scale,b*scale,c*scale,d*scale],outline='red',width=1);dr.text((a*scale,b*scale),str(rn),fill='red')
            index.append(dict(view_id=v['view_id'],row_number=rn,line_id=r['line_id'],native_bbox=box,source_row_bbox=r['bbox_xyxy'],body_height=body,body_path_knots=r['source_line']['baseline_polyline_xy'],native_source=v['native_source'],split=v['split'],folio_component=v['folio_component']))
        top=Image.new('RGB',(600,820),'white');top.paste(ov,(0,30));ImageDraw.Draw(top).text((5,5),v['view_id']+' native-source overview',fill='black');thumbs.append(top)
        ov.save(G/(v['view_id']+'_overview.png'))
    for start in range(0,len(thumbs),6):
        can=Image.new('RGB',(1800,1640),'white')
        for j,im in enumerate(thumbs[start:start+6]):can.paste(im,((j%3)*600,(j//3)*820))
        can.save(G/f'overviews_{start+1:03d}.png')
    write_json(D/'native_row_index.json',index)
    lookup={(r['view_id'],r['row_number']):r for r in index};sample=[lookup[tuple(k)] for k in plan['review_repeatability']['sample']]
    rng=np.random.default_rng(plan['seed']);key=[]
    for passid in ['A','B']:
        order=rng.permutation(len(sample));tiles=[]
        for j,i in enumerate(order):
            r=sample[i];ident=f'{passid}{j+1:03d}';im=Image.open(OUT/r['native_source']).convert('RGB').crop(r['native_bbox']);tiles.append((ident+' native RGB; no class/boundary suggestions',im));key.append(dict(id=ident,view_id=r['view_id'],row_number=r['row_number'],sample_index=int(i)))
        for start in range(0,len(tiles),6):sheet(tiles[start:start+6],G/f'masked_{passid}_{start+1:02d}.png')
    write_json(D/'repeatability_mask_key.json',key)
    print(len(index),'native-coordinate fields and masked repeat sheets prepared',flush=True)
if __name__=='__main__':main()
