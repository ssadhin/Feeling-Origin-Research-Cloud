"""EvoScientist original-role assembly and adversarial mutation sentinel.
Protocol frozen in pre_execution_protocol.md. No provider/API calls.
"""
import ast,hashlib,json,platform,shutil,subprocess,sys,tempfile
from pathlib import Path
import yaml

HERE=Path(__file__).resolve().parent
ROOT=Path(r"C:\Users\hasad\Research2\comparators_20261008\EvoScientist")
sys.path.insert(0,str(ROOT))
from EvoScientist.utils import load_subagents

PIN="3b382b92b8fdad6e1f13467c382dcdd91d9b19d2"
CFG=ROOT/"EvoScientist"/"subagents"
MAIN=ROOT/"EvoScientist"/"EvoScientist.py"
UTIL=ROOT/"EvoScientist"/"utils.py"
def sha(p):
 return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def git(*args):
 return subprocess.check_output(["git","-C",str(ROOT),*args],encoding="utf8",text=True).strip()
def role_gate(directory):
 roles={r["name"]:r for r in load_subagents(directory)}
 assert "research-agent" in roles and "code-agent" in roles,"MISSING_ROLE"
 research=roles["research-agent"];code=roles["code-agent"]
 assert research["system_prompt"].strip() and code["system_prompt"].strip(),"EMPTY_ROLE_PROMPT"
 assert research["system_prompt"].strip()!=code["system_prompt"].strip(),"COLLAPSED_ROLE_PROMPT"
 assert research["description"] and code["description"],"MISSING_DESCRIPTION"
 ra=set(research["_tool_names"]);ca=set(code["_tool_names"])
 assert "tavily_search" in ra and "think_tool" in ra,"RESEARCH_DECLARED_TOOLS_MISSING"
 assert "think_tool" in ca and "tavily_search" not in ca,"ENGINEER_TOOL_DECLARATIONS_INVALID"
 return {"role_names":sorted(roles),"research_declared_tools":sorted(ra),
         "code_declared_tools":sorted(ca),"distinct_prompts":True}
def has_wiring(tree,name):
 fn=next((x for x in ast.walk(tree) if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))
          and x.name==name),None)
 if fn is None:return False
 call=any(isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and
          x.func.id=="load_subagents" for x in ast.walk(fn))
 wired=any(isinstance(x,ast.Dict) and any(isinstance(k,ast.Constant) and
          k.value=="subagents" and isinstance(v,ast.Name) and v.id=="subs"
          for k,v in zip(x.keys,x.values) if k is not None)
          for x in ast.walk(fn))
 return call and wired

def mutate(folder,kind):
 if kind=="omit_code":
  (folder/"code.yaml").unlink()
 else:
  name="code.yaml" if kind=="duplicate_prompt" else "research.yaml"
  path=folder/name
  obj=yaml.safe_load(path.read_text(encoding="utf8"))
  if kind=="duplicate_prompt":
   other=yaml.safe_load((folder/"research.yaml").read_text(encoding="utf8"))
   obj["code-agent"]["system_prompt"]=other["research-agent"]["system_prompt"]
  elif kind=="collapse_tool":
   other=yaml.safe_load((folder/"code.yaml").read_text(encoding="utf8"))
   obj["research-agent"]["tools"]=other["code-agent"]["tools"]
  else:raise ValueError(kind)
  path.write_text(yaml.safe_dump(obj,sort_keys=False,allow_unicode=True),encoding="utf8")
def main():
 assert platform.node().upper()=="DESKTOP-SVFRAS5","WRONG_DEVICE"
 assert git("rev-parse","HEAD")==PIN and git("status","--porcelain")=="","PIN_OR_CLEAN_FAIL"
 base=role_gate(CFG)
 wiring_tree=ast.parse(MAIN.read_text(encoding="utf8"))
 names=("_build_base_kwargs","load_mcp_and_build_kwargs")
 wiring={n:has_wiring(wiring_tree,n) for n in names}
 assert all(wiring.values()),"MAIN_AGENT_WIRING_ABSENT"
 controls={}
 for kind in ("omit_code","duplicate_prompt","collapse_tool"):
  with tempfile.TemporaryDirectory(prefix="research2_es1_roles_") as raw:
   folder=Path(raw)
   for f in CFG.glob("*.yaml"):shutil.copy2(f,folder/f.name)
   mutate(folder,kind)
   try:
    role_gate(folder)
    controls[kind]="MISSED_MUTATION"
   except AssertionError as e:
    controls[kind]="CAUGHT_"+str(e)
 assert all(v.startswith("CAUGHT_") for v in controls.values()),"NEGATIVE_CONTROL_ESCAPED"
 assert git("rev-parse","HEAD")==PIN and git("status","--porcelain")=="","UPSTREAM_CHANGED"
 record={"status":"PARTIAL_ES1_ROLE_CONFIG_WIRING_PASS",
         "upstream_commit":PIN,"protocol_sha256":sha(HERE/"pre_execution_protocol.md"),
         "runner_sha256":sha(__file__),"upstream_files":{
           "EvoScientist.py":sha(MAIN),"utils.py":sha(UTIL),
           "research.yaml":sha(CFG/"research.yaml"),"code.yaml":sha(CFG/"code.yaml")},
         "original_roles":base,"builder_wiring":wiring,
         "negative_controls":controls,"source_clean":True,
         "model_calls":0,"full_ES1_handoff_certified":False}
 print("RESULT "+json.dumps(record,sort_keys=True))
if __name__=="__main__":main()
