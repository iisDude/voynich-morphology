"""Image-only line/component proposals with reversible coordinate mappings."""
from common import OUT, read_csv, read_json, write_csv, write_json
import argparse
import numpy as np
import cv2
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
from PIL import Image, ImageDraw


def ink_mask(rgb, config, contrast=None):
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32)
    background = cv2.GaussianBlur(gray, (0, 0), config["background_gaussian_sigma_px"])
    r, g, b = [rgb[:, :, i].astype(np.int16) for i in range(3)]
    limits = config["color_limits"]
    color = ((r - g >= limits["r_minus_g_min"]) & (r - g <= limits["r_minus_g_max"])
             & (b - r <= limits["b_minus_r_max"]))
    return ((background - gray >= (contrast or config["primary_ink_contrast"])) & color).astype(np.uint8)


def components(mask, config):
    n, labels, stats, centers = cv2.connectedComponentsWithStats(mask, connectivity=8)
    h, w = mask.shape
    margin = config["page_margin_fraction"]
    result = []
    for i in range(1, n):
        x, y, width, height, area = map(int, stats[i])
        if not (config["component_area_px"][0] <= area <= config["component_area_px"][1]
                and config["component_height_px"][0] <= height <= config["component_height_px"][1]
                and config["component_width_px"][0] <= width <= config["component_width_px"][1]
                and margin * w < x < (1 - margin) * w
                and margin * h < y < (1 - margin) * h):
            continue
        result.append(dict(label=i, x0=x, y0=y, x1=x + width, y1=y + height,
                           width=width, height=height, area=area, cx=float(centers[i, 0]),
                           cy=float(centers[i, 1])))
    return labels, result


