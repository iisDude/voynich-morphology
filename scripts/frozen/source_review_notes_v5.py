"""Explicit native-pixel adjudicator decisions; no structural class inputs."""
from common import OUT,read_json,write_json
from register_row_benchmark_v5 import D,G
from datetime import datetime,timezone
from PIL import Image,ImageDraw

NOTES={
'B001':dict(
 target=[7,9,11,12,14,19,20,24,27,28,35,36,37,38,49,52,53,55,57,76,85,87,88,90,94,98,115,118,121,122,126,127,129,134,135],
 neighbor=[17,34,47,56,86,132],
 uncertain=[8,10,13,15,18,32,33,46,64,66,70,89,95,96,108,112,120,124,128,130,133],
 detached=[12],
 physical_endpoints=[[415,495,422,613],[1987,636,2022,686]],
 mixed=[15],
 confirmed_joins=[[7,9]],possible_joins=[[55,57]],source_separations=[[9,11],[19,20]],
 note='First physical row. Faint paired upper uprights and compact body traces are writing. A vertically diffuse raster parent O015 contains visible body loops and inter-row brown trace; pure connected-parent ownership is unresolved. O047 is an upper trace of the next row. Minute ridge-only detections elsewhere are surface contrast; small near-trace remnants listed as uncertain. No pen-lift inference.'),
'B005':dict(
 target=[33,34,38,39,40,41,51,58,61,66,70,71,73,93,94,96,98,101,102,103,104,105,107,108,111,117,118,119,122,125,131,138,142,146,148,151,152,154,155,157,158,161,166,169,170,172,174,179,184,185,187,188,191,193,194],
 neighbor=[32,37,47,57,63,65,68,72,75,79,81,91,92,95,99,100,106,114,121,132,144,159,162,164,165,167,171,173,175,181,182,183,186,190,192],
 uncertain=[16,19,35,46,60,67,78,88,97,112,120,123,124,127,130,140,143,147,156,163,168,176,177,180,189,199,203,204,205,207,208,213,215,217,219,221,222,223],
 detached=[94,118,151],mixed=[120,189],possible_joins=[[33,34],[104,105,107],[169,170]],
 physical_endpoints=[[748,438,802,522],[2629,510,2665,553]],
 note='Top physical row. Multiple faint terminal fragments remain distinct from ridge texture. O189 is a tall diffuse substrate-connected mask, not a writing parent; it may include writing, so mixed and unresolved. O120 can span rows. Connected lower-row tall structures are assigned to the neighbor even when their tops enter the target body band. Native source endpoints are comfortably inside the photograph.'),
'B002':dict(target=[10,13,14,15,23,25,27,30,37,39,41,43,47,49,53,54,55,59,61,63,73,75,78,83,86,89,96,102,104,106,111,114,117],neighbor=[12,24,35,36,42,46,48,57,74,100],uncertain=[11,16,17,21,29,31,32,38,45,56,60,62,67,68,70,71,77,80,81,84,85,87,91,94,95,97,98,99,103,105,110,127,130,132,135],detached=[49],mixed=[17],possible_joins=[[61,63]],physical_endpoints=[[402,728,462,791],[2001,788,2021,825]],note='Third physical row. The initial provisional body aid mistakenly followed the fourth row on the left. Corrected before reference judgments: anchor at the source x-reference belongs to the third continuous sloping row. This is a source-layout correction, with original proposal and initial aid retained. Fourth-row tall structures remain neighbor objects.'),
'B006':dict(target=[51,53,55,58,62,64,66,72,73,74,77,80,81,85,87,88,90,94,97,98,103,107,111,113,116,119,120,123,128,133,138,140,144,146,148,149,151,154,155,157,160,163,165,167,169],neighbor=[50,52,54,56,60,63,65,67,69,70,75,83,84,86,93,96,100,105,109,112,115,117,124,130,131,134,136,137,139,142,143,145,152,153,156,159,164],uncertain=[1,29,34,57,89,92,101,102,108,118,126,141,158,166],detached=[80,148],mixed=[118,141],possible_joins=[],physical_endpoints=[[739,717,778,758],[2430,696,2484,782]],note='Continuous row near y750. Upper portions of preceding and following rows enter the context. O118 and O141 are possible cross-row structures; neither is forced into the target sequence. Narrow coherent curves are writing, unlike scattered ridge detections.'),
'B007':dict(target=[48,53,54,57,60,62,64,67,71,78,87,89,94,95,96,97,99,100,101,102,105,111,114,115,116,118,119,120,127,128,130,132,134,136,144,146,147,148,149,150,151,154,157,158,159,161,164,167,169,172,181,183,189,195],neighbor=[51,59,75,82,83,92,98,113,117,122,129,152,156,165,166,168,171,186,190,192],uncertain=[1,52,88,91,93,104,133,145,155,160,162,163,170,176,187,202,217,228,231,240],detached=[87,114,118,120],mixed=[],possible_joins=[[48,53,54],[94,95,96]],physical_endpoints=[[609,351,690,465],[2467,400,2501,449]],note='Top row. Very faint upper paired uprights are real writing; their primary-mask fragments do not establish physical disconnection. Competing parent assemblies retained. Small isolated brown candidates near endpoints remain unresolved; ridge-only candidates show substrate contrast.'),
'B008':dict(target=[30,31,33,35,37,44,46,49,53,55,57,59,63,65,67,69,72,77,91,94,96,97,99,110,114,120,123,128,135,139,142,143,144,146,148,149,151,157,159,160,162,165],neighbor=[28,32,34,36,38,43,45,47,48,50,51,56,58,60,62,64,70,74,76,78,81,82,84,87,90,92,95,98,100,102,103,105,106,107,109,111,112,113,115,117,118,119,122,125,126,129,130,131,133,136,138,141,145,147,153,156],uncertain=[41,61,66,68,71,73,75,79,83,85,86,88,89,93,101,104,108,116,121,124,132,137,140,152,154,155,158,161,163,164,167,169,172,173],detached=[],mixed=[75,161],possible_joins=[],physical_endpoints=[[626,541,658,587],[2493,512,2527,597]],note='Third horizontal row. Individual dark curves and loops are writing. The large O075 and O161 masks can contain neighboring-row contacts; no canonical parent is asserted. The tall lower-row uprights O111/O112 remain neighboring writing despite entering the body band.'),
'B011':dict(target=[7,13,16,17,20,23,28,35,37,39,41,44,50,52,54,63,65,69],neighbor=[5,8,9,11,12,14,15,18,21,22,24,26,29,30,31,34,38,40,42,43,47,48,49,51,53,57,59,66,67,68,81,87,90],uncertain=[3,6,10,19,27,32,33,36,58,60,61,62,70,71,72,73,74,75,76,83,85,89,91,94,95,97,101],nonwriting=[102],detached=[32],mixed=[10,19,27,33],possible_joins=[],physical_endpoints=[[466,842,538,875],[1678,846,1750,929]],reviewed_body_path=[[466,874],[950,888],[1450,922],[1750,924]],reviewed_scope=[466,1750],note='Second physical row, confirmed in coordinate-labeled full RGB context. It slopes from body y860 to y915; the upper row continues farther right. Four source-mask structures contain possible inter-row contacts or substrate contamination. O102 is the drawing contour at the field edge. O032 is a coherent curved writing trace with uncertain row/parent attachment.'),
'B012':dict(target=[5,9,12,16,17,18,23,27,31,32,37,40,44,47,49,53,56],neighbor=[4,6,7,10,11,13,15,19,20,22,25,28,30,33,34,35,36,38,39,41,42,45,46,48,50,52,54,55,57,59],uncertain=[1,2,3,8,14,21,24,26,43,51,58,60,61,62,63,64,65,66,67,68,69,70,71,72,73],mixed=[3,14,21],detached=[24],possible_joins=[],physical_endpoints=[[455,949,527,984],[1464,1002,1530,1039]],reviewed_body_path=[[455,979],[900,1000],[1300,1026],[1530,1040]],reviewed_scope=[455,1530],note='Fourth physical row is nearest the registered anchor at the source x-reference. The fifth row ends earlier on the left and was not substituted. The leading lower loop under O003 and the O014 mask touching two rows remain source-ownership unknown. Writing after the leading contact is fully traced. The enormous O021 raster is substrate/drawing contamination with possible embedded writing, not a parent.'),
'B009':dict(target=[8,11,13,14,18,19,20,22,23,24,28,33,35,36,38,49,51,52,54,55,60,62,65,67,68,71,79,80,82,87,90,98,101,114,117,123,127,134],neighbor=[12,15,21,25,31,34,42,47,50,53,56,66,69,74],uncertain=[9,10,16,17,26,27,29,32,37,39,40,43,44,45,46,48,57,58,59,61,63,64,70,72,73,75,78,81,83,86,91,94,95,103,104,108,113,118,120,124,126,128,129,132,133,137,138,141,144,151,152,160],nonwriting=[77],mixed=[48],detached=[52,62],possible_joins=[[8,11],[35,36]],physical_endpoints=[[284,416,363,501],[1910,480,1933,530]],reviewed_scope=[284,1933],reviewed_body_path=[[284,494],[850,489],[1350,498],[1750,523],[1933,533]],note='Top row. Full RGB sweep confirms its right end near x1933; the older field extends across empty textured parchment to x2238. O077 is an orange irregular stain, confirmed nonwriting. O048 contains a body-rooted tall form and a lower loop/stem with possible inter-row contact. Minute nearby remnants are unresolved; the numerous ridge-only detections after the actual end are nonwriting.'),
'B010':dict(target=[7,9,10,14,18,21,23,26,27,31,32,33,35,37,40,41,44,46,47,50,51,53,55,57,58,60,63,66,68,70,71,74,78,81,83,86,88,90,92,93],neighbor=[6,8,12,13,15,16,20,22,25,30,36,38,43,45,48,49,52,54,56,59,61,62,64,65,67,69,72,73,77,82,85,87,89,91],uncertain=[11,17,19,24,28,29,34,39,42,75,76,79,80,84,94,95,97,106,110,116,161,169,186,197,200,201,229,230,236,246,249,278,300,301],mixed=[17,39],writing_owner_unknown=[42],detached=[42],possible_joins=[],physical_endpoints=[[314,648,347,693],[1954,674,1998,748]],reviewed_scope=[314,1998],reviewed_body_path=[[314,684],[850,682],[1300,699],[1750,717],[1998,723]],note='Fourth row, with native body roots traced across the page. It ends near x1998, not the old field edge near x2286. The diffuse O017 and O039 masks combine uncertain brown substrate with visible writing. The terminal open loop has a long lower trace but does not touch the next row in the photograph. Off-row small texture remains outside the confirmed sequence.'),
'B015':dict(target=[2,3,4,6,8,9,10,11,14,15,16,18,20,21,23,24,28,32,33,34,35,37,41,42,43,45,46,47,48,50,51,53,55,57,58,60,61,63,65,66,67,70,72,74],neighbor=[12,17,22,29,38,44,49,52,54,59,64,68],margin=[75,80,86],nonwriting=[1],uncertain=[5,7,13,19,25,26,27,30,31,36,39,40,56,62,69,71,73,76,77,78,79,81,82,83,84,85],mixed=[7,13],writing_owner_unknown=[36],detached=[19,36],possible_joins=[[7,9]],physical_endpoints=[[238,172,343,272],[2260,298,2282,336]],reviewed_scope=[238,2282],reviewed_body_path=[[238,273],[850,279],[1500,287],[1900,302],[2282,328]],note='Top horizontal row beside drawn stars. O001 is a connected drawing-star/stem structure. O075/O080/O086 are dark detached marginal writing traces above the ordinary body line, recorded separately without interpreting their conventional meaning. The broad upper frame O009 is one connected writing construction, possibly compound; it is not split to fit a class. O007/O013 descend toward following-row ink; ownership at contacts remains unknown.'),
'B016':dict(target=[5,8,11,13,15,17,19,21,22,26,28,29,31,36,38,40,41,45,48,51,59,61,63,65,66,67,70,72,74,77,79,81,83,88],neighbor=[3,4,6,7,9,10,12,14,16,18,20,23,25,30,32,33,34,35,37,39,42,43,44,46,47,49,50,52,53,54,55,56,58,60,64,68,69,71,73,75,78,80,82,84,89,90],nonwriting=[1],uncertain=[2,24,27,57,62,76,85,86,87,91,92,93,94,95,96,97],mixed=[24,62,76],detached=[],possible_joins=[],physical_endpoints=[[261,533,349,554],[2194,589,2269,623]],reviewed_scope=[261,2269],reviewed_body_path=[[261,555],[900,579],[1450,592],[1900,605],[2269,624]],note='Registered anchor at the native x-reference belongs to the long row rising from x261,y533 to x2269,y623. The initial provisional aid followed the next row on the left, which ends around x1471. Corrected from full coordinate-labeled RGB before reference freeze. O024/O062/O076 have long descenders or possible adjoining-row contacts. The left star O001 is drawing.'),
}

