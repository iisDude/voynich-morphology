"""Canonical source-adjudicated candidate model. Never imports comparison data."""
from common import OUT,read_json,read_csv,write_json,write_csv,sha256
from collections import defaultdict,Counter
from PIL import Image,ImageDraw
import numpy as np

FACTORS={'VS12':['VS04','VS01'],'VS16':['VS13','VS07'],'VS17':['VS08','VS15'],'VS18':['VS08','VS04'],'VS19':['VS04','VS11'],'VS21':['VS01','VS10']}

def intersects(a,b):return a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]
def finalize_groups(obj,review,dense=False):
    groups=[];components=obj['components'];lookup={r['instance_id']:r for r in components};byline=defaultdict(list)
    for g in obj['groups']:byline[g['line_id']].append(dict(g))
    for lid,gg in byline.items():
        gg.sort(key=lambda g:g.get('group_rank',g.get('body_gap_span_x',[0])[0]));failed=not review.get('primary_eligible',True);extent_cap=None
        if dense:
            bi=int(lid.split('_BLOCK')[1].split('_')[0]);li=int(lid.rsplit('_L',1)[1]);failed=li in review['unknown_lines'].get(str(bi),[]);extent_cap=review.get('extent_caps',{}).get(str(bi),{}).get(str(li))
        for r in components:
            if any(intersects(r['bbox_xyxy'],z) for z in review.get('uncertain_zones',[])):r.update(status='unknown',admitted=False,fine_family=None,broad_family=None,source_uncertainty='Source-reviewed zone: substrate/drawing/contact; do not assign unit identity')
        if extent_cap:
            for r in components:
                if r['instance_id'] in {i for g in gg for i in g['member_ids']} and (r['bbox_xyxy'][0]<extent_cap[0] or r['bbox_xyxy'][2]>extent_cap[1]):r.update(status='unknown',admitted=False,fine_family=None,broad_family=None,source_uncertainty='Connected parent crosses source extent cap; no clipping into a known unit')
            for g in gg:g['member_ids']=[i for i in g['member_ids'] if extent_cap[0]<(lookup[i]['bbox_xyxy'][0]+lookup[i]['bbox_xyxy'][2])/2<extent_cap[1]]
            gg=[g for g in gg if g['member_ids']]
        # Recheck contacts before materializing any sequence; no stale admitted group.
        occurrences=Counter(i for g in gg for i in g['member_ids'])
        for i,n in occurrences.items():
            if n>1:lookup[i].update(status='unknown',admitted=False,fine_family=None,broad_family=None,group_boundary_contact='Same connected parent spans multiple proposed group slots; no cut imposed')
        extent_parts=[lookup[i] for i in occurrences]
        extent=[min([r['bbox_xyxy'][0] for r in extent_parts],default=0),max([r['bbox_xyxy'][2] for r in extent_parts],default=1)]
        if extent_cap:extent=[max(extent[0],extent_cap[0]),min(extent[1],extent_cap[1])]
        endpoint_unknown=False
        if gg:
            endpoint_unknown=any(lookup[i]['status']=='unknown' for g in (gg[0],gg[-1]) for i in g['member_ids'])
        for j,g in enumerate(gg):
            pp=[lookup[i] for i in g['member_ids']];a=min([r['bbox_xyxy'][0] for r in pp],default=extent[0]);c=max([r['bbox_xyxy'][2] for r in pp],default=extent[1]);b=min([r['bbox_xyxy'][1] for r in pp],default=0);d=max([r['bbox_xyxy'][3] for r in pp],default=0)
            manual_unknown=review.get('unknown_groups',[]);manual_unknown=manual_unknown=='all' or isinstance(manual_unknown,list) and j+1 in manual_unknown
            membership_unknown=failed or manual_unknown or any(r['status']=='unknown' for r in pp)
            known=bool(pp and not membership_unknown and all(r['admitted'] for r in pp));fine=[r['fine_family'] for r in pp] if known else None;broad=[r['broad_family'] for r in pp] if known and all(r['broad_family'] for r in pp) else None
            source_rank=j/(len(gg)-1) if len(gg)>1 else .5;pixel=((a+c)/2-extent[0])/max(1,extent[1]-extent[0]);eligible=bool(not failed and not endpoint_unknown)
            g.update(group_id=lid+f'_G{j+1:03d}',bbox_xyxy=[a,b,c,d],group_rank=j,group_count=len(gg),normalized_group_rank=source_rank,source_pixel_center_x=(a+c)/2,normalized_pixel_center=pixel,line_x_extent_px=extent,visual_fine_units=fine,visual_merged_units=broad,visual_factored_units=[v for u in broad for v in FACTORS.get(u,[u])] if broad else None,writing_membership='unknown' if membership_unknown else 'source writing candidate',boundary_status='unknown: failed complete row' if failed else 'source-inspected fixed gap hypothesis; internal/letter boundaries not certified',row_membership_status='unresolved_method_or_photo' if failed else 'source-inspected physical-row hypothesis',ordinal_extent_status='unknown' if failed else 'fixed source gap slots; includes unknown-unit slots',pixel_extent_status='unknown' if failed or endpoint_unknown else 'measured source writing bounding extent within source-adjudicated field',primary_eligible=eligible,endpoint_unknown=endpoint_unknown,section=None,hand=None,currier=None,conventional_mapping=None)
            # Failed rows stay unknown. Eligible ranks are not re-indexed after unknown units.
            groups.append(g)
    obj['groups']=groups;obj['components']=components;obj['source_adjudication']=review;return obj

