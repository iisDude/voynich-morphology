"""Read-only source inventory. All output stays below this project directory."""
from pathlib import Path
import csv
import hashlib
import json
import zipfile
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "voynich-groundup"


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main():
    for directory in ["data/source", "data/page_images", "data/crops",
                      "data/observations", "data/transcriptions", "data/controls",
                      "notebooks", "reports", "figures", "tests"]:
        (OUT / directory).mkdir(parents=True, exist_ok=True)
    files = []
    archives = []
    # The initial evidence consists of regular files at the project root.
    # Derived output, including this script, is deliberately excluded.
    for path in sorted(ROOT.iterdir(), key=lambda p: p.name.casefold()):
        if not path.is_file():
            continue
        files.append(dict(path=path.name, bytes=path.stat().st_size,
                          sha256=sha256(path)))
        if zipfile.is_zipfile(path):
            with zipfile.ZipFile(path) as z:
                for member in z.infolist():
                    archives.append(dict(archive=path.name, member=member.filename,
                                         bytes=member.file_size,
                                         compressed_bytes=member.compress_size,
                                         crc32=f"{member.CRC:08x}",
                                         is_directory=member.is_dir()))
    write_csv(OUT / "data/source/evidence_manifest.csv", files,
              ["path", "bytes", "sha256"])
    write_csv(OUT / "data/source/archive_members.csv", archives,
              ["archive", "member", "bytes", "compressed_bytes", "crc32", "is_directory"])
    reader = PdfReader(ROOT / "Voynich-Manuscript_all_Pages.pdf")
    pages = []
    images = []
    for index, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        lines = [s.strip() for s in text.splitlines() if s.strip()]
        image_id = next((s.split(":", 1)[1].strip() for s in lines
                         if s.startswith("Image ID:")), "")
        label = lines[0] if index else "Yale catalogue cover sheet"
        pages.append(dict(pdf_page=index + 1, pdf_index=index,
                          caption=label, yale_image_id=image_id,
                          width_pt=float(page.mediabox.width),
                          height_pt=float(page.mediabox.height),
                          rotation=int(page.get("/Rotate", 0)),
                          mapping_basis="embedded PDF caption"))
        objects = page.get("/Resources", {}).get("/XObject", {})
        objects = objects.get_object() if hasattr(objects, "get_object") else objects
        for name, ref in objects.items():
            obj = ref.get_object()
            if obj.get("/Subtype") != "/Image":
                raise ValueError(f"Uninspected nested XObject on page {index + 1}: {name}")
            images.append(dict(pdf_page=index + 1, object_name=name,
                               width_px=int(obj["/Width"]), height_px=int(obj["/Height"]),
                               bits_per_component=obj.get("/BitsPerComponent"),
                               color_space=str(obj.get("/ColorSpace")),
                               filters=str(obj.get("/Filter"))))
    write_csv(OUT / "data/source/page_folio_map.csv", pages, list(pages[0]))
    write_csv(OUT / "data/source/pdf_image_inventory.csv", images, list(images[0]))
    metadata = {str(k): str(v) for k, v in (reader.metadata or {}).items()}
    (OUT / "data/source/pdf_metadata.json").write_text(
        json.dumps(dict(metadata=metadata, page_count=len(pages),
                        page_labels=reader.page_labels, catalogue_text=reader.pages[0].extract_text()),
                   indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(dict(source_files=len(files), archive_members=len(archives),
                          pages=len(pages), images=len(images),
                          image_dimensions=sorted(set((p["width_px"], p["height_px"]) for p in images))),
                     indent=2))


if __name__ == "__main__":
    main()
