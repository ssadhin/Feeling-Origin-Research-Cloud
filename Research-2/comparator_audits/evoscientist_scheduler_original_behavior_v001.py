from pathlib import Path
import ast, json, hashlib, logging, threading, unittest, tempfile
from dataclasses import dataclass
from typing import NamedTuple
from types import SimpleNamespace
root=Path.home()/"Research2"/"comparators_20261008"/"EvoScientist"
path=root/"EvoScientist"/"memory"/"scheduler.py"
tree=ast.parse(path.read_text(encoding="utf-8"))
names={"ObservationLinkerContext","_BatchKey","_root_key","_batch_key_from_worker_run","MemoryScheduler"}
part=[x for x in tree.body if isinstance(x,(ast.ClassDef,ast.FunctionDef)) and x.name in names]
assert {x.name for x in part}==names
module=ast.Module(body=[ast.ImportFrom(module='__future__',names=[ast.alias(name='annotations')],level=0)]+part,type_ignores=[])
ast.fix_missing_locations(module)
activity=[]
globals_={"Path":Path,"dataclass":dataclass,"NamedTuple":NamedTuple,"threading":threading,
"logger":logging.getLogger("r2scheduler"),"has_active_memory_workers":lambda x:False,
"mark_observation_linker_launch_started":lambda:activity.append("start"),
"mark_observation_linker_launch_finished":lambda:activity.append("end"),
"read_observation_id_from_path":lambda p:None if "noid" in p.stem else p.stem}
exec(compile(module,str(path),"exec"),globals_)
S=globals_["MemoryScheduler"]; C=globals_["ObservationLinkerContext"]
def run(proj,dir):
    return SimpleNamespace(run_id="synthetic",metadata={"workspace_dir":str(dir),"project_id":proj})
def delta(path,*items):
    return SimpleNamespace(memory_dir=path,observation_paths=tuple(items))
class Tests(unittest.TestCase):
    def setUp(self):
        activity.clear()
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.work=Path(self.temp.name)/"work";self.work.mkdir()
        self.mem=Path(self.temp.name)/"mem";self.mem.mkdir()
        self.out=[];self.busy=False
        self.s=S(launch_linker=self.out.append,has_active_workers=lambda x:self.busy)
    def test_completed_worker_emits_id(self):
        self.s.record_worker_finished(run("p",self.work),delta(self.mem,"one.json"))
        self.assertEqual(self.out[0].observation_ids,("one",))
    def test_aborted_worker_preserves(self):
        self.s.record_worker_aborted(run("p",self.work),delta(self.mem,"kept.json"))
        self.assertEqual(self.out[0].observation_ids,("kept",))
    def test_busy_blocks_until_flush(self):
        self.busy=True;self.s.record_worker_finished(run("p",self.work),delta(self.mem,"one.json"))
        self.assertFalse(self.out);self.s.flush_ready();self.assertFalse(self.out)
        self.busy=False;self.s.flush_ready();self.assertEqual(len(self.out),1)
    def test_batch_deduplicates_and_sorts(self):
        self.busy=True
        self.s.record_observation_created(C(self.mem,self.work,"p",("z","a","z")))
        self.busy=False;self.s.flush_ready()
        self.assertEqual(self.out[0].observation_ids,("a","z"))
    def test_separate_projects_not_merged(self):
        self.busy=True
        for p in ("alpha","beta"):
            self.s.record_worker_finished(run(p,self.work),delta(self.mem,p+".json"))
        self.busy=False;self.s.flush_ready()
        self.assertEqual({x.project_id for x in self.out},{"alpha","beta"})
    def test_missing_id_skips(self):
        self.s.record_worker_finished(run("p",self.work),delta(self.mem,"noid.json"))
        self.assertFalse(self.out)
    def test_no_duplicate_second_flush(self):
        self.s.record_worker_finished(run("p",self.work),delta(self.mem,"a.json"))
        self.s.flush_ready();self.assertEqual(len(self.out),1)
    def test_linker_failure_balanced_lifecycle(self):
        self.s._launch_linker=lambda _:(_ for _ in ()).throw(RuntimeError("synthetic"))
        self.s.record_worker_finished(run("p",self.work),delta(self.mem,"a.json"))
        self.assertEqual(activity,["start","end"])
if __name__=="__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
    res=unittest.TextTestRunner(verbosity=0).run(suite)
    print(json.dumps({"method":"upstream EvoScientist MemoryScheduler AST","commit":"3b382b92b8fdad6e1f13467c382dcdd91d9b19d2","source_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"passed":res.testsRun-len(res.failures)-len(res.errors),"total":res.testsRun,"full_fidelity":False,"provider_calls":0,"decisive_runs":0},indent=2))
    if not res.wasSuccessful():raise SystemExit(2)
