"""Register core-band ownership after separating raw mask and membership errors."""
from common import OUT,write_json,sha256

OLD='''            distances=np.array([abs(y+ch-1-l['native_baseline']-l['native_slope']*(cx-l['native_xref']))/max(1,l['native_body']) for l in kept])
            if not len(distances):continue
            winner=int(distances.argmin());line=kept[winner];body=line['native_body']
            if distances[winner]>.65 or ch>3.5*body or cw>8*body:continue
            memberships[winner].append(dict(label=ci,x0=x,y0=y,x1=x+cw,y1=y+ch,width=cw,height=ch,area=area,cx=float(cx),cy=float(cy),baseline_distance_body=float(distances[winner])))'''
NEW='''            if not kept:continue
            py,px=np.nonzero(labels[y-ny0:y-ny0+ch,x-nx0:x-nx0+cw]==ci)
            py=py+y;px=px+x
            supports=[];bottom_distances=[];ownership_scores=[]
            for line in kept:
                body=max(12.,line['native_body'])
                baseline=line['native_baseline']+line['native_slope']*(px-line['native_xref'])
                support=float(np.mean((py>=baseline-body)&(py<=baseline+.25*body)))
                bottom=float(abs(y+ch-1-line['native_baseline']-line['native_slope']*(cx-line['native_xref']))/body)
                supports.append(support);bottom_distances.append(bottom)
                ownership_scores.append(support-.25*min(bottom,4.))
            winner=int(np.argmax(ownership_scores));line=kept[winner];body=max(12.,line['native_body'])
            if supports[winner]<.12 or ch>5*body or cw>20*body:continue
            rival_support=max([s for i,s in enumerate(supports) if i!=winner],default=0.)
            memberships[winner].append(dict(label=ci,x0=x,y0=y,x1=x+cw,y1=y+ch,width=cw,height=ch,area=area,cx=float(cx),cy=float(cy),
                baseline_distance_body=float(bottom_distances[winner]),core_band_ink_fraction=float(supports[winner]),
                other_row_core_support_fraction=float(rival_support),multiline_contact=bool(rival_support>=.3)))'''

def main():
    source=OUT/'src/regional_extract_v5.py';text=source.read_text(encoding='utf-8')
    if OLD not in text:raise ValueError('Registered membership source has changed')
    text=text.replace(OLD,NEW).replace("'v5'","'v9'").replace('v5 post-unblinding','v9 post-unblinding').replace('extraction_v5_protocol','extraction_v9_protocol')
    anchor="            if x1-x0<3*body:continue"
    if anchor not in text:raise ValueError('Line quality anchor absent')
    text=text.replace(anchor,anchor+"\n            if sum(c['area'] for c in members)/max(1,(x1-x0)*body)<.05:continue")
    text=text.replace("membership_rule='raster-component lowest pixel within 0.65 local-body height of closest proposed baseline'", "membership_rule='maximum core-band ink fraction minus 0.25 bottom-distance/body; ambiguous row contacts retained',multiline_component_count=sum(c['multiline_contact'] for c in members),core_band_component_ink_fraction_mean=float(np.mean([c['core_band_ink_fraction'] for c in members]))")
    target=OUT/'src/regional_extract_v9.py';target.write_text(text,encoding='utf-8')
    write_json(OUT/'data/observations/extraction_v9_protocol.json',dict(version=9,source_sha256=sha256(source),generated_source_sha256=sha256(target),
        diagnosis='Raw v5 foreground retains substantially more source writing than its assigned row masks. Hard lowest-pixel tolerance and width cutoff remove valid assemblies.',
        foreground='v5 Gaussian foreground: native preblur 1.2, background sigma 25, contrast 12; source RGB untouched',
        paths='native paths at every scale; baseline detector and minimum components unchanged from v5',
        membership='fraction of component ink in [baseline-body,baseline+0.25body], minus 0.25 normalized lowest-pixel distance, capped at four body units; minimum support 0.12',
        size='retain components up to five body heights and twenty body widths, with body lower bound 12px; original raster masks preserve excluded alternatives',
        row_gate='assigned ink area divided by line span times body must be >=0.05; no transcription target',
        ambiguity='component with >=0.3 ink support in another core band is flagged; no true pen-lift or grapheme claim',
        blinding='post-unblinding source-only repair',selection='twelve-view source calibration before any manuscript scale or unit fitting; no comparison/effect fitting'))

if __name__=='__main__':main()
