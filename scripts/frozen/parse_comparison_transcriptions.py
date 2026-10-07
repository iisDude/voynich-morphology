"""Conservative IVTFF comparison parsing, permitted only after visual freeze.

Literal transcription codepoints are an inherited unit hypothesis. Ambiguous
groups retain source slots and are not repaired using the visual assignments.
"""
from common import ROOT,OUT,read_json,read_csv,write_json,sha256
import re
import hashlib

SOURCES={'ZL_EVA':'httpswww.voynich.nudataZL3b-.txt','RF':'httpsvoynich-nudataRF1b-e.txt','v101':'httpsvoynich.nudataGC2a-n.txt'}


def main():
    freeze=OUT/'data/observations/visual_dataset_v0/FREEZE_MANIFEST.json'
    if not freeze.exists():raise ValueError('Visual dataset has not frozen; do not read transcriptions')
    manifest=read_json(freeze)
    if manifest['comparison_transcription_contents_opened']:raise ValueError('Unexpected visual snapshot provenance')
    # Verify frozen identities and sequence dataset before opening comparisons.
    critical=[r for r in manifest['files'] if r['path'].endswith(('assay_groups.json','fine_family_source_review_v4.json','medium_family_source_review_v4.json','visual_structure_merge_hypotheses_v0.json'))]
    for r in critical:
        if sha256(OUT/r['path'])!=r['sha256']:raise ValueError('Frozen candidate identities changed')
    views=read_csv(OUT/'data/source/all_view_manifest.csv');captions={}
    for v in views:
        for f in re.findall(r'(?<!\d)(\d+)([rv])',v['caption']):
            folio='f'+f[0]+f[1];captions.setdefault(folio,[]).append(v)
    summary=[]
    for name,filename in SOURCES.items():
        source=ROOT/filename;text=source.read_text(encoding='utf-8-sig',errors='strict')
        page_meta={};lines=[];groups=[];excluded=[];duplicate=[];seen={};header=None
        for lineno,raw in enumerate(text.splitlines(),1):
            # Header and locus syntax are checked against observed source records
            # after the guard. No token repairs or alphabet normalization occur.
            match=re.match(r'^\s*(?:#\s*)?<([^>]+)>\s*(.*)$',raw)
            if not match:continue
            locus,body=match.groups()
            folio=re.match(r'^(f\d+[rv](?:\d+)?)',locus)
            if folio is None:continue
            folio=folio.group(1)
            metadata=dict(re.findall(r'\$([A-Za-z])=([^\s{}]+)',body))
            if '.' not in locus:
                if metadata:page_meta.setdefault(folio,{}).update(metadata)
                header=folio;continue
            if metadata:page_meta.setdefault(folio,{}).update(metadata)
            key=locus.split(';',1)[0];transcriber=locus.split(';',1)[1] if ';' in locus else None
            if key in seen:
                duplicate.append(dict(source_line=lineno,locus=locus,first_source_line=seen[key],raw=body));continue
            seen[key]=lineno
            meta=page_meta.get(folio,{});physical=captions.get(folio,[])
            component=physical[0]['folio_component'] if physical else folio
            split=physical[0]['split'] if physical else ('train','train','train','validation','test')[int(hashlib.sha256(component.encode()).hexdigest()[:8],16)%5]
            # Comments are preserved in raw text and removed only from candidate
            # comparison strings. A token with other markup is abstained.
            cleaned=re.sub(r'\{[^}]*\}','',body).strip()
            slots=[s for s in re.split(r'[.\s]+',cleaned) if s]
            lineid=f'{name}|{key}';retained=[]
            for i,token in enumerate(slots):
                valid=bool(re.fullmatch(r'[a-z]+',token)) if name!='v101' else bool(re.fullmatch(r'[A-Za-z0-9]+',token))
                record=dict(group_id=f'{lineid}|G{i:03d}',line_id=lineid,physical_locus=key,folio=folio,folio_component=component,
                    split=split,group_rank=i,group_count=len(slots),normalized_group_rank=i/(len(slots)-1) if len(slots)>1 else .5,
                    normalized_pixel_center=None,source_pixel_center_x=None,source_pixel_x_page_fraction=None,
                    units=list(token) if valid else None,form=token,section=meta.get('I'),hand=meta.get('H'),currier=meta.get('L'),
                    transcriber=transcriber,source_line=lineno,locus_kind=re.search(r'@([A-Za-z]+)',key).group(1) if re.search(r'@([A-Za-z]+)',key) else None,
                    coordinate_kind='conventional source group ordinal rank; native pixel position unknown unless independently mapped',
                    parsing_status='literal codepoint comparison hypothesis' if valid else 'abstained: ambiguous or extended transcription notation')
                groups.append(record)
                if valid:retained.append(record['group_id'])
                else:excluded.append(record)
            lines.append(dict(line_id=lineid,physical_locus=key,folio=folio,source_line=lineno,raw=body,
                metadata=meta,groups=len(slots),retained_groups=retained,locus_kind=groups[-1]['locus_kind'] if slots else None))
        # Metadata may appear after initial loci; update only metadata fields.
        for g in groups:
            meta=page_meta.get(g['folio'],{});g.update(section=meta.get('I'),hand=meta.get('H'),currier=meta.get('L'))
        folder=OUT/'data/comparisons';folder.mkdir(parents=True,exist_ok=True)
        write_json(folder/f'{name}_groups.json',groups);write_json(folder/f'{name}_lines.json',lines);write_json(folder/f'{name}_metadata.json',page_meta)
        write_json(folder/f'{name}_excluded.json',excluded);write_json(folder/f'{name}_duplicate_loci.json',duplicate)
        retained=[g for g in groups if g['units'] is not None]
        summary.append(dict(dataset=name,filename=filename,source_sha256=sha256(source),visual_freeze_sha256=sha256(freeze),
            parsed_lines=len(lines),all_source_slots=len(groups),retained_groups=len(retained),types=len(set(g['form'] for g in retained)),
            currier_counts={c:sum(g['currier']==c for g in retained) for c in sorted(set(g['currier'] for g in retained),key=str)},
            locus_kinds={c:sum(g['locus_kind']==c for g in retained) for c in sorted(set(g['locus_kind'] for g in retained),key=str)},
            abstained_groups=len(excluded),duplicate_loci=len(duplicate),
            limitations=['Literal codepoints are not asserted conventional graphemes.','First occurrence per physical locus retained; alternative transcribers recorded.',
                'Uncertainty/extended notation abstained without choosing alternatives.','All raw source slots determine rank; removing ambiguous groups does not renumber physical slots.']))
        print(summary[-1],flush=True)
    write_json(OUT/'data/comparisons/comparison_manifest.json',dict(visual_freeze_sha256=sha256(freeze),datasets=summary,
        first_comparison_open_after_visual_freeze=True,status='conservative parser; source syntax review required'))

if __name__=='__main__':main()
