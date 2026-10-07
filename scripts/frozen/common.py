"""Project-confined paths, deterministic data helpers, local scientific runtime."""
from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "voynich-groundup"
LOCAL_PACKAGES = OUT / ".tools/python"
if LOCAL_PACKAGES.exists():
    sys.path.insert(0, str(LOCAL_PACKAGES))
sys.dont_write_bytecode = True
os.environ.setdefault("MPLCONFIGDIR", str(OUT / ".tools/matplotlib"))
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")

import csv
import hashlib
import json

SEED = 20261005


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path, value):
    path = Path(path)
    if not path.resolve().is_relative_to(ROOT):
        raise ValueError("Output would escape Voynich Project")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv(path):
    with Path(path).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields=None):
    rows = list(rows)
    path = Path(path)
    if not path.resolve().is_relative_to(ROOT):
        raise ValueError("Output would escape Voynich Project")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fields or list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
