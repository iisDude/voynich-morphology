"""Pilot crop/assembly proposals and threshold-sensitive raster measurements.

Connected components and skeletons are raster proxies. No characters or pen
strokes are assigned. Every box maps directly to the native PDF image.
"""
from common import OUT, read_csv, read_json, write_json, write_csv
from visual_extract import ink_mask
import numpy as np
import cv2
from scipy.ndimage import label as ndlabel, convolve
from scipy.signal import find_peaks
from skimage.morphology import skeletonize
from skimage.measure import euler_number
from PIL import Image, ImageDraw
import argparse


def projection_spans(mask, minimum_gap):
    occupied = np.flatnonzero(mask.any(axis=0))
    if not len(occupied):
        return []
    breaks = np.flatnonzero(np.diff(occupied) - 1 >= minimum_gap)
    starts = np.r_[0, breaks + 1]
    ends = np.r_[breaks, len(occupied) - 1]
    return [(int(occupied[a]), int(occupied[b]) + 1) for a, b in zip(starts, ends)]


def topology(binary, body_height):
    mask = binary.astype(bool)
    n = int(ndlabel(mask, structure=np.ones((3, 3)))[1])
    skel = skeletonize(mask)
    neighbors = convolve(skel.astype(np.uint8), np.ones((3, 3), np.uint8), mode="constant") - skel
    branch_clusters = int(ndlabel(skel & (neighbors >= 3), structure=np.ones((3, 3)))[1])
    endpoints = int((skel & (neighbors == 1)).sum())
    loops = int(n - euler_number(mask, connectivity=2))
    longest_horizontal = 0
    for row in mask:
        starts = np.flatnonzero(np.diff(np.r_[False, row, False].astype(int)) == 1)
        ends = np.flatnonzero(np.diff(np.r_[False, row, False].astype(int)) == -1)
        if len(starts):
            longest_horizontal = max(longest_horizontal, int(max(ends - starts)))
    profile = mask.sum(axis=0).astype(float)
    ridges, _ = find_peaks(profile, distance=max(2, round(body_height * .20)),
                           prominence=max(2, body_height * .25))
    return dict(raster_components=n, raster_loops=loops, skeleton_endpoint_pixels=endpoints,
                skeleton_branch_clusters=branch_clusters,
                longest_horizontal_ink_run_px=longest_horizontal,
                column_ink_ridge_count=int(len(ridges)), skeleton_pixels=int(skel.sum()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--native", action="store_true")
    args = ap.parse_args()
    suffix = "_native" if args.native else ""
    records = []
    selected_lines = []
    crops = OUT / f"data/crops/calibration{suffix}"
    crops.mkdir(parents=True, exist_ok=True)
    audit = OUT / f"figures/calibration{suffix}_audit"
    audit.mkdir(parents=True, exist_ok=True)
    all_components = []
    for path in sorted((OUT / f"data/observations/pilot{suffix}_proposals").glob("V_*.json")):
        proposal = read_json(path)
        config = proposal["effective_config"]
        view = proposal["view"]
        rgb = np.asarray(Image.open(OUT / view["image_path"]).convert("RGB"))
        masks = {t: ink_mask(rgb, config, t) for t in config["contrast_sensitivity"]}
        # Labels must come from the exact region-masked raster used for line proposals.
        # Re-labelling the full page would silently point stored member IDs at other ink.
        proposal_mask = (np.asarray(Image.open(path.with_name(path.stem + "_mask.png"))) > 0).astype(np.uint8)
        n, labels, _, _ = cv2.connectedComponentsWithStats(proposal_mask, connectivity=8)
        masks[config["primary_ink_contrast"]] = proposal_mask
        lines = proposal["lines"]
        if not lines:
            continue
        indexes = sorted(set(np.linspace(0, len(lines) - 1, min(4, len(lines))).round().astype(int)))
        tiles = []
        for index in indexes:
            line = lines[index]
            x0, y0, x1, y1 = [line[k] for k in ["x0", "y0", "x1", "y1"]]
            body = line["body_height"]
            assigned = np.isin(labels[y0:y1, x0:x1], line["component_labels"]).astype(np.uint8)
            primary = masks[config["primary_ink_contrast"]][y0:y1, x0:x1]
            inclusion = float(assigned.sum() / max(1, primary.sum()))
            line_record = dict(line_id=line["line_id"], view_id=view["view_id"],
                               image_sha256=view["image_sha256"], bbox_xyxy=[x0, y0, x1, y1],
                               coordinate_frame=view.get("coordinate_frame", "native_embedded_image"),
                               body_height_proxy_px=body, baseline_y_at_xref=line["baseline"],
                               baseline_slope=line["slope"], baseline_xref=line["xref"],
                               baseline_mad_px=line["baseline_mad"],
                               assigned_ink_fraction_of_bbox=inclusion, groups_by_gap={},
                               status="machine proposal awaiting strip audit")
            for ratio in config["group_gap_body_ratios"]:
                spans = projection_spans(assigned, max(2, int(np.ceil(ratio * body))))
                line_record["groups_by_gap"][str(ratio)] = [[x0 + a, x0 + b] for a, b in spans]
            group_spans = projection_spans(assigned, max(2, int(np.ceil(config["primary_group_gap_body_ratio"] * body))))
            for gi, (gx0, gx1) in enumerate(group_spans):
                group_id = f"{line['line_id']}_G{gi + 1:03d}"
                group = assigned[:, gx0:gx1]
                parts = projection_spans(group, max(1, int(np.ceil(config["assembly_small_gap_body_ratio"] * body))))
                for ai, (ax0, ax1) in enumerate(parts):
                    local = group[:, ax0:ax1]
                    ys, xs = np.where(local)
                    if not len(ys):
                        continue
                    ay0, ay1 = int(ys.min()), int(ys.max()) + 1
                    crop = local[ay0:ay1, :]
                    bx0, bx1 = x0 + gx0 + ax0, x0 + gx0 + ax1
                    by0, by1 = y0 + ay0, y0 + ay1
                    assembly_id = f"{group_id}_A{ai + 1:02d}"
                    native_path = crops / f"{assembly_id}.png"
                    Image.fromarray(rgb[by0:by1, bx0:bx1]).save(native_path)
                    Image.fromarray((255 - crop * 255).astype(np.uint8)).save(crops / f"{assembly_id}_mask.png")
                    features = topology(crop, body)
                    sensitivity = {str(t): topology(m[by0:by1, bx0:bx1], body)
                                   for t, m in masks.items()}
                    counts = [s["raster_components"] for s in sensitivity.values()]
                    loop_counts = [s["raster_loops"] for s in sensitivity.values()]
                    baseline_here = line["baseline"] + line["slope"] * ((bx0 + bx1) / 2 - line["xref"])
                    height_ratio = (by1 - by0) / body
                    record = dict(assembly_id=assembly_id, group_id=group_id, line_id=line["line_id"],
                                  view_id=view["view_id"], image_sha256=view["image_sha256"],
                                  bbox_xyxy=[bx0, by0, bx1, by1],
                                  body_height_proxy_px=body, height_ratio=height_ratio,
                                  upper_extent_ratio=(baseline_here - by0) / body,
                                  lower_extent_ratio=(by1 - 1 - baseline_here) / body,
                                  group_rank=gi, group_count=len(group_spans),
                                  normalized_group_rank=gi / (len(group_spans) - 1) if len(group_spans) > 1 else .5,
                                  normalized_pixel_center=((bx0 + bx1) / 2 - x0) / (x1 - x0),
                                  **features, topology_by_contrast=sensitivity,
                                  topology_threshold_stable=len(set(counts)) == 1 and len(set(loop_counts)) == 1,
                                  tall_candidate=height_ratio >= config["tall_candidate_height_ratio"],
                                  horizontal_connector_candidate=features["longest_horizontal_ink_run_px"] >= body * .8,
                                  repetition_candidate=features["column_ink_ridge_count"] >= 3,
                                  pen_lift_evidence="unresolved; raster fragments do not establish pen lifts",
                                  crop_path=native_path.relative_to(OUT).as_posix(),
                                  status="unreviewed assembly proposal", segmentation_alternatives=[
                                      "whole projection assembly", "visible disconnected components",
                                      "upper/lower subassemblies where present", "shared connector/frame if supported"])
                    records.append(record)
            selected_lines.append(line_record)
            patch = Image.fromarray(rgb[y0:y1, x0:x1]).copy()
            draw = ImageDraw.Draw(patch)
            for a, b in group_spans:
                draw.line((a, 0, a, patch.height), fill="blue")
                draw.line((b - 1, 0, b - 1, patch.height), fill="blue")
            target_width = 1280
            if patch.width > target_width:
                patch.thumbnail((target_width, 200))
            tile = Image.new("RGB", (1300, max(150, patch.height * 2 + 40)), "white")
            tile.paste(patch, (10, 30))
            mask_patch = Image.fromarray((255 - assigned * 255).astype(np.uint8)).convert("RGB")
            if mask_patch.width > target_width:
                mask_patch.thumbnail((target_width, 200))
            tile.paste(mask_patch, (10, 35 + patch.height))
            ImageDraw.Draw(tile).text((10, 6), f"{line['line_id']} source={x0},{y0},{x1},{y1} body={body:.1f} inclusion={inclusion:.2f}", fill="black")
            tiles.append(tile)
        sheet = Image.new("RGB", (1300, sum(t.height for t in tiles)), "#eeeeee")
        yy = 0
        for tile in tiles:
            sheet.paste(tile, (0, yy))
            yy += tile.height
        sheet.save(audit / f"{view['view_id']}_strips.png")
    write_json(OUT / f"data/observations/calibration{suffix}_lines.json", selected_lines)
    write_json(OUT / f"data/observations/calibration{suffix}_assemblies.json", records)
    summary = dict(selected_lines=len(selected_lines), assembly_proposals=len(records),
                    tall_proposals=sum(r["tall_candidate"] for r in records),
                    connector_proposals=sum(r["horizontal_connector_candidate"] for r in records),
                    repetition_proposals=sum(r["repetition_candidate"] for r in records),
                    topology_threshold_stable=sum(r["topology_threshold_stable"] for r in records),
                    positive_pen_lift_assignments=0,
                    warning="These are proposals. Counts are not empirical script-family findings before review.")
    write_json(OUT / f"reports/calibration{suffix}_proposal_summary.json", summary)
    print(summary, flush=True)


if __name__ == "__main__":
    main()
