#!/usr/bin/env python3
"""Reproduce CoSpine ds005883 behavioral screening. Stdlib only; network required.
Data pinned to source Git commit. No neural/causal/phenomenality claims."""
import csv, io, json, math, urllib.request
COMMIT = "037ed267e7f7f2024a5fe3d0e8fb4759f7f67bdd"
ROOT = "https://raw.githubusercontent.com/OpenNeuroDatasets/ds005883/" + COMMIT + "/"
def read_subject(i):
    sid = f"sub-{i:02d}"
    path = f"{sid}/func/{sid}_task-pain_events.tsv"
    with urllib.request.urlopen(ROOT + path, timeout=45) as r:
        txt = r.read().decode("utf-8")
    allrows = list(csv.DictReader(io.StringIO(txt), delimiter="\t"))
    pain = [r for r in allrows if r["trial_type"] == "pain"]
    pairs = [(float(r["PR"]), float(r["UpR"])) for r in pain
             if r["PR"] not in ("n/a", "") and r["UpR"] not in ("n/a", "")]
    assert len(pairs) == len(pain), (sid, "missing paired rating")
    return sid, pairs
def summarize(sid, pairs):
    n=len(pairs)
    assert n>=2, (sid, n)
    mx=sum(p for p,u in pairs)/n
    my=sum(u for p,u in pairs)/n
    xx=sum((p-mx)**2 for p,u in pairs)
    yy=sum((u-my)**2 for p,u in pairs)
    xy=sum((p-mx)*(u-my) for p,u in pairs)
    sse = yy-xy**2/xx if xx>0 else None
    groups={}
    for p,u in pairs: groups.setdefault(p,[]).append(u)
    cond_sse=sum(sum((u-sum(a)/len(a))**2 for u in a) for a in groups.values())
    return dict(subject=sid,n=n,ss_intensity=xx,ss_unpleasantness=yy,
                sp=xy,within_linear_sse=sse,conditional_sse=cond_sse,
                exact_matches=sum(p==u for p,u in pairs),
                mean_difference=my-mx,
                discordant_intensity_bins=sum(len(set(a))>1 for a in groups.values()))
def main():
    s=[summarize(*read_subject(i)) for i in range(1,40)]
    xx=sum(z["ss_intensity"] for z in s)
    yy=sum(z["ss_unpleasantness"] for z in s)
    xy=sum(z["sp"] for z in s)
    n=sum(z["n"] for z in s)
    result=dict(source_commit=COMMIT, subjects=len(s), trials=n,
        within_subject_centered_correlation=xy/math.sqrt(xx*yy),
        pooled_common_slope_residual_fraction=(yy-xy*xy/xx)/yy,
        participant_specific_slope_residual_fraction=sum(z["within_linear_sse"] for z in s)/yy,
        exact_intensity_bin_residual_fraction=sum(z["conditional_sse"] for z in s)/yy,
        equal_pairs=sum(z["exact_matches"] for z in s),
        subjects_with_nonzero_conditional_sse=sum(z["conditional_sse"]>1e-9 for z in s),
        subjects=s)
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
