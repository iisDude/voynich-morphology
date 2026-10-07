"""Verify downloaded capture alignment before transferring source coordinates."""
from common import OUT, read_csv, write_csv, write_json
import argparse
import numpy as np
import cv2
from PIL import Image


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", choices=["pilot", "all"], default="pilot")
    args = ap.parse_args()
    downloads = read_csv(OUT / f"data/source/yale_native_{args.scope}_manifest.csv")
    views = {r["view_id"]: r for r in read_csv(OUT / "data/source/all_view_manifest.csv")}
    registrations = []
    for row in downloads:
        if row["status"] != "downloaded":
            continue
        pdf = np.asarray(Image.open(OUT / views[row["view_id"]]["image_path"]).convert("RGB"))
        native = np.asarray(Image.open(OUT / row["path"]).convert("RGB"))
        down = cv2.resize(native, (pdf.shape[1], pdf.shape[0]), interpolation=cv2.INTER_AREA)
        g1, g2 = [cv2.cvtColor(a, cv2.COLOR_RGB2GRAY) for a in [pdf, down]]
        sift = cv2.SIFT_create(nfeatures=2500)
        k1, d1 = sift.detectAndCompute(g1, None)
        k2, d2 = sift.detectAndCompute(g2, None)
        matches = cv2.BFMatcher().knnMatch(d1, d2, k=2)
        good = [a for a, b in matches if a.distance < .70 * b.distance]
        if len(good) < 10:
            raise ValueError(f"Insufficient registration matches for {row['view_id']}")
        p1 = np.array([k1[m.queryIdx].pt for m in good], np.float32)
        p2 = np.array([k2[m.trainIdx].pt for m in good], np.float32)
        affine, inliers = cv2.estimateAffinePartial2D(p1, p2, method=cv2.RANSAC,
                                                     ransacReprojThreshold=1.5, maxIters=5000)
        a3 = np.vstack([affine, [0, 0, 1]])
        scale = np.diag([native.shape[1] / pdf.shape[1], native.shape[0] / pdf.shape[0], 1])
        transform = scale @ a3
        pred = cv2.transform(p1[None], affine)[0]
        errors = np.linalg.norm(pred - p2, axis=1)
        accepted = inliers[:, 0].astype(bool)
        median_error = float(np.median(errors[accepted]))
        status = "verified" if accepted.sum() >= 50 and median_error <= 1 else "unresolved"
        result = dict(view_id=row["view_id"], image_sha256=row["sha256"],
                      native_path=row["path"], native_width=native.shape[1], native_height=native.shape[0],
                      pdf_image_sha256=views[row["view_id"]]["image_sha256"],
                      matched_points=len(good), inlier_points=int(accepted.sum()),
                      median_reprojection_error_pdf_px=median_error,
                      rgb_downsample_mean_absolute_difference=float(np.abs(down.astype(float) - pdf).mean()),
                      grayscale_downsample_correlation=float(np.corrcoef(g1.ravel(), g2.ravel())[0, 1]),
                      pdf_to_native_matrix=transform.tolist(),
                      native_to_pdf_matrix=np.linalg.inv(transform).tolist(), status=status)
        registrations.append(result)
        print(f"{row['view_id']}: {status}, {accepted.sum()} inliers, median error {median_error:.3f} PDF px", flush=True)
    write_json(OUT / f"data/source/yale_registration_{args.scope}.json", registrations)


if __name__ == "__main__":
    main()
