from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

FEATURES = Path("results/o002_feature_rows.jsonl")
PRIMARY = Path("results_snapshots/case-external-replication-o002-run-37217735818.json")
OUT = Path("results")
N_PERM = 200
N_BOOT = 5000
SEED_BASE = 73000

def make_preprocess(target: str, phys: list[str]) -> ColumnTransformer:
    return ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["video_id"]),
        ("time", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), ["time_norm"]),
        ("prior", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), ["prior_" + target]),
        ("phys", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), phys),
    ], sparse_threshold=0.0)

def alpha_map(primary: dict, target: str) -> dict[str, float]:
    rows = primary["analysis"]["targets"][target]["chosen_alphas"]["peripheral"]
    return {str(r["subject"]): float(r["alpha"]) for r in rows}

def circular_shift_phys(df: pd.DataFrame, phys: list[str], rng: np.random.Generator) -> pd.DataFrame:
    out = df.copy()
    # Sort each sequence by time but assign back to original row positions.
    for (_, _), idx in df.groupby(["subject", "video_id"], sort=True).groups.items():
        idx = list(idx)
        if len(idx) < 2:
            continue
        idx_sorted = sorted(idx, key=lambda i: float(df.at[i, "time_norm"]))
        n = len(idx_sorted)
        if n >= 5:
            candidates = np.arange(2, n - 1, dtype=int)  # 2..n-2
        elif n == 4:
            candidates = np.array([2], dtype=int)
        else:
            candidates = np.arange(1, n, dtype=int)
        k = int(rng.choice(candidates))
        vals = df.loc[idx_sorted, phys].to_numpy(copy=True)
        out.loc[idx_sorted, phys] = np.roll(vals, shift=k, axis=0)
    return out

def bootstrap_subject(vals: list[float], seed: int) -> dict:
    x = np.asarray(vals, float)
    rng = np.random.default_rng(seed)
    z = np.asarray([np.mean(rng.choice(x, size=len(x), replace=True)) for _ in range(N_BOOT)])
    return {
        "mean": float(np.mean(x)),
        "ci95": [float(np.percentile(z, 2.5)), float(np.percentile(z, 97.5))],
    }

