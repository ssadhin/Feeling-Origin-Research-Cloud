from pathlib import Path
import ast, unittest, json, importlib.util, types, re
p=Path.home()/"Research2"/"evomaster_selector_original_behavior_v001.py"
spec=importlib.util.spec_from_file_location("evo_select_test",p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
original=m.Selector._get_selected_index
src=m.p.read_text(encoding="utf8")
tree=ast.parse(src)
cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=="SelectExp")
fn=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=="_get_selected_index")
mutations=0
for stmt in ast.walk(fn):
    if isinstance(stmt,ast.Return) and isinstance(stmt.value,ast.Call) and isinstance(stmt.value.func,ast.Name) and stmt.value.func.id=="max":
        stmt.value=ast.Name(id="idx",ctx=ast.Load())
        mutations+=1
assert mutations==1
outclass=ast.ClassDef(name="MutantSelector",bases=[],keywords=[],body=[fn],decorator_list=[])
mod=ast.Module(body=[outclass],type_ignores=[])
ast.fix_missing_locations(mod)
ns={"re":re};exec(compile(mod,str(m.p),"exec"),ns)
m.Selector._get_selected_index=ns["MutantSelector"]._get_selected_index
suite=unittest.defaultTestLoader.loadTestsFromTestCase(m.SourceSelectionBehavior)
result=unittest.TestResult();suite.run(result)
m.Selector._get_selected_index=original
out={"mutant":"REMOVE_SELECTOR_INDEX_BOUNDS_CLAMP","mutations":mutations,"tests_run":result.testsRun,
"mutant_detected":bool(result.failures or result.errors),"failing_tests":len(result.failures)+len(result.errors),
"source_unchanged":True,"decisive_runs":0}
print(json.dumps(out,indent=2))
assert out["mutant_detected"]
