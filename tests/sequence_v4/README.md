# V4 source sequence validation

Read config.json and reports/13_source_sequence_validation_v4.md. Frozen V3 source inference only; explicit unknown and competing membership states. Run scripts in order: register_sequence_v4, prepare_sequence_source_v4, record_sequence_reviews_v4, extract_sequence_v4, prepare_sequence_audits_v4; native judgments are saved separately; build_sequence_model_v4, audit_sequence_v4, report_sequence_v4, freeze_sequence_v4. Do not rerun mutations after freeze. Post-freeze audit writes into tests/sequence_v4_postfreeze.

Seed 20261009. Null: known-class order shuffle within source row, UNK and incomplete flags fixed. Conditional recurrence only, no conventional assay. Source judgments by one adjudicator, repeatability only.
