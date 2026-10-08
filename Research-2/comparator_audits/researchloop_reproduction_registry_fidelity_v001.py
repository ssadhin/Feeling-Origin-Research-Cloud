"""Research #2 nondecisive original-source ResearchLoop validator exercise.
Extracts byte-verified upstream AST; no external model call, no benchmark.
Original repo: plan-lab-szu/ResearchLoop @ 7e0a4fbe0cf646f4c859b6d20e46870d73abb11a
Original blob: d87c5536c5a1156fd319faa1766bb856315f33e7
"""
import ast
import copy
import hashlib
import json
import os
import unittest
from pathlib import Path
from dataclasses import dataclass
from typing import Literal

PINNED_GIT_BLOB="d87c5536c5a1156fd319faa1766bb856315f33e7"
SOURCE=Path(os.environ.get("R2_RESEARCHLOOP_SOURCE", str(Path(__file__).with_name("reproduction_registry.py"))))
CONTENT=SOURCE.read_bytes()
actual_blob=hashlib.sha1(b"blob "+str(len(CONTENT)).encode()+b"\0"+CONTENT).hexdigest()
if actual_blob!=PINNED_GIT_BLOB:
    raise RuntimeError("UPSTREAM_CONTENT_MISMATCH")
original=ast.parse(CONTENT.decode('utf8'))
source_defs={n.name:n for n in original.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
selected=[copy.deepcopy(source_defs[n]) for n in (
    "ReproductionTarget","_validate_required_fields", "_validate_non_blank_string","validate_reproduction_targets")]

def load_methods(mods):
    scope={"dataclass":dataclass,"Literal":Literal,"__name__":"r2_test",
           "Priority":Literal["P0","P1","P2"],
           "ReproductionMode":Literal["official_code_smoke","paper_based_adaptation","conceptual_control","source_dossier_only","blocked_closed_source"]}
    module=ast.Module(body=mods,type_ignores=[])
    ast.fix_missing_locations(module)
    exec(compile(module,str(SOURCE),'exec'),scope)
    return scope

scope=load_methods(copy.deepcopy(selected))
Target=scope["ReproductionTarget"]
validate=scope["validate_reproduction_targets"]
validate_required=scope["_validate_required_fields"]
validate_nonblank=scope["_validate_non_blank_string"]

def target(n,**kwargs):
    d=dict(target_id=n,priority="P0",related_work="published",baseline_role="benchmark",
           source_refs=("https://example.org/public",),reproduction_mode="official_code_smoke",
           smoke_command=None,blocker_policy="block",claim_support_allowed=False)
    d.update(kwargs)
    return Target(**d)

def valid():
    return [target("AGENT_LABORATORY"),target("AI_SCIENTIST_V2"),target("PROVENANCE_ONLY")]

class TestRealUpstream(unittest.TestCase):
    def test_baseline_complete_no_errors(self):self.assertEqual(validate(valid()),[])
    def test_claim_support_true_rejected(self):
        seq=valid();seq[0]=target("AGENT_LABORATORY",claim_support_allowed=True)
        self.assertIn('claim_support_allowed must be false',str(validate(seq)))
    def test_required_p0_missing(self):
        self.assertIn("missing required P0 targets",str(validate(valid()[:-1])))
    def test_bad_priority(self):
        seq=valid();seq[0]=target("AGENT_LABORATORY",priority="P9")
        self.assertIn("invalid priority",str(validate(seq)))
    def test_bad_reproduction_mode(self):
        seq=valid();seq[0]=target("AGENT_LABORATORY",reproduction_mode="shortcut")
        self.assertIn("invalid reproduction_mode",str(validate(seq)))
    def test_empty_refs(self):
        seq=valid();seq[0]=target("AGENT_LABORATORY",source_refs=())
        self.assertIn("source_refs must contain",str(validate(seq)))
    def test_blank_ref(self):
        seq=valid();seq[0]=target("AGENT_LABORATORY",source_refs=("",))
        self.assertIn("source_refs must contain",str(validate(seq)))
    def test_missing_ref_type(self):
        seq=valid();seq[0]=target("AGENT_LABORATORY",source_refs=(123,))
        self.assertIn("source_refs must contain",str(validate(seq)))
    def test_blank_baseline_role(self):
        seq=valid();seq[0]=target("AGENT_LABORATORY",baseline_role="  ")
        self.assertIn("baseline_role must be a non-blank",str(validate(seq)))
    def test_blank_blocker_policy(self):
        seq=valid();seq[0]=target("AGENT_LABORATORY",blocker_policy="")
        self.assertIn("blocker_policy must be a non-blank",str(validate(seq)))
    def test_required_field_rejected(self):
        with self.assertRaises(ValueError):validate_required({'target_id':'x'})
    def test_nonblank_helper(self):
        with self.assertRaises(ValueError):validate_nonblank("id", "   ")
    def test_metadata_type_gap_none_not_rejected(self):
        # An observed upstream limitation, NOT an endorsed contract behavior.
        seq=valid();seq[0]=target("AGENT_LABORATORY",claim_support_allowed=None)
        self.assertEqual(validate(seq),[])
    def test_metadata_type_gap_integer_false_not_rejected(self):
        seq=valid();seq[0]=target("AGENT_LABORATORY",claim_support_allowed=0)
        self.assertEqual(validate(seq),[])

def mutate(name):
    nodes=copy.deepcopy(selected)
    f=next(n for n in nodes if isinstance(n,ast.FunctionDef) and n.name=="validate_reproduction_targets")
    if name=="IGNORE_TRUE_CLAIMS":
        targets=[n for n in ast.walk(f) if isinstance(n,ast.If) and isinstance(n.test,ast.Attribute) and n.test.attr=="claim_support_allowed"]
        assert len(targets)==1
        targets[0].test=ast.Constant(False)
    elif name=="IGNORE_MISSING_SOURCE_REFS":
        targets=[n for n in ast.walk(f) if isinstance(n,ast.If) and isinstance(n.test,ast.BoolOp) and isinstance(n.test.op,ast.Or) and any(isinstance(x,ast.UnaryOp) and isinstance(x.operand,ast.Attribute) and x.operand.attr=="source_refs" for x in n.test.values)]
        assert len(targets)==1
        targets[0].test=ast.Constant(False)
    else:raise AssertionError(name)
    ns=load_methods(nodes)
    return ns["validate_reproduction_targets"]

if __name__=="__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(TestRealUpstream)
    ret=unittest.TextTestRunner(verbosity=0).run(suite)
    print(json.dumps({"original_git_blob_verified":True,"upstream_method_tests":ret.testsRun,
        "upstream_tests_passed":ret.testsRun-len(ret.failures)-len(ret.errors),
        "limitations":["nonbool None and 0 claim-support flag pass source validator"],"api_calls":0,"decisive_runs":0},indent=2))
    if not ret.wasSuccessful():raise SystemExit(1)
    for label in ["IGNORE_TRUE_CLAIMS","IGNORE_MISSING_SOURCE_REFS"]:
        mutant=mutate(label)
        seq=valid()
        if label=="IGNORE_TRUE_CLAIMS":seq[0]=target("AGENT_LABORATORY",claim_support_allowed=True)
        else:seq[0]=target("AGENT_LABORATORY",source_refs=())
        result=mutant(seq)
        detected= not any(("claim_support_allowed" if label=="IGNORE_TRUE_CLAIMS" else "source_refs") in x for x in result)
        print(json.dumps({"mutant":label,"detected":detected,"source_untouched":True}))
        assert detected
