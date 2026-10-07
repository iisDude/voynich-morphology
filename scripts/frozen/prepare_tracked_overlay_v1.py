"""Version the exact-mask audit renderer for the tracked frozen snapshot."""
from common import OUT

def main():
    source=(OUT/'src/overlay_crosswalk_membership_v0.py').read_text(encoding='utf-8')
    source=source.replace('data/comparisons/v2/visual_row_alignment_source_audit.json','data/comparisons/v11/visual_row_alignment_audit_plan.json').replace('data/comparisons/v2/visual_membership_overlay_audit_plan.json','data/comparisons/v11/visual_membership_overlay_audit_plan.json').replace('crosswalk_mask_audit_v0','crosswalk_mask_audit_v11').replace('regional_candidates_v4','regional_candidates_v11')
    source=source.replace("data=np.load(OUT/f'data/observations/regional_candidates_v11/{vid}_native_masks.npz')","archive=np.load(OUT/f'data/observations/regional_candidates_v11/{vid}_native_masks.npz');data={k:archive[k] for k in archive.files}")
    (OUT/'src/overlay_crosswalk_membership_v11.py').write_text(source,encoding='utf-8')

if __name__=='__main__':main()
