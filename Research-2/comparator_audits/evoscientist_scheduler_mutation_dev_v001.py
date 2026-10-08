from pathlib import Path
import ast, unittest, json
root=Path.home()/"Research2"
source=(root/"evoscientist_scheduler_original_behavior_v001.py").read_text(encoding="utf8")
needle="module=ast.Module(body=[ast.ImportFrom(module='__future__',names=[ast.alias(name='annotations')],level=0)]+part,type_ignores=[])"
assert source.count(needle)==1
injection="""
count=0
for definition in part:
    if isinstance(definition,ast.ClassDef) and definition.name=="MemoryScheduler":
        for fn in definition.body:
            if isinstance(fn,ast.FunctionDef) and fn.name=="record_worker_aborted":
                fn.body=[ast.Pass()]
                count+=1
assert count==1
"""
mutated=source.replace(needle,injection+"\n"+needle)
space={"__name__":"isolated_evo_scheduler_mutant"}
exec(compile(mutated,str(root/"evoscientist_scheduler_original_behavior_v001.py"),"exec"),space)
suite=unittest.defaultTestLoader.loadTestsFromTestCase(space["Tests"])
result=unittest.TestResult();suite.run(result)
out={"mutation":"ABORTED_WORKER_OBSERVATION_DISCARD","tests_run":result.testsRun,
"mutation_detected":bool(result.failures or result.errors),
"failing_tests":len(result.failures)+len(result.errors),
"source_unchanged":True,"decisive_trials":0}
print(json.dumps(out,indent=2))
assert out["mutation_detected"]
