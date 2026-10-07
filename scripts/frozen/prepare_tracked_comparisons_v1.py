"""Attach inherited context only to a copy of the second frozen visual snapshot."""
from common import OUT,read_json,read_csv,write_json,sha256
from collections import defaultdict
import shutil
import re

def main():
    freeze=OUT/'data/observations/visual_dataset_v11/FREEZE_MANIFEST.json';manifest=read_json(freeze)
    source=OUT/'data/observations/visual_dataset_v11/assay_groups.json'
    assert sha256(source)==next(r['sha256'] for r in manifest['files'] if r['path']==source.relative_to(OUT).as_posix())
    context={}
    for r in read_json(OUT/'data/comparisons/v2/visual_groups_with_metadata.json'):
        fields={k:r.get(k) for k in ['section','hand','currier','quire','bifolio','inherited_bifolio_block','comparison_metadata_sources','metadata_status']}
        if r['view_id'] in context:assert context[r['view_id']]==fields
        context[r['view_id']]=fields
    # New tracked rows can occur in views with no original horizontal groups.
    metadata=read_json(OUT/'data/comparisons/v2/ZL_EVA_metadata.json')
    for view in read_csv(OUT/'data/source/all_view_manifest.csv'):
        if view['view_id'] in context:continue
        bases=['f'+n+s for n,s in re.findall(r'(?<!\d)(\d+)([rv])',view['caption'])]
        candidates=[(key,v) for key,v in metadata.items() if any(re.fullmatch(re.escape(base)+r'\d*',key) for base in bases)]
        fields={'comparison_metadata_sources':[key for key,v in candidates],'metadata_status':'post-freeze inherited metadata, uniform across candidate panels' if candidates else 'no inherited panel metadata'}
        for field,sourcekey in [('section','I'),('hand','H'),('currier','L'),('quire','Q'),('bifolio','B')]:
            values={v.get(sourcekey) for key,v in candidates};value=next(iter(values)) if len(values)==1 else None;fields[field]=None if value=='@' else value
        fields['inherited_bifolio_block']=f"{fields['quire']}:{fields['bifolio']}" if fields['quire'] and fields['bifolio'] else None
        context[view['view_id']]=fields
    rows=read_json(source)
    for row in rows:
        assert all(row[k] is None for k in ['section','hand','currier','conventional_mapping'])
        row.update(context.get(row['view_id'],{}))
    root=OUT/'data/comparisons/v11';root.mkdir(parents=True,exist_ok=True);write_json(root/'visual_groups_with_metadata.json',rows)
    for name in ['ZL_EVA_groups.json','RF_groups.json','v101_groups.json','ZL_EVA_lines.json']:shutil.copyfile(OUT/'data/comparisons/v2'/name,root/name)
    write_json(root/'metadata_manifest.json',dict(frozen_source_sha256=sha256(source),visual_freeze_sha256=sha256(freeze),context_source_sha256=sha256(OUT/'data/comparisons/v2/visual_groups_with_metadata.json'),rule='Existing post-first-freeze context per capture copied after second freeze. No identities, gates, groups, native coordinates or ranks changed.',blinding='Second snapshot follows prior conventional/statistical exposure; no renewed blind claim.'))
    # Versioned generated crosswalk keeps its fixed seed, anchors and source audit.
    original=(OUT/'src/build_crosswalk_v0.py').read_text(encoding='utf-8')
    generated=original.replace("root=OUT/'data/comparisons/v2'","root=OUT/'data/comparisons/v11'").replace('crosswalk_source_audit_v0','crosswalk_source_audit_v11').replace('data/observations/visual_dataset_v0/assay_groups.json','data/observations/visual_dataset_v11/assay_groups.json')
    (OUT/'src/build_crosswalk_v11.py').write_text(generated,encoding='utf-8')
    print('Post-freeze tracked comparison copy',len(rows),'groups; canonical snapshot unchanged.')

if __name__=='__main__':main()
