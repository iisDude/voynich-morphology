"""Source-layout-only extension registered before any v2 assay inspection."""
from common import OUT,read_json,read_csv,write_json
from datetime import datetime,timezone
from PIL import Image,ImageDraw

def main():
    root=OUT/'data/observations/source_adjudication_v2';dest=root/'dense_blocks';dest.mkdir(exist_ok=True)
    if (dest/'selection.json').exists():raise ValueError('extension already registered')
    sources=read_csv(OUT/'data/source/yale_native_all_manifest.csv');curved={r['view_id'] for r in read_json(root/'queue_plan.json')['curved_views']};pool=[]
    for s in sources:
        obj=read_json(OUT/f'data/observations/regional_candidates_v11/{s["view_id"]}.json')
        w,h=Image.open(OUT/s['path']).size
        if w>=3000 or h/w<1.1 or s['view_id'] in curved:continue
        # Layout only: count candidate rows; no assigned unit families read.
        pool.append(dict(view_id=s['view_id'],split=obj['view']['split'],folio_component=obj['view']['folio_component'],native_source=s['path'],candidate_rows=len(obj['lines']),width=w,height=h))
    selected=[]
    for split,n in [('train',4),('validation',2),('test',2)]:selected.extend(sorted([r for r in pool if r['split']==split],key=lambda r:(-r['candidate_rows'],r['view_id']))[:n])
    write_json(dest/'selection.json',dict(registered_at_utc=datetime.now(timezone.utc).isoformat(),selection='Highest candidate-row count among portrait noncurved native views width<3000; 4 train,2 validation,2 test; no Currier metadata or visual-family/effect input',selected=selected,source_acceptance='Native overview must show dense writing block. Review every extracted row at native scale. Failed extraction retained unknown. No frequency/effect stopping rule.'))
    gallery=OUT/'figures/source_adjudication_v2/dense_blocks';gallery.mkdir(parents=True,exist_ok=True)
    for r in selected:
        im=Image.open(OUT/r['native_source']).convert('RGB');im.thumbnail((1000,1400));canvas=Image.new('RGB',(im.width,im.height+35),'white');canvas.paste(im,(0,35));ImageDraw.Draw(canvas).text((5,5),r['view_id']+' '+r['split']+' source overview',fill='black');canvas.save(gallery/(r['view_id']+'_overview.png'))
    print(selected)
if __name__=='__main__':main()
