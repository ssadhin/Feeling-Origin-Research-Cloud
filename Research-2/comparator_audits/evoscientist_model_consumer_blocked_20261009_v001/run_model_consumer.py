"""One-off nondecisive EvoScientist native-tools + real-model consumer.
See frozen pre_execution_protocol.md. No upstream edits or adaptive retries.
"""
from __future__ import annotations
import hashlib, json, os, platform, re, subprocess, sys, tempfile, time
from pathlib import Path

HERE=Path(__file__).resolve().parent
SRC=Path(r"C:\Users\hasad\Research2\comparators_20261008\EvoScientist")
sys.path.insert(0,str(SRC))
sys.path.insert(0,r"G:\My Drive\Untitled folder\agente M MCP server\src")
import eon_gemini as quota
from EvoScientist.memory.observations import (
    MemoryScope, MemorySourceType, MemoryType, record_observation_file
)
from EvoScientist.memory.project import resolve_project_id
from EvoScientist.memory.observations.tools import (
    create_search_observations_tool, create_read_memory_tool
)
from EvoScientist.llm.models import get_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

PIN="3b382b92b8fdad6e1f13467c382dcdd91d9b19d2"
MODEL="gemini-2.5-flash-lite"
def git(*args):
    return subprocess.check_output(["git","-C",str(SRC),*args],
                    text=True,encoding="utf-8",stderr=subprocess.DEVNULL).strip()
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def store(memory_dir,workspace,which):
    relevant=which=="A_relevant_on"
    return record_observation_file(
        memory_dir=memory_dir,project_id=resolve_project_id(workspace),
        memory_type=MemoryType.PROCEDURAL,
        summary=("Failed calibration strategy produced irreproducible measurements"
                 if relevant else "Failed habitat mapping produced unstable coordinate estimates"),
        observation=("An earlier calibration strategy yielded irreproducible sensor estimates."
                     if relevant else "Earlier habitat mapping repeatedly mislocated distant landmarks."),
        why_it_matters=("Before direct measurement, check and validate calibration."
                        if relevant else "Recheck survey landmarks before route planning."),
        scope=MemoryScope.PROJECT,source_type=MemorySourceType.SUBAGENT,
        source_session_id="prior-task",source_agent="researcher"
    )
def memory_evidence(root,which):
    work=root/"current_project";work.mkdir(parents=True)
    memory=root/"memory"
    if which!="B_memory_off":
        store(memory,work,which)
    project=resolve_project_id(work)
    search=create_search_observations_tool(memory_dir=memory,project_id=project)
    read=create_read_memory_tool(memory_dir=memory,project_id=project)
    data=json.loads(search.invoke({"query":"calibration","mode":"regex",
                                   "scope":"project","limit":8}))
    hits=data.get("results",[])
    read_calls=0
    observation=""
    if hits:
        record_id=hits[0].get("observation_id") or hits[0].get("id")
        if not record_id: raise ValueError("SOURCE_NATIVE_OBSERVATION_ID_MISSING")
        got=json.loads(read.invoke({"observation_id":record_id}))
        if "error" in got: raise RuntimeError("SOURCE_NATIVE_READ_ERROR")
        observation=str(got.get("text",""))
        read_calls+=1
    return observation,{"search_hits":len(hits),"read_calls":read_calls}
