"""Ledger-declared compound encodings, confined to post-freeze EVA comparisons."""
from common import OUT,write_json,write_csv,sha256,SEED
from run_structural_tests_v2 import load,input_path
from conventional_crossgraph_v0 import collapse
from structural_assays import pair_assay

def main():
    root=OUT/'tests/compound_stress_v1';root.mkdir(parents=True,exist_ok=True);rows=load('ZL_EVA');results=[]
    for name,spans in [('conservative_compounds',['cth','ckh','cph','cfh','iin','ch','sh','in']),('conservative_plus_ee',['cth','ckh','cph','cfh','iin','ch','sh','in','ee'])]:
        spans=sorted(spans,key=lambda s:(-len(s),s))
        transformed=[dict(r,units=collapse(r['units'],spans)) for r in rows]
        for currier in ('A','B'):
            result,pairs=pair_assay([r for r in transformed if r.get('currier')==currier],'normalized_group_rank',8,2,5,199)
            result.update(partition=name,currier=currier,compound_sequences=spans);results.append(result)
            write_json(root/f'pairs_{name}_{currier}.json',pairs);print(name,currier,result['pairs'],result.get('beta'),flush=True)
    write_json(root/'results.json',results);write_csv(root/'results.csv',[dict(partition=r['partition'],currier=r['currier'],pairs=r['pairs'],status=r['status'],beta=r.get('beta'),caption_ci=r.get('folio_bootstrap'),theme=r.get('theme')) for r in results])
    write_json(root/'config.json',dict(seed=SEED,frequency=8,edge_width=2,length_min=5,iterations=199,prior_art='Ledger 17 analogue; longest-match conventional reencoding only; no claim that these are visual graphemes. Historical exact parser/threshold settings unavailable.'))
    write_json(root/'input_manifest.json',dict(source_path=input_path('ZL_EVA').relative_to(OUT).as_posix(),sha256=sha256(input_path('ZL_EVA')),script_sha256=sha256(OUT/'src/complete_compound_stress_v1.py')))
    (root/'run.py').write_text('from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]/"src"))\nfrom complete_compound_stress_v1 import main\nmain()\n',encoding='utf-8')
    (root/'summary.md').write_text('# Additional ledger compound stress\n\nBench sequences, iin/in and optional ee are collapsed by declared longest match in EVA comparison strings. Primary thresholds are applied after reencoding. Rank is preserved; pixel positions unknown. Full negative, ambiguous and non-estimable outcomes retained. This cannot validate writing units.\n',encoding='utf-8')

if __name__=='__main__':main()
