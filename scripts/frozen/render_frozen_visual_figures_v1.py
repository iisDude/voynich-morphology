"""Post-freeze derivative plots; never overwrite a manifest-frozen artifact."""
from common import OUT,read_csv,read_json,write_json,sha256
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def main():
    frozen={r['path'] for version in ['v0','v11'] for r in read_json(OUT/f'data/observations/visual_dataset_{version}/FREEZE_MANIFEST.json')['files']};provenance=[]
    def save(chart,relative,source):
        if relative in frozen:raise ValueError('Refuse to overwrite frozen artifact')
        path=OUT/relative;path.parent.mkdir(parents=True,exist_ok=True);chart.tight_layout();chart.savefig(path,dpi=160);plt.close(chart);provenance.append(dict(path=relative,source=source,source_sha256=sha256(OUT/source)))
    source='tests/visual_reconstruction/summary.csv';rows=[r for r in read_csv(OUT/source) if r['split']=='test'];chart,axes=plt.subplots(1,2,figsize=(10,4))
    names=[r['model'].replace('_','\n') for r in rows];axes[0].bar(names,[float(r['mean_template_iou']) for r in rows],color='#155e75');axes[0].set_ylabel('Mean template IoU against assigned binary ink');axes[0].set_ylim(0,1);axes[0].set_title('Selected 1,824 groups, 22 captions')
    for i,r in enumerate(rows):axes[1].plot(float(r['equal_folio_excess_bits_per_pixel']),i,'o');axes[1].plot([float(r['folio_bootstrap_lower']),float(r['folio_bootstrap_upper'])],[i,i])
    axes[1].set_yticks(range(len(rows)),names);axes[1].set_xlabel('Conditional codec excess bits/pixel');axes[1].set_title('Caption bootstrap; selected masks');chart.suptitle('Frozen visual reconstruction — geometry, not grapheme truth');save(chart,'tests/visual_reconstruction/figures/heldout_geometry_derivative_v1.png',source)
    source='tests/visual_structure/summary.csv';rows=[r for r in read_csv(OUT/source) if r['split']=='test'];chart,ax=plt.subplots(figsize=(9,4))
    for i,r in enumerate(rows):ax.plot(float(r['equal_folio_fraction']),i,'o');ax.plot([float(r['bootstrap_lower']),float(r['bootstrap_upper'])],[i,i])
    ax.set_yticks(range(len(rows)),[r['metric'] for r in rows]);ax.set_xlabel('Equal-caption proxy fraction; descriptive bootstrap');ax.set_xlim(-.02,1.02);ax.set_title('Frozen morphology proxies — no pen-lift or sign-boundary claims');save(chart,'tests/visual_structure/figures/morphology_derivative_v1.png',source)
    source='data/source/yale_registration_all.json';rows=read_json(OUT/source);chart,ax=plt.subplots(figsize=(8,3.5));ax.hist([r['median_reprojection_error_pdf_px'] for r in rows],bins=20,color='#155e75');ax.set_xlabel('Median SIFT/RANSAC error in PDF image pixels');ax.set_ylabel('Capture views');ax.set_title('204 native-to-PDF registrations — same captures, not independent sources');save(chart,'tests/visual_geometry/figures/registration_derivative_v1.png',source)
    source='tests/candidate_integrity_v1/results.csv';rows=read_csv(OUT/source);chart,axes=plt.subplots(1,2,figsize=(10,3.5));axes[0].plot([int(r['view_id'][2:]) for r in rows],[int(r['groups']) for r in rows],'.',color='#155e75');axes[0].set_xlabel('PDF capture index');axes[0].set_ylabel('Candidate gray-gap groups');axes[0].set_title('Coverage is not writing recall');axes[1].plot([int(r['view_id'][2:]) for r in rows],[int(r['errors']) for r in rows],'.');axes[1].set_ylim(-.5,1);axes[1].set_xlabel('PDF capture index');axes[1].set_ylabel('Assigned-pixel conservation errors');axes[1].set_title('All four partitions and bridge cuts');save(chart,'tests/candidate_integrity_v1/figures/conservation_derivative_v1.png',source)
    write_json(OUT/'tests/reporting_v1/frozen_visual_figure_manifest.json',dict(status='Post-freeze derivative figures, not part of either original hashed snapshot',source_sha256=sha256(OUT/'src/render_frozen_visual_figures_v1.py'),figures=provenance))
    print('Added four derivative visual figures without changing frozen files.')

if __name__=='__main__':main()
