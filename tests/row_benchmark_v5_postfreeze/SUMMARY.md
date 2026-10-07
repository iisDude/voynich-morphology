# V5 postfreeze support assessment

Frozen manifest SHA-256: `16f040e6e80f8a1fd47b796811935df4c5546021d4b41f79933ee18cd668fed8`

**Downstream support: not qualified.** No rank/pixel-x assay, EVA/RF/v101 crosswalk, Currier metadata or minimal-pair support was opened.

| Gate | Observed | Required | Result |
|---|---:|---:|---|
| heldout_target_writing_recall | 0.9438202247191011 | min 0.95 | fail |
| heldout_nonwriting_false_inclusion | 0.00980392156862745 | max 0.05 | pass |
| heldout_resolved_target_owner_precision | 1.0 | min 0.95 | pass |
| heldout_reviewed_parent_support_recovery | 0.9753086419753086 | min 0.9 | pass |
| heldout_endpoint_x_accuracy | 0.875 | min 0.9 | fail |
| repeat_prior_resolved_membership_agreement | 0.8691588785046729 | min 0.9 | fail |
| complete_reference_structural_rows | 0 | min 12 | fail |
| unknown_confirmed_parent_rate | 0.512539184952978 | max 0.2 | fail |
| resolved_source_endpoint_fraction | 0.96875 | min 0.9 | pass |
| complete_groups_length3_gap0.35 | 0 | min 100 | fail |
| heldout_complete_groups_length3_gap0.35 | 0 | min 30 | fail |
| heldout_recurrence_length3_gap0.35 | not estimable | min 0.2 | fail |
| complete_groups_length3_gap0.55 | 0 | min 100 | fail |
| heldout_complete_groups_length3_gap0.55 | 0 | min 30 | fail |
| heldout_recurrence_length3_gap0.55 | not estimable | min 0.2 | fail |
| complete_groups_length3_gap0.75 | 0 | min 100 | fail |
| heldout_complete_groups_length3_gap0.75 | 0 | min 30 | fail |
| heldout_recurrence_length3_gap0.75 | not estimable | min 0.2 | fail |
