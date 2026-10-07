"""Record explicit source-gallery review of v4 medium candidate families."""
from common import OUT, read_json, write_json, sha256

ARTIFACT=[5,23,25,39,42,48,52,58,85,95,115,117,119]
MIXED=[1,2,3,6,10,12,13,21,26,34,49,51,54,62,70,72,76,97]
VARIABLE=[7,22,27,40,45,56,59,67,71,89,90,93,100,111,120]
DESCRIPTIONS={
4:'low connected curls followed by a closed loop and returning tail',
8:'paired tall uprights with upper loop, followed by repeated short slants and a return',
9:'upper curved return descending to an angular lower foot',11:'small closed loop; one exemplar is an open descending return',
14:'two vertically arranged loop-like compartments',15:'single rounded loop, variable closure and slant',
16:'lower loop joined to an upper curved compartment',17:'paired low curls joined by horizontal ink',
18:'small closed ring with variable thickness',19:'low connected curls followed by a ring',
20:'upper curved return and angular lower foot',24:'small repeated slant/arch-like traces',
28:'short angular returning trace',29:'small forked or returning trace; fragmentation unresolved',
30:'open upper return above a bent lower trace',31:'two low curl-like traces with horizontal connection',
32:'low curl followed by lower and upper loop-like compartments',
33:'paired tall uprights and upper loop followed by low connected curls',
35:'several short slants joined to a rounded returning trace',36:'small angular enclosed or nearly enclosed trace',
37:'paired tall uprights and upper loop followed by a low angled trace',
38:'short slants followed by an upper returning curve',41:'ring followed by looped angular return',
43:'upright narrow loop with angular descending return',44:'two vertically stacked loop-like compartments',
46:'small open curl-like trace',47:'two low connected curl-like traces',
50:'paired uprights with upper loop followed by low angled trace',53:'small horizontally oval closed ring',
55:'lower loop with upper return followed by low angled trace',57:'small upper curved loop descending into short lower trace',
60:'low connected curls and an oval compartment',61:'closed ring followed by looped angular return',
63:'small rounded ring',64:'two long uprights connected by an upper bar and loop',
65:'paired tall uprights with upper loop and following low curl',66:'two stacked closed compartments',
68:'small flattened ring',69:'narrow loop with returning extension; one exemplar is faint',
73:'ring followed by narrow loop and angular return',74:'small upper loop with a long descending curved tail',
75:'small oval ring',77:'upper return descending to an angular lower foot',
78:'low connected curl followed by a looped extension',79:'paired uprights with upper loop and nearby low traces',
80:'lower loop connected to upper narrow returning compartment',81:'upper curved return followed by a low loop',
82:'short raised return above low horizontal connected curls',83:'small rounded ring',
84:'narrow loop with angular descending return',86:'small open curl-like trace',
87:'looped angular return with descending tail; neighboring ring sometimes present',
88:'tall downward stem below horizontal bar with nearby small ring',
91:'paired uprights connected by upper loop and bar',92:'small closed loop; very small exemplar unresolved',
94:'small rounded ring of varying closure',96:'small rounded ring of varying thickness',
98:'small ring of varying slant',99:'low slants or loop followed by upper returning curve',
101:'small upper loop with descending curved tail',102:'two low curls with horizontal connection',
103:'stacked loop-like compartments; some exemplars have adjacent low traces',
104:'upper curve descending to angular lower foot',105:'low curl and loop with descending tail',
106:'lower closed loop joined to upper returning compartment',107:'paired uprights with upper loop followed by low loop and tail',
108:'closed ring followed by narrow loop and angular return',109:'low connected curls and ring followed by returning trace',
110:'lower loop joined to upper returning compartment',112:'raised curved return above low horizontally connected curls',
113:'raised short return above low connected curls',114:'multiple short slants joined to upper rounded return',
116:'small rounded ring',118:'small angled arch or nearly closed loop',
121:'two short slant/arch-like traces',122:'lower loop and upper return followed by a low loop with tail',
123:'upper curved return descending to angular foot',124:'raised small return above low connected curls',
125:'paired tall uprights with upper connecting bar and loop',126:'small rounded ring',
127:'lower loop and upper return followed by low loop with descending tail',
128:'lower loop and upper return followed by low slants and returning curve'}

def main():
    source=OUT/'data/observations/visual_family_models_v4/medium_assemblies_families.json'
    records=read_json(source);review=[]
    for r in records:
        n=r['cluster_index']+1
        category='artifact' if n in ARTIFACT else 'mixed' if n in MIXED else 'writing_variable' if n in VARIABLE else 'writing_consistent'
        if category=='artifact':desc='Closest training exemplars dominated by parchment texture, paint, long non-writing traces or extremely small fragments.'
        elif category=='mixed':desc='Training exemplars mix readable writing with blank texture, drawing, faint fragments, or incompatible structures.'
        elif category=='writing_variable':desc='Readable writing assemblies recur, but included structures and neighboring rows vary; atomic boundary unsupported.'
        else:desc=DESCRIPTIONS[n]
        review.append(dict(**r,review_category=category,review_scope='six closest exemplars from distinct training folio components; not a random prevalence audit',
            visual_description=desc,confidence='moderate for visible recurrence; low for atomic-unit identity' if category=='writing_consistent' else 'insufficient for an accepted unit identity',
            contexts='native writing-region proposals across listed source views; section and hand annotations withheld',
            observed_variants='See source exemplars and numerical height/connectivity medians; different clusters may be allographs of the same structure.',
            segmentation_alternatives=['whole assembly','separate raster components','cuts at low skeleton crossings','larger space-gap group'],
            prototype_gate_eligible=category=='writing_consistent',
            gallery=f'figures/visual_atlas_v4/medium_assemblies/{r["family_id"]}.png'))
    write_json(OUT/'data/observations/medium_family_source_review_v4.json',dict(source_sha256=sha256(source),
        reviewer='Codex visual review of all 16 source-gallery sheets; no conventional transcription opened',
        records=review,status='prototype source-quality review; held-out source audit required',
        limitations=['Closest exemplars are optimistically selected.','Visible crop context is not identical to assigned ink mask.',
            'This review does not establish an alphabet or globally consistent boundaries.']))
    print({cat:sum(r['review_category']==cat for r in review) for cat in ['artifact','mixed','writing_variable','writing_consistent']})

if __name__=='__main__':main()
