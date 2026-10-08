from pathlib import Path
import ast, unittest, copy, importlib.util, json
root=Path.home()/"Research2"
spec=importlib.util.spec_from_file_location("r2_memtest",root/"internagent_failed_memory_behavior_dev_v001.py")
test=importlib.util.module_from_spec(spec)
spec.loader.exec_module(test)
results={}
for label,path in test.files.items():
    tree=ast.parse(path.read_text(encoding="utf-8"))
    classname="GenerationAgent" if label=="generation" else "EvolutionAgent"
    klass=next(x for x in tree.body if isinstance(x,ast.ClassDef) and x.name==classname)
    fn=copy.deepcopy(next(x for x in klass.body if isinstance(x,ast.AsyncFunctionDef) and "failed_records" in x.name))
    count=0
    for node in ast.walk(fn):
        if isinstance(node,ast.Compare) and len(node.ops)==1 and isinstance(node.ops[0],ast.Eq) and node.comparators and isinstance(node.comparators[0],ast.UnaryOp) and isinstance(node.comparators[0].op,ast.USub) and isinstance(node.comparators[0].operand,ast.Constant) and node.comparators[0].operand.value==1:
            node.comparators[0]=ast.Constant(value=1);count+=1
    assert count==1,(label,count)
    c=ast.Module(body=[ast.ClassDef(name="RealMethod",bases=[],keywords=[],body=[fn],decorator_list=[])],type_ignores=[])
    ast.fix_missing_locations(c)
    ns={"logger":test.logging.getLogger("mutation_sentinel"),"Dict":test.Dict,"Any":test.Any}
    exec(compile(c,str(path),"exec"),ns)
    original=test.methods[label]
    test.methods[label]=ns["RealMethod"]
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(test.Behavior)
    outcome=unittest.TestResult();suite.run(outcome)
    test.methods[label]=original
    results[label]={"mutations":count,"tests_run":outcome.testsRun,
                    "detected":bool(outcome.failures or outcome.errors),
                    "failing_tests":len(outcome.failures)+len(outcome.errors)}
print(json.dumps({"result":"DEV_MUTATION_SENSITIVITY","mutants":results,"all_detected":all(x["detected"] for x in results.values()),"decisive_runs":0},indent=2))
assert all(x["detected"] for x in results.values())
