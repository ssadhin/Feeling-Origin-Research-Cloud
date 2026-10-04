from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

IN = Path("results_snapshots/o002_feature_rows_run-37217735818.jsonl")
OUT = Path("results")
ALPHAS = [0.1, 1.0, 10.0, 100.0, 1000.0]
NBOOT = 5000

def bootstrap(vals, seed):
    vals = np.asarray(vals, float)
    rng = np.random.default_rng(seed)
    z = np.asarray([np.mean(rng.choice(vals, size=len(vals), replace=True)) for _ in range(NBOOT)])
    return {
        "mean": float(np.mean(vals)),
        "ci95": [float(np.percentile(z, 2.5)), float(np.percentile(z, 97.5))]
    }

def prepare_rows():
    df = pd.read_json(IN, lines=True)
    df = df.sort_values(["subject", "video_id", "time_norm"]).reset_index(drop=True)
    for target in ("valence", "arousal"):
        base = "prior_" + target
        df[base + "_lag0"] = df[base]
        df[base + "_lag1"] = df.groupby(["subject", "video_id"], sort=False)[base].shift(1)
        df[base + "_lag2"] = df.groupby(["subject", "video_id"], sort=False)[base].shift(2)
    # Common complete-case set so model comparisons use exactly the same target rows.
    needed = [
        "prior_valence_lag0","prior_valence_lag1","prior_valence_lag2",
        "prior_arousal_lag0","prior_arousal_lag1","prior_arousal_lag2"
    ]
    return df.dropna(subset=needed).reset_index(drop=True)

def feature_spec(target, name, phys):
    cat = ["video_id"]
    num = ["time_norm"]
    if name != "context_only":
        lag = name[-1]  # names end in lag0/lag1/lag2
        num.append(f"prior_{target}_lag{lag}")
    if name.startswith("phys_"):
        num += phys
    return cat, num

def make_preprocess(target, name, phys):
    cat, num = feature_spec(target, name, phys)
    return ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat),
        ("num", Pipeline([
            ("imp", SimpleImputer(strategy="median")),
            ("sc", StandardScaler())
        ]), num),
    ], sparse_threshold=0.0)

def fit_tuned(train, test, target, name, phys):
    ycol = "y_" + target
    groups = train.subject.to_numpy()
    cv = GroupKFold(n_splits=min(5, len(np.unique(groups))))
    scores = {a: [] for a in ALPHAS}
    for it, iv in cv.split(train, train[ycol], groups):
        A = train.iloc[it]
        B = train.iloc[iv]
        pp = make_preprocess(target, name, phys)
        xa = pp.fit_transform(A)
        xb = pp.transform(B)
        ya = A[ycol].to_numpy(float)
        yb = B[ycol].to_numpy(float)
        for a in ALPHAS:
            pred = Ridge(alpha=a).fit(xa, ya).predict(xb)
            scores[a].append(mean_absolute_error(yb, pred))
    best = min(ALPHAS, key=lambda a: (float(np.mean(scores[a])), a))
    pp = make_preprocess(target, name, phys)
    xa = pp.fit_transform(train)
    xb = pp.transform(test)
    pred = Ridge(alpha=best).fit(xa, train[ycol].to_numpy(float)).predict(xb)
    return pred, best

