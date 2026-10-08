"""R2 six-comparator pre-freeze paired-binary N planning sensitivity.

NOT a frozen N or SESOI. Uses normal approximation and conservative
Bonferroni alpha for a six-way Holm family. Exact/clustered simulation
still required before a preregistered task count can be chosen.
"""
from math import ceil
from statistics import NormalDist
import json, unittest
NORM=NormalDist()
ALPHA_FAMILY=0.025
GLOBAL_RIVALS=6
POWER=0.90
def n_approx(q,d,m=GLOBAL_RIVALS,alpha_family=ALPHA_FAMILY,power=POWER):
    assert 0<abs(d)<=q<=1 and m>=1 and 0<alpha_family<1
    z_alpha=NORM.inv_cdf(1-alpha_family/m)   # single-sided family bound
    z_power=NORM.inv_cdf(power)
    return ceil(((z_alpha+z_power)**2)*q/(d*d))
def cluster_design_effect(m,icc):
    assert m>=1 and 0<=icc<1
    return 1+(m-1)*icc
def rows():
    out=[]
    for q in (0.10,0.20,0.30):
        for d in (0.02,0.03,0.05):
            if d<=q:
                n=n_approx(q,d)
                out.append({"discordance_q":q,"accuracy_SESOI_scenario":d,
                            "six_comparator_N_approx":n,
                            "cluster_m4_ICC02_N_sensitivity":ceil(n*cluster_design_effect(4,0.20))})
    return out
class PowerDevelopmentTests(unittest.TestCase):
    def test_more_rivals_cost_power(self):
        self.assertGreater(n_approx(.2,.03,6),n_approx(.2,.03,5))
    def test_smaller_effect_more_tasks(self):
        self.assertGreater(n_approx(.2,.02),n_approx(.2,.05))
    def test_more_discordance_more_tasks(self):
        self.assertGreater(n_approx(.3,.03),n_approx(.1,.03))
    def test_cluster_penalty(self):
        self.assertEqual(cluster_design_effect(4,.2),1.6)
    def test_development_not_fixed(self):
        self.assertEqual(len(rows()),9)
if __name__=="__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(PowerDevelopmentTests)
    result=unittest.TextTestRunner(verbosity=0).run(suite)
    print(json.dumps({"status":"DEVELOPMENT_SENSITIVITY_ONLY","source_rule":"21A/21C/21D proposals",
      "alpha_family_one_sided_candidate":ALPHA_FAMILY,"rival_count_candidate":GLOBAL_RIVALS,
      "power_candidate":POWER,"p_values_or_results_observed":False,"SESOI_frozen":False,
      "N_frozen":False,"tests_passed":result.testsRun-len(result.failures)-len(result.errors),
      "tests_total":result.testsRun,"rows":rows()},indent=2))
    assert result.wasSuccessful()
