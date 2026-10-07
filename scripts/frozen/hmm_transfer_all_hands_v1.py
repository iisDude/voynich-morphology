"""Explicitly confounded sensitivity after same-hand holdout coverage failure."""
from common import OUT,read_json,write_json,sha256
import hmm_transfer_v0 as registered
import sys

original_load=registered.load;original_input=registered.input_path
def underlying(name):return name.removesuffix('_all_hands')
def select(rows,name):
    return [dict(r,context=r['section']) for r in rows if r.get('currier')=='B' and r.get('section') in ('H','B')]

def main():
    registered.load=lambda name:original_load(underlying(name))
    registered.input_path=lambda name:original_input(underlying(name))
    registered.select=select;registered.main()
    name=sys.argv[sys.argv.index('--dataset')+1];root=OUT/'tests/hmm_transfer'/name
    config=read_json(root/'config.json');config.update(context='Currier B herbal versus biological across all recorded hands; explicitly confounded sensitivity',
        same_hand_status='Primary same-hand held-out comparison failed minimum block coverage and remains a separate non-estimable result.',
        limitation='Hand, layout, ink, date and subject are not isolated by this sensitivity. No state semantics or primary confirmation claimed.')
    write_json(root/'config.json',config)
    manifest=read_json(root/'input_manifest.json');manifest['sensitivity_runner_sha256']=sha256(OUT/'src/hmm_transfer_all_hands_v1.py');write_json(root/'input_manifest.json',manifest)
    (root/'run.py').write_text(f'from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[3]/"src"))\nsys.argv=[sys.argv[0],"--dataset","{name}"]\nfrom hmm_transfer_all_hands_v1 import main\nmain()\n',encoding='utf-8')

if __name__=='__main__':main()
