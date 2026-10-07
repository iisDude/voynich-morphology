"""Source-only geometric overlap proposals for repeated physical-side captions."""
from common import OUT,read_csv,write_json,write_csv,SEED,sha256
from collections import defaultdict
from itertools import combinations
from PIL import Image,ImageDraw
import numpy as np
import cv2
import re

def main():
    views=read_csv(OUT/'data/source/all_view_manifest.csv');groups=defaultdict(list)
    for row in views:
        if row['split']!='excluded_cover':
            for side in set(re.findall(r'(?<!\d)\d+[rv]',row['caption'])):groups[side].append(row)
    root=OUT/'tests/physical_overlap_v1';fig=root/'figures';fig.mkdir(parents=True,exist_ok=True);results=[]
    cv2.setRNGSeed(SEED);sift=cv2.SIFT_create(nfeatures=6000)
    seen=set()
    for caption,rows in groups.items():
        for a,b in combinations(rows,2):
            if (a['view_id'],b['view_id']) in seen:continue
            seen.add((a['view_id'],b['view_id']))
            images=[np.asarray(Image.open(OUT/r['image_path']).convert('RGB')) for r in (a,b)];gray=[cv2.cvtColor(im,cv2.COLOR_RGB2GRAY) for im in images];features=[sift.detectAndCompute(g,None) for g in gray];(ka,da),(kb,db)=features
            candidates=cv2.BFMatcher().knnMatch(da,db,k=2);good=[x for x,y in candidates if x.distance<.65*y.distance];model=None;inliers=np.zeros(len(good),bool);error=None
            if len(good)>=12:
                pa=np.float32([ka[m.queryIdx].pt for m in good]);pb=np.float32([kb[m.trainIdx].pt for m in good]);model,mask=cv2.findHomography(pa,pb,cv2.RANSAC,2.,maxIters=10000,confidence=.999)
                if model is not None:
                    inliers=mask.ravel().astype(bool);projected=cv2.perspectiveTransform(pa[None],model)[0];error=float(np.median(np.linalg.norm(projected[inliers]-pb[inliers],axis=1)))
            proposed=bool(inliers.sum()>=30 and inliers.mean()>=.35 and error<=1.) if len(good) else False
            hulls=[]
            if proposed:
                for points in [pa[inliers],pb[inliers]]:hulls.append(cv2.convexHull(points).reshape(-1,2).tolist())
            name=a['view_id']+'__'+b['view_id'];matched=cv2.drawMatches(images[0],ka,images[1],kb,[m for m,k in zip(good,inliers) if k],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS);canvas=Image.fromarray(matched);canvas.thumbnail((1800,1000));canvas.save(fig/f'{name}.png')
            record=dict(caption=caption,from_view=a['view_id'],to_view=b['view_id'],matches=len(good),inliers=int(inliers.sum()),median_error_pdf_px=error,status='geometric overlap proposal: source review required' if proposed else 'no reliable overlap recovered',pdf_from_to_homography=model.tolist() if model is not None else None,inlier_hulls_pdf_pixels=hulls,
              source_review='unreviewed',interpretation='Image feature overlap is not a verified panel boundary or physical bifolio. No transcription text or conventional unit count used.',figure=f'tests/physical_overlap_v1/figures/{name}.png')
            results.append(record);print(name,record['status'],record['inliers'],flush=True)
    write_json(root/'results.json',results);write_csv(root/'results.csv',[{k:r[k] for k in ['caption','from_view','to_view','matches','inliers','median_error_pdf_px','status']} for r in results]);write_json(root/'config.json',dict(seed=SEED,sift_features=6000,ratio=.65,ransac_px=2.,minimum_inliers=30,minimum_inlier_fraction=.35,maximum_median_error_px=1.,pair_selection='shared folio-side caption references, including differently worded repeated part views; each view pair once',images='PDF embedded captures; transforms explicitly in PDF image pixels'))
    write_json(root/'input_manifest.json',dict(manifest='data/source/all_view_manifest.csv',manifest_sha256=sha256(OUT/'data/source/all_view_manifest.csv'),source_sha256=sha256(OUT/'src/physical_view_overlap_v1.py')))
    (root/'run.py').write_text('from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]/"src"))\nfrom physical_view_overlap_v1 import main\nmain()\n',encoding='utf-8')
    (root/'README.md').write_text('# Physical capture overlap\n\nSource-only geometric proposals require source review. Absence of recovered feature matches does not prove different physical panels. Writing deduplication is not silently performed.\n',encoding='utf-8')
    (root/'summary.md').write_text('# Repeated caption overlap\n\nHomography proposals relate image captures, not transcription units. Source review and dense writing/panel annotation are needed before a deduplicated manuscript sequence can be certified. Caption-connected views remain in the same data split.\n',encoding='utf-8')

if __name__=='__main__':main()
