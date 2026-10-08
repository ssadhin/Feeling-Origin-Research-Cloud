"""Adversarial mutation-sensitivity test for R2 neutral claim gate (NONDECISIVE)."""
from pathlib import Path
import unittest, json, contextlib, io
path=Path(__file__).with_name("neutral_claim_gate_dev_v001.py")
source=path.read_text(encoding="utf-8")
mutants={
 "DROP_PREREG_GATE":('if not preregistered:\n        return "NOT_AUTHORIZED_NO_PREREG"',
                      'if not preregistered:\n        pass'),
 "DROP_H011_GATE":('if not fidelity or not telemetry:\n        return "BLOCKED_FIDELITY_OR_TELEMETRY"',
                   'if not fidelity or not telemetry:\n        pass'),
 "IGNORE_HOLM":('if v>alpha/(len(vals)-i):\n            return False',
                'if v>alpha/(len(vals)-i):\n            pass'),
 "IGNORE_CRITICAL_OOD":('if hi< -margin:\n            return "NO_GLOBAL_WIN_CRITICAL_OOD_REVERSAL"',
                        'if hi< -margin:\n            pass'),
 "IGNORE_SCOPED_LOSS":('if scoped_losses:\n        return "NO_GLOBAL_WIN_SCOPED_LOSS"',
                       'if scoped_losses:\n        pass')
}
report={}
for name,(old,new) in mutants.items():
    assert source.count(old)==1,(name,source.count(old))
    ns={"__name__":"mutant_"+name}
    exec(compile(source.replace(old,new),str(path), "exec"),ns)
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ns["AdversarialFixtures"])
    result=unittest.TestResult()
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        suite.run(result)
    report[name]={"tests_run":result.testsRun,
                  "detected":bool(result.failures or result.errors),
                  "failed_tests":len(result.failures)+len(result.errors)}
print(json.dumps({"status":"MUTATION_SENSITIVITY_DEVELOPMENT_ONLY","mutations":report,
                  "all_detected":all(x["detected"] for x in report.values()),
                  "decisive_runs":0},indent=2))
assert all(x["detected"] for x in report.values()),"UNDETECTED_MUTATION"
