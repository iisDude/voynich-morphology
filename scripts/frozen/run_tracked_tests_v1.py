"""Run unchanged registered tests on the second frozen source candidate copy."""
from common import OUT,read_json,write_json,sha256
import run_structural_tests as structural
import context_assays_v0 as context
import finish_depth_order_repetition_v1 as depth
import hmm_transfer_v0 as hmm
import sys

def input_path(name):return OUT/'data/comparisons/v11/visual_groups_with_metadata.json'

def load(name):
    field={'visual_v11_fine':'visual_fine_units','visual_v11_merged':'visual_merged_units','visual_v11_factored':'visual_factored_units','visual_v11_medium':'primary_candidate_units'}[name]
    return [dict(r,units=r[field]) for r in read_json(input_path(name)) if r.get(field)]

def main():
    mode=sys.argv[1];sys.argv.pop(1);name=sys.argv[sys.argv.index('--dataset')+1]
    runner={'structural':structural,'context':context,'depth':depth,'hmm':hmm}[mode]
    runner.load=load
    if hasattr(runner,'input_path'):runner.input_path=input_path
    runner.main()
    root=OUT/({'structural':'tests/structural','context':'tests/context','depth':'tests/depth_order_repetition','hmm':'tests/hmm_transfer'}[mode])/name
    manifest=read_json(root/'input_manifest.json');manifest.update(path=input_path(name).relative_to(OUT).as_posix(),source_path=input_path(name).relative_to(OUT).as_posix(),sha256=sha256(input_path(name)),source_sha256=sha256(input_path(name)),visual_freeze_sha256=sha256(OUT/'data/observations/visual_dataset_v11/FREEZE_MANIFEST.json'),original_visual_freeze_sha256=sha256(OUT/'data/observations/visual_dataset_v0/FREEZE_MANIFEST.json'),runner_sha256=sha256(OUT/'src/run_tracked_tests_v1.py'),exposure='Source-only second repair after conventional/statistical exposure; diagnostic test set, not a new blind confirmation.')
    write_json(root/'input_manifest.json',manifest)
    (root/'run.py').write_text(f'from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[3]/"src"))\nsys.argv=[sys.argv[0],"{mode}","--dataset","{name}"]\nfrom run_tracked_tests_v1 import main\nmain()\n',encoding='utf-8')

if __name__=='__main__':main()
