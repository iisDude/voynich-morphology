"""Full-width source contexts and native-resolution local cases; no effects."""
from common import OUT,read_json
from PIL import Image,ImageDraw
import math

def main():
    q=read_json(OUT/'data/observations/source_adjudication_v2/queue_plan.json')
    dest=OUT/'figures/source_adjudication_v2'
    for row in q['selected_rows']:
        im=Image.open(OUT/row['native_source']).convert('RGB');a,b,c,d=row['bbox_xyxy'];body=row['body_height_proxy_px'];y0=max(0,int(b-2*body));y1=min(im.height,int(d+2*body))
        source=im.crop((0,y0,im.width,y1));source.thumbnail((2200,900));canvas=Image.new('RGB',(source.width+20,source.height+50),'white');canvas.paste(source,(10,40));draw=ImageDraw.Draw(canvas);draw.text((10,5),row['case_id']+' FULL WIDTH native [0,'+str(y0)+','+str(im.width)+','+str(y1)+']',fill='black');sc=source.width/im.width;draw.rectangle([10+a*sc,40+(b-y0)*sc,10+c*sc,40+(d-y0)*sc],outline='magenta',width=2);canvas.save(dest/(row['view_id']+'_full_row.png'))
        cases=[r for r in q['selected_local_assemblies'] if r['view_id']==row['view_id']];tiles=[]
        for case in cases:
            crop=Image.open(dest/(case['case_id']+'.png')).convert('RGB');tile=Image.new('RGB',(max(480,crop.width+20),crop.height+50),'white');tile.paste(crop,(10,40));ImageDraw.Draw(tile).text((10,5),case['case_id']+' '+str(case['bbox_xyxy']),fill='black');tiles.append(tile)
        width=max(t.width for t in tiles)*2;heights=[max(t.height for t in tiles[i:i+2]) for i in range(0,len(tiles),2)];canvas=Image.new('RGB',(width,sum(heights)),'#ddd');y=0
        for i,h in zip(range(0,len(tiles),2),heights):
            for j,tile in enumerate(tiles[i:i+2]):canvas.paste(tile,(j*width//2,y))
            y+=h
        canvas.save(dest/(row['view_id']+'_local_cases.png'))
    # Curved captures: overview + native quadrant crops; panel folds remain source coordinates.
    for case in q['curved_views']:
        im=Image.open(OUT/case['native_source']).convert('RGB');overview=im.copy();overview.thumbnail((1600,1600));overview.save(dest/(case['view_id']+'_curved_overview.png'))
        w,h=im.size
        for side,box in [('top',[0,0,w,h//2]),('bottom',[0,h//2,w,h])]:
            patch=im.crop(box);patch.thumbnail((2400,1400));patch.save(dest/(case['view_id']+'_curved_'+side+'.png'))

if __name__=='__main__':main()
