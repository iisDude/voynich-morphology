"""Checkpointed two-worker region processing after pilot method calibration."""
from common import OUT,read_csv,write_json,sha256
import concurrent.futures
import subprocess
import sys
import time
import argparse

VERSION='v3'


def run_one(row):
    vid=row['view_id'];folder=OUT/f'data/observations/regional_candidates_{VERSION}'
    if (folder/f'{vid}.json').exists() and (folder/f'{vid}_shapes.npz').exists():
        return dict(view_id=vid,status='checkpoint_present')
    result=subprocess.run([sys.executable,str(OUT/'src/regional_extract.py'),'--scope','all','--view-id',vid,'--version',VERSION],cwd=OUT,capture_output=True,text=True)
    record=dict(view_id=vid,status='candidates_generated' if result.returncode==0 else 'failed',exit_code=result.returncode,message=(result.stdout+result.stderr)[-3000:])
    print(f'{vid}: {record["status"]}',flush=True)
    write_json(folder/f'{vid}_processing.json',record)
    return record


def main():
    global VERSION
    ap=argparse.ArgumentParser();ap.add_argument('--version',choices=['v3','v4'],default='v4');args=ap.parse_args();VERSION=args.version
    rows=[r for r in read_csv(OUT/'data/source/all_view_manifest.csv') if r['split']!='excluded_cover']
    snapshot=dict(status='candidate_extraction_protocol_snapshot_not_unit_freeze',version=VERSION,started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),code_sha256=sha256(OUT/'src/regional_extract.py'),layout_sha256=sha256(OUT/'data/observations/layout_regions_fractional.json'),calibration_layout_sha256=sha256(OUT/'data/observations/calibration_regions.json'),unit_plan_sha256=sha256(OUT/'data/observations/visual_family_analysis_plan.json'),source='native Yale registered to supplied PDF',native_mask_background_sigma=25,native_mask_primary_contrast=6 if VERSION=='v4' else 8,native_preblur_sigma=.9 if VERSION=='v4' else 0,localisation='PDF for ordinary views; native for scale transfer above three',models=['fine_components','medium_assemblies','compound_candidates','group_only'],quality='Candidate data; no final alphabet or accepted physical line claim')
    write_json(OUT/f'data/observations/regional_candidate_protocol_snapshot_{VERSION}.json',snapshot)
    normal=[r for r in rows if int(r['width_px'])*int(r['height_px'])<30000000]
    # PDF dimensions do not identify native giant views. Keep known rosette view serial.
    normal=[r for r in normal if r['view_id']!='V_159'];large=[r for r in rows if r not in normal]
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(run_one,normal):
            results.append(result);write_json(OUT/f'reports/regional_processing_progress_{VERSION}.json',results)
    for row in large:
        results.append(run_one(row));write_json(OUT/f'reports/regional_processing_progress_{VERSION}.json',results)
    write_json(OUT/f'reports/regional_processing_summary_{VERSION}.json',dict(snapshot=snapshot,results=results))


if __name__=='__main__':main()
