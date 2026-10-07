"""Attach inherited context to copies; preserve frozen unit identities exactly."""
from common import OUT, read_json, read_csv, write_json, sha256
from collections import Counter,defaultdict
import re

def main():
    dest=OUT/'data/comparisons/v2';meta=read_json(dest/'ZL_EVA_metadata.json')
    views={r['view_id']:r for r in read_csv(OUT/'data/source/all_view_manifest.csv')}
    visual=read_json(OUT/'data/observations/visual_dataset_v0/assay_groups.json');counts=Counter()
    for r in visual:
        caption=views[r['view_id']]['caption'];bases=['f'+n+s for n,s in re.findall(r'(?<!\d)(\d+)([rv])',caption)]
        candidates=[(key,v) for key,v in meta.items() if any(re.fullmatch(re.escape(base)+r'\d*',key) for base in bases)]
        r['comparison_metadata_sources']=[key for key,v in candidates]
        for field,source in [('section','I'),('hand','H'),('currier','L'),('quire','Q'),('bifolio','B')]:
            values={v.get(source) for key,v in candidates};value=next(iter(values)) if len(values)==1 else None
            r[field]=None if value=='@' else value
        r['inherited_bifolio_block']=f"{r['quire']}:{r['bifolio']}" if r['quire'] and r['bifolio'] else None
        r['metadata_status']='post-freeze inherited metadata, uniform across candidate panels' if candidates else 'no inherited panel metadata'
        counts[r['metadata_status']]+=1
    write_json(dest/'visual_groups_with_metadata.json',visual)
    for name in ('ZL_EVA','RF','v101'):
        rows=read_json(dest/f'{name}_groups.json');write_json(dest/f'{name}_groups_with_metadata.json',rows)
    control_summary=[]
    for name in ('finnish','turkish','latin'):
        rows=read_json(OUT/f'data/controls/{name}_sentence_groups.json');c=Counter()
        for r in rows:
            doc=r['folio_component']
            if name=='latin':
                source=doc.split('|source|')[-1]
                r['section']=source.split(',')[0].strip()
                r['same_author_work']='Atticum' if 'Epistulae' in source else 'Officiis' if 'De officiis' in source else None
            elif name=='finnish':
                prefix=doc.split('|sent_id_prefix|')[-1];m=re.match(r'([A-Za-z]+)',prefix)
                r['section']=m[1] if m else None
            else:r['section']=None
            c[r['section']]+=1
        write_json(OUT/f'data/controls/{name}_groups_with_context.json',rows)
        control_summary.append(dict(corpus=name,groups=len(rows),source_partition_counts=dict(c),
            limitation='Source partitions are corpus-context labels, not inferred semantic genres. Turkish context not available.'))
    write_json(dest/'metadata_manifest.json',dict(frozen_visual_input_sha256=sha256(OUT/'data/observations/visual_dataset_v0/assay_groups.json'),
        visual_metadata_coverage=dict(counts),control_contexts=control_summary,
        prohibition='No family identities, segmentation choices or admission rules changed. Context was attached after the visual freeze.',
        dependence='Quire/bifolio fields are inherited metadata, not yet a verified physical reconstruction. Primary resampling uses frozen caption/document blocks.'))
    print(dict(counts),control_summary,flush=True)

if __name__=='__main__':main()
