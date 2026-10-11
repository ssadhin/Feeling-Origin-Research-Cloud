"""Nonblind eligibility/feasibility calculation; NOT a participant-level analysis.
2026-10-11 Asia/Dhaka. Requires scipy. No external data are read.
Reference: Arulpragasam et al., medRxiv 2026-09-20, DOI 10.64898/2026.09.18.26363360.
"""
from math import sqrt
from scipy.stats import t

def ci90_halfwidth_in_paired_difference_sd(n):
    """Half-width of paired-mean two-sided 90% t CI, in SD of paired differences."""
    return t.ppf(0.95, n - 1) / sqrt(n)

if __name__ == "__main__":
    for n in (9, 10, 31, 32):
        print(f"n={n} halfwidth={ci90_halfwidth_in_paired_difference_sd(n):.6f}")
    min_n = next(n for n in range(2, 10000)
                 if ci90_halfwidth_in_paired_difference_sd(n) < 0.30)
    print(f"minimum_n_for_90pct_CI_halfwidth_below_0.30_SDdiff={min_n}")
    assert min_n == 32
    assert abs(ci90_halfwidth_in_paired_difference_sd(9)-0.619849) < 1e-6
    # This is a feasibility bound conditional on SDdiff-standardized equivalence.
    # It does not estimate any actual cognitive, sensory, or affect outcome.
