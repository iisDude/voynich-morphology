from inventory_v6_common import *
from PIL import Image,ImageDraw
def main():
    guard();rec={r['parent_id']:r for r in read_json(D/'discovery_parents.json')};comp=read_json(D/'composition_discovery.json');rows=[]
    for family,c in comp['candidates'].items():
        if not c['eligible']:continue
        ps=[p for p in comp['parents'] if any(q['description']==family for q in p['explanations'])][:10]
        can=Image.new('RGB',(1400,((len(ps)+4)//5)*230),'#eee');dr=ImageDraw.Draw(can)
        for j,p in enumerate(ps):
            r=rec[p['parent_id']];q=next(q for q in p['explanations'] if q['description']==family);x,y,c,d=r['native_bbox'];rgb=Image.open(OUT/r['native_source']).convert('RGB');im=rgb.crop((x-10,y-10,c+10,d+10));sc=min(3,260/im.width,170/im.height);im=im.resize((round(im.width*sc),round(im.height*sc)),Image.Resampling.NEAREST);a=(j%5)*280;b=(j//5)*230;can.paste(im,(a+5,b+35));xx,yy,xe,ye=q['base_local_bbox'];dr.rectangle((a+5+(xx+10)*sc,b+35+(yy+10)*sc,a+5+(xe+10)*sc,b+35+(ye+10)*sc),outline='#c30',width=2);dr.text((a+5,b+3),r['parent_id']+' cap'+r['caption'],fill='black');dr.text((a+5,b+19),q['side']+' removal '+str(q['fraction']),fill='black');dr.text((a+5,b+211),'red=proposed base extent',fill='black');rows.append(dict(parent_id=r['parent_id'],family=family,base_description=q['description']))
        can.save(G/('factor_'+family.replace('+','_')+'.png'))
    save(D/'factor_review_index.json',rows)
if __name__=='__main__':main()
