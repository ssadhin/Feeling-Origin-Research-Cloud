"""R2 PRE-FREEZE paired-cluster uncertainty development sentinel.
Independent sampling unit: task family / generator cluster, NOT individual task.
Equal cluster weighting is exploratory and must be explicitly chosen/frozen later.
"""
from __future__ import annotations
import random, math, json, unittest

def _check(clusters):
    if not isinstance(clusters,(list,tuple)) or len(clusters)<2:
        raise ValueError("At least 2 independent clusters required")
    clean=[]
    for group in clusters:
        if not isinstance(group,(list,tuple)) or not group:raise ValueError("Empty cluster")
        out=[]
        for item in group:
            if not isinstance(item,tuple) or len(item)!=2 or any(type(x)!=int or x not in (0,1) for x in item):
                raise ValueError("Require same-task paired binary correctness")
            out.append(item[0]-item[1])
        clean.append(sum(out)/len(out))
    return clean

def ci(clusters,reps=2001,seed=41,alpha=.05):
    means=_check(clusters)
    if type(reps)!=int or reps<50 or not 0<alpha<1:raise ValueError("Bad interval settings")
    rng=random.Random(seed);k=len(means)
    boot=sorted(sum(means[rng.randrange(k)] for _ in range(k))/k for j in range(reps))
    low=boot[max(0,int((alpha/2)*(reps-1)))]
    high=boot[min(reps-1,int((1-alpha/2)*(reps-1)))]
    return {"effect":sum(means)/k,"lower":low,"upper":high,"clusters":k,
            "cluster_weighting":"equal","method":"percentile bootstrap DEVELOPER ONLY",
            "margin_validated":False,"decisive":False}

class TestClusterGuard(unittest.TestCase):
    def test_positive_constant(self):
        x=ci([[(1,0)]*6,[(1,0)]*4])
        self.assertEqual((x["effect"],x["lower"],x["upper"]),(1,1,1))
    def test_zero_constant(self):
        x=ci([[(1,1)]*6,[(0,0)]*4])
        self.assertEqual((x["effect"],x["lower"],x["upper"]),(0,0,0))
    def test_cross_family_reversal(self):
        x=ci([[(1,0)]*10,[(1,0)]*12,[(0,1)]*7,[(0,1)]*12])
        self.assertTrue(x["lower"]<=0<=x["upper"])
    def test_reproducible_seed(self):
        x=[[(1,0)],[(0,1)],[(1,1)]]
        self.assertEqual(ci(x,seed=31),ci(x,seed=31))
    def test_permutation_inside_cluster(self):
        groups=[[(1,0),(0,1),(1,0)],[(1,1),(0,1)]]
        self.assertEqual(ci(groups),ci([list(reversed(x)) for x in groups]))
    def test_no_silent_empty_cluster(self):
        with self.assertRaises(ValueError):ci([[(1,0)],[]])
    def test_requires_two_clusters(self):
        with self.assertRaises(ValueError):ci([[(1,0)]])
    def test_bool_excluded(self):
        with self.assertRaises(ValueError):ci([[(True,False)],[(0,1)]])
    def test_missing_pair_excluded(self):
        with self.assertRaises(ValueError):ci([[(1,0)],[(1,)]])
    def test_unequal_cluster_naive_weighting_trap(self):
        groups=[[(1,0)]*100]+[[(0,1)] for _ in range(9)]
        x=ci(groups)
        naive=sum(a-b for group in groups for a,b in group)/sum(len(g) for g in groups)
        self.assertLess(x["effect"],0)
        self.assertGreater(naive,0)
        self.assertEqual(x["clusters"],10)
    def test_no_nonzero_margin_claim(self):
        self.assertFalse(ci([[(1,0)],[(1,0)]])["margin_validated"])
if __name__=="__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(TestClusterGuard)
    result=unittest.TextTestRunner(verbosity=0).run(suite)
    print(json.dumps({"kind":"R2_CLUSTER_BOOTSTRAP_DEVELOPMENT","passed":result.testsRun-len(result.failures)-len(result.errors),"total":result.testsRun,"nonzero_SESOI_inference":"NOT_VALIDATED","cluster_scheme":"UNFROZEN","real_Aes_results":0},indent=2))
    if not result.wasSuccessful():raise SystemExit(2)
