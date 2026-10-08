"""Research #2 neutral claim-gate falsification; DEVELOPMENT ONLY, no AES runs.

Six global competitors are a *provisional* pre-freeze family.
All p-values and critical-family intervals supplied to tests are synthetic.
This checks logic only: it does not estimate effects, freeze SESOI, or authorize a winner.
"""
from __future__ import annotations
import math
import unittest

RIVALS=("InternAgent-1.5","OmniScientist-V2","AI-Scientist-v2",
        "EvoScientist","ResearchLoop","EvoMaster")
ALPHA=0.025
CRITICAL=("E","O")

def holm_all_reject(p, alpha=ALPHA):
    """Reject all 6 one-sided superiority nulls using Holm, only with valid p-values."""
    if not isinstance(p,dict) or set(p)!=set(RIVALS):
        return False
    vals=list(p.values())
    if any(type(v) not in (int,float) or not math.isfinite(v) or not 0<=v<=1 for v in vals):
        return False
    for i,v in enumerate(sorted(vals)):
        if v>alpha/(len(vals)-i):
            return False
    return True

def gate(p,*,fidelity,telemetry,families,intervals,models,scoped_losses=(),
         margin=None, preregistered=False):
    # This prototype fails closed: it cannot make a paper-facing claim before freeze.
    if not preregistered:
        return "NOT_AUTHORIZED_NO_PREREG"
    if not fidelity or not telemetry:
        return "BLOCKED_FIDELITY_OR_TELEMETRY"
    if margin is None or type(margin) not in (int,float) or not math.isfinite(margin) or not 0<margin<1:
        return "BLOCKED_UNFROZEN_MARGIN"
    if not isinstance(p,dict) or set(p)!=set(RIVALS):
        return "INCONCLUSIVE_COMPARATOR_COVERAGE"
    if not isinstance(models,dict) or set(models)!={"B1","B2"}:
        return "INCONCLUSIVE_MODEL_COVERAGE"
    if any(x not in ("POSITIVE","NEGATIVE","EQUIVALENT","INCONCLUSIVE") for x in models.values()):
        return "BLOCKED_MODEL_METADATA"
    if models["B1"]!=models["B2"] and {"POSITIVE","NEGATIVE"}==set(models.values()):
        return "MODEL_DEPENDENT_SIGN_REVERSAL"
    if not isinstance(families,dict) or any(x not in ("AVAILABLE","MISSING","INVALID") for x in families.values()):
        return "BLOCKED_FAMILY_METADATA"
    if any(x=="INVALID" for x in families.values()):
        return "BLOCKED_INVALID_FAMILY"
    if any(c not in families for c in CRITICAL):
        return "INCONCLUSIVE_UNDECLARED_CRITICAL_FAMILY"
    if any(c not in intervals for c in CRITICAL if families[c]=="AVAILABLE"):
        return "INCONCLUSIVE_CRITICAL_FAMILY_CI_MISSING"
    for family,ci in intervals.items():
        if family not in families or families[family]!="AVAILABLE":
            return "BLOCKED_INVALID_CRITICAL_INTERVAL"
        if not isinstance(ci,dict) or ci.get("multiplicity_adjusted") is not True:
            return "BLOCKED_UNADJUSTED_CRITICAL_INTERVAL"
        lo,hi=ci.get("lower"),ci.get("upper")
        if (type(lo) not in (float,int) or type(hi) not in (float,int)
                or not math.isfinite(lo) or not math.isfinite(hi) or lo>hi):
            return "BLOCKED_MALFORMED_CRITICAL_INTERVAL"
        if hi< -margin:
            return "NO_GLOBAL_WIN_CRITICAL_OOD_REVERSAL"
    if scoped_losses:
        return "NO_GLOBAL_WIN_SCOPED_LOSS"
    if not holm_all_reject(p):
        return "NO_ESTABLISHED_GLOBAL_SUPERIORITY"
    if models["B1"]!="POSITIVE" or models["B2"]!="POSITIVE":
        return "NO_GLOBAL_WIN_MODEL_UNCERTAIN"
    if any(families[c]=="MISSING" for c in CRITICAL):
        return "INTERNAL_ONLY_BOUNDED"
    return "ELIGIBLE_FURTHER_INDEPENDENT_REVIEW"

