"""Source-only membership benchmark; structural inference is a later stage."""
from common import OUT,read_json,write_json,sha256
from register_row_benchmark_v5 import D,T,G,F
from prepare_row_objects_v5 import GEOMETRY
from source_review_notes_v5 import NOTES
from visual_extract import ink_mask
from datetime import datetime,timezone
from collections import Counter
from PIL import Image
import numpy as np,cv2
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks

def build_reference(aids,notes):
    result=[]
    for r in aids:
        note=notes[r['row_id']];sets={k:set(note.get(k,[])) for k in ['target','neighbor','uncertain','margin','nonwriting','mixed','detached','writing_owner_unknown']}
        assert not(sets['target']&sets['neighbor']),r['row_id']
        assert not(sets['target']&sets['uncertain']),r['row_id']
        assert not(sets['neighbor']&sets['uncertain']),r['row_id']
        path=note.get('reviewed_body_path',r['provisional_body_path']);scope=note.get('reviewed_scope',[note['physical_endpoints'][0][0],note['physical_endpoints'][1][2]])
        obs=[]
        for p in r['objects']:
            n=int(p['object_id'][-3:]);p=dict(p)
            if n in sets['target']:membership='confirmed_writing';owner='target'
            elif n in sets['neighbor']:membership='confirmed_writing';owner='neighbor'
            elif n in sets['margin']:membership='confirmed_writing';owner='margin'
            elif n in sets['writing_owner_unknown']:membership='confirmed_writing';owner='unknown'
            elif n in sets['mixed']:membership='mixed_writing_and_unresolved';owner='unknown'
            elif n in sets['uncertain']:membership='unresolved';owner='unknown'
            else:membership='confirmed_nonwriting';owner='outside_row'
            x,y,c,d=p['native_bbox'];base=np.interp((x+c)/2,np.array(path)[:,0],np.array(path)[:,1]);body=r['body_proxy']
            admissible=x<scope[1]+.35*body and c>scope[0]-.35*body and y<base+.65*body and d>base-1.8*body
            p.update(membership=membership,owner=owner,possible_target_owner=bool(owner=='target' or owner=='unknown' and admissible),source_category='possible_showthrough_or_extraction_artifact' if n in sets['mixed'] else 'detached_mark_uncertain_attachment' if n in sets['detached'] else 'connected_writing_structure_possible_compound' if membership=='confirmed_writing' and p['area']>=35 else 'unresolved_faint_or_near_trace' if membership=='unresolved' else 'surface_texture_or_drawing' if membership=='confirmed_nonwriting' else 'writing',source_review='Native RGB full context + complete compact object atlas; no V3 suggestion',physical_parent_status='unresolved_mixed_contact' if n in sets['mixed'] else 'competing_join' if any(n in j for j in note.get('possible_joins',[])) else 'confirmed_connected_trace' if owner=='target' else 'not_a_confirmed_target_parent')
            obs.append(p)
        result.append(dict(row_id=r['row_id'],view_id=r['view_id'],caption=r['caption'],split=r['split'],native_source=r['native_source'],body_proxy=r['body_proxy'],selection_proposal_id=r['selection_proposal_id'],source_anchor_y=r['source_anchor_y'],body_path=path,physical_scope=scope,physical_endpoint_boxes=note['physical_endpoints'],endpoint_status=['unknown_contact' if r['row_id']=='B012' else 'resolved','resolved'],start_alternatives=[455,501] if r['row_id']=='B012' else None,field_edge_truncation=False,objects=obs,possible_joins=note.get('possible_joins',[]),confirmed_joins=note.get('confirmed_joins',[]),source_separations=note.get('source_separations',[]),notes=note['note'],missing_object_sweep='Full native RGB context and source-labeled overlapping panels reviewed; no additional separable visible target ink object identified outside the location ledger. Faint connective traces inside/among boxes remain ambiguity, not proof of raster atomicity.',pixel_mask_truth=False))
    return result

def page_features(r):
    rgb=np.asarray(Image.open(OUT/r['native_source']).convert('RGB'));smooth=cv2.GaussianBlur(rgb,(0,0),.8)
    cfg=read_json(OUT/'data/observations/visual_protocol_draft.json');cfg['background_gaussian_sigma_px']=25
    gray=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY).astype(float);bg=cv2.GaussianBlur(gray,(0,0),25);delta=bg-gray
    masks=[ink_mask(smooth,cfg,c) for c in [9,6,12]];cc=[cv2.connectedComponentsWithStats(m,8) for m in masks]
    return rgb,delta,cc

def features(p,r,delta,cc):
    x,y,c,d=p['native_bbox'];vi=0 if p['raster']=='primary9' else 1;mask=cc[vi][1][y:d,x:c]==p['cc_label'];vals=delta[y:d,x:c][mask]
    return dict(area=p['area'],h=(d-y)/r['body_proxy'],w=(c-x)/r['body_proxy'],contrast90=float(np.percentile(vals,90)) if len(vals) else 0,contrast50=float(np.median(vals)) if len(vals) else 0,density=float(mask.mean()))

def strong(f):
    return f['area']>=35 and f['h']>=.2 and f['w']>=.075 and f['h']<=4.5 and f['w']<=12 and f['contrast90']>=50 and f['contrast50']>=25

