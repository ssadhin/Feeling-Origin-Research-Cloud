# Feeling Origin Research — Cloud Compute

Private, manual-only GitHub Actions compute backend for the Feeling Origin / CRFI research program.

## Safety / cost controls
- Workflows run only with workflow_dispatch (no automatic runs on push).
- Jobs have a hard 45-minute timeout.
- No paid external services are required by the workflow.
- Results are uploaded as workflow artifacts.

## Workloads
- smoke: environment + NumPy compute test.
- core: current lightweight CRFI simulation suite.
- ablation: CRFI parameter-sweep ablation test with configurable trial count.

This repository is compute infrastructure, not a claim that the simulations themselves are conscious.
