"""Extract native sample images without reading transcription content."""
from pathlib import Path
import csv
import hashlib
import io
import json
from PIL import Image, ImageDraw
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "voynich-groundup"
SAMPLE = [
    ("B_001", 4, "discovery", "early illustration and text"),
    ("B_002", 82, "discovery", "middle manuscript illustration and text"),
    ("B_003", 122, "discovery", "circular layout"),
    ("B_004", 136, "discovery", "figures and text"),
    ("B_005", 162, "discovery", "small illustrations and short groups"),
    ("B_006", 184, "discovery", "late dense text"),
    ("B_007", 52, "reserve", "early/middle text comparison"),
    ("B_008", 116, "reserve", "middle manuscript comparison"),
    ("B_009", 127, "reserve", "circular and combined caption comparison"),
    ("B_010", 150, "reserve", "figures and text comparison"),
    ("B_011", 176, "reserve", "small illustrations comparison"),
    ("B_012", 198, "reserve", "late dense text comparison"),
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    reader = PdfReader(ROOT / "Voynich-Manuscript_all_Pages.pdf")
    rows = []
    thumbnails = []
    for blind_id, page_number, split, rationale in SAMPLE:
        page = reader.pages[page_number - 1]
        images = list(page.images)
        if len(images) != 1:
            raise ValueError(f"Expected one image on PDF page {page_number}")
        source_image = images[0]
        im = Image.open(io.BytesIO(source_image.data)).convert("RGB")
        native_path = OUT / f"data/page_images/{blind_id}{Path(source_image.name).suffix}"
        png_path = OUT / f"data/page_images/{blind_id}.png"
        native_path.write_bytes(source_image.data)
        im.save(png_path)
        rows.append(dict(blind_page_id=blind_id, pdf_page=page_number,
                         split=split, selection_basis=rationale,
                         native_path=native_path.relative_to(OUT).as_posix(),
                         native_file_sha256=digest(source_image.data),
                         png_path=png_path.relative_to(OUT).as_posix(),
                         png_sha256=digest(png_path.read_bytes()),
                         decoded_rgb_sha256=digest(im.tobytes()),
                         width_px=im.width, height_px=im.height,
                         source_object_name=source_image.name,
                         coordinate_frame="decoded embedded image; top-left origin; x right; y down",
                         transforms="RGB decoding only; PNG export; no geometric transform"))
        # Reserve images are extracted but never displayed on the discovery sheet.
        if split == "discovery":
            thumb = im.copy()
            thumb.thumbnail((390, 490))
            tile = Image.new("RGB", (420, 540), "white")
            tile.paste(thumb, ((420 - thumb.width) // 2, 32))
            ImageDraw.Draw(tile).text((12, 8), blind_id, fill="black")
            thumbnails.append(tile)
    with (OUT / "data/source/sample_manifest.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    sheet = Image.new("RGB", (1260, 1080), "#dddddd")
    for index, tile in enumerate(thumbnails):
        sheet.paste(tile, ((index % 3) * 420, (index // 3) * 540))
    sheet.save(OUT / "figures/discovery_contact_sheet.png")
    # A source-coordinate quality check; this is not an annotated assembly crop.
    im = Image.open(OUT / "data/page_images/B_001.png")
    box = (140, 180, 1420, 600)
    im.crop(box).save(OUT / "figures/B_001_resolution_check.png")
    (OUT / "figures/B_001_resolution_check.json").write_text(json.dumps(
        dict(blind_page_id="B_001", bbox_xyxy=list(box),
             source_image="data/page_images/B_001.png", scale=1,
             purpose="image-quality check; no segmentation annotations"), indent=2), encoding="utf-8")
    print(f"Extracted {len(rows)} sample images; contact sheet contains six discovery pages only.")


if __name__ == "__main__":
    main()
