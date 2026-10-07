"""Read-only access to canonical evidence, including lossless transport compression."""
from pathlib import Path
import io,json,gzip,hashlib
PACKAGE=Path(__file__).resolve().parents[1]
def sha_bytes(b):return hashlib.sha256(b).hexdigest()
class Evidence:
 def __init__(self,package=PACKAGE):
  self.root=Path(package).resolve(); self.index=json.loads((self.root/'manifests/FILE_INDEX.json').read_text(encoding='utf-8'))
  self.files={r['logical_path']:r for r in self.index['files']}
 def bytes(self,path,verify=True):
  r=self.files[str(path).replace('\\','/')]
  if r['storage']=='external_source':raise FileNotFoundError('Obtain the separately indexed Yale native image: '+str(r.get('source_url')))
  b=(self.root/r['public_path']).read_bytes()
  if verify:assert sha_bytes(b)==r['stored_sha256'],r['public_path']
  if r['storage']=='gzip':b=gzip.decompress(b)
  if verify:assert sha_bytes(b)==r['sha256'],path
  return b
 def json(self,path):return json.loads(self.bytes(path).decode('utf-8-sig'))
 def npz(self,path):
  import numpy as np
  return np.load(io.BytesIO(self.bytes(path)),allow_pickle=False)
 def outside(self,target):
  q=Path(target).resolve()
  if q==self.root or q.is_relative_to(self.root):raise ValueError('The contribution is immutable. Use an output directory outside it.')
  return q