class AdversarialFixtures(unittest.TestCase):
    def base(self,**changes):
        d=dict(p=dict.fromkeys(RIVALS,0.001),fidelity=True,telemetry=True,
               families={"E":"AVAILABLE","O":"AVAILABLE"},
               intervals={"E":{"lower":0.00,"upper":0.08,"multiplicity_adjusted":True},
                          "O":{"lower":0.01,"upper":0.05,"multiplicity_adjusted":True}},
               models={"B1":"POSITIVE","B2":"POSITIVE"},margin=0.03,
               preregistered=True)
        d.update(changes)
        return gate(**d)
    def test_positive_is_only_review_eligible(self):
        self.assertEqual(self.base(),"ELIGIBLE_FURTHER_INDEPENDENT_REVIEW")
    def test_default_prereg_gate_blocks(self):
        self.assertEqual(self.base(preregistered=False),"NOT_AUTHORIZED_NO_PREREG")
    def test_holm_six_p_of_001_pass(self):
        self.assertTrue(holm_all_reject(dict.fromkeys(RIVALS,0.001)))
    def test_holm_six_p_of_01_fail(self):
        self.assertFalse(holm_all_reject(dict.fromkeys(RIVALS,0.01)))
    def test_missing_sixth_comparator(self):
        self.assertEqual(self.base(p=dict.fromkeys(RIVALS[:5],0.001)),"INCONCLUSIVE_COMPARATOR_COVERAGE")
    def test_extra_unfrozen_comparator(self):
        self.assertEqual(self.base(p={**dict.fromkeys(RIVALS,0.001),"EXTRA":0.001}),"INCONCLUSIVE_COMPARATOR_COVERAGE")
    def test_single_weak_pair(self):
        p=dict.fromkeys(RIVALS,0.001);p["EvoMaster"]=0.9
        self.assertEqual(self.base(p=p),"NO_ESTABLISHED_GLOBAL_SUPERIORITY")
    def test_missing_model(self):
        self.assertEqual(self.base(models={"B1":"POSITIVE"}),"INCONCLUSIVE_MODEL_COVERAGE")
    def test_model_sign_reversal(self):
        self.assertEqual(self.base(models={"B1":"POSITIVE","B2":"NEGATIVE"}),"MODEL_DEPENDENT_SIGN_REVERSAL")
    def test_ood_negative_even_if_other_family_positive(self):
        ci={"E":{"lower":0.21,"upper":0.29,"multiplicity_adjusted":True},
            "O":{"lower":-0.13,"upper":-0.06,"multiplicity_adjusted":True}}
        self.assertEqual(self.base(intervals=ci),"NO_GLOBAL_WIN_CRITICAL_OOD_REVERSAL")
    def test_missing_critical_family_ceiling(self):
        self.assertEqual(self.base(families={"E":"AVAILABLE","O":"MISSING"},
            intervals={"E":{"lower":0.01,"upper":0.04,"multiplicity_adjusted":True}}),
            "INTERNAL_ONLY_BOUNDED")
    def test_undeclared_critical_family(self):
        self.assertEqual(self.base(families={"E":"AVAILABLE"}),"INCONCLUSIVE_UNDECLARED_CRITICAL_FAMILY")
    def test_missing_critical_ci(self):
        self.assertEqual(self.base(intervals={"E":{"lower":0.02,"upper":0.09,"multiplicity_adjusted":True}}),
                         "INCONCLUSIVE_CRITICAL_FAMILY_CI_MISSING")
    def test_unadjusted_interval(self):
        ci=self.base_params_interval();ci["O"]["multiplicity_adjusted"]=False
        self.assertEqual(self.base(intervals=ci),"BLOCKED_UNADJUSTED_CRITICAL_INTERVAL")
    def base_params_interval(self):
        return {"E":{"lower":0.0,"upper":0.08,"multiplicity_adjusted":True},
                "O":{"lower":0.01,"upper":0.05,"multiplicity_adjusted":True}}
    def test_nan_invalid_p(self):
        p=dict.fromkeys(RIVALS,0.001);p["ResearchLoop"]=float("nan")
        self.assertEqual(self.base(p=p),"NO_ESTABLISHED_GLOBAL_SUPERIORITY")
    def test_invalid_interval(self):
        ci=self.base_params_interval();ci["O"]["upper"]=float("nan")
        self.assertEqual(self.base(intervals=ci),"BLOCKED_MALFORMED_CRITICAL_INTERVAL")
    def test_invalid_critical_family(self):
        self.assertEqual(self.base(families={"E":"INVALID","O":"AVAILABLE"}),"BLOCKED_INVALID_FAMILY")
    def test_scoped_specialist_win(self):
        self.assertEqual(self.base(scoped_losses=("biology",)),"NO_GLOBAL_WIN_SCOPED_LOSS")
    def test_h011(self):
        self.assertEqual(self.base(telemetry=False),"BLOCKED_FIDELITY_OR_TELEMETRY")
    def test_fidelity(self):
        self.assertEqual(self.base(fidelity=False),"BLOCKED_FIDELITY_OR_TELEMETRY")
    def test_unfrozen_margin(self):
        self.assertEqual(self.base(margin=None),"BLOCKED_UNFROZEN_MARGIN")
    def test_margin_boundary_not_material_reversal(self):
        ci=self.base_params_interval();ci["O"]={"lower":-0.15,"upper":-0.03,"multiplicity_adjusted":True}
        self.assertNotEqual(self.base(intervals=ci),"NO_GLOBAL_WIN_CRITICAL_OOD_REVERSAL")
if __name__=="__main__":
    unittest.main(verbosity=2)
