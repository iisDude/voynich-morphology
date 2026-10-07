# Completed workflow integrity verification

Run `python voynich-groundup/tests/workflow_audit_v1/run.py` from the project root. This rechecks frozen hashes, source evidence, post-freeze unit/position invariance, review counts and 68 empirical artifact contracts, then renders this report. It writes only the audit and artifact index, not frozen evidence. Passing does not establish writing recall, sign boundaries or a transcription crosswalk.
