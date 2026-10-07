"""Post-freeze IVTFF 2 comparison parser; preserve literal signs and uncertainty.

This creates a new comparison version. It never changes a frozen visual unit.
Primary apparent-boundary hypothesis splits uncertain commas, while alternative
join records remain available. Angle annotations are not alphabet characters.
"""
from common import ROOT, OUT, read_json, read_csv, write_json, sha256
from parse_comparison_transcriptions import SOURCES
from collections import Counter
import re, hashlib

DEST=OUT/'data/comparisons/v2'

def logical_lines(text):
    pending=None
    for number, raw in enumerate(text.splitlines(),1):
        if raw.startswith('#') or not raw.strip():continue
        if pending:
            if not raw.lstrip().startswith('/'):raise ValueError('Missing IVTFF continuation')
            pending[1]+=raw.lstrip()[1:]
        else:pending=[number,raw]
        if pending[1].rstrip().endswith('/'):
            pending[1]=pending[1].rstrip()[:-1];continue
        yield pending;pending=None
    if pending:raise ValueError('Incomplete continuation')

def clean(body, metadata):
    events=[]
    def annotation(m):
        token=m.group(1)
        tag=re.fullmatch(r'@([A-Za-z])=([^\s]+)',token)
        if tag:
            metadata[tag[1]]=tag[2];events.append(token)
        return '.' if token in ('-','~') else ''
    value=re.sub(r'<([^>]*)>',annotation,body)
    value=re.sub(r'\s+','',value)
    # Ligature braces are markup around retained signs; their spans are also
    # stored separately, without assuming either atomization is correct.
    ligatures=re.findall(r'\{([^{}]*)\}',value)
    value=value.replace('{','').replace('}','')
    return value,events,ligatures

def signs(token,name):
    if any(x in token for x in '[]:?<>/{},'):return None
    units=[];i=0
    while i<len(token):
        if token[i]=='@':
            m=re.match(r'@(\d+);',token[i:])
            if not m or not 128<=int(m[1])<=255:return None
            units.append(m[0]);i+=len(m[0]);continue
        if token[i] in '.;' or (name!='v101' and not token[i].islower()):return None
        units.append(token[i]);i+=1
    return units or None

