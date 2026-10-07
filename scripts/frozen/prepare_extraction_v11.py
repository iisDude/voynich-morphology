"""Versioned source-density seams. No conventional comparison input."""
from common import OUT,write_json,sha256

TRACK=r'''
def track_baseline(eligible,seed,body,pitch):
    from scipy.ndimage import gaussian_filter1d
    height,width=eligible.shape
    grid=np.arange(0,width,96,dtype=int);grid=np.unique(np.r_[grid,width-1])
    radius=max(18,round(.75*pitch));low=max(0,round(seed-radius));high=min(height,round(seed+radius)+1)
    ys=np.arange(low,high);scores=[]
    for x in grid:
        density=gaussian_filter1d(eligible[:,max(0,x-96):min(width,x+96)].sum(axis=1).astype(float),max(3,body*.15))
        density=density/(density.max()+1e-9)
        scores.append(density[ys]-.35*((ys-seed)/max(pitch*.65,1))**2)
    values=scores[0].copy();backs=[]
    shifts=np.arange(-18,19);penalty=.12*(shifts/9)**2
    for score in scores[1:]:
        candidates=np.full((len(shifts),len(ys)),-np.inf)
        for j,shift in enumerate(shifts):
            if shift>=0:candidates[j,shift:]=values[:len(ys)-shift]-penalty[j]
            else:candidates[j,:shift]=values[-shift:]-penalty[j]
        choice=np.argmax(candidates,axis=0);values=candidates[choice,np.arange(len(ys))]+score;backs.append(choice)
    index=int(np.argmax(values));indexes=[index]
    for back in reversed(backs):index-=int(shifts[back[index]]);indexes.append(index)
    centers=ys[np.array(indexes[::-1])]
    return grid.tolist(),(centers+.3*body).tolist()

def baseline_at(line,x):
    if 'native_track_x' in line:return np.interp(x,line['native_track_x'],line['native_track_y'])
    return line['native_baseline']+line['native_slope']*(x-line['native_xref'])

'''

def main():
    origin=OUT/'src/regional_extract_v10.py';text=origin.read_text(encoding='utf-8')
    text=text.replace("'v10'","'v11'").replace('v10 post-unblinding','v11 post-unblinding').replace('extraction_v10_protocol','extraction_v11_protocol')
    text=text.replace('def detect_lines(',TRACK+'\ndef detect_lines(')
    text=text.replace("baseline=float(peak+.3*body)","track_x,track_y=track_baseline(eligible,int(peak),body,pitch)\n        baseline=float(np.interp(width/2,track_x,track_y))")
    text=text.replace("paths.append(dict(x0=x0", "paths.append(dict(track_x=track_x,track_y=track_y,x0=x0")
    text=text.replace("candidates.append(line)","if 'track_x' in line:\n                line['native_track_x']=[v+nx0 for v in line['track_x']]\n                line['native_track_y']=[v+ny0 for v in line['track_y']]\n            candidates.append(line)")
    text=text.replace("line['native_baseline']+line['native_slope']*(px-line['native_xref'])","baseline_at(line,px)")
    text=text.replace("y+ch-1-line['native_baseline']-line['native_slope']*(cx-line['native_xref'])","y+ch-1-baseline_at(line,cx)")
    text=text.replace("if supports[winner]<.12 or ch>5*body or cw>20*body:continue","if supports[winner]<.12 or ch>5*body or cw>20*body:continue")
    text=text.replace("baseline_slope=line['native_slope'],membership_rule=", "baseline_slope=line['native_slope'],baseline_polyline_xy=list(zip(line['native_track_x'],line['native_track_y'])),membership_rule=")
    text=text.replace("line['native_baseline']+line['native_slope']*((bx0+bx1)/2-line['native_xref'])","baseline_at(line,(bx0+bx1)/2)")
    text=text.replace("line['native_baseline']-line['native_slope']*((bx0+bx1)/2-line['native_xref'])","baseline_at(line,(bx0+bx1)/2)")
    text=text.replace("shapes=[];path_tiles=[]", "shapes=[];native_bytes=[];native_offsets=[0];native_sizes=[];path_tiles=[]")
    text=text.replace("shapes.append(normalise(cm,body));records.append(record)","shapes.append(normalise(cm,body));packed=np.packbits(cm.reshape(-1),bitorder='little');native_bytes.append(packed);native_offsets.append(native_offsets[-1]+len(packed));native_sizes.append(cm.shape);records.append(record)")
    text=text.replace("write_json(folder/f'{vid}.json'", "np.savez_compressed(folder/f'{vid}_native_masks.npz',data=np.concatenate(native_bytes) if native_bytes else np.empty(0,np.uint8),offsets=np.array(native_offsets,np.int64),sizes=np.array(native_sizes,np.int32).reshape(-1,2))\n    write_json(folder/f'{vid}.json'")
    target=OUT/'src/regional_extract_v11.py';target.write_text(text,encoding='utf-8')
    write_json(OUT/'data/observations/extraction_v11_protocol.json',dict(version=11,source_sha256=sha256(origin),generated_source_sha256=sha256(target),
        change='Track each source-density peak through 96px x samples with local 192px ink windows; row membership and heights use interpolated local tracks.',
        objective='Maximize vertically smoothed local density, minus fixed seed-distance and movement penalties. Each seam can move <=18px per 96px horizontal step, within .75 detected pitch of its seed.',
        parameters='Seed penalty .35*(dy/(.65pitch))^2; continuity penalty .12*(step/9)^2; density smoothing max(3,.15body). All thresholds fixed before pilot inspection.',
        limitations=['Density center +.3body is an estimated baseline, not a manually measured writing bottom.','Seeds can duplicate or miss rows.','Drawings, touching rows, detached strokes and faint writing remain risks.','Original gap and component partitions remain hypotheses.'],
        blinding='Post-transcription-exposure source-only repair; comparison strings/counts/effect statistics absent.',stage='twelve-view calibration'))

if __name__=='__main__':main()
