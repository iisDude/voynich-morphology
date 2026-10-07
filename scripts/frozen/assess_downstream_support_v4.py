"""Post-freeze support readout. Never loads conventional metadata or outcomes."""
from common import OUT,read_json,write_json,sha256
from build_sequence_model_v4 import F
from register_sequence_v4 import T,D
from datetime import datetime,timezone
def main():
    manifest=F/'FREEZE_MANIFEST.json';m=read_json(manifest);bad=[r['path'] for r in m['files'] if sha256(OUT/r['path'])!=r['sha256']];assert not bad
    q=read_json(T/'qualification.json');plan=read_json(D/'PLAN.json');assert sha256(T/'qualification.json')==m['qualification_sha256'];assert sha256(D/'PLAN.json')==q['preregistered_support_sha256']
    target=OUT/'tests/sequence_v4_postfreeze';target.mkdir(exist_ok=True)
    result=dict(assessed_at_utc=datetime.now(timezone.utc).isoformat(),v4_frozen_at_utc=m['frozen_at_utc'],frozen_manifest_sha256=sha256(manifest),manifest_files_verified=len(m['files']),predeclared_thresholds=plan['sequence_support_gates'],frozen_source_qualification=q,downstream_allowed=q['downstream_support'],ordinal_assay='not run: registered source support failed',native_pixel_x_assay='not run: source support and physical row endpoints unavailable',transcription_crosswalks='not run: registered source support failed',conventional_metadata_or_outcomes_read=False)
    write_json(target/'downstream_support_assessment.json',result)
    (target/'summary.md').write_text('# Post-freeze V4 support assessment\n\nV4 was frozen before this assessment. Practical notation support failed on the registered source coverage, membership, unknown, boundary and endpoint thresholds. All V4 manifest files verified. No Currier metadata, conventional strings or positional outcomes were loaded. Ordinal-rank assay, native pixel-x assay and EVA/RF/v101 crosswalks were not run. This is a partial source sequence evidence freeze, with V3 unchanged.\n',encoding='utf-8')
    print('Post-freeze assessment:',q['downstream_support'],'downstream allowed;',len(m['files']),'files verified',flush=True)
if __name__=='__main__':main()
