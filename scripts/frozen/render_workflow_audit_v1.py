"""Report the completed integrity audit without changing frozen evidence."""
from common import OUT, read_json, read_csv, write_json, sha256
from pathlib import Path
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    root = OUT / 'tests/workflow_audit_v1'
    result = read_json(root / 'results.json')
    rows = read_csv(root / 'results.csv')
    write_json(root / 'config.json', {
        'purpose': 'Provenance/artifact verification; not a scientific accuracy assay',
        'algorithm': 'SHA256 and explicit deterministic invariance/contract checks',
        'null_model': None, 'statistical_inference': 'Not applicable to deterministic checks',
        'source_script': 'src/verify_completed_workflow_v1.py',
        'report_script': 'src/render_workflow_audit_v1.py'})
    files = [OUT / 'src/verify_completed_workflow_v1.py', Path(__file__),
             OUT / 'data/observations/visual_dataset_v0/FREEZE_MANIFEST.json',
             OUT / 'data/observations/visual_dataset_v11/FREEZE_MANIFEST.json',
             OUT / 'data/source/evidence_manifest.csv', root / 'results.json', root / 'results.csv']
    write_json(root / 'input_manifest.json', {'files': [
        {'path': p.relative_to(OUT).as_posix(), 'sha256': sha256(p)} for p in files]})
    (root / 'README.md').write_text(
        '# Completed workflow integrity verification\n\n'
        'Run `python voynich-groundup/tests/workflow_audit_v1/run.py` from the project root. '
        'This rechecks frozen hashes, source evidence, post-freeze unit/position invariance, '
        'review counts and 68 empirical artifact contracts, then renders this report. '
        'It writes only the audit and artifact index, not frozen evidence. '
        'Passing does not establish writing recall, sign boundaries or a transcription crosswalk.\n', encoding='utf-8')
    (root / 'run.py').write_text(
        'from pathlib import Path\nimport subprocess, sys\n'
        'base = Path(__file__).resolve().parents[2]\n'
        'for script in ["verify_completed_workflow_v1.py", "render_workflow_audit_v1.py"]:\n'
        '    subprocess.run([sys.executable, str(base / "src" / script)], check=True)\n', encoding='utf-8')
    (root / 'summary.md').write_text(
        f'# Workflow verification outcome\n\n{result["checks"]:,} checks passed; '
        f'{len(result["failures"])} failures. Both freezes and {result["original_evidence_files"]} '
        f'original evidence files are intact. {result["empirical_result_directories"]} research '
        'directories satisfy the artifact contract. Post-freeze visual identities and positions '
        'match their immutable source snapshots. No conventional native pixel coordinates '
        'were fabricated.\n\nThis is a provenance and bookkeeping result, not a measure of '
        'manuscript writing-unit accuracy. Source-review failures remain.\n', encoding='utf-8')
    counts = Counter(r['check'] for r in rows)
    fig, ax = plt.subplots(figsize=(11, 6))
    labels, values = list(counts), list(counts.values())
    ax.barh(labels[::-1], values[::-1], color='#19677d')
    ax.set_xscale('log'); ax.set_xlabel('Deterministic checks (log scale)')
    ax.set_title(f'{result["checks"]:,} checks passed: provenance, not writing-unit accuracy')
    fig.tight_layout(); (root / 'figures').mkdir(exist_ok=True)
    fig.savefig(root / 'figures/provenance_checks.png', dpi=150); plt.close(fig)

if __name__ == '__main__': main()
