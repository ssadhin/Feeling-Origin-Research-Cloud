# Adaptive Epistemic Search — Methodology Benchmark v001

This directory is the executable companion to the Google Drive meta-research canon.

## What v001 tests

Equal-budget research policies are evaluated in hidden-ground-truth synthetic research worlds. The worlds plant failure modes including missing hypotheses, confounds, observational mimics, non-identifiability, intervention-only identifiability, parameter fragility, analytic flexibility, weak-null/equivalence traps, OOD failures, circular metrics, software bugs, hybrid truths, overcomplexity, re-evaluation drift, ancestor recovery, surprise distractors, myopic information gain, and shared analyst bias.

Policies receive only `PublicState`. Hidden truth and world-class mechanics stay inside `Environment`.

## Development firewall

The normal CLI and GitHub Actions workflow expose only:

- `train`
- `validation`

The locked test and OOD meta-test seed blocks exist in code/config but are intentionally unavailable through the development workflow. A separate locked-test workflow must be created only after policy definitions, metrics, equivalence margins, and decision rules are frozen.

## Policies

P0 one-pass  
P1 preregistered confirmatory  
P2 Bayesian-workflow analogue  
P3 strong inference  
P5 recursive tournament  
P6 tournament + MIST  
P7 full fixed verification stack  
P8 Adaptive Epistemic Search  
P9 minimal adaptive  
P10 diversity/hierarchical search  
P11 surprise/MCTS analogue  
P12 parallel independent lanes

## Run locally

```bash
python meta_methodology/benchmark_v001.py --self-test
python meta_methodology/benchmark_v001.py --split validation --n-per-class 250 \
  --output results/methodology_v001_validation.csv \
  --summary results/methodology_v001_validation_summary.json
```

## Claim ceiling

TRAIN/VALIDATION results are development evidence only. Even a strong result cannot justify “best scientific method.” At minimum, locked TEST, OOD meta-test, benchmark red-team/ablation, and external real-case/domain validation are required.
