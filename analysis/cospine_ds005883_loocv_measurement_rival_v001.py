#!/usr/bin/env python3
"""CoSpine ds005883: reproducible behavioral aggregates and exploratory LOOCV.
Source pinned; no causal, neural, or phenomenal inference. Stdlib only.
The aggregate was independently calculated in JS on 2026-10-08.
This standalone Python script is supplied for third-party reproduction and
was NOT executed in that run because its environment lacked outbound DNS.
"""
import csv, io, json, math, urllib.request
COMMIT = "037ed267e7f7f2024a5fe3d0e8fb4759f7f67bdd"
ROOT = "https://raw.githubusercontent.com/OpenNeuroDatasets/ds005883/" + COMMIT + "/"

def read_pairs(i):
    sid = f"sub-{i:02d}"
    url = ROOT + f"{sid}/func/{sid}_task-pain_events.tsv"
    with urllib.request.urlopen(url, timeout=45) as r:
        rows = list(csv.DictReader(io.StringIO(r.read().decode("utf-8")), delimiter="\t"))
    pain = [r for r in rows if r["trial_type"] == "pain"]
    if any(r["PR"] in ("", "n/a") or r["UpR"] in ("", "n/a") for r in pain):
        raise ValueError(f"{sid}: missing rating; no imputation permitted")
    pairs = [(float(r["PR"]), float(r["UpR"])) for r in pain]
    if len(pairs) != 15:
        raise ValueError(f"{sid}: expected 15 pain trials; found {len(pairs)}")
    return sid, pairs

def fit_linear(train, x):
    mx = sum(a for a, _ in train) / len(train)
    my = sum(b for _, b in train) / len(train)
    xx = sum((a-mx)**2 for a, _ in train)
    xy = sum((a-mx)*(b-my) for a, b in train)
    return my + (xy/xx)*(x-mx) if xx > 1e-12 else my

def subject(sid, pairs):
    n = len(pairs)
    mx = sum(x for x, _ in pairs) / n
    my = sum(y for _, y in pairs) / n
    xx = sum((x-mx)**2 for x, _ in pairs)
    yy = sum((y-my)**2 for _, y in pairs)
    xy = sum((x-mx)*(y-my) for x, y in pairs)
    bins = {}
    for x, y in pairs:
        bins.setdefault(x, []).append(y)
    cond_sse = sum(sum((y-sum(v)/len(v))**2 for y in v) for v in bins.values())
    sse_A = sse_B = sse_C = 0.0
    fallbacks = 0
    for j, (x, y) in enumerate(pairs):
        train = pairs[:j] + pairs[j+1:]
        a = sum(v for _, v in train) / len(train)
        b = fit_linear(train, x)
        matches = [v for u, v in train if u == x]
        if matches:
            c = sum(matches) / len(matches)
        else:
            c = b
            fallbacks += 1
        sse_A += (y-a)**2
        sse_B += (y-b)**2
        sse_C += (y-c)**2
    return dict(subject=sid, n=n, ss_x=xx, ss_y=yy, sp=xy,
                conditional_sse=cond_sse,
                linear_sse=(yy-xy*xy/xx) if xx>0 else None,
                equal_pairs=sum(x==y for x,y in pairs),
                mean_difference=my-mx,
                sse_A=sse_A, sse_B=sse_B, sse_C=sse_C,
                bin_fallbacks=fallbacks)

def main():
    s = [subject(*read_pairs(i)) for i in range(1,40)]
    total = lambda k: sum(z[k] for z in s)
    n, xx, yy, xy = total("n"), total("ss_x"), total("ss_y"), total("sp")
    a,b,c = total("sse_A"),total("sse_B"),total("sse_C")
    out = dict(source_commit=COMMIT, subjects=len(s), trials=n,
        ss_x=xx, ss_y=yy, cross_product=xy,
        centered_correlation=xy/math.sqrt(xx*yy),
        common_slope_residual_fraction=(yy-xy*xy/xx)/yy,
        person_slope_residual_fraction=total("linear_sse")/yy,
        exact_bin_residual_fraction=total("conditional_sse")/yy,
        equal_pairs=total("equal_pairs"),
        mean_difference=sum(z["mean_difference"]*z["n"] for z in s)/n,
        mse_A=a/n, mse_B=b/n, mse_C=c/n,
        rmse_A=math.sqrt(a/n),rmse_B=math.sqrt(b/n),rmse_C=math.sqrt(c/n),
        linear_vs_mean_improvement=1-b/a,
        bin_vs_linear_improvement=1-c/b,
        linear_subject_wins=sum(z["sse_B"]<z["sse_A"]-1e-9 for z in s),
        bin_subject_wins=sum(z["sse_C"]<z["sse_B"]-1e-9 for z in s),
        bin_subject_losses=sum(z["sse_C"]>z["sse_B"]+1e-9 for z in s),
        bin_fallback_trials=total("bin_fallbacks"),
        jackknife_bin_worse_all=sum(c-b-(z["sse_C"]-z["sse_B"])>0 for z in s)==len(s),
        per_subject=s)
    print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
