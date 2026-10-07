"""Acquire public higher-resolution Yale captures registered by PDF image ID."""
from common import OUT, read_csv, write_csv, write_json, sha256
import argparse
import concurrent.futures
import json
import urllib.request
from PIL import Image
import io


def acquire(row):
    image_id = row["yale_image_id"]
    service = f"https://collections.library.yale.edu/iiif/2/{image_id}"
    headers = {"User-Agent": "Voynich image-structure investigation; public IIIF images"}
    folder = OUT / "data/source/yale_native"
    folder.mkdir(parents=True, exist_ok=True)
    info_path = folder / f"{image_id}_info.json"
    path = folder / f"{image_id}.jpg"
    try:
        if info_path.exists():
            info = json.loads(info_path.read_text(encoding="utf-8"))
        else:
            with urllib.request.urlopen(urllib.request.Request(service + "/info.json", headers=headers), timeout=35) as response:
                info = json.load(response)
            write_json(info_path, info)
        service = info.get("@id", service)
        url = service + "/full/full/0/default.jpg"
        if not path.exists():
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as response:
                data = response.read()
            image = Image.open(io.BytesIO(data))
            if image.size != (info["width"], info["height"]):
                raise ValueError(f"IIIF native-size mismatch: {image.size}")
            path.write_bytes(data)
        with Image.open(path) as image:
            width, height = image.size
        result = dict(view_id=row["view_id"], yale_image_id=image_id, url=url,
                      path=path.relative_to(OUT).as_posix(), sha256=sha256(path),
                      width_px=width, height_px=height, pdf_width_px=int(row["width_px"]),
                      pdf_height_px=int(row["height_px"]),
                      nominal_scale_x=width / int(row["width_px"]), nominal_scale_y=height / int(row["height_px"]),
                      registration_status="nominal scaling only; pixel alignment needs verification",
                      status="downloaded")
        print(f"{row['view_id']}: Yale native {width}x{height}", flush=True)
        return result
    except Exception as error:
        print(f"{row['view_id']}: source acquisition failed: {error}", flush=True)
        return dict(view_id=row["view_id"], yale_image_id=image_id, url=service,
                    path="", sha256="", width_px="", height_px="", pdf_width_px=row["width_px"],
                    pdf_height_px=row["height_px"], nominal_scale_x="", nominal_scale_y="",
                    registration_status="unavailable", status=str(error))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", choices=["pilot", "all"], default="pilot")
    ap.add_argument("--workers", type=int, default=2)
    args = ap.parse_args()
    rows = read_csv(OUT / "data/source/all_view_manifest.csv")
    if args.scope == "pilot":
        numbers = {int(r["pdf_page"]) for r in read_csv(OUT / "data/source/sample_manifest.csv")}
        rows = [r for r in rows if int(r["pdf_page"]) in numbers]
    else:
        rows = [r for r in rows if r["split"] != "excluded_cover"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = list(executor.map(acquire, rows))
    write_csv(OUT / f"data/source/yale_native_{args.scope}_manifest.csv", results)


if __name__ == "__main__":
    main()
