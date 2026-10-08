from pathlib import Path
import unittest, json
path=Path.home()/"Research2"/"paired_cluster_bootstrap_dev_v001.py"
original=path.read_text(encoding="utf8")
old="means=_check(clusters)"
new="means=[a-b for group in clusters for a,b in group]  # WRONG task-level resampling"
assert original.count(old)==1
namespace={"__name__":"r2_mutant"}
exec(compile(original.replace(old,new),str(path),"exec"),namespace)
suite=unittest.defaultTestLoader.loadTestsFromTestCase(namespace["TestClusterGuard"])
result=unittest.TestResult();suite.run(result)
print(json.dumps({"mutation":"SILENTLY_POOL_CORRELATED_TASKS_AS_INDEPENDENT",
    "tests_run":result.testsRun,"detected":bool(result.failures or result.errors),
    "failing_tests":len(result.failures)+len(result.errors),
    "pinned_source_modified":False,"decisive_runs":0},indent=2))
assert result.failures or result.errors
