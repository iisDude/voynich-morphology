"""Prepare a separate source-only extraction experiment; retain frozen v4.

Changes are registered before v5 source review, with no transcription count or
positional outcome in the selection rule. Previous comparison exposure makes
this an explicitly post-unblinding repair, not a fresh blind replication.
"""
from common import OUT,write_json,sha256

def main():
    source=OUT/'src/regional_extract.py';text=source.read_text(encoding='utf-8')
    substitutions=[
        ("version='v4'","version='v5'"),
        ("version=='v4'","version=='v5'"),
        (".9 if version=='v5'","1.2 if version=='v5'"),
        ("6 if version=='v5'","12 if version=='v5'"),
        ("cv2.GaussianBlur(rgb,(0,0),.9)","cv2.GaussianBlur(rgb,(0,0),1.2)"),
        ("version in ('v3','v4') and scale>3","version=='v5'"),
        ("component_area_px=[12,16000],component_height_px=[4,240],component_width_px=[2,600]","component_area_px=[60,16000],component_height_px=[8,240],component_width_px=[3,600]"),
        ("baseline_peak_min_distance_px=24","baseline_peak_min_distance_px=40"),
        ("if area<12 or cw<2 or ch<3:continue","if area<60 or cw<3 or ch<8:continue"),
        ("choices=['v1','v2','v3','v4'],default='v4'","choices=['v5'],default='v5'"),
    ]
    changes=[]
    for a,b in substitutions:
        count=text.count(a)
        if not count:raise ValueError('Unmatched preparation change: '+a)
        text=text.replace(a,b);changes.append(dict(before=a,after=b,replacements=count))
    header='"""v5 post-unblinding source-only repair. Frozen v4 remains unchanged.\nSee extraction_v5_protocol.json for prespecified changes and limitations.\n"""\n'
    # Retain original docstring as a harmless second string expression.
    target=OUT/'src/regional_extract_v5.py';target.write_text(header+text,encoding='utf-8')
    write_json(OUT/'data/observations/extraction_v5_protocol.json',dict(version=5,source_sha256=sha256(source),generated_source_sha256=sha256(target),
        changes=changes,pilot_views=[4,52,82,116,122,127,136,150,162,176,184,198],
        selection='Review complete source line crops for coherent row membership, retained visible ink and texture/drawing contamination. No source transcription strings/counts or positional outcomes enter parameter choice.',
        aim='Reduce faint parchment bridges and tiny false gap groups; native paths on every source.',
        costs=['Faint writing may disappear; all v4 candidates retained as alternatives.','Fixed native seed sizes may fail very small foldout writing.','A stricter mask is not a validated pen trajectory.'],
        blinding='Post-unblinding repair; inherited transcriptions have already been examined. Never call this a fresh blind confirmation.',
        freeze='v4 visual_candidate_v0 untouched; v5 not admitted until pilot source audit'))

if __name__=='__main__':main()
