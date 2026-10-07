"""Register a multiscale dark-ridge foreground hypothesis, independent of text."""
from common import OUT,write_json,sha256

INK='''
def ink_mask(rgb,config,contrast=None):
    gray=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY).astype(np.float32)
    response=np.zeros_like(gray)
    for sigma in (1.5,2.5):
        smoothed=cv2.GaussianBlur(gray,(0,0),sigma)
        dxx=cv2.Sobel(smoothed,cv2.CV_32F,2,0,ksize=3,scale=.25)*sigma*sigma
        dyy=cv2.Sobel(smoothed,cv2.CV_32F,0,2,ksize=3,scale=.25)*sigma*sigma
        dxy=cv2.Sobel(smoothed,cv2.CV_32F,1,1,ksize=3,scale=.25)*sigma*sigma
        radius=np.sqrt((dxx-dyy)**2+4*dxy*dxy)
        low=(dxx+dyy-radius)/2;high=(dxx+dyy+radius)/2
        value=np.maximum(high,0)*np.exp(-.5*(low/np.maximum(high,1e-4)/.5)**2)
        response=np.maximum(response,value)
    ridges=(response>=8).astype(np.uint8)
    paper=cv2.morphologyEx(gray,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(51,51)))
    dark=(paper-gray)>=8
    nearby=cv2.dilate(ridges,np.ones((5,5),np.uint8))>0
    r,g,b=[rgb[:,:,i].astype(np.int16) for i in range(3)]
    limits=config['color_limits']
    color=(r-g>=limits['r_minus_g_min'])&(r-g<=limits['r_minus_g_max'])&(b-r<=limits['b_minus_r_max'])
    return (dark&nearby&color).astype(np.uint8)

'''

def main():
    source=OUT/'src/regional_extract_v6.py';text=source.read_text(encoding='utf-8')
    text=text.replace("'v6'","'v8'").replace('v6 post-unblinding','v8 post-unblinding').replace('extraction_v6_protocol','extraction_v8_protocol')
    text=text.replace('from visual_extract import ink_mask,detect_lines','from visual_extract import detect_lines').replace('def boxes_for(',INK+'\ndef boxes_for(')
    target=OUT/'src/regional_extract_v8.py';target.write_text(text,encoding='utf-8')
    write_json(OUT/'data/observations/extraction_v8_protocol.json',dict(version=8,source_sha256=sha256(source),generated_source_sha256=sha256(target),
        foreground='Positive dark-ridge Hessian at sigma 1.5/2.5, scale normalized, eigenvalue-ratio penalty width 0.5; response >=8; retain dark paper-envelope pixels within 2px of ridge.',
        envelope='51px ellipse grayscale closing; source-relative darkness >=8 intensity levels; existing color limits',
        limitations=['Junction shape and nib width affect ridgeness.','Dilated ridge support is algorithmic, never claimed pen connectivity.','Paper scratches and drawings may also be ridges.','No recovered unit or accepted row until source audited.'],
        decision='Source coverage, row coherence and drawing/texture contamination, without transcription or positional targets.',
        blinding='post-unblinding repair',stage='twelve-view calibration'))

if __name__=='__main__':main()