def main():
    freeze=OUT/'data/observations/visual_dataset_v0/FREEZE_MANIFEST.json'
    frozen=read_json(freeze)
    for entry in frozen['files']:
        if entry['path'].endswith('assay_groups.json') and sha256(OUT/entry['path'])!=entry['sha256']:
            raise ValueError('Visual sequences have changed')
    captions={}
    for v in read_csv(OUT/'data/source/all_view_manifest.csv'):
        for num,side in re.findall(r'(?<!\d)(\d+)([rv])',v['caption']):
            captions.setdefault('f'+num+side,[]).append(v)
    summaries=[]
    for name, filename in SOURCES.items():
        path=ROOT/filename;text=path.read_text(encoding='utf-8-sig')
        page_meta={};effective={};loci=[];duplicates=[];seen=set();spurious=[]
        for lineno,raw in logical_lines(text):
            m=re.match(r'^\s*<([^>]+)>\s*(.*)$',raw)
            if not m:continue
            locus,body=m.groups()
            if '.' not in locus and ',' not in locus and ';' not in locus:
                meta=dict(re.findall(r'\$([A-Za-z])=([^\s>]+)',body))
                page_meta[locus]=meta;effective[locus]=dict(meta);continue
            loc=re.fullmatch(r'([^.,;]+)\.([^,;]+),([@+*=~&/!])([A-Z][A-Za-z0-9])(?:;(.+))?',locus)
            if not loc:raise ValueError(f'Unexpected locus at {filename}:{lineno}: {locus}')
            page,num,locator,ltype,scribe=loc.groups();key=locus.split(';')[0]
            if key in seen:duplicates.append(dict(locus=locus,source_line=lineno,raw=body));continue
            seen.add(key)
            if locator=='!':spurious.append(dict(locus=locus,source_line=lineno,raw=body));continue
            meta=effective.setdefault(page,dict(page_meta.get(page,{})))
            value,events,ligatures=clean(body,meta)
            loci.append(dict(physical_locus=key,folio=page,locus_number=num,locator=locator,locus_kind=ltype[0],locus_type=ltype,
                transcriber=scribe,source_line=lineno,raw=body,cleaned=value,metadata=dict(meta),inline_tags=events,ligatures=ligatures))
        physical=[]
        for loc in loci:
            # '=' and '~' extend the previous physical horizontal row. Restrict
            # this merge to P loci on the same page; circles are separate paths.
            previous=physical[-1] if physical else None
            if loc['locator'] in ('=','~') and loc['locus_kind']=='P' and previous and previous['folio']==loc['folio'] and previous['locus_kind']=='P':
                previous['cleaned']+='.'+loc['cleaned'];previous['source_loci'].append(loc['physical_locus'])
                previous['source_types'].append(loc['locus_type']);previous['source_lines'].append(loc['source_line'])
                previous['ligatures']+=loc['ligatures']
                if previous['metadata']!=loc['metadata']:previous['metadata_conflict']=True
            else:
                physical.append(dict(loc,source_loci=[loc['physical_locus']],source_types=[loc['locus_type']],source_lines=[loc['source_line']],metadata_conflict=False))
        all_groups=[];join_groups=[]
        for row in physical:
            base=re.match(r'^(f\d+[rv])',row['folio']);base=base[1] if base else row['folio']
            vv=captions.get(base,[]);component=vv[0]['folio_component'] if vv else base
            split=vv[0]['split'] if vv else ('train','train','train','validation','test')[int(hashlib.sha256(component.encode()).hexdigest()[:8],16)%5]
            meta=row['metadata'];lineid=f"{name}|{row['physical_locus']}"
            for hypothesis,collector,body in [('comma_split',all_groups,row['cleaned'].replace(',','.')),('comma_join',join_groups,row['cleaned'].replace(',',''))]:
                slots=[x for x in body.split('.') if x]
                for rank,token in enumerate(slots):
                    units=signs(token,name)
                    collector.append(dict(group_id=f'{lineid}|G{rank:03d}',line_id=lineid,physical_locus=row['physical_locus'],source_loci=row['source_loci'],
                        folio=row['folio'],folio_component=component,split=split,group_rank=rank,group_count=len(slots),
                        normalized_group_rank=rank/(len(slots)-1) if len(slots)>1 else .5,
                        normalized_pixel_center=None,source_pixel_center_x=None,source_pixel_x_page_fraction=None,
                        units=units,form=token,section=meta.get('I'),hand=None if meta.get('H')=='@' else meta.get('H'),currier=meta.get('L'),
                        quire=meta.get('Q'),bifolio=meta.get('B'),inherited_bifolio_block=f"{meta.get('Q')}:{meta.get('B')}" if meta.get('Q') and meta.get('B') else None,
                        locus_kind=row['locus_kind'],locus_type=row['locus_type'],locator=row['locator'],source_line=row['source_line'],
                        source_types=row['source_types'],transcriber=row['transcriber'],boundary_hypothesis=hypothesis,
                        line_contains_uncertain_spaces=',' in row['cleaned'],metadata_conflict=row['metadata_conflict'],
                        parsing_status='retained literal comparison signs' if units else 'unresolved reading or reserved markup'))
        write_json(DEST/f'{name}_groups.json',all_groups);write_json(DEST/f'{name}_comma_join_groups.json',join_groups)
        write_json(DEST/f'{name}_lines.json',physical);write_json(DEST/f'{name}_loci.json',loci);write_json(DEST/f'{name}_metadata.json',page_meta)
        write_json(DEST/f'{name}_duplicate_loci.json',duplicates);write_json(DEST/f'{name}_spurious_loci.json',spurious)
        retained=[g for g in all_groups if g['units']]
        summary=dict(dataset=name,source_sha256=sha256(path),loci=len(loci),physical_paths=len(physical),source_slots=len(all_groups),retained=len(retained),
            paragraph_retained=sum(g['locus_kind']=='P' for g in retained),types=len(set(tuple(g['units']) for g in retained)),
            currier_counts=dict(Counter(g['currier'] for g in retained)),locus_kinds=dict(Counter(g['locus_kind'] for g in retained)),
            ambiguous=len(all_groups)-len(retained),duplicate_loci=len(duplicates),spurious_loci=len(spurious))
        summaries.append(summary);print(summary,flush=True)
    write_json(DEST/'comparison_manifest.json',dict(visual_freeze_sha256=sha256(freeze),datasets=summaries,parser_version=2,
        primary='split apparent and uncertain group separators; preserve all original ranks; abstain unresolved readings',
        alternatives=['join uncertain commas','remove all lines containing uncertain commas','ligature-atomic hypothesis retained in locus records'],
        source_documentation=['https://www.voynich.nu/software/ivtt/IVTFF_format.pdf','https://www.voynich.nu/transcr.html'],
        dependence='RF is a derived combination of ZL and GC, according to the source documentation; these datasets are not three independent witnesses',
        first_parser_status='failed syntax experiment preserved under data/comparisons; never used as assay input'))

if __name__=='__main__':main()
