from pathlib import Path
import ast, json, hashlib, unittest
from typing import Literal

root=Path.home()/"Research2"/"comparators_20261008"/"AIS"
f=root/"ai_scientist"/"treesearch"/"journal.py"
tree=ast.parse(f.read_text(encoding="utf8"))
upstream=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=="Node")
wanted={"__post_init__","__eq__","__hash__","stage_name","is_leaf","debug_depth"}
nodes=[n for n in upstream.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in wanted]
assert set(n.name for n in nodes)==wanted
classdef=ast.ClassDef(name="Node",bases=[],keywords=[],body=nodes,decorator_list=[])
module=ast.Module(body=[classdef],type_ignores=[])
ast.fix_missing_locations(module)
ns={"Literal":Literal}
exec(compile(module,str(f),"exec"),ns)
Node=ns["Node"]
def init(self,parent=None,is_buggy=False,id="item"):
    self.id=id
    self.parent=parent
    self.children=set()
    self.is_buggy=is_buggy
    self.__post_init__()
Node.__init__=init

class TrueSourceTests(unittest.TestCase):
    def test_root_stage(self):
        self.assertEqual(Node(id="a").stage_name,"draft")
    def test_parent_tracks_children(self):
        root=Node(id="r");leaf=Node(root,id="l")
        self.assertIn(leaf,root.children)
        self.assertFalse(root.is_leaf)
        self.assertTrue(leaf.is_leaf)
    def test_buggy_parent_debug(self):
        root=Node(is_buggy=True,id="r");child=Node(root,id="c")
        self.assertEqual(child.stage_name,"debug")
        self.assertEqual(child.debug_depth,1)
    def test_nonbuggy_parent_improve(self):
        root=Node(is_buggy=False,id="r");child=Node(root,id="c")
        self.assertEqual(child.stage_name,"improve")
        self.assertEqual(child.debug_depth,0)
    def test_consecutive_debug_depth(self):
        root=Node(is_buggy=True,id="r")
        a=Node(root,is_buggy=True,id="a")
        b=Node(a,id="b")
        self.assertEqual((a.debug_depth,b.debug_depth),(1,2))
    def test_distinct_sibling_paths(self):
        root=Node(is_buggy=True,id="r")
        a=Node(root,id="a")
        b=Node(root,id="b")
        self.assertEqual(len(root.children),2)
        self.assertNotEqual(a,b)
    def test_same_id_equality_hash(self):
        self.assertEqual(Node(id="x"),Node(id="x"))
        self.assertEqual(hash(Node(id="x")),hash(Node(id="x")))
    def test_string_parent_not_added(self):
        node=Node(parent="serialized-parent",id="a")
        self.assertEqual(node.children,set())
    def test_leaf_after_descendant(self):
        r=Node(id="r");self.assertTrue(r.is_leaf)
        Node(parent=r,id="c");self.assertFalse(r.is_leaf)

if __name__=="__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(TrueSourceTests)
    result=unittest.TextTestRunner(verbosity=1).run(suite)
    print(json.dumps({"upstream":"AI-Scientist-v2","commit":"96bd51617cfdbb494a9fc283af00fe090edfae48",
          "source_sha256":hashlib.sha256(f.read_bytes()).hexdigest(),"tests_run":result.testsRun,
          "tests_passed":result.testsRun-len(result.errors)-len(result.failures),
          "methods_executed":sorted(wanted),"full_behavioral_fidelity":False,
          "provider_calls":0,"decisive_runs":0},indent=2))
    if not result.wasSuccessful():raise SystemExit(2)
