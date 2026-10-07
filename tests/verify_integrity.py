"""Verify transport, original hashes, and every original manifest record, without writes."""
from pathlib import Path
import sys,json,gzip,hashlib,collections
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from evidence import Evidence,sha_bytes
def run():
 e=Evidence();verified={};external=[]
 for i,r in enumerate(e.index['files'],1):
  if r['storage']=='external_source':external.append(r['logical_path']);continue
  if r['public_path'] not in verified:
   b=e.bytes(r['logical_path']);verified[r['public_path']]=(sha_bytes(b),len(b))
  assert verified[r['public_path']]==(r['sha256'],r['bytes']),r['logical_path']
  if i%4000==0:print('Integrity',i,flush=True)
 checks=0
 for m in e.index['original_manifests']:
  p=e.root/'manifests/original'/m['path'];raw=p.read_bytes();assert sha_bytes(raw)==m['sha256'];d=json.loads(raw)
  for r in d['files']:
   s=r['path'].replace('\\','/');assert e.files[s]['sha256']==r['sha256'];checks+=1
 result=dict(logical_files=len(e.files),unique_payloads_verified=len(verified),original_manifest_n=len(e.index['original_manifests']),original_manifest_records_checked=checks,external_native_images=len(external),external_source_content_verification='not claimed; retrieve separately and hash-check',failures=[])
 print(json.dumps(result,indent=2));return result
if __name__=='__main__':run()
