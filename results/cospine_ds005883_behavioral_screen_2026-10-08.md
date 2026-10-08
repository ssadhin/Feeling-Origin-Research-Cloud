# CoSpine ds005883 behavioral screening — 2026-10-08

Status: descriptive, NOT proof-grade or paper-worthy. Pinned source Git SHA: 037ed267e7f7f2024a5fe3d0e8fb4759f7f67bdd. Freeze before event inspection: Google Doc 1SZnO_4YFMUKcHE-PmAhcabDrZ1bxcFimpRHsA3AWPR0. GitHub mirror was written after inspection and is not an independently timestamped preregistration.

39 subjects x 15 events = 585 paired intensity PR and unpleasantness UpR reports, zero missing. 130/585 (22.22%) exactly equal; subject 05 equal on all 15. Mean UpR minus PR = -1.59316.

Within-subject demeaning: SS(PR)=531.066661; SS(UpR)=679.599990; cross-product=468.466667; r=0.779790. A common PR slope leaves 39.1928% of within-person UpR variance unexplained; participant-specific slopes leave 34.5906%. Post-freeze nonlinear rival check: exact PR bins within subject leave 184.799063 / 679.599990 = 27.1923% residual, in 38/39 subjects. Input per-subject moments rounded to six decimals; rerun code for unrounded values.

These are rating differences, NOT phenomenal evidence. Nonlinear response scales, attention, rating noise, temporal context, and unmeasured physiology can explain residuals. Within-person heat temperature is constant; no direct M intervention, no reasoning/access converse perturbation, no independent replication. Dataset version mismatch: README v1.1.0 versus dataset_description DOI v1.1.1.

Prior art: Rainville 1997 DOI 10.1126/science.277.5328.968; Hofbauer 2001 DOI 10.1152/jn.2001.86.1.402; CoSpine paper Wei 2025 DOI 10.1038/s41597-025-05982-x. Original paper already reports different mean intensity and unpleasantness. Not novel.

Next: independently rerun analysis/cospine_ds005883_behavioral_screen_v001.py, then acquire neural/physiological signals, freeze ROI and rival models, evaluate held-out subjects. Preserve nulls and all causal kill conditions. Distinguish phenomenal presence P from affective significance S. Ownership-dependent old equation remains rejected.
