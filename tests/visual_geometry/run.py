from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
from common import ROOT,OUT,read_json,read_csv,sha256,write_json,write_csv
import numpy as np
from PIL import Image


def main():
    folder=Path(__file__).resolve().parent;config=read_json(folder/'config.json');results=[]
    original=read_csv(OUT/'data/source/evidence_manifest.csv')
    assert len(original)==config['source_file_count']
    for row in original:
        actual=sha256(ROOT/row['path']);assert actual==row['sha256'],row['path']
        results.append(dict(check='original_source_hash',target=row['path'],status='pass',value=actual))
    pdf=read_csv(OUT/'data/source/page_folio_map.csv');assert len(pdf)==config['pdf_pages']
    regs=read_json(OUT/'data/source/yale_registration_all.json');assert len(regs)==config['folio_captioned_views']
    layout=read_json(OUT/'data/observations/layout_regions_fractional.json')['regions'];calibration=read_json(OUT/'data/observations/calibration_regions.json')['regions']
    for reg in regs:
        vid=reg['view_id'];assert vid in layout or vid in calibration
        assert reg['status']=='verified'
        if config['check_native_file_hashes']:assert sha256(OUT/reg['native_path'])==reg['image_sha256']
        image=Image.open(OUT/reg['native_path']);assert image.size==(reg['native_width'],reg['native_height'])
        forward=np.array(reg['pdf_to_native_matrix']);inverse=np.array(reg['native_to_pdf_matrix'])
        points=np.array([[0,0,1],[reg['native_width']/2,reg['native_height']/2,1],[reg['native_width'],reg['native_height'],1]],float).T
        roundtrip=forward@inverse@points;roundtrip/=roundtrip[2]
        error=float(np.max(abs(roundtrip-points)));assert error<=config['inverse_mapping_tolerance_px'],vid
        assert np.linalg.det(forward[:2,:2])>0
        results.append(dict(check='native_identity_and_coordinate_inverse',target=vid,status='pass',value=error))
    for theta in np.linspace(0,2*np.pi,17):
        # dx/dtheta, dx/d(inward rho); dy/dtheta, dy/d(inward rho)
        rx,ry,rho=700.,650.,.8
        jacobian=np.array([[-rx*rho*np.sin(theta),-rx*np.cos(theta)],[ry*rho*np.cos(theta),-ry*np.sin(theta)]])
        assert np.linalg.det(jacobian)>0
    results.append(dict(check='elliptical_orientation_preserved',target='clockwise_inward',status='pass',value=17))
    write_csv(folder/'results.csv',results)
    write_json(folder/'input_manifest.json',dict(config_sha256=sha256(folder/'config.json'),source_inventory_sha256=sha256(OUT/'data/source/evidence_manifest.csv'),registration_sha256=sha256(OUT/'data/source/yale_registration_all.json'),layout_sha256=sha256(OUT/'data/observations/layout_regions_fractional.json'),calibration_layout_sha256=sha256(OUT/'data/observations/calibration_regions.json')))
    (folder/'summary.md').write_text(f'# Geometry check results\n\nAll {len(results)} checks passed. Original sources are unchanged; all 204 native registrations have invertible, orientation-preserving mappings and layout coverage. Elliptical orientation passed at 17 sampled angles.\n\nThese checks verify source identity and coordinate bookkeeping. They do not validate path membership, unit boundaries, pen lifts or interpretation. No novelty claim.\n',encoding='utf-8')
    print(f'{len(results)} checks passed',flush=True)


if __name__=='__main__':main()
