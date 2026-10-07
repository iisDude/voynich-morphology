"""Systematic native-view proposal pass, without opening any transcription.

Checkpoint each view. This expands the evidence to audit, not accepted units.
"""
from common import OUT, read_json, sha256, write_json
import concurrent.futures
import subprocess
import sys
import time


def run_one(row):
    view=row['view_id']; folder=OUT/'data/observations/all_native_global_proposals'
    if (folder/f'{view}.json').exists() and (folder/f'{view}_mask.png').exists():
        return dict(view_id=view,status='checkpoint_present')
    completed=subprocess.run([sys.executable,str(OUT/'src/visual_extract.py'),'--scope','all','--native','--unmasked','--view-id',view],cwd=OUT,capture_output=True,text=True)
    result=dict(view_id=view,status='proposal_generated' if completed.returncode==0 else 'failed',exit_code=completed.returncode,message=(completed.stdout+completed.stderr)[-4000:])
    print(f'{view}: {result["status"]}',flush=True)
    write_json(folder/f'{view}_processing.json',result)
    return result


def main():
    rows=read_json(OUT/'data/source/yale_registration_all.json')
    snapshot=dict(status='candidate_collection_protocol_snapshot_not_unit_freeze',started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),source='registered native Yale pixels',transcription_content_opened=False,
                  code_sha256=sha256(OUT/'src/visual_extract.py'),configuration_sha256=sha256(OUT/'data/observations/visual_protocol_draft.json'),
                  all_views=len(rows),quality_gate='No acceptance implied. Candidate rows may include drawings and texture; visual-unit freeze requires independent quality evaluation.',
                  limitations=['Straight horizontal candidates only; curved and radial writing requires separate path audit.','Caption view mapping is not a complete physical panel or bifolio map.'])
    write_json(OUT/'data/observations/candidate_collection_snapshot.json',snapshot)
    normal=[r for r in rows if r['native_width']*r['native_height']<30000000]
    large=[r for r in rows if r not in normal]
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(run_one,normal):
            results.append(result)
            write_json(OUT/'reports/full_proposal_processing_progress.json',results)
    for row in large:
        results.append(run_one(row));write_json(OUT/'reports/full_proposal_processing_progress.json',results)
    write_json(OUT/'reports/full_proposal_processing_summary.json',dict(snapshot=snapshot,results=results))


if __name__=='__main__': main()
