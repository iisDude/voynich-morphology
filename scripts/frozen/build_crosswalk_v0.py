"""Post-freeze group correspondences, with geometric alignment hypotheses.

No transcription identity or positional coefficient enters page/row alignment.
Exact count agreement alone does not certify that a candidate group is writing.
"""
from common import OUT,read_json,read_csv,write_json,write_csv,SEED,sha256
from collections import defaultdict,Counter
import re
import numpy as np
from PIL import Image,ImageDraw,ImageFont

def main():
    root=OUT/'data/comparisons/v2';sources={n:read_json(root/f'{n}_groups.json') for n in ('ZL_EVA','RF','v101')}
    # Paired conventional strings at an identical row/count remain a boundary
    # hypothesis. One-to-many unit mappings are never silently flattened.
    bysource={}
    for name,rows in sources.items():
        byline=defaultdict(list)
        for r in rows:byline[r['physical_locus']].append(r)
        bysource[name]=byline
    correspondences=[];failures=[]
    for name in ('RF','v101'):
        for key,aa in bysource['ZL_EVA'].items():
            bb=bysource[name].get(key)
            if bb is None or len(aa)!=len(bb):
                failures.append(dict(from_dataset='ZL_EVA',to_dataset=name,locus=key,reason='row missing or boundary count differs',from_count=len(aa),to_count=len(bb) if bb else None));continue
            for a,b in zip(aa,bb):
                correspondences.append(dict(from_dataset='ZL_EVA',to_dataset=name,from_group_id=a['group_id'],to_group_id=b['group_id'],
                    from_units=a['units'],to_units=b['units'],split=a['split'],folio_component=a['folio_component'],
                    status='same physical locus and equal apparent-boundary count; ordinal pairing hypothesis',
                    unit_alignment='unresolved even when unit counts happen to agree'))
    write_json(root/'conventional_group_crosswalk.json',correspondences);write_json(root/'conventional_alignment_failures.json',failures)
    visual=read_json(root/'visual_groups_with_metadata.json');views=read_csv(OUT/'data/source/all_view_manifest.csv');native={v['view_id']:v for v in read_csv(OUT/'data/source/yale_native_all_manifest.csv')}
    vv=defaultdict(lambda:defaultdict(list))
    for r in visual:vv[r['view_id']][r['line_id']].append(r)
    proposals=[];viewstatus=[]
    for view in views:
        vid=view['view_id']
        if vid not in vv:continue
        caption=view['caption'];base=re.fullmatch(r'(\d+)([rv])',caption)
        if not base:
            viewstatus.append(dict(view_id=vid,status='unresolved panel/caption; no automatic row mapping',proposal_lines=0));continue
        page='f'+base[1]+base[2];transrows=[r for r in read_json(root/'ZL_EVA_lines.json') if r['folio']==page and r['locus_kind']=='P']
        if not transrows:
            viewstatus.append(dict(view_id=vid,status='no paragraph comparison rows',proposal_lines=0));continue
        vl=sorted(vv[vid].values(),key=lambda x:(np.mean([r['source_pixel_center_y'] for r in x]),min(r['source_pixel_center_x'] for r in x)))
        tc=[len(bysource['ZL_EVA'][r['physical_locus']]) for r in transrows];vc=[len(x) for x in vl]
        ta=defaultdict(list);va=defaultdict(list)
        for i in range(len(tc)-3):ta[tuple(tc[i:i+4])].append(i)
        for i in range(len(vc)-3):va[tuple(vc[i:i+4])].append(i)
        anchors=[(va[k][0],ta[k][0]) for k in va if len(va[k])==1 and len(ta.get(k,[]))==1 and len(set(k))>1]
        offsets={a-b for a,b in anchors};accepted=set()
        if len(offsets)==1:
            for a,b in anchors:
                for d in range(4):accepted.add((a+d,b+d))
        for a,b in sorted(accepted):
            rows=sorted(vl[a],key=lambda r:r['group_rank']);tr=bysource['ZL_EVA'][transrows[b]['physical_locus']]
            proposals.append(dict(view_id=vid,folio=page,visual_line_id=rows[0]['line_id'],comparison_locus=transrows[b]['physical_locus'],
                visual_groups=[r['group_id'] for r in rows],comparison_groups=[r['group_id'] for r in tr],
                visual_bboxes=[r['bbox_xyxy'] for r in rows],comparison_forms=[r['form'] for r in tr],
                split=view['split'],group_count=len(rows),status='unverified geometry/count hypothesis; pixel crosswalk withheld',
                anchor_rule='unique four-row count sequence in both page streams, all anchor offsets agree'))
        viewstatus.append(dict(view_id=vid,status='source-audit proposals only' if accepted else 'no unique consistent four-row anchor',
            proposal_lines=len(accepted),visual_lines=len(vc),comparison_lines=len(tc),anchors=len(anchors),offsets=list(offsets)))
    write_json(root/'visual_row_alignment_proposals.json',proposals);write_csv(root/'visual_alignment_coverage.csv',viewstatus)
    # Source sheets permit checking row identity AND visible group boundaries.
    rng=np.random.default_rng(SEED);chosen=[]
    for split in ('train','validation','test','calibration'):
        pp=[r for r in proposals if r['split']==split];ix=rng.permutation(len(pp))[:6]
        chosen.extend(pp[i] for i in ix)
    figures=OUT/'figures/crosswalk_source_audit_v0';figures.mkdir(parents=True,exist_ok=True)
    font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
    for n,row in enumerate(chosen,1):
        with Image.open(OUT/native[row['view_id']]['path']) as source:
            bb=row['visual_bboxes'];x0=min(x[0] for x in bb)-10;y0=min(x[1] for x in bb)-10;x1=max(x[2] for x in bb)+10;y1=max(x[3] for x in bb)+10
            crop=source.crop((x0,y0,x1,y1)).convert('RGB');draw=ImageDraw.Draw(crop)
            for i,b in enumerate(bb):draw.rectangle((b[0]-x0,b[1]-y0,b[2]-x0,b[3]-y0),outline='red',width=1)
            scale=min(1,1800/crop.width);crop=crop.resize((int(crop.width*scale),int(crop.height*scale)))
        canvas=Image.new('RGB',(max(1000,crop.width),crop.height+160),'white');canvas.paste(crop,(0,50));draw=ImageDraw.Draw(canvas)
        draw.text((8,5),f"{n:02d} {row['view_id']} {row['visual_line_id']} <> {row['comparison_locus']} n={row['group_count']}",fill='black',font=font)
        words=' | '.join(f'{i+1}:{w}' for i,w in enumerate(row['comparison_forms']))
        for j in range(0,len(words),130):draw.text((8,crop.height+60+(j//130)*23),words[j:j+130],fill='black',font=font)
        canvas.save(figures/f'audit_{n:02d}.png');row['audit_figure']=(figures/f'audit_{n:02d}.png').relative_to(OUT).as_posix()
    write_json(root/'visual_row_alignment_audit_plan.json',chosen)
    write_json(root/'crosswalk_summary.json',dict(conventional_proposed_group_pairs=len(correspondences),conventional_failed_rows=len(failures),
        visual_proposed_rows=len(proposals),visual_proposed_groups=sum(r['group_count'] for r in proposals),audited_rows=0,
        accepted_visual_pixel_group_pairs=0,accepted_unit_pairs=0,view_status_counts=dict(Counter(r['status'] for r in viewstatus)),
        limitation='Row-count proposals are unverified. No conventional group has received an invented native coordinate. Equal unit counts do not establish grapheme correspondence.',
        frozen_visual_sha256=sha256(OUT/'data/observations/visual_dataset_v0/assay_groups.json')))
    print('Conventional pairs',len(correspondences),'visual proposals',len(proposals),'audit rows',len(chosen),flush=True)

if __name__=='__main__':main()
