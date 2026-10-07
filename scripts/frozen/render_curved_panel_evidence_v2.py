"""Native local evidence for curved paths and caption-shared foldout pairs."""
from common import OUT,read_json,read_csv
from PIL import Image,ImageDraw

def main():
    q=read_json(OUT/'data/observations/source_adjudication_v2/queue_plan.json');dest=OUT/'figures/source_adjudication_v2';sources={r['view_id']:r for r in read_csv(OUT/'data/source/yale_native_all_manifest.csv')}
    for case in q['curved_views']:
        im=Image.open(OUT/case['native_source']).convert('RGB');obj=read_json(OUT/case['hypotheses_path']);tiles=[]
        for region in obj['regions'][:1]:
            cx,cy=region['native_ellipse_center'];rx,ry=region['native_ellipse_radii']
            for label,x,y in [('top',cx,cy-ry*.9),('right',cx+rx*.9,cy),('bottom',cx,cy+ry*.9),('left',cx-rx*.9,cy)]:
                x0=max(0,min(im.width-650,round(x-325)));y0=max(0,min(im.height-650,round(y-325)));box=[x0,y0,min(im.width,x0+650),min(im.height,y0+650)];crop=im.crop(box)
                tile=Image.new('RGB',(670,700),'white');tile.paste(crop,(10,40));ImageDraw.Draw(tile).text((10,5),case['case_id']+' '+label+' '+str(box),fill='black');tiles.append(tile)
        canvas=Image.new('RGB',(1340,1400),'#ddd')
        for i,tile in enumerate(tiles):canvas.paste(tile,((i%2)*670,(i//2)*700))
        canvas.save(dest/(case['view_id']+'_curved_native.png'))
    for pair in q['foldout_pairs']:
        tiles=[]
        for vid in [pair['from_view'],pair['to_view']]:
            im=Image.open(OUT/sources[vid]['path']).convert('RGB');w,h=im.size;im.thumbnail((1100,1300));tile=Image.new('RGB',(1120,im.height+70),'white');tile.paste(im,(10,60));d=ImageDraw.Draw(tile);d.text((10,5),vid+' native '+str([w,h])+'; x-grid = native image fractions',fill='black')
            for f in [.25,.5,.75]:
                x=10+im.width*f;d.line([x,60,x,60+im.height],fill='#555',width=1);d.text((x+2,35),str(round(w*f)),fill='black')
            tiles.append(tile)
        canvas=Image.new('RGB',(2240,max(t.height for t in tiles)),'white')
        for i,tile in enumerate(tiles):canvas.paste(tile,(i*1120,0))
        canvas.save(dest/(pair['from_view']+'__'+pair['to_view']+'_native_panels.png'))

if __name__=='__main__':main()
