from dm2_robustness_common import *
from verify_dm2_robustness import verify as replay
from verify_dm2_robustness_repeat import verify as repeat_replay
from seal_direct_morphology2 import prior_integrity
def main():
    verify_seal(D/'FREEZE_MANIFEST.json');verify_base();prior=prior_integrity();print('Prior and robustness freezes intact',flush=True);r=replay();write_json(P/'REPLAY.json',r);rr=repeat_replay();write_json(P/'REPEAT_REPLAY.json',rr)
    try:guard()
    except RuntimeError:blocked=True
    else:blocked=False
    assert blocked;verify_seal(D/'FREEZE_MANIFEST.json');verify_base();digest=sha256(D/'FREEZE_MANIFEST.json');write_json(P/'INTEGRITY.json',dict(checked_at_utc=now(),robustness_manifest_sha256=digest,robustness_frozen_files=read_json(D/'FREEZE_MANIFEST.json')['file_count'],Trial2_manifest_sha256=sha256(B/'FREEZE_MANIFEST.json'),Trial2_files_intact=len(read_json(B/'FREEZE_MANIFEST.json')['files']),prior_Trial2_postfreeze_files_intact=len(read_json(D/'PRIOR_POSTFREEZE_SNAPSHOT.json')['files']),prior=prior,analysis_conditions_replayed=r['analysis_conditions_replayed'],independent_numerical_checks=r['independent_sklearn_AUROC_checks'],repeat_analyses_exact=True,writer_guard_blocks=True,no_downstream_assays=True,failures=[]))
    summary=f'''# Postfreeze robustness disposition

**Sensitive to one or more evaluation assumptions.** This classification describes the separate robustness investigation. Direct Morphology Trial2 remains exactly frozen and supported within its original registered sample.

The frozen same/different signal persists, including after exclusion of flagged raster recoveries. Each-parent-once analysis reduces AUROC from0.879 to0.805, with conditional95%0.496–1.000 and an aspect-only tie. Recovery-clean original binary pairs score0.942; the source/recovery-clean disjoint-parent selection scores0.964. Caption-dyad constraints produce small, seed-sensitive category samples and cannot support uniform precision claims.

Target choice is consequential: all partial-as-same gives0.672; all partial-as-different gives0.853. These are two sensitivity scenarios, not true-label bounds or replacements. Same/partial separation is0.824, partial/different0.623. Broad-random contour0.798 versus aspect0.812 and aspect-matched0.907 versus0.655 show sampling-mixture dependence.

The125 anonymous repeats agree exactly on101/125(80.8%) and linearly across ordinal distance on90.4%; linear kappa0.772. Same/partial/different category retention is77.1%/80.0%/84.4%. All24 changes are adjacent and none directly reverses same/different. The selected repeat corpus's binary AUROC remains strong,0.888 with original labels and0.911 with repeat labels, while memberships change. Same-AI memory and source-target uncertainty persist; no independent human validation is claimed.

All108 conditions, constraint selections, bootstrap calculations and repeat analyses replay. All943 Trial2 frozen files, its eight prior postfreeze files, earlier frozen packages and14 original evidence files are unchanged. No alternate morphology metric or downstream assay was substituted.

[Frozen report](../../reports/27_direct_morphology_trial2_robustness.md) · [Condition dashboard](../../reports/28_direct_morphology_trial2_robustness_dashboard.html) · [Robustness manifest](../../data/observations/direct_morphology_trial2_robustness_v1/FREEZE_MANIFEST.json) · [Integrity](INTEGRITY.json)

Robustness SHA256: `{digest}`.
'''
    import re
    lines=[]
    for line in summary.splitlines():
        if not line.startswith('Robustness SHA256:') and '](' not in line:
            line=re.sub(r'(?<=[A-Za-z])(?=[0-9])',' ',line);line=re.sub(r'(?<=[0-9])(?=[A-Za-z])',' ',line);line=re.sub(r';(?=[A-Za-z0-9])','; ',line);line=re.sub(r'\.(?=[A-Z])','. ',line);line=re.sub(r'(?<=[0-9])\((?=[0-9])',' (',line)
        lines.append(line)
    (P/'SUMMARY.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');print('Postfreeze robustness audit complete; previous evidence preserved',flush=True)
if __name__=='__main__':main()