def detect_lines(mask, config):
    scale = config.get("geometry_scale", 1.)
    labels, cc = components(mask, config)
    if not cc:
        return [], cc, labels
    eligible = np.isin(labels, [c["label"] for c in cc]).astype(np.uint8)
    linked = cv2.dilate(eligible, np.ones((1, max(1, round(23 * scale))), np.uint8))
    segments = cv2.HoughLinesP(linked, 1, np.pi / 720, threshold=round(100 * scale),
                              minLineLength=round(180 * scale), maxLineGap=round(30 * scale))
    slopes = []
    if segments is not None:
        for segment in segments[:, 0, :]:
            xa, ya, xb, yb = segment
            if xb != xa and abs((yb - ya) / (xb - xa)) <= .08:
                slopes.append((yb - ya) / (xb - xa))
    slope = float(np.median(slopes)) if slopes else 0.
    xref = mask.shape[1] / 2
    votes = np.zeros(mask.shape[0], dtype=float)
    for c in cc:
        # Bottom-alignment proposals; no glyph inventory or OCR involved.
        y = round(c["y1"] - 1 - slope * (c["cx"] - xref))
        if 0 <= y < len(votes):
            votes[y] += c["area"] / (12 * scale)
    profile = gaussian_filter1d(votes, config["baseline_vote_sigma_px"])
    peaks, _ = find_peaks(profile, distance=config["baseline_peak_min_distance_px"],
                          prominence=max(8, profile.max() * .045))
    groups = {int(p): [] for p in peaks}
    for c in cc:
        if len(peaks) == 0:
            break
        corrected_y = c["y1"] - 1 - slope * (c["cx"] - xref)
        p = int(peaks[np.argmin(abs(peaks - corrected_y))])
        if abs(p - corrected_y) <= config["baseline_assignment_tolerance_px"]:
            groups[p].append(c)
    # Bottom votes only propose path locations. Recover membership from pixels
    # touching a core band, including larger connected constructions excluded
    # from baseline voting. Keep each raster component in at most one line.
    all_n, all_labels, all_stats, all_centers = cv2.connectedComponentsWithStats(mask, connectivity=8)
    expanded = []
    groups = {int(p): [] for p in peaks}
    scale_heights = [c["height"] for c in cc if 7 * scale <= c["height"] <= 35 * scale]
    core_height = float(np.percentile(scale_heights, 65)) if scale_heights else 14. * scale
    for i in range(1, all_n):
        x, y, width, height, area = map(int, all_stats[i])
        if not (area >= 12 * scale**2 and height >= 3 * scale and width >= 2 * scale
                and height <= config.get("recovery_height_px", 140 * scale)
                and width <= config.get("recovery_width_px", 280 * scale)
                and area <= config.get("recovery_area_px", 6500 * scale**2)):
            continue
        ys, xs = np.where(all_labels[y:y + height, x:x + width] == i)
        corrected = ys + y - slope * (xs + x - xref)
        scores = np.array([((corrected >= p - core_height) & (corrected <= p + 3 * scale)).sum() for p in peaks])
        if not len(scores) or scores.max() < 2 * scale**2:
            continue
        # A tall construction on the following line can have more upper-loop
        # ink in the preceding body band. Penalize distance of its lowest ink
        # from the baseline; retain explicit multi-line ambiguity below.
        corrected_bottom = y + height - 1 - slope * (all_centers[i, 0] - xref)
        assignment_scores = scores - 3 * scale * abs(peaks - corrected_bottom)
        assignment_scores[scores < 2 * scale**2] = -np.inf
        winner = int(assignment_scores.argmax())
        p = int(peaks[winner])
        c = dict(label=i, x0=x, y0=y, x1=x + width, y1=y + height,
                 width=width, height=height, area=area, cx=float(all_centers[i, 0]),
                 cy=float(all_centers[i, 1]), core_band_support_px=int(scores[winner]),
                 multiline_contact=bool((scores >= max(3 * scale**2, scores.max() * .3)).sum() > 1))
        groups[p].append(c)
        expanded.append(c)
    cc, labels = expanded, all_labels
    lines = []
    for peak, members in groups.items():
        members.sort(key=lambda c: c["x0"])
        runs = [[]]
        right = None
        for c in members:
            if right is not None and c["x0"] - right > config["line_horizontal_break_px"]:
                runs.append([])
            runs[-1].append(c)
            right = max(right or 0, c["x1"])
        for run in runs:
            if len(run) < config["minimum_line_component_count"]:
                continue
            major = [c for c in run if c["area"] >= 20 * scale**2 and c["height"] >= 5 * scale]
            if len(major) < config["minimum_line_component_count"]:
                continue
            x0, x1 = min(c["x0"] for c in major), max(c["x1"] for c in major)
            run = [c for c in run if x0 <= c["cx"] <= x1]
            if x1 - x0 < config["minimum_line_width_px"]:
                continue
            # Robust local body scale; deliberately a geometric estimate, not a class definition.
            anchored = [c for c in run if c['area'] >= 40 * scale**2 and c['height'] >= 8 * scale
                        and abs(c['y1']-1-slope*(c['cx']-xref)-peak) <= 12 * scale]
            heights = np.array([c["height"] for c in anchored])
            if len(heights) >= 4:
                weights = np.sqrt(np.array([c['area'] for c in anchored]))
                order = np.argsort(heights)
                body = float(heights[order][np.searchsorted(np.cumsum(weights[order]), weights.sum()*.5)])
            else:
                heights = np.array([c["height"] for c in run if c["height"] >= 7 * scale])
                body = float(np.median(heights[heights <= np.percentile(heights, 75)])) if len(heights) else 10. * scale
            ordinary = [c for c in run if .5 * body <= c["height"] <= 1.6 * body]
            baseline = float(np.median([c["y1"] - 1 - slope * (c["cx"] - xref) for c in ordinary or run]))
            # Native crop includes assigned tall components; bounds padded only for viewing.
            y0, y1 = min(c["y0"] for c in run), max(c["y1"] for c in run)
            lines.append(dict(x0=x0, y0=y0, x1=x1, y1=y1, baseline=baseline,
                              body_height=body, slope=slope, xref=xref,
                              component_labels=[c["label"] for c in run],
                              baseline_mad=float(np.median(abs(np.array([c["y1"] - 1 for c in ordinary or run]) - baseline))),
                              multiline_component_count=sum(c["multiline_contact"] for c in run),
                              component_count=len(run), proposal_status="unreviewed"))
    lines.sort(key=lambda line: (line["baseline"], line["x0"]))
    return lines, cc, labels


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", choices=["pilot", "all"], default="pilot")
    ap.add_argument("--config", default="data/observations/visual_protocol_draft.json")
    ap.add_argument("--native", action="store_true")
    ap.add_argument("--unmasked", action="store_true")
    ap.add_argument("--view-id")
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()
    base_config = read_json(OUT / args.config)
    calibration_regions = read_json(OUT / "data/observations/calibration_regions.json")["regions"]
    views = read_csv(OUT / "data/source/all_view_manifest.csv")
    pilot_pages = {int(r["pdf_page"]) for r in read_csv(OUT / "data/source/sample_manifest.csv")}
    if args.scope == "pilot":
        views = [r for r in views if int(r["pdf_page"]) in pilot_pages]
    else:
        views = [r for r in views if r["split"] != "excluded_cover"]
    if args.view_id:
        views = [r for r in views if r['view_id'] == args.view_id]
    suffix = "_native" if args.native else ""
    if args.unmasked:
        suffix += "_global"
    folder = OUT / f"data/observations/{args.scope}{suffix}_proposals"
    folder.mkdir(parents=True, exist_ok=True)
    overlays = OUT / f"figures/{args.scope}{suffix}_line_overlays"
    overlays.mkdir(parents=True, exist_ok=True)
    summary = []
    if args.native:
        registrations = {r["view_id"]: r for r in read_json(OUT / f"data/source/yale_registration_{args.scope}.json")}
    for row in views:
        row = dict(row)
        view_id = row["view_id"]
        if args.resume and (folder/f'{view_id}.json').exists() and (folder/f'{view_id}_mask.png').exists():
            continue
        config = dict(base_config)
        region_boxes = calibration_regions.get(view_id, [])
        if args.native:
            registration = registrations[view_id]
            if registration["status"] != "verified":
                raise ValueError(f"Cannot transfer unverified coordinates: {view_id}")
            matrix = np.asarray(registration["pdf_to_native_matrix"])
            scale = float(np.sqrt(np.linalg.det(matrix[:2, :2])))
            # Scan scale transfers coordinates, not an assumed writing size.
            # Foldout text has a different local body scale from ordinary pages.
            # Native captures use broad native-pixel seeds; body height is local.
            config.update(geometry_scale=1., background_gaussian_sigma_px=12,
                          component_area_px=[12, 16000], component_height_px=[4, 240],
                          component_width_px=[2, 600], baseline_vote_sigma_px=4,
                          baseline_peak_min_distance_px=40, baseline_assignment_tolerance_px=12,
                          minimum_line_width_px=180, line_horizontal_break_px=250,
                          recovery_height_px=240, recovery_width_px=600, recovery_area_px=20000)
            config["coordinate_transfer_scale"] = scale
            row["pdf_image_path"] = row["image_path"]
            row["image_path"] = registration["native_path"]
            row["image_sha256"] = registration["image_sha256"]
            row["coordinate_frame"] = "native_yale_image"
            row["pdf_to_native_matrix"] = registration["pdf_to_native_matrix"]
            row["width_px"] = registration["native_width"]
            row["height_px"] = registration["native_height"]
            transformed = []
            for x0, y0, x1, y1 in region_boxes:
                corners = np.array([[[x0, y0], [x1, y0], [x1, y1], [x0, y1]]], dtype=np.float32)
                points = cv2.perspectiveTransform(corners, matrix)[0]
                transformed.append([max(0, int(np.floor(points[:, 0].min()))), max(0, int(np.floor(points[:, 1].min()))),
                                    int(np.ceil(points[:, 0].max())), int(np.ceil(points[:, 1].max()))])
            region_boxes = transformed
        im = Image.open(OUT / row["image_path"]).convert("RGB")
        rgb = np.asarray(im)
        mask = ink_mask(rgb, config)
        if args.scope == "pilot" and not args.unmasked:
            region_mask = np.zeros(mask.shape, np.uint8)
            for x0, y0, x1, y1 in region_boxes:
                region_mask[y0:y1, x0:x1] = 1
            mask *= region_mask
        lines, cc, labels = detect_lines(mask, config)
        for i, line in enumerate(lines):
            line["line_id"] = f"{view_id}_L{i + 1:03d}"
        write_json(folder / f"{view_id}.json", dict(view=row, config_version=config["version"],
                                                    effective_config=config,
                                                    lines=lines, components=cc,
                                                    claim="Machine line proposals; not reviewed observations"))
        Image.fromarray(mask * 255).save(folder / f"{view_id}_mask.png")
        draw = ImageDraw.Draw(im)
        for i, line in enumerate(lines):
            box = [line[k] for k in ["x0", "y0", "x1", "y1"]]
            draw.rectangle(box, outline="blue", width=2)
            draw.line((line["x0"], line["baseline"] + line["slope"] * (line["x0"] - line["xref"]),
                       line["x1"], line["baseline"] + line["slope"] * (line["x1"] - line["xref"])), fill="red", width=1)
            draw.text((line["x0"], max(0, line["y0"] - 12)), str(i + 1), fill="blue")
        im.save(overlays / f"{view_id}.png")
        summary.append(dict(view_id=view_id, pdf_page=row["pdf_page"], caption=row["caption"],
                            split=row["split"], proposed_lines=len(lines), eligible_components=len(cc),
                            median_body_height=np.median([line["body_height"] for line in lines]) if lines else None,
                            review_status="unreviewed"))
        print(f"{view_id}: {len(lines)} line proposals", flush=True)
    if summary:
        write_csv(folder / ("summary.csv" if not args.view_id else f"{args.view_id}_summary.csv"), summary)


if __name__ == "__main__":
    main()
