#!/usr/bin/env python3
"""Nonblind source-code sanity checks only; NOT participant data."""
import json
from scipy.stats import t
df, statistic = 409, -1.83
p_two = float(2 * t.sf(abs(statistic), df))
p_one = float(t.sf(abs(statistic), df))
null = [0.2, 0.5, 0.8, 1.2]
def p_as_written(observed):
    return sum(x > observed for x in null) / len(null)
def p_abs(observed):
    return sum(x > abs(observed) for x in null) / len(null)
ks = [0.03, 0.08, 0.02]
out = {"student_t_two":p_two,"student_t_one":p_one,
       "negative_signed_fwer":p_as_written(-1.0),
       "negative_abs_fwer":p_abs(-1.0),
       "positive_signed_fwer":p_as_written(1.0),
       "ks_selected_by_max":max(ks),"ks_minimum":min(ks)}
assert abs(p_two - 0.06797759659467753) < 1e-12
assert abs(p_one - 0.033988798297338765) < 1e-12
assert out["negative_signed_fwer"] == 1.0
assert out["negative_abs_fwer"] == 0.25
assert out["ks_selected_by_max"] == 0.08
print(json.dumps(out, sort_keys=True, indent=2))
