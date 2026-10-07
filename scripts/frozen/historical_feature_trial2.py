"""Historical reused-input sensitivity, never fresh validation or tuning."""
from feature_trial2_common import *
import numpy as np
from collections import Counter
def main():
    guard();verify_dependencies();spec=read_json(D/'PLAN.json');old=read_json(OUT/'data/observations/neutral_feature_trial_v1/parent_feature_profiles.json')['parents'];source={r['parent_id']:r for r in read_json(D/'source_decisions.json')['parents']};byid={r['parent_id']:r for r in read_json(OLD/'discovery_parents.json')+read_json(OLD/'fresh_source_reference.json')['parents']};rows=[]
    for r in old:
        body=byid[r['parent_id']]['body_proxy'];fields={};primary_cavity=r['features']['significant_cavity_count']['primary'];sr=source.get(r['parent_id']);cavity_ok=sr is not None and sr['source_cavity_count'] is not None and sr['source_cavity_count']==primary_cavity;up=r['features']['cavity_upper_count']['primary'];lo=r['features']['cavity_lower_count']['primary'];place='both' if up and lo else 'upper' if up else 'lower' if lo else 'none';position_ok=cavity_ok and sr['source_cavity_placement']==place
        for k,d in spec['features'].items():
            if k in ['log_height_native','log_width_native']:
                key='log_height_body' if k=='log_height_native' else 'log_width_body';values=[v+np.log(body*(.9 if j==5 else 1.1 if j==6 else 1)) if v is not None else None for j,v in enumerate(r['features'][key]['values'])]
            else:values=r['features'][k]['values']
            pp=[v for v in values if v is not None];status='not_applicable' if not pp else 'unknown_presence' if len(pp)!=len(values) else 'stable' if max(pp)-min(pp)<=d['range_tolerance']+1e-9 else 'unknown_variant_sensitive';qualified=status
            if d['family']=='cavity':
                if not cavity_ok:qualified='unknown_source_cavity'
                elif k not in ['significant_cavity_count','cavity_area_fraction'] and not position_ok:qualified='unknown_source_placement'
            fields[k]=dict(raster_status=status,source_qualified_status=qualified)
        stable=[k for k in spec['core_features'] if fields[k]['source_qualified_status']=='stable'];fam={spec['features'][k]['family'] for k in stable};ok=r['source_resolved'] and r['whole_parent_variant_correspondence'] and len(stable)>=8 and {'geometry','distribution'}<=fam and bool(fam&{'cavity','run'})
        rows.append(dict(parent_id=r['parent_id'],caption=r['caption'],source_resolved=r['source_resolved'],usable=ok,features=fields))
    save(T/'historical_reused_input_sensitivity.json',dict(parents=rows,n=len(rows),resolved_n=sum(r['source_resolved'] for r in rows),usable_n=sum(r['usable'] for r in rows),feature_stable={k:dict(raster=sum(r['features'][k]['raster_status']=='stable' for r in rows),source_qualified=sum(r['features'][k]['source_qualified_status']=='stable' for r in rows)) for k in spec['features']},source_audited_n=sum(r['parent_id'] in source for r in rows),method='Replay Trial1 seven variant values with sealed Trial2 dimensional tolerance/core feature rules. Native dimension recovered using matching body-reference multiplier. Source cavity qualification only where Trial2 audit exists; all other cavities unknown. No old class labels or sequence outcomes used. Historical source eligibility retained; this is reused data, not fresh validation.'))
    print('Historical sensitivity',sum(r['usable'] for r in rows),'/',sum(r['source_resolved'] for r in rows),flush=True)
if __name__=='__main__':main()
