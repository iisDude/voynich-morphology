"""Register a spatial ink-density path hypothesis, without character bottoms."""
from common import OUT,write_json,sha256

DETECT='''
def detect_lines(mask,config):
    from scipy.ndimage import gaussian_filter1d
    from scipy.signal import find_peaks
    if config.get('geometry_scale')!=1.:return [],[],None
    n,labels,stats,centers=cv2.connectedComponentsWithStats(mask,8)
    candidates=[i for i in range(1,n) if stats[i,4]>=60 and 8<=stats[i,3]<=180 and 3<=stats[i,2]<=800]
    eligible=np.isin(labels,candidates)
    heights=[stats[i,3] for i in candidates if stats[i,3]<=80 and stats[i,4]>=100]
    body=float(np.percentile(heights,60)) if heights else 25.
    width=mask.shape[1];tiles=[]
    for x in range(0,width,64):
        # A dense patch cannot dominate the path vote simply through area.
        tiles.append(np.minimum(eligible[:,x:x+64].sum(axis=1),8))
    profile=gaussian_filter1d(np.sum(tiles,axis=0).astype(float),4)
    centered=profile-gaussian_filter1d(profile,40)
    ac=np.correlate(centered,centered,'full')[len(centered)-1:]
    possible,_=find_peaks(ac)
    possible=[p for p in possible if 20<=p<=150]
    pitch=int(max(possible,key=lambda p:ac[p])) if possible else 60
    minimum_distance=max(15,round(.65*pitch))
    peaks,_=find_peaks(profile,distance=minimum_distance,prominence=max(3,float(profile.max())*.12))
    paths=[]
    for peak in peaks:
        baseline=float(peak+.3*body)
        band=eligible[max(0,round(peak-body*.5)):min(mask.shape[0],round(peak+body*.5))]
        occupied=np.where(band.sum(axis=0)>=2)[0]
        if len(occupied)<100 or not candidates:continue
        x0=int(occupied.min());x1=int(occupied.max())+1
        if x1-x0<config['minimum_line_width_px']:continue
        count=sum(max(0,min(stats[i,1]+stats[i,3],baseline)-max(stats[i,1],baseline-body))>0 for i in candidates)
        if count<6:continue
        paths.append(dict(x0=x0,x1=x1,baseline=baseline,slope=0.,xref=width/2,body_height=body,component_count=count,
            path_peak_y=int(peak),density_profile_peak=float(profile[peak]),pitch_proxy_px=pitch,baseline_uncertainty='unestimated density-to-baseline offset; no glyph or transcription bottom used'))
    return paths,[],labels

'''

def main():
    source=OUT/'src/regional_extract_v9.py';text=source.read_text(encoding='utf-8')
    text=text.replace("'v9'","'v10'").replace('v9 post-unblinding','v10 post-unblinding').replace('extraction_v9_protocol','extraction_v10_protocol')
    text=text.replace('from visual_extract import ink_mask,detect_lines','from visual_extract import ink_mask').replace('def boxes_for(',DETECT+'\ndef boxes_for(')
    target=OUT/'src/regional_extract_v10.py';target.write_text(text,encoding='utf-8')
    write_json(OUT/'data/observations/extraction_v10_protocol.json',dict(version=10,source_sha256=sha256(source),generated_source_sha256=sha256(target),
        change='Path proposals from capped spatial ink-density projection, replacing component-bottom votes. Foreground and core-band ownership remain v9.',
        density='64px vertical tiles; per-row eligible ink capped at 8 in each tile; Gaussian profile sigma4; background trend sigma40 subtracted for pitch estimation.',
        pitch='Largest autocorrelation local peak at lag20..150 only chooses minimum peak spacing 0.65pitch; peaks still occur at observed density maxima, not forced grid.',
        baseline='density peak +0.3 median local component height proxy; horizontal slope zero is an explicit approximation',
        source_gate='source ink coherence/coverage, no expected line counts or comparison strings',
        risks=['Density peak is not an established physical baseline.','Variable line slope and curved paths remain uncertain.','Dense drawings may still make false paths.','Global region body proxy may conflate size variation.'],
        blinding='post-unblinding source-only repair',stage='twelve-view calibration'))

if __name__=='__main__':main()
