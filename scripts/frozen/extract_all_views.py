"""Native extraction and deterministic folio-connected splits; no corpus reads."""
from common import ROOT, OUT, SEED, read_csv, write_csv, write_json, sha256
import hashlib
import io
import re
from PIL import Image, ImageDraw
from pypdf import PdfReader


def main():
    source = ROOT / "Voynich-Manuscript_all_Pages.pdf"
    reader = PdfReader(source)
    captions = read_csv(OUT / "data/source/page_folio_map.csv")
    pilot = read_csv(OUT / "data/source/sample_manifest.csv")
    calibration_pages = {int(r["pdf_page"]) for r in pilot}
    # Union folio numbers mentioned in combined captions so they cannot split.
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    for row in captions:
        numbers = re.findall(r"(\d+)[rv]", row["caption"])
        for n in numbers:
            find(n)
        for n in numbers[1:]:
            parent[find(n)] = find(numbers[0])
    calibration_roots = set()
    for row in captions:
        if int(row["pdf_page"]) in calibration_pages:
            calibration_roots.update(find(n) for n in re.findall(r"(\d+)[rv]", row["caption"]))
    records = []
    thumb_tiles = []
    contact_dir = OUT / "figures/page_inventory"
    contact_dir.mkdir(parents=True, exist_ok=True)
    for row, page in zip(captions, reader.pages):
        number = int(row["pdf_page"])
        if number == 1:
            continue
        view_id = f"V_{number:03d}"
        path = OUT / f"data/page_images/all/{view_id}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        im = Image.open(io.BytesIO(list(page.images)[0].data)).convert("RGB")
        im.save(path)
        nums = re.findall(r"(\d+)[rv]", row["caption"])
        folio_component = find(nums[0]) if nums else None
        h = hashlib.sha256(f"{SEED}:{folio_component}".encode()).digest()[0] % 5
        split = ("excluded_cover" if not nums else "calibration" if folio_component in calibration_roots
                 else "validation" if h == 0 else "test" if h == 1 else "train")
        records.append(dict(view_id=view_id, pdf_page=number, caption=row["caption"],
                            yale_image_id=row["yale_image_id"],
                            folio_component=folio_component, split=split,
                            image_path=path.relative_to(OUT).as_posix(),
                            image_sha256=sha256(path), width_px=im.width, height_px=im.height,
                            panel_mapping="caption_only; multiple visible panels may occur"))
        tile = Image.new("RGB", (310, 420), "white")
        thumb = im.copy()
        thumb.thumbnail((300, 385))
        tile.paste(thumb, ((310 - thumb.width) // 2, 30))
        ImageDraw.Draw(tile).text((5, 5), f"{view_id} {row['caption']}", fill="black")
        thumb_tiles.append(tile)
        if len(thumb_tiles) == 16 or number == len(reader.pages):
            sheet = Image.new("RGB", (1240, 1680), "#dddddd")
            for i, tile in enumerate(thumb_tiles):
                sheet.paste(tile, ((i % 4) * 310, (i // 4) * 420))
            sheet.save(contact_dir / f"views_through_{number:03d}.png")
            thumb_tiles = []
        if number % 25 == 0:
            print(f"Extracted through PDF view {number}", flush=True)
    write_csv(OUT / "data/source/all_view_manifest.csv", records)
    write_json(OUT / "data/source/visual_split_manifest.json", dict(
        seed=SEED, source_pdf_sha256=sha256(source),
        unit="connected components of folio numbers from embedded captions; all sides/views kept together",
        calibration="All folios touched by twelve-view pilot removed from formal train/validation/test",
        train_fraction_of_noncalibration="3/5 hash buckets", validation_fraction="1/5", test_fraction="1/5",
        caveat="Caption grouping does not prove complete panel-level or bifolio independence.",
        counts={s: sum(r["split"] == s for r in records) for s in sorted({r["split"] for r in records})}))
    print("All views extracted and hashed.", flush=True)


if __name__ == "__main__":
    main()
