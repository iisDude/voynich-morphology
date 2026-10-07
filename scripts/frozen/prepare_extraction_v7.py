"""A distinct paper-envelope foreground hypothesis after Gaussian-mask failure."""
from common import OUT,write_json,sha256

INK='''
def ink_mask(rgb,config,contrast=None):
    # A grayscale closing fills dark strokes to estimate a local paper
    # envelope. Source RGB is unchanged; binary topology stays hypothetical.
    gray=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY).astype(np.float32)
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(51,51))
    paper=cv2.morphologyEx(gray,cv2.MORPH_CLOSE,kernel)
    residual=(paper-gray)/np.maximum(paper,1.)
    r,g,b=[rgb[:,:,i].astype(np.int16) for i in range(3)]
    limits=config['color_limits']
    color=(r-g>=limits['r_minus_g_min'])&(r-g<=limits['r_minus_g_max'])&(b-r<=limits['b_minus_r_max'])
    return ((residual>=.035)&color).astype(np.uint8)

'''

def main():
    source=OUT/'src/regional_extract_v6.py';text=source.read_text(encoding='utf-8')
    text=text.replace("'v6'","'v7'").replace('v6 post-unblinding','v7 post-unblinding').replace('extraction_v6_protocol','extraction_v7_protocol')
    text=text.replace('from visual_extract import ink_mask,detect_lines','from visual_extract import detect_lines')
    text=text.replace('def boxes_for(',INK+'\ndef boxes_for(')
    target=OUT/'src/regional_extract_v7.py';target.write_text(text,encoding='utf-8')
    write_json(OUT/'data/observations/extraction_v7_protocol.json',dict(version=7,source_sha256=sha256(source),generated_source_sha256=sha256(target),
        foreground='51px ellipse morphological grayscale closing estimates paper; relative darkness >=0.035; existing broad color limits',
        changes='Foreground background model only; native paths and component filters remain v6.',
        rationale='Gaussian local average can be depressed by dense ink. Envelope estimates local paper while retaining original RGB.',
        review='Source ink coverage, false rows, neighboring-row contamination and drawings; never comparison strings/counts/effects.',
        blinding='post-unblinding repair',stage='twelve-view calibration before scale'))

if __name__=='__main__':main()