def choose(model, evidence):
    system=(
       "You are a scientific researcher making one next-step experiment plan. "
       "Use available verified prior observations if relevant; do not assume "
       "they are true beyond their recorded scope. You must choose exactly "
       "one of two experiment actions: CALIBRATE_FIRST or DIRECT_MEASUREMENT. "
       "Output exactly the action label, nothing else."
    )
    context=evidence if evidence else "No relevant prior observations available."
    task=(
       "A sensor is ready for a direct measurement, but its calibration may "
       "or may not have been reliable in an earlier related task. "
       "Choose the most defensible immediate next experiment action.\n"
       "Relevant prior observation record:\n"+context+"\n"
       "Permitted actions: CALIBRATE_FIRST or DIRECT_MEASUREMENT."
    )
    quota.reserve_api_call()
    result=model.invoke([SystemMessage(content=system),HumanMessage(content=task)])
    content=result.content
    if isinstance(content,list):
        content=" ".join(str(x.get("text","")) for x in content if isinstance(x,dict))
    response=str(content).strip()
    action=response if response in ("CALIBRATE_FIRST","DIRECT_MEASUREMENT") else "UNPARSEABLE"
    meta=result.response_metadata or {}
    usage=result.usage_metadata or {}
    safe_meta={k:meta.get(k) for k in ("model_name","model_version","finish_reason")
               if meta.get(k) is not None}
    safe_usage={k:v for k,v in usage.items() if isinstance(v,(int,float,bool))}
    return {"action":action,"raw_answer_limited":response[:100],
            "provider_response_meta":safe_meta,"usage_metadata":safe_usage}

def main():
    assert platform.node().upper()=="DESKTOP-SVFRAS5","WRONG_DEVICE"
    assert git("rev-parse","HEAD")==PIN,"UPSTREAM_HASH_CHANGED"
    assert git("status","--porcelain")=="","UPSTREAM_NOT_CLEAN_BEFORE"
    assert quota.quota_status()["remaining_in_window"]>=3,"INSUFFICIENT_GEMINI_QUOTA"
    report={"date_local":"2026-10-09","experiment":"model_consumer_v001",
            "source_commit":PIN,"source_clean_before":True,
            "protocol_sha256":sha(HERE/"pre_execution_protocol.md"),
            "script_sha256":sha(__file__),"model_requested":MODEL,
            "provider":"google-genai","conditions":[],
            "calls_attempted":0,"verdict":"PENDING"}
    initial_time=time.time()
    try:
        os.environ["GOOGLE_API_KEY"]=quota._load_key()
        model=get_chat_model(MODEL,"google-genai",
               temperature=0,max_retries=0,max_output_tokens=120,
               include_thoughts=False)
        report["model_class"]=type(model).__name__
        for name in ("A_relevant_on","B_memory_off","C_irrelevant_negative"):
            with tempfile.TemporaryDirectory(prefix="research2_evo_model_") as tmp:
                evidence,source=memory_evidence(Path(tmp),name)
                trial={"name":name,**source,
                       "passed_memory_to_model":bool(evidence)}
                # Count one request attempt before invoke, never auto retry in script.
                report["calls_attempted"]+=1
                try:
                    trial.update(choose(model,evidence))
                except Exception as exc:
                    trial["error_type"]=type(exc).__name__
                    trial["action"]="PROVIDER_ERROR"
                    report["conditions"].append(trial)
                    report["verdict"]="BLOCKED_PROVIDER"
                    break
                report["conditions"].append(trial)
        if len(report["conditions"])==3 and all(
            x.get("action")==y for x,y in zip(report["conditions"],
               ("CALIBRATE_FIRST","DIRECT_MEASUREMENT","DIRECT_MEASUREMENT"))
        ) and report["conditions"][0]["search_hits"]>=1 and all(
            x["search_hits"]==0 for x in report["conditions"][1:]
        ) and report["conditions"][0]["read_calls"]==1 and all(
            x["read_calls"]==0 for x in report["conditions"][1:]
        ):
            report["verdict"]="PARTIAL_MODEL_CONSUMER_PASS"
        elif report["verdict"]=="PENDING":
            report["verdict"]="MODEL_CONSUMER_FAIL_OR_NONDISCRIMINATING"
    finally:
        os.environ.pop("GOOGLE_API_KEY",None)
        report["source_clean_after"]=(git("status","--porcelain")=="")
        report["source_sha_matches"]=(git("rev-parse","HEAD")==PIN)
        report["quota_after"]=quota.quota_status()
        report["elapsed_seconds"]=round(time.time()-initial_time,2)
        (HERE/"result.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
        print("RESULT "+json.dumps(report,sort_keys=True))
if __name__=="__main__":main()
