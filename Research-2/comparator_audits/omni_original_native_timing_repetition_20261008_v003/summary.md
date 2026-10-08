# Research #2 — OmniScientist-V2 native timing reproducibility (v003)

**2026-10-08, exploratory/nondecisive, source unchanged.**

## Design
- Upstream: `tsinghua-fib-lab/OmniScientist-V2`, frozen checkout `1cbb9f6f6d793290326ca29df4d389fb64832f91`.
- Tested original `cli/tests/agent/test_paper_review_engine.py` without modifying tests or contestant implementation; source SHA-256 `62daaf6f03c13a9ac1e5ea59d7edf83a730874098ed66e10e13789f452b874d8`.
- Runner: original isolated `omni312` Python 3.12 venv, `python -B -m pytest -q -p no:cacheprovider tests/agent/test_paper_review_engine.py`.
- Three additional consecutive attempts, with per-process-tree sampled peak RSS and CPU time; nondecisive, resource measures descriptive only. No actual provider calls; existing mocked upstream tests.
- Original Git checkout clean before and after all three repetitions.

## Results
| Run | Native results | Wall-clock s | Peak RSS MB | Sampled CPU s |
|---|---|---:|---:|---:|
| v003/run001 | 31 pass, 0 fail | 10.590 | 140.76 | 8.688 |
| v003/run002 | 31 pass, 0 fail | 10.805 | 140.95 | 9.156 |
| v003/run003 | 31 pass, 0 fail | 10.098 | 141.28 | 9.109 |

Previous archived measurements:
- v001/run001 original suite 30 passed, 1 failed, where upstream concurrency timing expected positive three-way overlap but observed 0.0; source clean.
- v002/run002 original suite 31 passed, 0 failed; source clean.
- Combined five runs: **4 fully passing / 1 partially failing**. This is NOT a statistically justified failure-rate estimate and is **not** an AES versus Omni head-to-head result.

## Interpretation
Observed instability is **intermittent native timing-test reproducibility**, not evidence that the rival research methodology is inferior. The three new passes do not erase the earlier failure. Native runtime unit tests do not certify full execution fidelity, independent knowledgeable defense, frozen equal-resource action parity, prospective benchmark calibration, or OOD validity.

**Scientific state unchanged:** 6 source snapshots pinned, full faithful original-behavior certifications 0/6, decisive prospective AES v2 trials 0. AES v2 could win, lose, tie, or remain underdetermined when properly tested.

## Next scientifically meaningful step
For OmniScientist's original source, inspect the timing-dependent three-way overlap assertion and async scheduler assumptions, record additional reproduction evidence only if needed for a predeclared stability gate, then advance the **19C/19G/19H behavioral sentinel and independent defender** fidelity gates across all six rivals. Do not keep running unit tests merely to accumulate green checks, and never adjust frozen decisive criteria after evidence.

## Provenance
Four raw artifacts in this same immutable GitHub directory: `prerun_metadata.json`, `run001.json`, `run002.json`, `run003.json`.
Home PC local originals under `G:\My Drive\Consciousness Formula Research\09_Checkpoints\OmniV2_native_timing_20261008_v003`.
Existing prior records and their immutable hashes remain archived in v001/v002.