def apply_manual_gaps(obj,review):
    cuts=review.get('cuts')
    if cuts is None or not cuts:return obj
    npz=np.load(OUT/'data/observations/source_adjudication_v2/reconstructed_core'/f'{obj["view_id"]}_masks.npz');core=npz['body_core'];x0,cy0,w,y1=obj['source_crop'];occupied=core.any(axis=0);lo=int(np.flatnonzero(occupied).min()) if occupied.any() else 0;hi=int(np.flatnonzero(occupied).max())+1 if occupied.any() else w;resolved=[];cutrecords=[]
    for c in cuts:
        if not lo<c<hi:continue
        nearby=[x for x in range(max(lo,c-12),min(hi,c+13)) if not occupied[x]];cut=min(nearby,key=lambda x:abs(x-c)) if nearby else c
        a=cut;b=cut
        if not occupied[cut]:
            while a>lo and not occupied[a-1]:a-=1
            while b<hi and not occupied[b]:b+=1
        cutrecords.append(dict(requested_native_x=c,cut_native_x=cut,blank_body_interval=[a,b],status='source whitespace hypothesis' if b>a else 'unknown contact; no connected parent cut'))
        resolved.append(cut)
    spans=list(zip([lo]+sorted(set(resolved)),sorted(set(resolved))+[hi]));groups=[];vid=obj['view_id'];lid=vid+'_ADJ_L001'
    for j,(a,c) in enumerate(spans):
        parts=[r for r in obj['components'] if r['bbox_xyxy'][0]<c and a<r['bbox_xyxy'][2]];parts.sort(key=lambda r:(r['bbox_xyxy'][0],r['bbox_xyxy'][1]))
        groups.append(dict(group_id=lid+f'_G{j+1:03d}',line_id=lid,view_id=vid,split=obj['review']['split'],folio_component=obj['review']['folio_component'],group_rank=j,member_ids=[r['instance_id'] for r in parts],body_gap_span_x=[a,c]))
    obj['groups']=groups;obj['source_boundary_overrides']=cutrecords;return obj

