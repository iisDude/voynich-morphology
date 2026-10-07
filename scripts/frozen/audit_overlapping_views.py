"""Image-only overlap audit for views whose captions name the same leaf side.

The registration is acquisition geometry, not a transcription alignment.
"""
from common import OUT,read_csv,write_json
import re
import itertools
import numpy as np
import cv2


def main():
    views=[r for r in read_csv(OUT/'data/source/all_view_manifest.csv') if r['split']!='excluded_cover']
    for row in views:row['leaf_sides']=set(re.findall(r'(\d+[rv])',row['caption']))
    pairs=[(a,b) for a,b in itertools.combinations(views,2) if a['leaf_sides']&b['leaf_sides']]
    cache={};sift=cv2.SIFT_create(nfeatures=5000)
    for row in views:
        if not any(row['view_id'] in (a['view_id'],b['view_id']) for a,b in pairs):continue
        gray=cv2.imread(str(OUT/row['image_path']),cv2.IMREAD_GRAYSCALE)
        kp,des=sift.detectAndCompute(gray,None);cache[row['view_id']]=(np.array([p.pt for p in kp],np.float32),des)
    results=[]
    for a,b in pairs:
        pa,da=cache[a['view_id']];pb,db=cache[b['view_id']]
        matches=cv2.BFMatcher().knnMatch(da,db,k=2)
        good=[m for m,n in matches if m.distance<.70*n.distance]
        result=dict(from_view=a['view_id'],to_view=b['view_id'],shared_leaf_sides=sorted(a['leaf_sides']&b['leaf_sides']),matches=len(good),status='no_verified_overlap')
        if len(good)>=12:
            xa=np.array([pa[m.queryIdx] for m in good]);xb=np.array([pb[m.trainIdx] for m in good])
            matrix,inliers=cv2.findHomography(xa,xb,cv2.RANSAC,2.)
            if matrix is not None and np.isfinite(matrix).all() and abs(np.linalg.det(matrix))>1e-10 and np.linalg.cond(matrix)<1e10:
                flags=inliers[:,0].astype(bool);pred=cv2.perspectiveTransform(xa[:,None,:],matrix)[:,0,:]
                error=np.linalg.norm(pred-xb,axis=1)
                result.update(inliers=int(flags.sum()),median_error_pdf_px=float(np.median(error[flags])),pdf_from_to_homography=matrix.tolist(),pdf_to_from_homography=np.linalg.inv(matrix).tolist())
                spread=np.ptp(xa[flags],axis=0)
                result['inlier_span_px']=spread.tolist()
                if flags.sum()>=80 and np.median(error[flags])<=1 and min(spread)>=100:
                    result['status']='verified_overlap_candidate'
                    result['limitation']='Image registration alone does not identify every physical panel. Review overlap crops before excluding occurrences.'
        results.append(result)
    write_json(OUT/'data/source/overlapping_view_registrations.json',results)
    print(dict(pairs=len(results),registered=sum(r['status']=='verified_overlap_candidate' for r in results)),flush=True)


if __name__=='__main__':main()
