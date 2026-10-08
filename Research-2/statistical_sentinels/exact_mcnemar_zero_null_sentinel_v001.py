"""R2 exact paired-binary discordance ZERO-NULL sentinel (development only).

Deliberately does NOT test superiority over a nonzero SESOI and must not
be used alone to make a confirmatory AES superiority claim.
"""
from math import comb
import unittest,json

def exact_binomial_zero_null(n10,n01,alternative="two-sided"):
    if type(n10)!=int or type(n01)!=int or n10<0 or n01<0:
        raise ValueError("Nonnegative integer discordance counts required")
    n=n10+n01
    if n==0:
        return 1.0
    total=2**n
    if alternative=="greater":  # method A correct, method B incorrect
        return sum(comb(n,k) for k in range(n10,n+1))/total
    if alternative=="less":
        return sum(comb(n,k) for k in range(0,n10+1))/total
    if alternative=="two-sided":
        k=min(n10,n01)
        return min(1.,2*sum(comb(n,j) for j in range(k+1))/total)
    raise ValueError("alternative")

def zero_null_significance_is_not_margin_superiority(p,margin):
    """Guard: exact zero-null inference cannot establish a >margin claim."""
    if margin is None or margin<=0:
        raise ValueError("Requires nonzero SESOI")
    return "ZERO_NULL_ONLY_NOT_MARGIN_TEST"

class ExactPairedChecks(unittest.TestCase):
    def test_no_discordant_pairs(self):
        self.assertEqual(exact_binomial_zero_null(0,0),1.)
    def test_exact_ten_vs_zero(self):
        self.assertAlmostEqual(exact_binomial_zero_null(10,0),2/(2**10))
    def test_single_pair_not_significant(self):
        self.assertEqual(exact_binomial_zero_null(1,0),1.)
    def test_symmetry_two_sided(self):
        self.assertEqual(exact_binomial_zero_null(7,2),exact_binomial_zero_null(2,7))
    def test_symmetry_one_sided(self):
        self.assertAlmostEqual(exact_binomial_zero_null(7,2,"greater"),exact_binomial_zero_null(2,7,"less"))
    def test_balanced_discordance(self):
        self.assertEqual(exact_binomial_zero_null(10,10),1.)
    def test_significance_not_margin(self):
        self.assertEqual(zero_null_significance_is_not_margin_superiority(0.00001,0.03),"ZERO_NULL_ONLY_NOT_MARGIN_TEST")
    def test_invalid_counts(self):
        with self.assertRaises(ValueError):exact_binomial_zero_null(-1,3)
    def test_invalid_alternative(self):
        with self.assertRaises(ValueError):exact_binomial_zero_null(3,4,"oops")
    def test_fractional_counts(self):
        with self.assertRaises(ValueError):exact_binomial_zero_null(2.5,4)
if __name__=="__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ExactPairedChecks)
    r=unittest.TextTestRunner(verbosity=0).run(suite)
    print(json.dumps({"status":"DEV_EXACT_MCNEMAR_ZERO_NULL_ONLY","passed":r.testsRun-len(r.failures)-len(r.errors),
          "total":r.testsRun,"real_policy_runs":0,
          "nonzero_margin_test":"NOT_IMPLEMENTED","clustering":"NOT_IMPLEMENTED",
          "preregistration":"NOT_FROZEN"},indent=2))
    assert r.wasSuccessful()
