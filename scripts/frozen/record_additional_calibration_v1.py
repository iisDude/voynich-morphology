from common import OUT,read_csv,write_json

views=[f"V_{int(r['pdf_page']):03d}" for r in read_csv(OUT/'data/source/sample_manifest.csv')]
write_json(OUT/'data/observations/additional_calibration_reviews_v1.json',dict(
    review_source='Native source RGB and actual assigned binary-mask strips; no conventional strings or expected counts used.',
    versions=[dict(version='v5',reviewed_views=views,status='Rejected as full writing extraction. Raw foreground retains substantial writing; row ownership explains much missing assigned ink. Strong threshold also fragments faint writing.'),
        dict(version='v6',reviewed_views=views[:6],status='Not accepted. Lower threshold restores texture and does not repair row ownership. Remaining six galleries not reviewed in this pass.'),
        dict(version='v7',reviewed_views=['V_004'],status='Rejected: near-total background connectivity leaves almost no writing paths across pilot; raw diagnostic confirms background merging.'),
        dict(version='v8',reviewed_views=['V_004','V_052','V_116'],status='Rejected: ridge filtering fragments writing; raw diagnostic on V_004 confirms.'),
        dict(version='v9',reviewed_views=['V_004','V_052','V_116'],status='Ownership improves some retention; source false paths and row contacts persist. Not accepted.'),
        dict(version='v10',reviewed_views=views,status='All twelve four-strip galleries reviewed. Dense rows improve, but horizontal bands switch physical rows and include drawings. Not accepted as canonical extraction.'),
        dict(version='v11',reviewed_views=views,status='All twelve four-strip galleries reviewed. Local tracks improve dense slanted rows; drawings, faint writing, split flows and row contacts persist. Protocol representation workable for systematic candidate expansion; writing coverage, membership and boundaries NOT accepted.'),
        dict(version='bridge_v0',reviewed_views=views,status='All twelve galleries reviewed. Thin skeleton cuts frequently bisect loops and stems, and can lie in artifact masks. Realizable as competing geometric partitions; rejected as automatic grapheme or pen-lift boundaries. Uncut alternatives retained.')],
    blinding='All these repairs/realizations occur after comparison exposure; image-only inputs do not recreate a fresh blind investigation.',
    next_gate='Expand unchanged v11 candidate protocol to all 204 views; source-audit exact masks. Preserve v4 freeze and failures.'))
print('Calibration review recorded; unreviewed galleries explicitly listed.')
