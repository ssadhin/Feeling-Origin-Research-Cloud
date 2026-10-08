"""Exploratory source-native EvoScientist memory integration test, research phase 3.
Does not modify original source, frozen instances, or call paid model providers.
"""
from __future__ import annotations
import datetime,hashlib,json,os,pathlib,subprocess,time,sys
root=pathlib.Path(r"C:\Users\hasad\Research2\comparators_20261008\EvoScientist")
exe=pathlib.Path(r"C:\Users\hasad\Research2\venvs\evosci312\Scripts\python.exe")
out=pathlib.Path(r"G:\My Drive\Consciousness Formula Research\09_Checkpoints\EvoScientist_original_memory_20261008_v001")
out.mkdir(parents=True,exist_ok=True)
path=out/"run002.json"
if path.exists():raise SystemExit("PRIOR_RESULT_EXISTS: cannot overwrite")
def git(*args):
 p=subprocess.run(["git","-C",str(root),*args],capture_output=True,text=True,timeout=12)
 if p.returncode:raise RuntimeError("GIT_PROVENANCE_ERROR")
 return p.stdout.strip()
sha=git("rev-parse","HEAD")
expect="3b382b92b8fdad6e1f13467c382dcdd91d9b19d2"
if sha!=expect:raise RuntimeError("IMMUTABLE_SOURCE_COMMIT_MISMATCH")
before=git("status","--porcelain")
if before:raise RuntimeError("UPSTREAM_CHECKOUT_DIRTY_BEFORE_RUN")
files=[root/"tests/test_observation_memory.py",root/"tests/test_profile_memory_middleware.py"]
digests={str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
env=os.environ.copy()
env.update(PYTHONDONTWRITEBYTECODE="1",PIP_NO_INDEX="1",HTTP_PROXY="http://127.0.0.1:9",HTTPS_PROXY="http://127.0.0.1:9",ALL_PROXY="http://127.0.0.1:9",NO_PROXY="localhost,127.0.0.1")
args=[str(exe),"-B","-m","pytest","-q","-p","no:cacheprovider","tests/test_observation_memory.py","tests/test_profile_memory_middleware.py"]
start=time.time()
try:
 p=subprocess.run(args,cwd=str(root),env=env,capture_output=True,text=True,errors="replace",timeout=140)
 rc=p.returncode;status="EXITED";stdout=p.stdout;stderr=p.stderr
except subprocess.TimeoutExpired as e:
 rc=None;status="TIMEOUT_140S";stdout=str(e.stdout or "");stderr=str(e.stderr or "")
elapsed=round(time.time()-start,3)
after=git("status","--porcelain")
data={"timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"method":"EvoScientist","pinned_upstream_commit":sha,"upstream_repo":"EvoScientist/EvoScientist","scope":"nondecisive source-native memory unit/integration checks, no live LLM/provider","tests":digests,"runner":str(exe),"python_version":subprocess.run([str(exe),"--version"],capture_output=True,text=True).stdout.strip(),"argv":args[1:],"exit_code":rc,"status":status,"wall_seconds":elapsed,"source_clean_before":not bool(before),"source_clean_after":not bool(after),"stdout_tail":stdout[-11000:],"stderr_tail":stderr[-6500:],"claim_ceiling":"selected original-source test reproducibility only, not full ES-1..ES-5 fidelity certification and not AES prospective comparison","aes_v2_prospective_decisive_trials":0}
path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("EVO_SOURCE_SHA_PINNED",sha)
print("PROCESS",status,"RETURN_CODE",rc,"WALL_SECONDS",elapsed)
print("GIT_UNCHANGED_BEFORE_AND_AFTER",not bool(before) and not bool(after))
print("RESULT",str(path))
print("STDOUT_TAIL",stdout[-4200:])
print("STDERR_TAIL",stderr[-1600:])
