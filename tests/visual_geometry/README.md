# Visual geometry and source identity checks

Run `run.py` with the project scientific Python runtime. This test verifies source hashes, native-to-PDF round trips, image bounds, caption coverage and the orientation of elliptical coordinates. It checks bookkeeping and geometry; it does not establish writing-unit validity.

Expected source inventory: 14 original evidence files, 214 PDF pages, 204 folio-captioned native Yale scans. Every manuscript view must have a layout review record, including explicit abstentions.

For clockwise angle and inward radial image y, the local two-dimensional mapping must preserve orientation. The original clockwise/outward unwrapping reflected local forms and is excluded from unit discovery.

Seed: 20261005. No statistical null is relevant to deterministic coordinate identity. Failure is any changed source, missing review record, inconsistent image dimension, inverse mapping error above 1e-6 pixels, or reflected local mapping.