def main():
    dest=OUT/'data/observations/visual_dataset_v2'
    if (dest/'FREEZE_MANIFEST.json').exists():raise ValueError('v2 frozen; no mutation permitted')
    dest.mkdir(exist_ok=True);sources=read_csv(OUT/'data/source/yale_native_all_manifest.csv');root=OUT/'data/observations/source_adjudication_v2';boundary={r['view_id']:r for r in read_json(root/'boundary_judgments.json')};dense_reviews={r['view_id']:r for r in read_json(root/'dense_blocks/source_reviews.json')};curves={r['view_id']:r for r in read_json(root/'curved_judgments.json')};allgroups=[];allcomponents=[];coverage=[];indexes=[]
    for src in sources:
        vid=src['view_id'];records=[]
        if vid in boundary:
            obj=read_json(root/'reconstructed_core'/f'{vid}.json');obj=apply_manual_gaps(obj,boundary[vid]);records.append(finalize_groups(obj,boundary[vid]))
        if vid in dense_reviews:
            obj=read_json(root/'dense_blocks/proposals'/f'{vid}.json');obj=finalize_groups(obj,dense_reviews[vid],True)
            # Dense block supersedes the isolated failed row on the same capture;
            # retain its source review as audit evidence, not duplicate assay data.
            if records:records[0]['groups']=[];records[0]['superseded_by_dense_blocks']=True
            records.append(obj)
        groups=[g for obj in records for g in obj['groups']];components=[r for obj in records for r in obj['components']];allgroups.extend(groups);allcomponents.extend([dict(r,view_id=vid,native_source=src['path'],split=groups[0]['split'] if groups else 'unknown') for r in components])
        prior=read_json(OUT/f'data/observations/regional_candidates_v11/{vid}.json')
        status='source reviewed partial writing fields' if records or vid in curves else 'unknown: unadjudicated proposals only'
        canonical=dict(view_id=vid,native_source=src['path'],source_sha256=sha256(OUT/src['path']),status=status,writing_fields=records,curved_writing_adjudication=curves.get(vid),prior_proposal_path=f'data/observations/regional_candidates_v11/{vid}.json',prior_rows_status='Unknown unless a reviewed field explicitly supersedes them; no old unit sequences admitted',unreviewed_prior_rows=len(prior['lines']),physical_folio_identity='caption only; panel correspondence unknown',canonical_graphemes='unknown',pen_lifts='unknown')
        write_json(dest/f'{vid}.json',canonical);coverage.append(dict(view_id=vid,source_reviewed_fields=len(records)+(vid in curves),groups=len(groups),eligible_groups=sum(g['primary_eligible'] for g in groups),admitted_eligible_fine_groups=sum(g['primary_eligible'] and bool(g['visual_fine_units']) for g in groups),unreviewed_prior_rows=len(prior['lines'])));indexes.append(dict(view_id=vid,status=status,model_path=f'data/observations/visual_dataset_v2/{vid}.json'))
    write_json(dest/'assay_groups_source_only.json',allgroups);write_json(dest/'view_index.json',indexes);write_csv(dest/'coverage.csv',coverage)
    write_json(dest/'model_contract.json',dict(version='manuscript-derived source-adjudicated segmentation v2',scope='204 native captures indexed; selected source fields adjudicated; other writing/rows unknown',observations='writing/drawing/decoration zones, native connected parents, body-path geometry, source-visible gap hypotheses, source bounding extents',units='Connected ink assemblies, fine source image-family labels, broad/factor hypotheses; neither letters nor alphabet',representations=['visual_fine_units','visual_merged_units','visual_factored_units'],internal_cuts='No source-supported universal internal grapheme cut or pen-lift order established',alternative_boundaries='Original 0.35/0.55/0.75 body-gap proposals remain comparison hypotheses in immutable v11; v2 primary fixed source review overrides and 16px dense gap, not selected for assay support',pixel_formula='((min_parent_x+max_parent_x)/2 - line_writing_left)/(line_writing_right-line_writing_left), in native Yale pixels; unknown endpoints exclude both matched primary endpoints',rank_formula='j/(N-1), N includes unknown-unit slots in source-inspected row hypothesis; no re-ranking after exclusions',null_units='Unknown membership, incomplete coverage or unrecognized source family remains null; no reconstruction from EVA/RF/v101',post_exposure='Previously exposed to conventional claims; source-only repair is not a new blind replication',physical_identity='Capture/caption grouping only; no newly certified duplicate-writing overlap',freeze_before_v2_assay=True))
    # Neutral atlas: examples from source writing candidates only, training first.
    eligible_ids={i for g in allgroups if g['primary_eligible'] and g['visual_fine_units'] for i in g['member_ids']}
    atlas=[];gallery=OUT/'figures/source_adjudication_v2/atlas_accepted';gallery.mkdir(exist_ok=True)
    for family in sorted({r['fine_family'] for r in allcomponents if r['instance_id'] in eligible_ids and r.get('fine_family') and r['status']=='writing_candidate'}):
        pool=sorted([r for r in allcomponents if r['instance_id'] in eligible_ids and r.get('fine_family')==family and r['status']=='writing_candidate'],key=lambda r:(r['split']!='train',r['view_id'],r['instance_id']));seen=set();examples=[]
        for r in pool:
            if r['view_id'] in seen:continue
            seen.add(r['view_id']);im=Image.open(OUT/r['native_source']).convert('RGB');a,b,c,d=r['bbox_xyxy'];crop=im.crop((max(0,a-12),max(0,b-12),min(im.width,c+12),min(im.height,d+12)));path=gallery/f'{family}_{len(examples)+1}.png';crop.save(path);examples.append(dict(view_id=r['view_id'],instance_id=r['instance_id'],bbox_xyxy=r['bbox_xyxy'],source_crop=path.relative_to(OUT).as_posix(),split=r['split'],geometry=r['features']))
            if len(examples)==3:break
        atlas.append(dict(family=family,broad_hypothesis=pool[0].get('broad_family'),examples=examples,grapheme_atomicity='unknown',pen_lifts='unknown',allography='Image-family assignment hypothesis, not linguistic equivalence',source_family_model='Original frozen source-only fine K128 model transferred without retuning'))
    write_json(dest/'neutral_visual_atlas.json',atlas);write_json(dest/'factor_hypotheses.json',FACTORS)
    write_json(dest/'summary.json',dict(native_captures=len(sources),reviewed_isolated_rows=len(boundary),reviewed_local_assemblies=len(read_json(root/'assembly_judgments.json')),reviewed_dense_captures=len(dense_reviews),dense_paths=sum(len(read_json(root/'dense_blocks/proposals'/f'{v}.json')['lines']) for v in dense_reviews),reviewed_curved_captures=len(curves),reviewed_panel_pairs=len(read_json(root/'panel_judgments.json')),groups=len(allgroups),primary_eligible_groups=sum(g['primary_eligible'] for g in allgroups),admitted_eligible_fine_groups=sum(g['primary_eligible'] and bool(g['visual_fine_units']) for g in allgroups),admitted_eligible_broad_groups=sum(g['primary_eligible'] and bool(g['visual_merged_units']) for g in allgroups),atlas_families=len(atlas),unreviewed_proposals_status='unknown, not wholesale promoted to segmentation',complete_manuscript_alphabet_established=False))
    print(read_json(dest/'summary.json'),flush=True)
if __name__=='__main__':main()