def track(r,delta,cc):
    # Image density track is computed without the reference path/endpoints.
    body=r['body_proxy'];lab,st=cc[0][1],cc[0][2];good=[]
    for k in range(1,len(st)):
        x,y,w,h,a=map(int,st[k]);
        if a<35 or h<.28*body or h>1.6*body or w<.075*body or w>12*body:continue
        vals=delta[y:y+h,x:x+w][lab[y:y+h,x:x+w]==k]
        if np.percentile(vals,90)>=50 and np.median(vals)>=25:good.append(k)
    mask=np.isin(lab,good);width=mask.shape[1];xref=width//2;anchor=r['source_anchor_y']-.3*body
    low=max(0,int(anchor-3*body));high=min(mask.shape[0],int(anchor+3*body));ys=np.arange(low,high)
    xs=np.unique(np.r_[np.arange(0,width,96),width-1]);scores=[]
    for x in xs:
        profile=gaussian_filter1d(mask[low:high,max(0,x-110):min(width,x+110)].sum(1).astype(float),max(3,.15*body));scores.append(profile/(profile.max()+1e-8))
    mid=int(np.argmin(abs(xs-xref)));peaks,_=find_peaks(scores[mid],distance=max(12,int(.8*body)),prominence=.12)
    seed=int(peaks[np.argmin(abs(ys[peaks]-anchor))]) if len(peaks) else int(np.argmin(abs(ys-anchor)))
    index=np.zeros(len(xs),int);index[mid]=seed
    for direction in [-1,1]:
        j=mid+direction
        while 0<=j<len(xs):
            prior=index[j-direction];lo=max(0,prior-12);hi=min(len(ys),prior+13);values=scores[j][lo:hi]-.20*((np.arange(lo,hi)-prior)/8)**2;index[j]=lo+int(np.argmax(values));j+=direction
    return xs,ys[index]+.3*body

def predict(r,delta,cc,layout_assisted=False):
    if layout_assisted:xs,path=np.array(r['body_path']).T
    else:xs,path=track(r,delta,cc)
    body=r['body_proxy'];out=[]
    for p in r['objects']:
        f=features(p,r,delta,cc);x,y,c,d=p['native_bbox'];center=(x+c)/2;base=float(np.interp(center,xs,path));vi=0 if p['raster']=='primary9' else 1;mask=cc[vi][1][y:d,x:c]==p['cc_label'];yy,xx=np.where(mask);by=np.interp(xx+x,xs,path)
        core=(yy+y>=by-.95*body)&(yy+y<=by+.25*body);n=int(core.sum());bottom=d-base
        accepted=strong(f) and n>=8 and -.8*body<=bottom<=.9*body
        texture=f['area']<35 and f['contrast90']<45
        state='target_writing_candidate' if accepted else 'texture_candidate' if texture else 'unknown_or_other_row'
        out.append(dict(object_id=p['object_id'],state=state,membership_state='writing_candidate' if strong(f) else 'texture_candidate' if texture else 'unknown',source_features=f,core_support=n,bottom_offset_px=bottom))
    accepted=[p for p,o in zip(r['objects'],out) if o['state']=='target_writing_candidate'];ends=[min(p['native_bbox'][0] for p in accepted),max(p['native_bbox'][2] for p in accepted)] if accepted else [None,None]
    return dict(row_id=r['row_id'],body_path=list(map(list,zip(xs.tolist(),path.tolist()))),predicted_endpoints=ends,objects=out,mode='source_adjudicated_body_path_assisted; endpoint boxes and object labels not inputs' if layout_assisted else 'automatic_source_density_track; reference path/endpoints not inputs')

def development():
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen(source_stage=True)
    rows=build_reference(read_json(D/'development_object_location_aids.json')['rows'],NOTES);write_json(D/'development_source_reference.json',dict(created_at_utc=datetime.now(timezone.utc).isoformat(),rows=rows,status='Source decisions before any class inference; reference boundaries still awaiting repeat review'))
    pred=[];assisted=[];dist={k:[] for k in ['target','neighbor','outside_row','unknown','margin']}
    for r in rows:
        rgb,delta,cc=page_features(r);pr=predict(r,delta,cc);pred.append(pr);assisted.append(predict(r,delta,cc,True))
        for p,o in zip(r['objects'],pr['objects']):dist[p['owner']].append(o['source_features']['contrast90'])
        truth={p['object_id']:p for p in r['objects']};accept=[truth[o['object_id']] for o in pr['objects'] if o['state']=='target_writing_candidate'];print(r['row_id'],'writing',sum(p['owner']=='target' for p in r['objects']),'recovered',sum(p['owner']=='target' for p in accept),'nonwriting',sum(p['membership']=='confirmed_nonwriting' for p in accept),'wrong_owner',sum(p['owner'] in ['neighbor','margin'] for p in accept),'end',pr['predicted_endpoints'],flush=True)
    write_json(D/'development_rule_predictions_final.json',pred);write_json(D/'development_layout_assisted_predictions_final.json',assisted);write_json(T/'development_contrast_diagnostics.json',{k:dict(n=len(v),quantiles=np.percentile(v,[10,50,90]).tolist()) for k,v in dist.items() if v})
if __name__=='__main__':development()
