"""Verify source integrity, coordinate dimensions, and native sample pixels."""
from pathlib import Path
import csv
import hashlib
import io
import json
import platform
import sys
from PIL import Image
import PIL
import pypdf
from pypdf import PdfReader
try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator = None

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "voynich-groundup"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def rows(name):
    with (OUT / "data/source" / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    manifest = rows("evidence_manifest.csv")
    for row in manifest:
        assert digest((ROOT / row["path"]).read_bytes()) == row["sha256"], row["path"]
    initial = rows("evidence_manifest_initial.csv")
    current_hashes = {r["path"]: r["sha256"] for r in manifest}
    assert all(current_hashes[r["path"]] == r["sha256"] for r in initial)
    reader = PdfReader(ROOT / "Voynich-Manuscript_all_Pages.pdf")
    page_map = rows("page_folio_map.csv")
    assert len(page_map) == len(reader.pages) == 214
    assert [int(p["pdf_page"]) for p in page_map] == list(range(1, 215))
    sample = rows("sample_manifest.csv")
    for row in sample:
        native = list(reader.pages[int(row["pdf_page"]) - 1].images)[0]
        im = Image.open(io.BytesIO(native.data)).convert("RGB")
        exported = Image.open(OUT / row["png_path"]).convert("RGB")
        assert im.size == exported.size == (int(row["width_px"]), int(row["height_px"]))
        assert im.tobytes() == exported.tobytes(), row["blind_page_id"]
        assert digest(im.tobytes()) == row["decoded_rgb_sha256"]
        assert digest((OUT / row["png_path"]).read_bytes()) == row["png_sha256"]
        assert digest((OUT / row["native_path"]).read_bytes()) == row["native_file_sha256"]
        assert (OUT / row["png_path"]).resolve().is_relative_to(ROOT)
    schema = json.loads((OUT / "data/observations/annotation_schema.json").read_text(encoding="utf-8"))
    template = json.loads((OUT / "data/observations/annotation_template.json").read_text(encoding="utf-8"))
    if Draft202012Validator is not None:
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(template)
        schema_status = "Draft 2020-12 valid; empty scaffold conforms"
    else:
        # Limited, explicit checks; do not claim full JSON Schema validation.
        assert set(schema["required"]) <= set(template)
        assert set(template) <= set(schema["properties"])
        assert template["schema_version"] == schema["properties"]["schema_version"]["const"]
        assert template["status"] in schema["properties"]["status"]["enum"]
        assert set(schema["properties"]["provenance"]["required"]) <= set(template["provenance"])
        assert all(isinstance(template[k], list) for k in schema["properties"]
                   if schema["properties"][k].get("type") == "array")
        def check_refs(node):
            if isinstance(node, dict):
                if "$ref" in node:
                    ref = node["$ref"]
                    assert ref.startswith("#/$defs/") and ref.split("/")[-1] in schema["$defs"]
                for value in node.values():
                    check_refs(value)
            elif isinstance(node, list):
                for value in node:
                    check_refs(value)
        check_refs(schema)
        schema_status = "JSON parses; local schema references and scaffold keys checked; full validator unavailable"
    images = rows("pdf_image_inventory.csv")
    assert len(images) == 214
    assert all(max(int(r["width_px"]), int(r["height_px"])) == 2000 for r in images if int(r["pdf_page"]) > 1)
    result = dict(status="passed", source_files_verified=len(manifest),
                  initial_source_files_unchanged=len(initial), pdf_pages_mapped=len(page_map),
                  sample_images_pixel_verified=len(sample),
                  discovery_views=sum(r["split"] == "discovery" for r in sample),
                  reserve_views=sum(r["split"] == "reserve" for r in sample),
                  schema_structure=schema_status,
                  limitation="No annotation referential-integrity or scientific hypothesis tests have run.")
    (OUT / "reports/setup_verification.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    runtime = dict(python=platform.python_version(), executable=sys.executable,
                   pypdf=pypdf.__version__, Pillow=PIL.__version__)
    (OUT / "data/source/runtime_manifest.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")
    # Human-readable inventory; source hashes are generated rather than copied by hand.
    table = "\n".join(f"| `{r['path']}` | {int(r['bytes']):,} | `{r['sha256']}` |" for r in manifest)
    report = f"""# Evidence inventory v0

Date: 2026-10-05. All work products reside under the Voynich Project folder. No source evidence was modified. Verification rehashed all {len(manifest)} current root files and confirmed the original {len(initial)} files remain identical to the initial snapshot.

## Files and hashes

| Exact filename | Bytes | SHA-256 |
|---|---:|---|
{table}

Machine-readable records: `../data/source/evidence_manifest.csv`. The thirteen-file inventory recorded before the test ledger arrived is retained as `evidence_manifest_initial.csv`. The ZL filename actually present ends in `ZL3b-.txt`; the handoff/ledger's `ZL3b-(1).txt` is not a second local file.

## Evidence roles and provenance

- `Voynich-Manuscript_all_Pages.pdf`: primary local visual evidence. Its embedded Yale catalogue sheet gives title "Cipher manuscript", Beinecke MS 408, and Yale catalogue URL `https://collections.library.yale.edu/catalog/2002046`. PDF creation metadata and embedded generation text date this export to 2026-08-17. This is file provenance, not a new external-source verification or historical dating conclusion.
- ZL3b, RF1b, and GC2a: comparison transcriptions identified by the handoff/ledger. Contents have not been used for the initial visual segmentation. Exact upstream versions and transcription dependence are pending review.
- Three UD ZIPs: natural-language comparison corpora, retained compressed. Archive names and internal roots identify Finnish TDT, Turkish IMST, and Latin PROIEL. Exact upstream commits are not verified.
- `voynich-main.zip`: 344 archive entries. Its root README describes a statistical/generative project derived from dbourdeau/cyphersolver. Strong claims in that README have not been endorsed, audited, or reproduced here.
- `Voynich-public-main.zip`: 1,857 archive entries. Its root README describes a multiscale structural/generative research project with unresolved semantics. It contains third-party code and reports; its connection to the Yoshida work named in the chat remains to be verified from attribution/provenance files.
- Three saved chat files, handoff, and test ledger: provenance/instructions. The handoff, second chat, and test ledger were read fully. The two older chat files were inventoried but not yet read in full. Reported numerical results remain reported until a reproducible rerun exists.

All five ZIPs have been listed without extracting or executing their code: 2,231 entries including directory entries; each UD archive has ten entries. `archive_members.csv` preserves names, uncompressed/compressed sizes, and CRC32. CRC32 is not an independent cryptographic member hash; SHA-256 identifies each whole archive.

## PDF readability, mapping, and image resolution

The PDF is unencrypted, version 1.4, with 214 letter-sized pages (612 × 792 points), no outlines, and numeric PDF page labels. Its structure, caption text, and all page image descriptors were read successfully. This is structural readability, not visual verification of every manuscript page.

Each page contains one directly embedded image. Page 1 is a catalogue sheet with a 120 × 120 image. The other 213 image views, including covers, have a longest edge of 2,000 pixels. Tall views are up to 2,000 pixels high; wide unfolded views are up to 2,000 pixels wide and can have substantially fewer vertical pixels. The PDF canvas size does not determine the original manuscript scale or a trustworthy manuscript DPI.

`page_folio_map.csv` gives one-based PDF page, zero-based index, exact embedded caption, Yale image ID, canvas dimensions, and rotation for every page. Example: PDF page 4 → caption `1r`, Yale image ID `1006076`; page 127 → `69v and 70r`. Repeated/combined captions and multi-panel imagery require a separate panel mapping. Caption extraction is complete; physical-panel mapping is not.

`pdf_image_inventory.csv` gives embedded pixel dimensions, filters, color spaces, and component depth. Twelve selected views have been decoded at native size into PNG and saved with their native extracted image data. Verification compared every exported sample PNG's RGB pixels with a fresh PDF image decode: all twelve match. Their hashes and coordinate frames are in `sample_manifest.csv`.

## Visual quality and limitations

Six discovery views were visually inspected on a contact sheet; a native-size text crop from B_001 was also inspected. Recurring broad shapes and whitespace can be examined. Fine joins, touching strokes, and stroke order can be unresolved at this source resolution, particularly for small writing and foldouts. Enlarging a PNG cannot recover absent detail.

No loose higher-resolution Yale scans were found at the project root. Archives include other illustrations/PDFs; these have not all been inspected for primary manuscript scan content. Do not infer that no better local or online source exists. Any later higher-resolution acquisition must be separately hashed and registered, with a mapping to the present views.

No local AGENTS.md was found. The folder is not currently a Git repository. Source files remain at the root; derived output is isolated in `voynich-groundup/`. `runtime_manifest.json` records the bundled Python and library versions used. Schema verification: {schema_status}. No downloads, source modifications, OCR assignments, corpus assays, crosswalks, or decipherment were performed.

## Next gate

Review the neutral schema and the twelve-view proposal. Annotate the six discovery views with competing boundaries, then freeze candidate segmentation and provenance before mapping it to transcriptions. The ledger's ordinal token-rank endpoint must be reproduced explicitly; measured pixel position is a separate endpoint. Dependence-aware uncertainty and null design remain required, not already satisfied.
"""
    (OUT / "reports/00_evidence_inventory.md").write_text(report, encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
