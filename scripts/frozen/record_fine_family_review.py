"""Source-reviewed connected structures and competing visual allograph merges.

Broad visual categories are hypotheses of common structure, not a new alphabet.
Every category is derived from training source galleries and retains raw bins.
"""
from common import OUT,read_json,write_json,sha256

ARTIFACT={4,5,7,49,85}
MIXED={8,28,31,45,51,55,56,66,68,82,84,101,116}
FRAGMENT={9,19,39,41,47,58,65,69,74,75,83,95,104,124}
VARIABLE={35,53,72,78,87,100}
STRUCTURES={
 'VS01':('small closed rounded compartment',{2,10,23,32,44,50,54,57,61,86,108}),
 'VS02':('rounded open return, variable closure',{1,38}),
 'VS03':('upper curve descending to an angular lower return',{16,80,81,89,92,96,111}),
 'VS04':('two low curl-like traces connected horizontally',{3,25,52,79,119,128}),
 'VS05':('short repeated slant or arch-like traces',{6,59,67,126}),
 'VS06':('small single slant-like or angled trace',{11,43}),
 'VS07':('two stacked loop-like compartments; closure varies',{12,18,40,70,94,98,115,118}),
 'VS08':('paired tall uprights connected by upper bar and loop',{21,24,29,33,37,42,46,76,97,109,127}),
 'VS09':('tall downward stem, upper bar and nearby ring-like compartment',{13,26,107}),
 'VS10':('narrow loop joined to angular descending return',{14,34,36,71,77,93,112,123}),
 'VS11':('small upper loop with a longer curved descending tail',{15,27,63,64,99,105,117}),
 'VS12':('low connected curls followed by a closed compartment',{17,102}),
 'VS13':('small open curl-like trace',{22,30,60,90}),
 'VS14':('raised short return above horizontally connected low curls',{73,103}),
 'VS15':('small arch-like or nearly enclosed angular trace',{20,110,113,114}),
 'VS16':('low curl joined to stacked loop-like compartments',{48,88}),
 'VS17':('paired tall uprights with adjoining low arch or loop',{91,125}),
 'VS18':('paired tall structure with lower horizontal connection and curls',{120}),
 'VS19':('low curls and closed compartment with descending tail',{62,121}),
 'VS20':('short slants joined to rounded returning trace',{106}),
 'VS21':('closed compartment adjoining narrow looped angular return',{122})}

def main():
    source=OUT/'data/observations/visual_family_models_v4/fine_components_families.json';rr=read_json(source)
    mapping={n:(sid,desc) for sid,(desc,nn) in STRUCTURES.items() for n in nn};reviews=[]
    for r in rr:
        n=r['cluster_index']+1
        category='artifact' if n in ARTIFACT else 'mixed' if n in MIXED else 'fragment' if n in FRAGMENT else 'writing_variable' if n in VARIABLE else 'writing_consistent'
        if category=='writing_consistent':sid,desc=mapping[n]
        else:sid=None;desc={'artifact':'Texture, paint or long non-writing traces dominate source exemplars.',
            'mixed':'Source exemplars mix writing, drawing, blank texture or incompatible extents.',
            'fragment':'Tiny isolated fragments recur but identity and completeness remain unresolved.',
            'writing_variable':'Writing visible but connected assemblies include variable neighboring structures or rows.'}[category]
        reviews.append(dict(**r,review_category=category,visual_description=desc,visual_structure_merge_hypothesis=sid,
            confidence='moderate for recurrence, low for atomic identity' if sid else 'unresolved',
            review_scope='all 16 gallery sheets; six nearest training exemplars per family',
            contexts='source writing-region proposals; unknown hand and section; physical x order is not pen order',
            observed_variants='Slant, closure, height, thickness and adjoining traces vary; gallery and median geometry preserve differences.',
            segmentation_alternatives=['connected object as whole','sparse-crossing internal cuts','larger medium assembly','visual allograph merge with related prototype bins'],
            gallery=f'figures/visual_atlas_v4/fine_components/{r["family_id"]}.png',prototype_gate_eligible=bool(sid)))
    write_json(OUT/'data/observations/fine_family_source_review_v4.json',dict(source_sha256=sha256(source),records=reviews,
        status='training source review; connected object is not asserted atomic',
        limitations=['Nearest exemplars are optimistic; held-out source-quality audit required.',
            'VS identifiers describe competing shape categories, not graphemes or letters.',
            'Merging similar shapes can conflate distinct units; retaining bins can split allographs.']))
    write_json(OUT/'data/observations/visual_structure_merge_hypotheses_v0.json',dict(
        source='training source galleries only; conventional transcriptions withheld',
        structures=[dict(structure_id=s,description=d,prototype_bins=sorted(nn),status='hypothesis; raw prototype identities retained') for s,(d,nn) in STRUCTURES.items()],
        compound_factor_hypotheses=[dict(compound=s,proposed_factors=f,status='proposed visual analogy; boundaries and pen lifts unresolved') for s,f in
            [('VS12',['VS04','VS01']),('VS16',['VS13','VS07']),('VS17',['VS08','VS15']),
             ('VS18',['VS08','VS04']),('VS19',['VS04','VS11']),('VS21',['VS01','VS10'])]],
        caution='These analogies do not establish compositional identity. Whole and factored interpretations both remain.'))
    print({c:sum(r['review_category']==c for r in reviews) for c in ['artifact','mixed','fragment','writing_variable','writing_consistent']})

if __name__=='__main__':main()
