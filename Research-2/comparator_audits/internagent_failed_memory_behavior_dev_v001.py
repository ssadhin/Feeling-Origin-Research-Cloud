from pathlib import Path
import ast, asyncio, logging, unittest, types, hashlib, json
from typing import Dict, Any, List, Optional

root=Path.home()/"Research2"/"comparators_20261008"/"InternAgent"/"internagent"/"mas"/"agents"
files={"generation":root/"generation_agent.py","evolution":root/"evolution_agent.py"}
methods={}
for label,path in files.items():
    tree=ast.parse(path.read_text(encoding="utf-8"))
    name="GenerationAgent" if label=="generation" else "EvolutionAgent"
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==name)
    fn=next(n for n in cls.body if isinstance(n,ast.AsyncFunctionDef) and "check" in n.name and "failed_records" in n.name)
    wrapper=ast.Module(body=[ast.ClassDef(name="RealMethod",bases=[],keywords=[],body=[fn],decorator_list=[])],type_ignores=[])
    ast.fix_missing_locations(wrapper)
    space={"logger":logging.getLogger("r2_internagent_sentinel"), "Dict": Dict, "Any": Any}
    exec(compile(wrapper,str(path),"exec"),space)
    methods[label]=space["RealMethod"]

class FakeRetriever:
    def __init__(self,records=None,error=False):
        self.records=records or []
        self.error=error
    async def retrieve(self,query):
        if self.error:raise RuntimeError("expected upstream recovery sentinel")
        return {"success":True,"similar_records":self.records}

class Behavior(unittest.IsolatedAsyncioTestCase):
    async def check(self,kind,records,text="candidate",enabled=True,filter_on=True,error=False):
        item=methods[kind]()
        item.use_memory=enabled
        item.memory_retriever=FakeRetriever(records,error)
        item.filter_failed_ideas=filter_on
        item.failed_similarity_threshold=.70
        fn=next(getattr(item,n) for n in dir(item) if "check" in n and "failed_records" in n)
        return await fn({"text":text})
    async def test_negative_at_threshold(self):
        for k in methods:
            should,records=await self.check(k,[{"label":-1,"similarity_score":.71,"name":"failed"}])
            self.assertTrue(should);self.assertEqual(len(records),1)
    async def test_positive_record_not_filtered(self):
        for k in methods:
            should,_=await self.check(k,[{"label":1,"similarity_score":.99}])
            self.assertFalse(should)
    async def test_low_similarity_not_filtered(self):
        for k in methods:
            should,_=await self.check(k,[{"label":-1,"similarity_score":.69}])
            self.assertFalse(should)
    async def test_no_query(self):
        for k in methods:
            should,_=await self.check(k,[{"label":-1,"similarity_score":.99}],text="")
            self.assertFalse(should)
    async def test_disabled_memory(self):
        for k in methods:
            should,_=await self.check(k,[{"label":-1,"similarity_score":.99}],enabled=False)
            self.assertFalse(should)
    async def test_filter_disabled(self):
        for k in methods:
            should,_=await self.check(k,[{"label":-1,"similarity_score":.99}],filter_on=False)
            self.assertFalse(should)
    async def test_retriever_error_bounded(self):
        for k in methods:
            should,_=await self.check(k,[],error=True)
            self.assertFalse(should)

if __name__=="__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Behavior)
    result=unittest.TextTestRunner(verbosity=0).run(suite)
    print(json.dumps({"status":"ORIGINAL_UPSTREAM_AST_METHOD_BEHAVIOR_WITH_TEST_DOUBLES",
      "commit":"fa8c3eedfa9751d3752ea6eb49220b303ac2397d",
      "source_hashes":{k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in files.items()},
      "tests_passed":result.testsRun-len(result.failures)-len(result.errors),
      "tests_total":result.testsRun,"both_source_agents_exercised":True,
      "full_policy_fidelity":"NOT_ESTABLISHED","model_calls":0,"decisive_runs":0},indent=2))
    if not result.wasSuccessful():raise SystemExit(2)
