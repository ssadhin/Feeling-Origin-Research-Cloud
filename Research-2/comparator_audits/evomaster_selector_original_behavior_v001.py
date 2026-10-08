from pathlib import Path
import ast, re, logging, unittest, json, hashlib
root=Path.home()/"Research2"/"comparators_20261008"/"EvoMaster"
p=root/"playground"/"x_master"/"core"/"exp"/"select_exp.py"
tree=ast.parse(p.read_text(encoding="utf-8"))
cls=next(x for x in tree.body if isinstance(x,ast.ClassDef) and x.name=="SelectExp")
method_names={"_get_selected_index","_parse_selector_choice","_format_solutions_prompt"}
methods=[x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name in method_names]
assert {x.name for x in methods}==method_names
node=ast.Module(body=[ast.ClassDef(name="SelectExp",bases=[],keywords=[],body=methods,decorator_list=[])],type_ignores=[])
ast.fix_missing_locations(node)
env={"re":re,"List":list,"strip_think_and_exec":lambda x:x.replace("<think>private</think>","").strip()}
exec(compile(node,str(p),"exec"),env)
Selector=env["SelectExp"]
class SourceSelectionBehavior(unittest.TestCase):
    def setUp(self):
        self.s=Selector()
        self.s.logger=logging.getLogger("evo-selector")
    def test_picks_number_two(self):
        self.assertEqual(self.s._get_selected_index("<select>Response 2</select>",3),1)
    def test_case_insensitive(self):
        self.assertEqual(self.s._get_selected_index("<SELECT>response 3</SELECT>",3),2)
    def test_missing_choice_defaults_first(self):
        self.assertEqual(self.s._get_selected_index("No choice",3),0)
    def test_high_choice_clamped(self):
        self.assertEqual(self.s._get_selected_index("<select>Response 900</select>",3),2)
    def test_zero_choice_clamped(self):
        self.assertEqual(self.s._get_selected_index("<select>Response 0</select>",3),0)
    def test_empty_response_defaults_first(self):
        self.assertEqual(self.s._get_selected_index("",3),0)
    def test_returns_original_solution(self):
        xs=["A","B","C"]
        self.assertEqual(self.s._parse_selector_choice("<select>Response 2</select>",xs),"B")
    def test_empty_solution_list_parse(self):
        self.assertEqual(self.s._parse_selector_choice("abc",[]),"")
    def test_prompt_preserves_numbering(self):
        out=self.s._format_solutions_prompt(["alpha","beta"])
        self.assertIn("## Response 1",out)
        self.assertIn("## Response 2",out)
    def test_empty_prompt(self):
        self.assertEqual(self.s._format_solutions_prompt([]),"No solutions")
    def test_strip_private_think(self):
        self.assertNotIn("<think>",self.s._format_solutions_prompt(["<think>private</think>answer"]))
    def test_empty_solution_replaced(self):
        self.assertIn("empty solution",self.s._format_solutions_prompt([""]))
if __name__=="__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(SourceSelectionBehavior)
    result=unittest.TextTestRunner(verbosity=0).run(suite)
    print(json.dumps({"method":"EvoMaster/X-Master original SelectExp AST","commit":"36a52bc6c42a6b9fd710a41c52f3c3bb948b9ac9","source_sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"passed":result.testsRun-len(result.failures)-len(result.errors),"total":result.testsRun,"full_policy_fidelity":False,"provider_calls":0,"decisive_runs":0},indent=2))
    if not result.wasSuccessful():raise SystemExit(2)
