"""Refuse original research inputs and any lab access during contribution replay."""
from pathlib import Path
import sys,os,json
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parents[1];project=P.parent
sys.path.insert(0,str(P/'scripts'));from evidence import Evidence
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ.setdefault(k,'2')
opens=0
def audit(event,args):
 global opens
 if event!='open' or not isinstance(args[0],(str,bytes,os.PathLike)):return
 try:q=Path(os.fsdecode(args[0])).resolve()
 except Exception:return
 if q.is_relative_to(project/'SCIENTIFIC_LAB'):raise RuntimeError('Lab access forbidden during contribution replay: '+str(q))
 if q.is_relative_to(project/'voynich-groundup') and not q.is_relative_to(project/'voynich-groundup/.tools'):raise RuntimeError('Original research input access forbidden: '+str(q))
 if q.is_relative_to(P):opens+=1
sys.addaudithook(audit)
sys.path.insert(0,str(P/'tests'));from replay_results import run
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('--output',required=True);a=a.parse_args();e=Evidence();out=e.outside(a.output);r=run();out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(dict(numerical_replay=r,contribution_file_opens=opens,original_research_input_access_forbidden=True,scientific_lab_access_forbidden=True,dependency_code_from_installed_runtime_allowed=True),indent=2),encoding='utf-8')
