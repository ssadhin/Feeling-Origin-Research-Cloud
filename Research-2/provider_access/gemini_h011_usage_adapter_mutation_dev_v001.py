"""Adversarial mutation sentinel for R2 Gemini provider usage guard. No API calls."""
from pathlib import Path
import json,unittest
p=Path.home()/"Research2"/"gemini_h011_usage_adapter_dev_v001.py"
src=p.read_text(encoding="utf-8")
mutations={
    "ACCEPT_WRONG_RETURNED_MODEL":("if requested!=actual:","if False:"),
    "ACCEPT_UNDERCOUNTED_TOTAL":("if c<a+b+(thought if thought is not None else 0):","if False:")}
results=[]
for name,(old,new) in mutations.items():
    assert src.count(old)==1,(name,"not unique")
    scope={"__name__":"gemini_h011_mutant_test"}
    exec(compile(src.replace(old,new),str(p),"exec"),scope)
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(scope["TestGeminiAccounting"])
    res=unittest.TestResult();suite.run(res)
    results.append({"mutation":name,"mutant_detected":bool(res.failures or res.errors),
                    "tests_run":res.testsRun,"failed_tests":len(res.failures)+len(res.errors)})
print(json.dumps({"mutations":results,"actual_provider_calls":0,"original_script_changed":False},indent=2))
assert all(x["mutant_detected"] for x in results)
