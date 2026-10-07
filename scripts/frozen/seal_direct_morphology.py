from direct_morphology_common import *
import ast,numpy,cv2,scipy,sklearn
def main():
    guard();verify()
    for name in ['SPECIFICATION_SEAL','SHAPE_SEAL','DISTANCE_SEAL']:verify_seal(D/(name+'.json'))
    replay=read_json(T/'deterministic_replay.json');assert replay['native_candidate_masks']==1124 and replay['parents']==217 and replay['ten_distance_matrices_exact'] and not replay['failures']
    save(D/'ENVIRONMENT.json',dict(numpy=numpy.__version__,opencv=cv2.__version__,scipy=scipy.__version__,sklearn=sklearn.__version__,scope='Version provenance; mask/coordinate/metric replay tested on this workstation.'))
    scripts=list((OUT/'src').glob('*direct_morphology*.py'))
    for p in scripts:ast.parse(p.read_text(encoding='utf-8'))
    records=read_json(D/'source_parent_ensembles.json')['parents'];plan=read_json(D/'PLAN.json');dependencies=[OUT/p for p in plan['dependencies']]+[OUT/r[k] for r in records for k in ['native_source','native_crop']]+[OUT/r['mask_path'] for r in read_json(SOURCE/'source_location_aids.json')['parents']]+[OUT/'src/common.py',OUT/'src/visual_extract.py',OUT/'src/register_row_benchmark_v5.py',OUT/'src/prepare_row_objects_v5.py',OUT/'src/source_review_notes_v5.py']
    paths=[p for folder in [D,T,G] for p in folder.rglob('*') if p.is_file()]+scripts+dependencies+[OUT/'reports/23_direct_contour_morphology_trial1.md',OUT/'reports/24_direct_contour_morphology_atlas_trial1.html'];paths=sorted(set(paths));accept=read_json(T/'acceptance_summary.json')
    save(D/'FREEZE_MANIFEST.json',dict(frozen_at_utc=now(),trial='Direct continuous contour/morphology space Trial1',status='Frozen operational feasibility and post-exposure reused-source sensitivity. Not fresh validation, new classes, segmentation or notation.',files=[dict(path=p.relative_to(OUT).as_posix(),sha256=sha256(p)) for p in paths],file_count=len(paths),operational_feasibility=accept['operational_feasibility'],descriptive_source_predictivity=accept['descriptive_source_predictivity'],fresh_independent_confirmation=False,physical_shape_boundaries_not_certified_by_metric=True,earlier_freezes_unchanged=True,no_downstream_assays=True))
    print('Direct morphology frozen',len(paths),sha256(D/'FREEZE_MANIFEST.json'),flush=True)
if __name__=='__main__':main()
