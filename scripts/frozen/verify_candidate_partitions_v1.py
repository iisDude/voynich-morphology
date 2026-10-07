"""Read-only native-pixel conservation checks for tracked and bridge models."""
from common import OUT,read_json,write_json,write_csv,sha256
from analyse_native_structure import unpack
from regional_extract import normalise
import numpy as np
from collections import Counter

def main():
    results=[];totals=Counter();failures=[]
    root=OUT/'data/observations/regional_candidates_v11'
    paths=[p for p in sorted(root.glob('V_*.json')) if p.stem[2:].isdigit()]
    assert len(paths)==204
    for path in paths:
        obj=read_json(path)
        with np.load(path.with_name(path.stem+'_native_masks.npz')) as archive:packed={k:archive[k] for k in archive.files}
        shapes=np.load(path.with_name(path.stem+'_shapes.npz'))['shapes'];byid={r['instance_id']:r for r in obj['instances']};errors=[];maximum=0
        if len(byid)!=len(obj['instances']):errors.append('duplicate instance ID')
        for rec in obj['instances']:
            mask=unpack(packed,rec['shape_index']);x,y,c,d=rec['bbox_xyxy']
            if mask.shape!=(d-y,c-x):errors.append(rec['instance_id']+' dimensions')
            error=float(np.max(abs(normalise(mask,rec['body_height_proxy_px'])-shapes[rec['shape_index']])));maximum=max(maximum,error)
            if error>1e-6:errors.append(rec['instance_id']+' normalized pixels')
        for group in obj['groups']:
            x,y,c,d=group['bbox_xyxy'];reference=None
            for model,ids in group['models'].items():
                image=np.zeros((d-y,c-x),np.uint8)
                for iid in ids:
                    rec=byid[iid];a,b,e,f=rec['bbox_xyxy']
                    if not (x<=a<e<=c and y<=b<f<=d):errors.append(iid+' outside group');continue
                    image[b-y:f-y,a-x:e-x]|=unpack(packed,rec['shape_index'])
                if reference is None:reference=image
                elif not np.array_equal(image,reference):errors.append(group['group_id']+' unequal partition ink: '+model)
        # Bridge alternatives trim blank bounds but must conserve every parent pixel.
        bridgepath=OUT/f'data/observations/regional_candidates_bridge_v0/{path.name}'
        bridge=read_json(bridgepath);originalpath=OUT/f'data/observations/regional_candidates_v4/{path.name}';original=read_json(originalpath);parents={r['instance_id']:r for r in original['instances']}
        with np.load(originalpath.with_name(path.stem+'_native_masks.npz')) as archive:oldpacked={k:archive[k] for k in archive.files}
        bridgeshapes=np.load(bridgepath.with_name(path.stem+'_shapes.npz'))['shapes'];recon={}
        for rec in bridge['instances']:
            parent=parents[rec['original_assembly_id']];mask=unpack(oldpacked,parent['shape_index']);px,py,_,_=parent['bbox_xyxy'];a,b,c,d=rec['bbox_xyxy'];piece=mask[b-py:d-py,a-px:c-px]
            dest=recon.setdefault(parent['instance_id'],np.zeros_like(mask));dest[b-py:d-py,a-px:c-px]|=piece
            if np.max(abs(normalise(piece,rec['body_height_proxy_px'])-bridgeshapes[rec['shape_index']]))>1e-6:errors.append(rec['instance_id']+' bridge normalized pixels')
        for parent in original['instances']:
            if parent['model']=='medium_assemblies' and not np.array_equal(recon.get(parent['instance_id']),unpack(oldpacked,parent['shape_index'])):errors.append(parent['instance_id']+' bridge lost pixels')
        record=dict(view_id=path.stem,lines=len(obj['lines']),groups=len(obj['groups']),instances=len(obj['instances']),fine_components=sum(r['model']=='fine_components' for r in obj['instances']),multiline_components=sum(r['multiline_component_count'] for r in obj['lines']),bridge_pieces=len(bridge['instances']),max_normalized_pixel_error=maximum,errors=len(errors),candidate_sha256=sha256(path),bridge_sha256=sha256(bridgepath))
        results.append(record);totals.update({k:record[k] for k in ['lines','groups','instances','fine_components','multiline_components','bridge_pieces']});failures.extend(dict(view_id=path.stem,error=e) for e in errors)
        print(path.stem,record['groups'],record['bridge_pieces'],len(errors),flush=True)
    root=OUT/'tests/candidate_integrity_v1';root.mkdir(parents=True,exist_ok=True)
    write_csv(root/'results.csv',results);write_json(root/'results.json',dict(status='passed' if not failures else 'failed',views=len(paths),totals=dict(totals),failures=failures,limitations='Verifies assigned pixel bookkeeping only. Drawing contamination, omitted writing, incorrect rows and grapheme boundaries remain unvalidated. Bridge cuts conserve ink but often bisect visible loops/stems.'))
    write_json(root/'config.json',dict(normalized_pixel_tolerance=1e-6,mask_endianness='little',required_views=204))
    write_json(root/'input_manifest.json',dict(candidate_files=[dict(path=f'data/observations/regional_candidates_v11/{r["view_id"]}.json',sha256=r['candidate_sha256']) for r in results],source_sha256=sha256(OUT/'src/verify_candidate_partitions_v1.py')))
    (root/'run.py').write_text('from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]/"src"))\nfrom verify_candidate_partitions_v1 import main\nmain()\n',encoding='utf-8')
    (root/'summary.md').write_text('# Assigned pixel conservation\n\n'+str(dict(totals))+'\n\n'+str(len(failures))+' errors. This does not validate source membership, pen lifts or writing-unit boundaries. All 204 views checked.\n',encoding='utf-8')
    if failures:raise ValueError(failures[:5])

if __name__=='__main__':main()
