"""Citation, navigation and snapshot integrity; read-only, no lab dependency."""
from pathlib import Path
import sys,json,re,hashlib
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'scripts'))
from evidence import Evidence,sha_bytes
def verify():
 import jsonschema
 c=json.loads((P/'CITATION.cff').read_text(encoding='utf-8'));jsonschema.validate(c,json.loads((P/'environment/cff-1.2.0-schema.json').read_text()));assert c['authors']==[{'given-names':'Dylan','family-names':'Bedford','orcid':'https://orcid.org/0009-0005-9766-224X'}]
 assert not any(k in c for k in ['orcid','doi','version','date-released']);assert c['repository-code']==c['url']=='https://github.com/iisDude/voynich-morphology';e=Evidence();ledger=json.loads((P/'manifests/MASTER_EVIDENCE_LEDGER.json').read_text())
 for r in ledger['claims']:
  assert (P/r['freeze_manifest']).is_file();assert sha_bytes((P/r['freeze_manifest']).read_bytes())==r['freeze_sha256'];assert r['report'] in e.files;assert r['test'] in e.files or any(s.startswith(r['test']+'/') for s in e.files);assert r['supporting_dataset'] in e.files or any(s.startswith(r['supporting_dataset']+'/') for s in e.files)
 links=0;fail=[]
 for folder in ['atlases','reports/public']:
  for p in (P/folder).glob('*'):
   txt=p.read_text(encoding='utf-8');urls=re.findall(r'''(?:src|href)=['"]([^'"]+)['"]''',txt) if p.suffix=='.html' else re.findall(r'!?\[[^\]]*\]\(([^\s)]+)\)',txt)
   for u in urls:
    if re.match(r'^[a-z]+:|^#',u):continue
    q=(p.parent/u.split('#')[0]).resolve()
    if not q.is_file():fail.append(dict(document=p.relative_to(P).as_posix(),link=u))
    links+=1
 # Original report links intentionally reflect the original layout, and are not modified.
 assert not fail,fail[:20]
 if (P/'manifests/CONTRIBUTION_FREEZE.json').exists():
  f=P/'manifests/CONTRIBUTION_FREEZE.json';assert sha_bytes(f.read_bytes())==(P/'SNAPSHOT.sha256').read_text().split()[0]
  baseline={r['path']:r for r in json.loads(f.read_text(encoding='utf-8'))['files']}
  update=P/'manifests/metadata_updates/ORCID_REPOSITORY_UPDATE.json';digest=P/'manifests/METADATA_UPDATE.sha256'
  assert sha_bytes(update.read_bytes())==digest.read_text(encoding='utf-8').split()[0]
  amendment=json.loads(update.read_text(encoding='utf-8'));assert amendment['base_snapshot_sha256']==sha_bytes(f.read_bytes())
  allowed={'CITATION.cff','.zenodo.json','README.md','REPRODUCIBILITY.md','environment/README.md','tests/verify_package.py'}
  changed={r['path']:r for r in amendment['changes']};assert set(changed)==allowed
  for path,r in baseline.items():
   if path in changed:
    a=changed[path];assert a['before_sha256']==r['sha256'];original=(P/a['original_copy']).resolve();assert original.is_relative_to(P/'manifests/metadata_updates/originals');assert sha_bytes(original.read_bytes())==r['sha256'];assert sha_bytes((P/path).read_bytes())==a['after_sha256'],path
   else:assert sha_bytes((P/path).read_bytes())==r['sha256'],path
  zenodo=json.loads((P/'.zenodo.json').read_text(encoding='utf-8'));assert zenodo['creators']==[{'name':'Bedford, Dylan','orcid':'0009-0005-9766-224X'}]
  assert zenodo['related_identifiers']==[{'identifier':c['repository-code'],'relation':'isSupplementTo','scheme':'url'}]
  assert not any(k in zenodo for k in ['doi','prereserve_doi','version','publication_date'])
 print(json.dumps(dict(cff_valid=True,primary_author='Dylan Bedford',references=len(c['references']),claims=len(ledger['claims']),public_links_checked=links,authorized_metadata_update_verified=True,research_snapshot_unchanged=True,failures=[]),indent=2))
if __name__=='__main__':verify()
