"""Reconstruct one suspect canonical view in memory; never overwrite the freeze."""
from common import OUT,read_json,sha256,write_json
import json,hashlib

path=OUT/'data/observations/visual_dataset_v0/V_038.json'
manifest=read_json(OUT/'data/observations/visual_dataset_v0/FREEZE_MANIFEST.json')
expected=next(r for r in manifest['files'] if r['path']==path.relative_to(OUT).as_posix())
raw=path.read_bytes();variants={}
for key,data in [('current',raw),('LF',raw.replace(b'\r\n',b'\n')),('CRLF',raw.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n'))]:
    variants[key]=dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
captured={}
def capture(p,value):captured.update(value)
source=(OUT/'src/build_visual_dataset.py').read_text(encoding='utf-8')
source=source.replace("for path in sorted((OUT/'data/observations/assigned_visual_candidates_v4').glob('V_*.json')):","for path in [OUT/'data/observations/assigned_visual_candidates_v4/V_038.json']:")
source=source.replace("write_json(root/path.name,dataset)","dataset['status']='frozen'\n        capture(root/path.name,dataset)\n        return")
namespace={'__name__':'integrity_memory_reconstruction','capture':capture};exec(compile(source,'<unchanged_builder_with_output_capture>','exec'),namespace)
namespace['main']()
reconstructed=json.dumps(captured,indent=2,ensure_ascii=False)
for key,text in [('reconstructed_LF',reconstructed),('reconstructed_CRLF',reconstructed.replace('\n','\r\n'))]:
    data=text.encode('utf-8');variants[key]=dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
    if variants[key]['sha256']==expected['sha256']:(OUT/f'reports/V_038_verified_reconstruction_{key}.json').write_bytes(data)
current=read_json(path);differences=[]
def compare(a,b,where=''):
    if type(a)!=type(b):differences.append(dict(path=where,current_type=type(a).__name__,reconstructed_type=type(b).__name__));return
    if isinstance(a,dict):
        for k in sorted(set(a)|set(b)):
            if k not in a or k not in b:differences.append(dict(path=where+'/'+k,missing_in='current' if k not in a else 'reconstructed'))
            else:compare(a[k],b[k],where+'/'+k)
    elif isinstance(a,list):
        if len(a)!=len(b):differences.append(dict(path=where,current_length=len(a),reconstructed_length=len(b)))
        for i,(aa,bb) in enumerate(zip(a,b)):compare(aa,bb,where+'/'+str(i))
    elif a!=b:differences.append(dict(path=where,current=a,reconstructed=b))
compare(current,captured)
write_json(OUT/'reports/frozen_view_integrity_diagnosis_v1.json',dict(expected=expected,variants=variants,semantic_differences=differences))
print(json.dumps(dict(expected=expected,variants=variants,semantic_differences=differences[:20]),indent=2))