def main():
    OUT.mkdir(exist_ok=True)
    df = pd.read_json(FEATURES, lines=True)
    primary = json.loads(PRIMARY.read_text(encoding="utf-8"))
    phys = sorted(c for c in df.columns if c.startswith("phys_"))
    subjects = sorted(df.subject.unique())
    if len(subjects) != 30 or len(phys) != 29:
        raise RuntimeError(f"Frozen O002 shape mismatch: subjects={len(subjects)} phys={len(phys)}")

    # Pre-generate deterministic autocorrelation-preserving time-misaligned datasets.
    shifted = []
    for p in range(N_PERM):
        rng = np.random.default_rng(SEED_BASE + p)
        shifted.append(circular_shift_phys(df, phys, rng))
    result = {
        "status": "O002_P1_TEMPORAL_ALIGNMENT_PERMUTATION",
        "protocol": "protocols/o002_p1_temporal_alignment_permutation.json",
        "parent_primary_run": 37217735818,
        "parent_sensitivity_run": 37218283683,
        "n_permutations": N_PERM,
        "shift_control": "within-subject x within-video circular shift of full 29-feature physiology vector",
        "targets": {},
        "firewall": "Post-primary mechanistic sensitivity only; no causal, phenomenal-identity, or consciousness inference.",
    }

    any_positive = False
    any_negative = False
    for ti, target in enumerate(("valence", "arousal")):
        amap = alpha_map(primary, target)
        real_subject_mae = {}
        shifted_subject_mae = {s: [] for s in subjects}
        primary_subject_mae = primary["analysis"]["targets"][target]["subject_mae"]

        for si, sub in enumerate(subjects, 1):
            print(f"{target} subject {si}/{len(subjects)} {sub}", flush=True)
            tr_mask = df.subject != sub
            te_mask = ~tr_mask
            tr = df.loc[tr_mask].reset_index(drop=True)
            te = df.loc[te_mask].reset_index(drop=True)
            ytr = tr["y_" + target].to_numpy(float)
            yte = te["y_" + target].to_numpy(float)
            alpha = amap[sub]

            pp = make_preprocess(target, phys)
            xtr = pp.fit_transform(tr)
            xte = pp.transform(te)
            pred = Ridge(alpha=alpha).fit(xtr, ytr).predict(xte)
            rmae = float(mean_absolute_error(yte, pred))
            real_subject_mae[sub] = rmae

            frozen_mae = float(primary_subject_mae[sub]["peripheral"])
            if abs(rmae - frozen_mae) > 1e-9:
                raise RuntimeError(f"Real-data reproduction mismatch {target} {sub}: {rmae} vs {frozen_mae}")

            # Fit every shifted condition using the exact same alpha and preprocessing rule.
            for p, sdf in enumerate(shifted):
                strn = sdf.loc[tr_mask].reset_index(drop=True)
                sten = sdf.loc[te_mask].reset_index(drop=True)
                # Because circular shifts preserve training-fold feature distributions exactly,
                # reuse the frozen real-data-fitted transformer; only row alignment changes.
                sxtr = pp.transform(strn)
                sxte = pp.transform(sten)
                spred = Ridge(alpha=alpha).fit(sxtr, ytr).predict(sxte)
                shifted_subject_mae[sub].append(float(mean_absolute_error(yte, spred)))

        subj_delta = []
        subject_summary = {}
        for sub in subjects:
            arr = np.asarray(shifted_subject_mae[sub], float)
            d = float(np.mean(arr) - real_subject_mae[sub])
            subj_delta.append(d)
            subject_summary[sub] = {
                "real_mae": real_subject_mae[sub],
                "mean_shifted_mae": float(np.mean(arr)),
                "delta_shifted_minus_real": d,
            }

        primary_stat = bootstrap_subject(subj_delta, 74000 + ti)
        # Per-permutation pooled mean subject contrast for diagnostics.
        perm_means = []
        for p in range(N_PERM):
            perm_means.append(float(np.mean([
                shifted_subject_mae[sub][p] - real_subject_mae[sub] for sub in subjects
            ])))
        frac_real_better = float(np.mean(np.asarray(perm_means) > 0))

        lo, hi = primary_stat["ci95"]
        if lo > 0:
            alignment_verdict = "ALIGNED_REAL_BETTER_THAN_SHIFTED"
            any_positive = True
        elif hi < 0:
            alignment_verdict = "SHIFTED_BETTER_ANOMALY"
            any_negative = True
        else:
            alignment_verdict = "NO_ALIGNMENT_EVIDENCE"

        frozen_delta = primary["analysis"]["targets"][target]["primary_delta"]
        frozen_primary_verdict = primary["analysis"]["targets"][target]["verdict"]
        if alignment_verdict == "ALIGNED_REAL_BETTER_THAN_SHIFTED" and frozen_primary_verdict == "NO_PERIPHERAL_INCREMENT":
            interpretation = "REAL_SIGNAL_BUT_NO_INCREMENT"
        else:
            interpretation = alignment_verdict

        result["targets"][target] = {
            "alignment_verdict": alignment_verdict,
            "interpretation": interpretation,
            "primary_shifted_minus_real": primary_stat,
            "fraction_permutations_real_better": frac_real_better,
            "permutation_mean_deltas": perm_means,
            "subject_results": subject_summary,
            "frozen_o002_primary_verdict": frozen_primary_verdict,
            "frozen_o002_baseline_minus_real_delta": frozen_delta,
        }

    if any_negative:
        overall = "SHIFTED_BETTER_ANOMALY"
    elif any_positive:
        overall = "REAL_SIGNAL_BUT_NO_INCREMENT"
    else:
        overall = "NO_ALIGNMENT_EVIDENCE"
    result["verdict"] = overall
    (OUT / "o002_p1_temporal_alignment_permutation.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "verdict": overall,
        "targets": {
            t: {
                "interpretation": v["interpretation"],
                "primary": v["primary_shifted_minus_real"],
                "fraction_permutations_real_better": v["fraction_permutations_real_better"],
            } for t, v in result["targets"].items()
        }
    }, indent=2))

if __name__ == "__main__":
    main()
