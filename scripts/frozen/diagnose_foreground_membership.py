"""Separate source-mask failure from component membership rejection."""
from common import OUT,read_json,write_json
import importlib,numpy as np,cv2
from PIL import Image,ImageDraw

def main():
    vid='V_004';bbox=[420,480,2500,710];tiles=[];results=[]
    for version in ('v4','v5','v6','v7','v8'):
        doc=read_json(OUT/f'data/observations/regional_candidates_{version}/{vid}.json');rgb=np.array(Image.open(OUT/doc['native_source']).convert('RGB'));config=doc['native_mask_config']
        smoothed=cv2.GaussianBlur(rgb,(0,0),config.get('preblur_sigma_px',0) or .001)
        module=importlib.import_module('regional_extract' if version=='v4' else 'regional_extract_'+version)
        mask=module.ink_mask(smoothed,config)
        x0,y0,x1,y1=bbox;crop=Image.fromarray(rgb[y0:y1,x0:x1]);binary=Image.fromarray((255-mask[y0:y1,x0:x1]*255).astype(np.uint8)).convert('RGB')
        crop.thumbnail((1600,300));binary.thumbnail((1600,300));tile=Image.new('RGB',(1600,crop.height+binary.height+30),'white');draw=ImageDraw.Draw(tile)
        draw.text((8,5),f'{version} RAW foreground before component assignment, native bbox {bbox}',fill='black');tile.paste(crop,(0,25));tile.paste(binary,(0,25+crop.height));tiles.append(tile)
        n,labels,stats,_=cv2.connectedComponentsWithStats(mask[y0:y1,x0:x1],8)
        results.append(dict(version=version,raw_ink_pixels=int(mask[y0:y1,x0:x1].sum()),components=n-1,large_components=sorted(stats[1:,4].tolist(),reverse=True)[:10]))
    canvas=Image.new('RGB',(1600,sum(t.height for t in tiles)),'white');y=0
    for tile in tiles:canvas.paste(tile,(0,y));y+=tile.height
    path=OUT/'figures/foreground_membership_diagnostic_V004.png';canvas.save(path);write_json(OUT/'data/observations/foreground_membership_diagnostic_V004.json',dict(native_bbox=bbox,versions=results))

if __name__=='__main__':main()
