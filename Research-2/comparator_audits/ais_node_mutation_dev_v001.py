from pathlib import Path
import importlib.util, unittest, json
p=Path.home()/"Research2"/"ais_node_behavior_dev_v001.py"
s=importlib.util.spec_from_file_location("r2_ais_nodes",p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
saved=m.Node.stage_name
# Test-only mutation: all children incorrectly forced to "improve".
m.Node.stage_name=property(lambda self: "draft" if self.parent is None else "improve")
suite=unittest.defaultTestLoader.loadTestsFromTestCase(m.TrueSourceTests)
result=unittest.TestResult()
suite.run(result)
m.Node.stage_name=saved
out={"mutation":"DISABLE_BUGGY_PARENT_DEBUG_ROUTING","tests_run":result.testsRun,
     "mutant_detected":bool(result.failures or result.errors),
     "failing_tests":len(result.failures)+len(result.errors),
     "upstream_changed":False,"decisive_runs":0}
print(json.dumps(out,indent=2))
assert out["mutant_detected"] and out["failing_tests"]>=1
