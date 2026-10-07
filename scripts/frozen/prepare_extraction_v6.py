"""Register lower-contrast native-path calibration after v5 source rejection."""
from common import OUT,write_json,sha256

def main():
    source=OUT/'src/regional_extract_v5.py';text=source.read_text(encoding='utf-8')
    text=text.replace("'v5'","'v6'").replace('v5 post-unblinding','v6 post-unblinding').replace('extraction_v5_protocol','extraction_v6_protocol')
    a="12 if version=='v6'";b="6 if version=='v6'"
    if a not in text:raise ValueError('Expected registered contrast source missing')
    text=text.replace(a,b)
    target=OUT/'src/regional_extract_v6.py';target.write_text(text,encoding='utf-8')
    write_json(OUT/'data/observations/extraction_v5_pilot_review.json',dict(status='rejected as general method',reviewed_views=12,reviewed_rows=48,
        failure='Contrast 12 removes substantial visible faint writing on V004, fractures some other forms; drawing contamination and multi-row contacts remain.',
        observations={'V004':'all four preview paths fail writing coverage','V052':'plants, detached upper ink and partial rows','V082':'plants and partial rows','V116':'mostly coherent rows, omissions and a stray neighboring descender',
            'V122':'faint forms broken or clipped','V127':'mixed rows and plant/neighboring ink','V136':'mostly coherent partial rows; drawing fragments','V150':'mixed tall forms and drawing contamination',
            'V162':'mostly coherent rows with omissions','V176':'drawing and multi-row contamination','V184':'faint/stained top row fails; star and neighboring tall ink elsewhere','V198':'neighboring rows mixed, top label retained'},
        source_review='untranscribed source and mask previews; no conventional count matching',passed_complete_segmentation=False))
    write_json(OUT/'data/observations/extraction_v6_protocol.json',dict(version=6,source_sha256=sha256(source),generated_source_sha256=sha256(target),
        change='Native foreground contrast 6 instead of 12; all other v5 native path and minimum-component settings retained.',
        decision='Inspect row membership and retained source ink, not conventional counts or positional coefficients.',
        primary_risks=['Texture may reappear.','Faint minim components below size filter remain unknown.','Body-scale, inter-row assignment and drawing boundaries require source audit.'],
        blinding='post-unblinding source-only repair; no claim of fresh blind confirmation',stage='twelve-view calibration; no full scale acceptance yet'))

if __name__=='__main__':main()
