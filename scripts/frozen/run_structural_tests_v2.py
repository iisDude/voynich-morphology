"""Versioned post-freeze inputs for the unchanged registered assay functions."""
from common import OUT,read_json,write_json,sha256
import run_structural_tests as registered
import sys

def input_path(name):
    if name in ('ZL_EVA','RF','v101'):return OUT/f'data/comparisons/v2/{name}_groups_with_metadata.json'
    if name in ('Finnish','Turkish','Latin'):return OUT/f'data/controls/{name.lower()}_groups_with_context.json'
    return OUT/'data/comparisons/v2/visual_groups_with_metadata.json'

def load(name):
    rows=read_json(input_path(name))
    if name in ('ZL_EVA','RF','v101'):return [r for r in rows if r.get('units') and r.get('locus_kind')=='P']
    if name in ('Finnish','Turkish','Latin'):return rows
    field={'visual_fine':'visual_fine_units','visual_merged':'visual_merged_units','visual_factored':'visual_factored_units','visual_medium':'primary_candidate_units'}[name]
    return [dict(r,units=r[field]) for r in rows if r.get(field)]

def main():
    registered.load=load;registered.main()
    name=sys.argv[sys.argv.index('--dataset')+1];root=OUT/'tests/structural'/name
    manifest=read_json(root/'input_manifest.json');path=input_path(name)
    manifest.update(source_path=path.relative_to(OUT).as_posix(),source_sha256=sha256(path),runner_version=2,
        assay_source_sha256=sha256(OUT/'src/structural_assays.py'),parser_source_sha256=sha256(OUT/'src/parse_comparison_transcriptions_v2.py'),
        inherited_metadata='Post-freeze comparison fields; no visual units changed.',
        comparison_dependence='RF derived from ZL and GC; correlated measurement systems, not independent witnesses.')
    write_json(root/'input_manifest.json',manifest)
    (root/'run.py').write_text(f'from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[3]/"src"))\nsys.argv=[sys.argv[0],"--dataset","{name}"]\nfrom run_structural_tests_v2 import main\nmain()\n',encoding='utf-8')

if __name__=='__main__':main()
