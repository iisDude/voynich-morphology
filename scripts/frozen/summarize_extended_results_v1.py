"""Compact read-only extraction of saved outcomes for final research synthesis."""
from common import OUT,read_json,write_json
from collections import Counter

def main():
    result={}
    for name in ['ZL_EVA','RF','v101','visual_fine','visual_merged','visual_factored','visual_medium','Finnish','Turkish','Latin']:
        structural=OUT/'tests/structural'/name
        primary=[r for r in read_json(structural/'minimal_pair_results.json') if r['minimum_frequency']==8 and r['edge_width']==2 and r['length_min']==5 and not r.get('specification')]
        result[name]={'primary':[dict(subset=r['subset'],position=r['position'],pairs=r['pairs'],beta=r.get('beta'),bootstrap=r.get('folio_bootstrap'),null=r.get('within_line_null'),theme=r.get('theme'),leave_one_folio_out=r.get('leave_one_folio_out')) for r in primary]}
        c=read_json(OUT/f'tests/context/{name}/results.json')
        result[name]['context']=dict(same_hand=[r for r in c['same_hand_context'] if r['status']=='estimated'],broad_context=[r for r in c['context_prediction'] if r['status']=='estimated'],wrappers=c['wrappers'],compression=c['compression'],same_author_wrappers=c.get('same_author_Cicero_wrappers'),same_author_prediction=c.get('same_author_Cicero_prediction'))
        h=read_json(OUT/f'tests/hmm_transfer/{name}/results.json')
        result[name]['hmm']=[{k:v for k,v in r.items() if k not in ['document_scores','model_matrices','warnings']} for r in h]
        d=OUT/'tests/depth_order_repetition'/name
        result[name]['section_order_estimated']=[r for r in read_json(d/'section_order_results.json') if r['status'].startswith('estimated')]
        result[name]['ordinary_preferences']=read_json(d/'ordinary_preference_results.json')
    v=read_json(OUT/'tests/visual_family_stability_v1/results.json');context=v['context_geometry'];paired=v['within_caption_context']
    result['visual_stability']=dict(keys=list(v),samples=v['samples'],context_records=len(context),context_status=dict(Counter(r['status'] for r in context)),context_q05=[r for r in context if r.get('bh_q_exploratory',1)<.05],paired_records=len(paired),paired_status=dict(Counter(r['status'] for r in paired)))
    result['dependence']={name:read_json(OUT/'tests/dependence_boundaries'/name) for name in ['bifolio_split_audit.json','family_and_theme_results.json','purged_graph_results.json']}
    result['all_hand_hmm']=[{k:v for k,v in r.items() if k not in ['document_scores','model_matrices','warnings']} for r in read_json(OUT/'tests/hmm_transfer/ZL_EVA_all_hands/results.json')]
    write_json(OUT/'reports/extended_result_synthesis_v1.json',result)
    print('Saved extended synthesis',flush=True)
    print('Visual stability',result['visual_stability'],flush=True)

if __name__=='__main__':main()