# Full coordinate-labeled RGB sweep corrections. IDs retain their original
# source-raster identity; corrections precede all class inference and rule fit.
NOTES['B005']['target']=[i for i in NOTES['B005']['target'] if i!=194]+[160,182]
NOTES['B005']['neighbor']=[i for i in NOTES['B005']['neighbor'] if i!=182]+[77,194]
NOTES['B005']['physical_endpoints'][1]=[2614,463,2649,499]
NOTES['B005']['reviewed_scope']=[748,2649]
NOTES['B005']['reviewed_body_path']=[[748,523],[1300,530],[1900,539],[2300,510],[2649,500]]
NOTES['B006']['target']=[i for i in NOTES['B006']['target'] if i not in [66,97]]+[68,99]
NOTES['B006']['uncertain'] += [66,97]
NOTES['B006']['writing_owner_unknown']=[102]
NOTES['B006']['possible_joins']=[[146,148]]
NOTES['B007']['target']=[i for i in NOTES['B007']['target'] if i!=67]+[66,173,175]
NOTES['B007']['neighbor'] += [67,81,174]
NOTES['B007']['uncertain'] += [226]
NOTES['B008']['neighbor']=[i for i in NOTES['B008']['neighbor'] if i not in [84,129,131,133,136]]+[134]
NOTES['B008']['target'] += [84,129,131,133]
NOTES['B008']['uncertain'] += [136]
NOTES['B008']['writing_owner_unknown']=[136]
NOTES['B008']['detached']=[136]
NOTES['B008']['possible_joins']=[[129,131]]
NOTES['B011']['writing_owner_unknown']=[32]
NOTES['B012']['neighbor'] += [29]
NOTES['B012']['writing_owner_unknown']=[24]

def write_notes():
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen(source_stage=True)
    write_json(D/'source_review_notes.json',dict(updated_at_utc=datetime.now(timezone.utc).isoformat(),status='In-progress source decisions, V3 labels concealed',rows=NOTES))

def contacts(row,boxes):
    from row_benchmark_guard_v5 import require_unfrozen
    require_unfrozen()
    r=next(x for x in read_json(D/'PLAN.json')['rows'] if x['row_id']==row)
    im=Image.open(OUT/r['native_source']).convert('RGB')
    for i,box in enumerate(boxes):
        p=im.crop(box);p=p.resize((p.width*4,p.height*4));can=Image.new('RGB',(p.width,p.height+25),'white');can.paste(p,(0,25));ImageDraw.Draw(can).text((3,3),f'{row} native {box}',fill='black');can.save(G/f'{row}_contact_{i+1:02d}.png')

if __name__=='__main__':
    write_notes();contacts('B001',[[403,480,490,625],[628,473,723,619],[1172,548,1240,630],[505,517,600,760]])
