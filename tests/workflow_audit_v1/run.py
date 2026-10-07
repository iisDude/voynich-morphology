from pathlib import Path
import subprocess, sys
base = Path(__file__).resolve().parents[2]
for script in ["verify_completed_workflow_v1.py", "render_workflow_audit_v1.py"]:
    subprocess.run([sys.executable, str(base / "src" / script)], check=True)
