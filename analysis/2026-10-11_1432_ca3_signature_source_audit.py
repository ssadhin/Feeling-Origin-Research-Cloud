#!/usr/bin/env python3
"""NONBLIND SOURCE AUDIT ONLY; never substitute for participant-level reanalysis.
Usage: python ca3_signature_source_audit.py path/to/signatures.ipynb
Pinned source: pni-lab/placebo-conditioning-meta-analysis@475672df1e6156eb10b6d0d755e5901ae09a9460
"""
import hashlib
import json
import math
import re
import sys

PINNED_BLOB_SHA = "173eae4c216008a17c3c789100133a043be5316d"

def main(path):
    raw = open(path, "rb").read()
    git_blob_sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert git_blob_sha == PINNED_BLOB_SHA, f"Source mismatch: {git_blob_sha}"
    nb = json.loads(raw)
    c = nb["cells"][7]
    src = "".join(c["source"])
    assert "plc_induction * Rating_diff" in src
    assert "n_iterations = 10000" in src
    assert "np.mean(bootstrap_tscores>0, axis=0)" in src
    assert "sample = resample(data)" in src
    outputs = c["outputs"]
    ols = next("".join(o["text"]) for o in outputs if o.get("output_type") == "stream" and "OLS Regression Results" in "".join(o.get("text", [])))
    tab = next("".join(o["data"]["text/plain"]) for o in outputs if "text/plain" in o.get("data", {}) and "p_boot" in "".join(o["data"]["text/plain"]))
    assert "No. Observations:                              409" in ols
    assert "Df Residuals:                                  388" in ols
    match = re.search(r"plc_induction:Rating_diff\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", tab)
    assert match, "Cannot find archived interaction bootstrap row"
    sign_tail, ci_low, ci_high = map(float, match.groups())
    assert (sign_tail, ci_low, ci_high) == (0.0320, -0.000350, 0.000011)
    try:
        from scipy.stats import t
        parametric_p_two = float(2*t.sf(1.825,388))
    except ImportError:
        parametric_p_two = None
    print(json.dumps({
        "pinned_blob_sha": git_blob_sha,
        "observations":409, "df_residual":388,
        "ols_interaction_t_rounded":-1.825,
        "ols_two_sided_p_from_scipy":parametric_p_two,
        "archived_bootstrap_sign_tail":sign_tail,
        "diagnostic_doubled_tail_not_a_formal_null_test":2*min(sign_tail,1-sign_tail),
        "archived_percentile_95ci":[ci_low,ci_high],
        "archived_95ci_includes_zero":ci_low <= 0 <= ci_high,
        "published_fig6_p_labeled_two_tailed":0.034,
        "published_fig6_ci":[-0.0004,-0.00001],
        "caution":"No raw data or independent final-paper rerun; source-to-paper discrepancy not adjudicated."
    },indent=2))
if __name__ == "__main__":
    if len(sys.argv)!=2: raise SystemExit(__doc__)
    main(sys.argv[1])
