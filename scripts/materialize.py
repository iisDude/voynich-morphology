"""Restore original layout outside this immutable package; no experiment input mutation."""
from evidence import Evidence
from pathlib import Path
import argparse,urllib.request,hashlib
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--retrieve-native',action='store_true');ap.add_argument('--prefix',action='append',default=[]);a=ap.parse_args();e=Evidence();out=e.outside(a.output);n=0;missing=[]
 for r in e.index['files']:
  s=r['logical_path']
  if a.prefix and not any(s.startswith(p) for p in a.prefix):continue
  target=(out/'voynich-groundup'/s).resolve()
  if not target.is_relative_to(out):raise ValueError('Unsafe original path')
  if r['storage']=='external_source':
   if not a.retrieve_native:missing.append(s);continue
   if target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest()==r['sha256']:continue
   if not r.get('source_url'):raise ValueError('Missing retrieval URL for '+s)
   b=urllib.request.urlopen(urllib.request.Request(r['source_url'],headers={'User-Agent':'VoynichSourceEvidenceReplay/1.0'}),timeout=120).read()
   if hashlib.sha256(b).hexdigest()!=r['sha256']:raise ValueError('Remote image bytes differ from frozen source; do not substitute: '+s)
  else:b=e.bytes(s)
  target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b);n+=1
  if n%1000==0:print('Materialized',n,flush=True)
 print('Restored',n,'files; external source files not retrieved:',len(missing),flush=True)
if __name__=='__main__':main()
