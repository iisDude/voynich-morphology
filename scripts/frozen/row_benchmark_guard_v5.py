"""Never overwrite the source seal or final V5 snapshot."""
from common import OUT
def require_unfrozen(source_stage=False):
    root=OUT/'data/observations/visual_dataset_v5'
    if (root/'FREEZE_MANIFEST.json').exists():raise RuntimeError('V5 is immutable. Reproduce or extend into a new version/output directory.')
    if source_stage and (root/'SOURCE_REFERENCE_SEAL.json').exists():raise RuntimeError('V5 source reference is already sealed; source annotation writers are closed.')
