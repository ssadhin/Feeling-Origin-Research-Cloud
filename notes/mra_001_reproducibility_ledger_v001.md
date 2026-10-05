# MRA-001 reproducibility ledger v001

Date: 2026-10-05
Status: CORE CASE + POPANE R1/R2/R4 REPRODUCIBILITY PASS; R3/R5 results pending.

## Common cloud environment

GitHub Actions Ubuntu runners.
Python 3.12.
Core dependency bounds used by CASE and POPANE workflows:
- numpy >=2,<3
- pandas >=2.2,<3
- scipy >=1.14,<2
- scikit-learn >=1.6,<2

GitHub actions:
- actions/checkout@v7
- actions/setup-python@v7
- actions/upload-artifact@v7

Workflows are path-gated one-shot runs tied to explicit trigger files, reducing accidental reruns or silent parameter drift.

## CASE O002 primary provenance

Dataset:
- CASE — Continuously Annotated Signals of Emotion.
- Sharma et al. Scientific Data 2019, DOI 10.1038/s41597-019-0209-0.
- Figshare public release used by code; expected archive MD5 hard-coded as 5e679ce69d6602c5f8225f03c489df76.
- Raw archive is downloaded during the run and removed afterward.

Frozen protocol commit:
- b5b08f77d098844632fbd8bf329076e4df9a0b9b

Analysis commit:
- cdcbeda402e4a6739d9ea16c878bdd9566e91b5c

Workflow commit:
- 8a06aabdfbd929bbb481b4bff7342ef55f0462c0
- workflow path: .github/workflows/o002-case-full-once.yml

Trigger:
- ad4a0de93ffef961cf0a7e0f21671ca2db75576e

Canonical run:
- 37217735818

Artifact:
- ID 11308319169
- name o002-case-full-37217735818
- SHA256 af773747ba08a68b96726435e6e908c0e82e24eec744951929aa83cebbb61e7a
- contains case_external_replication_o002.json + o002_feature_rows.jsonl

Permanent GitHub preservation:
- primary result commit 4bd4dd755667b8a347d1d20a68a03517770d4c01
- frozen feature-row preservation commit 446dd42a05f053d8a9a2125ee5328fd60b5537dd

The preserved feature rows are the input for later outcome-frozen sensitivities, avoiding repeated raw-data extraction and preserving exact primary-derived predictors.

## CASE follow-up provenance

G1 double holdout:
- protocol 049bb88b4edeecf494a6adeb0ce6076e6ce59adf
- analysis 7ce5684a62dd2baf83e301d681c670d145c77e60
- workflow 74f3771c8df9e7963ad47eed679b178c88a5fe65
- run 37226922346
- artifact 11311754909
- SHA256 250d1f1a7c63c6abc1b42b7e7854519d9202a1519f9bbd6750175f6a8976b951
- summary commit 25480b229747fee5fbfc4d9430c05076e7d06d44

G2 horizon stress:
- protocol fc936cd6cd6cd77beb6622d0ab96a5ae86468452
- analysis 9401e8bfd6cb5cdf09b222e874ddb1ee3ad02c93
- workflow 30277b4796296d8e31b743dc6e6220e13bbb8430
- run 37255619996
- artifact 11322846291
- SHA256 b26e4a02d48c993158ccf8c072710a037b0a242452e755638fea3c83bd1c4a55
- summary commit 949cb3887c3901d9c94d911454336236b5ed5d40

B1 naive persistence:
- protocol c5ac129e7e425efb317aa276cfa02f99de86c556
- analysis d88f475581e67a28da860f3b8eba66e66865036f
- workflow f424b8011f855d8cc058b2896b2fe82ec91f1f27
- run 37256052367
- artifact 11323095942
- SHA256 8d29c1b5c8e48edf8ae34b524b5ef3f525d925e5873bccc31849f35824855f66
- summary commit 2a7d6c9996962f6b5e94d37711ee2912b17bd477

D1 future-change attack:
- protocol 46ffbbef436d2dc4b247f9016665b4119710bfae
- analysis ec90b1ab9abdabedf3471cf5acea1e5be9ae4122
- workflow 0a5a6742665465752243887976bfeef4d4d9d019
- run 37263399125
- artifact 11326166327
- SHA256 afe62df422e9c69ec3a3930ab9b4b4225c9725afff96b3b85632d77f99ac90d8
- permanent result snapshot exists in results_snapshots/o002_d1_summary_run-37263399125.json

## POPANE dataset provenance

