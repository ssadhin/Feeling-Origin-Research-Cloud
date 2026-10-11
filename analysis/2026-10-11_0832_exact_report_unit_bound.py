#!/usr/bin/env python3
"""NONBLIND methods QA: exact McNemar lower bounds, not a participant-data analysis."""
from math import comb
from scipy.stats import binomtest, chi2
for n in range(1,13):
    two = binomtest(0,n,0.5,alternative="two-sided").pvalue
    one = binomtest(0,n,0.5,alternative="less").pvalue
    assert abs(two-min(1,2.0**(1-n))) < 1e-12
    assert abs(one-2.0**(-n)) < 1e-12
    print(n, f"{two:.10f}", f"{one:.10f}")
print("uncorrected chi2 n9 extreme",chi2.sf(9,1))