def main():
    OUT.mkdir(exist_ok=True)
    df = prepare_rows()
    phys = sorted(c for c in df.columns if c.startswith("phys_"))
    subjects = sorted(df.subject.unique())
    specs = [
        "context_only",
        "prior_lag0","prior_lag1","prior_lag2",
        "phys_lag0","phys_lag1","phys_lag2"
    ]
    if len(subjects) != 30 or len(phys) != 29:
        raise RuntimeError(f"Unexpected frozen data shape subjects={len(subjects)} phys={len(phys)}")
    counts = df.groupby("subject").size()
    if int((counts >= 20).sum()) < 24:
        raise RuntimeError("Insufficient common lag-depth rows")

    result = {
        "status": "O002_H1_PRIOR_LAG_DEPTH",
        "protocol": "protocols/o002_h1_prior_lag_depth.json",
        "source_snapshot": str(IN),
        "n_rows_common": int(len(df)),
        "n_subjects": int(len(subjects)),
        "n_phys_features": int(len(phys)),
        "targets": {},
        "firewall": "Robustness/measurement-inertia attack only; no causal or phenomenal inference."
    }

    for ti, target in enumerate(("valence","arousal")):
        subject_mae = {s: {} for s in subjects}
        pooled_y = []
        pooled_pred = {spec: [] for spec in specs}
        chosen_alphas = {spec: [] for spec in specs}

        for si, sub in enumerate(subjects, 1):
            print(f"{target} subject {si}/{len(subjects)} {sub}", flush=True)
            tr = df[df.subject != sub].reset_index(drop=True)
            te = df[df.subject == sub].reset_index(drop=True)
            y = te["y_" + target].to_numpy(float)
            pooled_y.extend(y.tolist())
            for spec in specs:
                pred, alpha = fit_tuned(tr, te, target, spec, phys)
                mae = float(mean_absolute_error(y, pred))
                subject_mae[sub][spec] = mae
                pooled_pred[spec].extend(pred.tolist())
                chosen_alphas[spec].append({"subject": sub, "alpha": alpha})

        Y = np.asarray(pooled_y)
        metrics = {}
        for spec in specs:
            P = np.asarray(pooled_pred[spec])
            metrics[spec] = {
                "mae": float(mean_absolute_error(Y, P)),
                "mean_subject_mae": float(np.mean([subject_mae[s][spec] for s in subjects])),
                "pearson_r": float(np.corrcoef(Y, P)[0,1]) if np.std(P) > 0 and np.std(Y) > 0 else None
            }

        persistence_depth = {}
        physiology_increment = {}
        for lag in (0,1,2):
            persistence_depth[f"lag{lag}"] = bootstrap(
                [subject_mae[s]["context_only"] - subject_mae[s][f"prior_lag{lag}"] for s in subjects],
                81000 + 10*ti + lag
            )
            physiology_increment[f"lag{lag}"] = bootstrap(
                [subject_mae[s][f"prior_lag{lag}"] - subject_mae[s][f"phys_lag{lag}"] for s in subjects],
                82000 + 10*ti + lag
            )
        immediate_advantage = bootstrap(
            [subject_mae[s]["prior_lag1"] - subject_mae[s]["prior_lag0"] for s in subjects],
            83000 + ti
        )

        lag0_pos = persistence_depth["lag0"]["ci95"][0] > 0
        lag1_pos = persistence_depth["lag1"]["ci95"][0] > 0
        lag2_pos = persistence_depth["lag2"]["ci95"][0] > 0
        phys_pos = {lag: physiology_increment[lag]["ci95"][0] > 0 for lag in ("lag0","lag1","lag2")}

        if lag0_pos and not lag1_pos and not lag2_pos:
            persistence_verdict = "NEAR_REPORT_ONLY"
        elif lag1_pos or lag2_pos:
            persistence_verdict = "PERSISTENCE_BEYOND_IMMEDIATE_REPORT"
        else:
            persistence_verdict = "NO_CLEAR_PRIOR_REPORT_ADVANTAGE"

        if (not phys_pos["lag0"]) and (phys_pos["lag1"] or phys_pos["lag2"]):
            physiology_verdict = "PHYSIOLOGY_EMERGES_WITH_OLDER_PRIOR"
        elif not any(phys_pos.values()):
            physiology_verdict = "NO_PHYSIOLOGY_INCREMENT_ACROSS_LAGS"
        else:
            physiology_verdict = "PHYSIOLOGY_INCREMENT_PATTERN_MIXED"

        result["targets"][target] = {
            "metrics": metrics,
            "persistence_depth": persistence_depth,
            "immediate_advantage_lag1_minus_lag0": immediate_advantage,
            "physiology_increment": physiology_increment,
            "persistence_verdict": persistence_verdict,
            "physiology_verdict": physiology_verdict,
            "subject_mae": subject_mae,
            "chosen_alphas": chosen_alphas
        }

    result["overall"] = {
        "persistence_verdicts": {t:v["persistence_verdict"] for t,v in result["targets"].items()},
        "physiology_verdicts": {t:v["physiology_verdict"] for t,v in result["targets"].items()}
    }
    (OUT/"o002_h1_prior_lag_depth.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "n_rows_common": result["n_rows_common"],
        "overall": result["overall"],
        "summary": {
            t: {
                "persistence_depth": v["persistence_depth"],
                "immediate_advantage": v["immediate_advantage_lag1_minus_lag0"],
                "physiology_increment": v["physiology_increment"]
            } for t,v in result["targets"].items()
        }
    }, indent=2))

if __name__ == "__main__":
    main()