POPANE paper:
- Scientific Data 2022, DOI 10.1038/s41597-021-01117-0.
- OSF DOI 10.17605/OSF.IO/94BPX.
- Study 6 public archive used by workflows.
- license documented in frozen protocol: CC BY-NC 4.0.
- raw ~2.7 GB archive is downloaded transiently in workflow and removed afterward.
- raw POPANE signals are not committed to GitHub.

Outcome-blind schema preflight:
- P0b run 37256777934
- artifact 11322509270
- SHA256 db853390a157ced74378f00d588ec474e21f1163b699525e21a3fe8cb23c3406
- permanent schema summary commit 152308397dd8646bfdb1074c250ca7125f819953

## POPANE-R1 primary external replication provenance

Protocol:
- 5ae69733800c4e7a9e510b6911e908c3d65ab181

Analysis:
- 193893f736c0d6dfeddbb580326bfd58f07431e4

Workflow:
- 28a20ae6a021accbc3ac267f68743f018e29b4d1
- .github/workflows/popane-r1-valence-replication-once.yml

Trigger:
- 2a44cfc375f30ac8acac4a4d48e60a37b2081c89

Canonical run:
- 37257239830

Artifact:
- 11324086038
- SHA256 28fa484c7d9907a8329465af42f8abe7ad6957be8536028f2adbe6de763b6575

Permanent result summary:
- 5ef7f541e77cd1102ad4d0a1d76c0fd2575966e0

R1 artifact contains aggregate result only; no raw participant physiology is persisted in the repository.

## POPANE-R2 change-target replication

Frozen protocol:
- 5e8f8038f06fb96b216b93a6ddc81371e748eb24

Initial run:
- 37263637334
- technical failure before scientific result due Python import path.

Failure audit:
- 836417ff980b11e5bb552ecec540e6aa28134cd0

Import-only correction:
- a167a33be9f2e5712aa5572fdf58d9a22df91cfe

Successful canonical rerun:
- 37267526360
- artifact 11327232849
- SHA256 c15442896e92fffd1dbab6e2ba714fa08970a8a2179286e008edd2244f94104e
- permanent summary 4679c1a2fdbe298d04925a098be0b60e3d2f0fdb

Scientific protocol was unchanged by rerun.

## POPANE-R4 crossed uncertainty

Protocol:
- 2a045859843682738ecc30f2919b978daa8e9dca
Analysis:
- 316d061bb28b3ea18293071acf1ae32f04dead9e
Workflow:
- d8d4cad46eda79fc40cde653ad91974a736d9ff6
Trigger:
- a785e01c726e4aa9335a4607eff24a4ae058cb35
Run:
- 37267984382
Artifact:
- 11327433516
- SHA256 0cb68c756168fc78bc5fb07e39308afdf7b76d44b28f682fc661509d7a945eb4
Permanent summary:
- df649067b667167e197dec0d91a251f96c619f49

## POPANE-R3 technical history

Scientific protocol remains:
- 8e2fb4e00a4dfeaed358b651d8e7570ceab6d1b4

Two runs failed during result summarization because a prediction column named "shift" collided with pandas DataFrame.shift attribute access:
- run 37267700807; failure audit c012e55561319181f9e7682887ff3eb7b0eaafc3
- run 37268391855; failure audit 2d1611d4765d34d3c6f6f323f7265b54740b3494

Corrections:
- 6b3819d22351ea885d748b2c5fc6f76d67f9650b
- b2a68bad26f09eeb5a8395e049da97ed3c8ceebf

Both corrections change explicit column access only.
Third rerun:
- trigger 4cab68f9796f3e7482023698c94680ae219c75dd
- run 37269068756
- outcome pending at this ledger version.

## POPANE-R5

Pre-authorized family-ablation sensitivity:
- protocol 2d4a8d2c2b8e511761415074f688bdb38cad3eda
- analysis 4d2ad2a6962189b8e3aacc6039695d5898db7660
- workflow c2d415ac032e456ba5f4525bbea0ba41b9f8ccc9
- trigger dda3377b47f2a2aae16cae092ca74cf9ae90aad1
- run 37268598144
- outcome pending at this ledger version.

## Reproducibility verdict

Core evidence chain: PASS.
- public or documented dataset provenance;
- frozen protocol commits;
- versioned analysis/workflow commits;
- immutable GitHub Actions run IDs and artifact digests;
- permanent compact result snapshots;
- technical failures preserved rather than erased;
- raw licensed data not redistributed;
- dependency version bounds and Python runtime recorded.

Before final manuscript submission:
1. update this ledger with R3/R5 final artifacts/summary commits;
2. generate a machine-readable manifest of all claim-supporting commits/runs/artifacts;
3. cite dataset licenses and exact data-release versions in Methods/Data Availability;
4. expose enough code/configuration that an independent researcher can reproduce from the source datasets.
