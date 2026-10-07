"""Source-only field triage and first anonymous native-context judgments."""
from common import OUT,read_json,write_json,sha256
from register_sequence_v4 import D,T
from PIL import Image
from datetime import datetime,timezone
# Fractions of actual native-source overview width, not the six-up canvas.
FIELDS={7:(.25,.57),9:(.17,.55),12:(.18,.74),13:(.23,.77),16:(.20,.45),17:(.24,.47),20:(.17,.53),21:(.16,.44),23:(.34,.80),24:(.14,.63),25:(.30,.85),26:(.20,.42),27:(.31,.50),29:(.25,.82),31:(.34,.58),32:(.14,.43),33:(.20,.44),34:(.16,.40),37:(.53,.89),38:(.16,.40),39:(.33,.62),41:(.30,.57),42:(.15,.69),43:(.33,.67),44:(.12,.40),46:(.12,.27),47:(.30,.52),48:(.23,.40),49:(.23,.39),50:(.18,.68),51:(.31,.78),55:(.35,.45),57:(.34,.80),58:(.13,.38),59:(.28,.49),60:(.15,.42),61:(.28,.69),62:(.13,.43),63:(.25,.85),65:(.28,.57),66:(.15,.71),67:(.25,.38),68:(.13,.28),69:(.28,.83),72:(.12,.37),74:(.16,.41),76:(.60,.80),77:(.30,.60),78:(.11,.55),79:(.24,.85),88:(.18,.50),90:(.12,.50),91:(.28,.52),92:(.13,.72),93:(.22,.75),94:(.14,.47),95:(.30,.52),96:(.13,.78),100:(.15,.74),101:(.30,.58),103:(.34,.58),104:(.15,.70),105:(.33,.53),106:(.13,.35),107:(.32,.66),108:(.14,.57),109:(.27,.47),110:(.14,.73),111:(.30,.49),112:(.13,.40),113:(.30,.61),114:(.11,.40),119:(.33,.46),121:(.33,.86),148:(.20,.64),149:(.34,.82),153:(.32,.72),155:(.30,.53),160:(.17,.45),161:(.30,.55),169:(.33,.53),170:(.17,.43),171:(0.,1.),172:(.27,.85),173:(.22,.80),174:(.15,.35),175:(.23,.45),178:(.16,.55),180:(.22,.82),181:(0.,1.),182:(.24,.54),183:(.32,.75),191:(.23,.86),194:(.15,.84),197:(.23,.85),201:(.25,.83),203:(.23,.87),204:(.14,.85),205:(.22,.86),207:(.18,.82)}
EXCLUDE={27:[6],79:[9],149:[24],160:[14],182:[1,2,3,7,8,9,10],183:[7],203:[1],204:[1],205:[1]}
NOTES={171:'Wide capture: three separate horizontal blocks. Each proposal retains its own x field; physical panel identity and reading order unknown.',181:'Wide capture with three horizontal blocks; proposal-specific fields, panel identity unknown.',119:'Split writing fields separated by green stalk; retain narrow left field, other side unknown.',148:'Main block between painted bathing figures; margins/drawing contacts withheld.',149:'Main block above painted figures; bottom drawing proposal excluded.',155:'Left block retained; right labels and lower painted basin contacts withheld.',182:'Foldout with plants crossing several proposals; drawing/interrupted fields excluded; panel mapping unknown.'}
def main():
    if (D/'ordinary_source_reviews.json').exists():raise RuntimeError('Recorded already')
    records=[]
    for v in read_json(D/'PLAN.json')['selected_views']:
        n=int(v['view_id'][2:]);f=FIELDS[n];w=Image.open(OUT/v['native_source']).width
        records.append(dict(view_id=v['view_id'],safe_x=[round(f[0]*w),round(f[1]*w)],exclude_rows=EXCLUDE.get(n,[]),reviewed_row_numbers=list(range(1,len(v['rows'])+1)),review_level='overview_field_triage',complete_physical_line=False,complete_ink_recall_certified=False,note=NOTES.get(n,'Conservative local horizontal writing field; drawing and margins withheld. Native faint/ownership ambiguity requires separate review.'),panel_mapping='unknown' if n in [171,181,182] else 'capture_only'))
    write_json(D/'ordinary_source_reviews.json',records)
    # Image-only first pass. Context may contain adjacent rows; that alone is not ownership evidence.
    drawing=['right','central','right','margin_star','central','right','none','none','none','margin_star','margin','right','central','central','none','edge','margin_star','right','edge','right','margin_star','none','margin_star','right']
    rows=[2,1,2,3,3,3,4,3,2,4,5,2,3,4,3,4,4,3,2,3,4,2,4,3]
    # Narrow gaps, detached arches, joined tall/lower traces remain unresolved, not forced boundaries.
    judgments=[dict(id=f'A{i+1:03d}',drawing_contact_region=drawing[i],visible_body_rows=rows[i],boundary_interpretation='clear_large_gaps_and_competing_narrow_gaps',detached_ownership='unknown',connected_parent_splitting='not_justified_by_source',faint_ink='unknown' if i in [1,18,21] else 'locally_visible',class_suggestion_shown=False,previous_boundary_shown=False) for i in range(24)]
    write_json(D/'masked_context_judgments_A.json',dict(recorded_at_utc=datetime.now(timezone.utc).isoformat(),judgments=judgments,method='Direct inspection of four anonymous native RGB sheets; whole-context descriptors, not complete parent-by-parent adjudication or class accuracy.'))
    write_json(D/'SOURCE_PROTOCOL_SEAL.json',dict(sealed_at_utc=datetime.now(timezone.utc).isoformat(),plan_sha256=sha256(D/'PLAN.json'),reviews_sha256=sha256(D/'ordinary_source_reviews.json'),repeat_pass_A_sha256=sha256(D/'masked_context_judgments_A.json'),v3_model_sha256=read_json(D/'PLAN.json')['v3_model_sha256'],new_class_results_not_yet_computed=True))
    print(len(records),'source fields reviewed; pass A saved; protocol sealed',flush=True)
if __name__=='__main__':main()
