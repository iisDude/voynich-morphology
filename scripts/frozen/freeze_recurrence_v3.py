"""Freeze qualified source model and its inputs; never overwrite older freezes."""
from common import OUT,read_json,read_csv,write_json,sha256
from datetime import datetime,timezone
BASE=OUT/'data/observations/recurrence_v3_structural_candidate';PREV=OUT/'data/observations/recurrence_v3_development';DEST=OUT/'data/observations/visual_dataset_v3';TEST=OUT/'tests/recurrence_v3_development'

def main():
    target=DEST/'FREEZE_MANIFEST.json'
    if target.exists():raise ValueError('V3 immutable freeze already exists')
    q=read_json(TEST/'freeze_qualification_v3.json');assert all(q['gates'].values())
    for folder in [BASE,PREV]:write_json(folder/'INPUTS_IMMUTABLE_V3.json',dict(version='V3',freeze_manifest=target.relative_to(OUT).as_posix(),rule='Do not edit these inputs, models, judgments or artifacts. Continue in a new version directory.'))
    files=set(DEST.rglob('*'))
    files|={p for p in BASE.rglob('*') if p.is_file() and 'native_rows' not in p.parts}
    files|={p for p in PREV.glob('*') if p.is_file()}
    files|=set(TEST.glob('*'))
    files|={p for p in (OUT/'figures/recurrence_v3').rglob('*') if p.is_file() and 'source_review' not in p.parts and 'structural_source_review' not in p.parts}
    files|=set((OUT/'src').glob('*_v3.py'))
    files|={OUT/'reports/11_recurrence_bottleneck_and_structural_v3.md',OUT/'reports/12_neutral_structural_atlas_v3.html',OUT/'data/source/yale_native_all_manifest.csv'}
    # Primary photographs and advertised native dimensions stay part of the audited provenance.
    for r in read_csv(OUT/'data/source/yale_native_all_manifest.csv'):
        p=OUT/r['path'];files.add(p);info=p.with_name(p.stem+'_info.json')
        if info.exists():files.add(info)
    # Preserve source exemplars referenced by the first failed candidate's audits/atlas.
    for p in read_json(PREV/'pair_audit_key.json'):
        files.add(OUT/p['left_crop']);files.add(OUT/p['right_crop'])
    for a in read_json(BASE/'train_source_atlas.json'):
        for path in a['source_crop_paths']:files.add(OUT/path)
    rows=[]
    for i,p in enumerate(sorted(p for p in files if p.is_file() and p!=target)):
        assert p.resolve().is_relative_to(OUT.resolve());rows.append(dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p),bytes=p.stat().st_size))
        if (i+1)%5000==0:print('hashed',i+1,'freeze inputs',flush=True)
    payload=dict(version='V3 manuscript-derived local parent/structural model',frozen_at_utc=datetime.now(timezone.utc).isoformat(),v2_immutable_manifest_sha256='bbfd0e6f4e25dbad613c4b713d2b5bb50b6bd5d856487bfd9c6fd030ee408dc6',qualified_core_classes=14,classes_frozen_before_downstream_assays=True,no_positional_rerun=True,scope=read_json(DEST/'model_contract.json'),qualification_sha256=sha256(TEST/'freeze_qualification_v3.json'),files=rows)
    write_json(target,payload);print('V3 FROZEN',len(rows),'files',sha256(target),flush=True)

if __name__=='__main__':main()
