#!/usr/bin/env python3
"""NONDECISIVE Research #2, genuinely native AIS Journal selection on real localhost LLM."""
import contextlib, hashlib, http.server, importlib, io, json, logging, os, pathlib, subprocess, sys, threading, time, traceback, urllib.request
from collections import Counter
from dataclasses import asdict

ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=ROOT/"research2"/"qualification"/"output-ais-native-selector-v002"
OUT.mkdir(parents=True,exist_ok=True)
PIN="96bd51617cfdbb494a9fc283af00fe090edfae48"
ORIGINAL=pathlib.Path(os.environ["R2_AIS_ORIGINAL"])
MODEL_ID=os.environ["R2_REAL_MODEL_ID"]
EVENTS=[]
CHECKS=[]
run_start=time.monotonic()
def git(*args):
    v=subprocess.run(["git","-C",str(ORIGINAL),*args],text=True,capture_output=True)
    if v.returncode:raise RuntimeError("git "+str(args)+": "+v.stderr[-400:])
    return v.stdout.strip()
def record(name,fn):
    try:
        val=fn()
        CHECKS.append({"name":name,"status":"PASS","detail":str(val)})
        print("PASS",name,str(val),flush=True)
        return val
    except Exception as e:
        CHECKS.append({"name":name,"status":"FAIL","error":type(e).__name__+": "+str(e),"traceback":traceback.format_exc()[-1400:]})
        print("FAIL",name,type(e).__name__,str(e),flush=True)
        return None
class Transport(http.server.BaseHTTPRequestHandler):
    def log_message(self,*a):pass
    def forward(self):
        n=int(self.headers.get("Content-Length","0"))
        body=self.rfile.read(n) if n else b""
        start=time.monotonic()
        status=0
        output=b""
        try:
            req=urllib.request.Request("http://127.0.0.1:8080"+self.path,data=body if self.command=="POST" else None,headers={"Content-Type":"application/json"},method=self.command)
            with urllib.request.urlopen(req,timeout=130) as resp:
                output=resp.read()
                status=resp.status
        except urllib.error.HTTPError as e:
            output=e.read()
            status=e.code
        except Exception as e:
            status=502
            output=json.dumps({"error":{"message":str(e),"type":"proxy_transport_error"}}).encode()
        self.send_response(status)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",str(len(output)))
        self.end_headers()
        self.wfile.write(output)
        request_summary={}
        response_summary={}
        try:
            p=json.loads(body) if body else {}
            request_summary={"model":p.get("model"),"max_tokens":p.get("max_tokens"),
              "tool_choice":p.get("tool_choice"),"tools":[t.get("function",{}).get("name") for t in p.get("tools",[])],
              "message_roles":[m.get("role") for m in p.get("messages",[])],
              "message_texts":[str(m.get("content",""))[:2300] for m in p.get("messages",[])]}
        except Exception:pass
        try:
            p=json.loads(output)
            response_summary={"model":p.get("model"),"usage":p.get("usage"),"finish_reasons":[c.get("finish_reason") for c in p.get("choices",[])],
              "tool_calls":[{"name":t.get("function",{}).get("name"),"arguments":t.get("function",{}).get("arguments","")[:1500]} for c in p.get("choices",[]) for t in (c.get("message",{}).get("tool_calls") or [])],
              "message_content":[str(c.get("message",{}).get("content",""))[:1700] for c in p.get("choices",[])]}
        except Exception:pass
        EVENTS.append({"path":self.path,"status":status,"elapsed_sec":round(time.monotonic()-start,2),"request":request_summary,"response":response_summary})
    do_POST=forward
    do_GET=forward

handler=http.server.ThreadingHTTPServer(("127.0.0.1",11434),Transport)
thread=threading.Thread(target=handler.serve_forever,daemon=True)
thread.start()
journal=None
metric=None
cfg=None
def source_import():
    global journal,metric,cfg
    assert git("rev-parse","HEAD")==PIN,"original source pin mismatch"
    assert git("status","--porcelain=v1","--untracked-files=all")=="","dirty source"
    source_sha=hashlib.sha256((ORIGINAL/"ai_scientist/treesearch/journal.py").read_bytes()).hexdigest()
    assert source_sha=="5690b2b803300f655788064ec253159f2f41c86802e886e601cf640f798cd5b6",source_sha
    sys.path.insert(0,str(ORIGINAL))
    journal=importlib.import_module("ai_scientist.treesearch.journal")
    metric=importlib.import_module("ai_scientist.treesearch.utils.metric")
    from omegaconf import OmegaConf
    cfg=OmegaConf.create({"agent":{"select_node":{"model":"ollama/"+MODEL_ID,"temp":0.0}}})
    return "original journal import, MetricValue import, backend import; pinned git clean; cfg=original ollama model routing"
record("ORIGINAL_AIS_PACKAGE_IMPORT_AND_PIN",source_import)
def make_nodes():
    j=journal.Journal()
    root=journal.Node(id="root",metric=metric.MetricValue(value=1,maximize=True),is_buggy=False,is_buggy_plots=False,plan="simple validated baseline",analysis="Solid baseline")
    candidate=journal.Node(id="candidateA",parent=root,metric=metric.MetricValue(value=5,maximize=True),is_buggy=False,is_buggy_plots=False,plan="improved implementation",analysis="Sound evidence")
    buggy=journal.Node(id="high_but_buggy",parent=root,metric=metric.MetricValue(value=100,maximize=True),is_buggy=True,is_buggy_plots=False,plan="invalid implementation",analysis="Failing code")
    for n in (root,candidate,buggy):j.append(n)
    assert buggy not in j.good_nodes
    return j,candidate,buggy
def negative_controls():
    global j,candidate,buggy
    j,candidate,buggy=make_nodes()
    before=len(EVENTS)
    assert j.get_best_node(only_good=True,use_val_metric_only=True) is candidate
    all_bad=journal.Journal(nodes=[journal.Node(id="bad_only",metric=metric.MetricValue(value=100,maximize=True),is_buggy=True,is_buggy_plots=False)])
    assert all_bad.get_best_node(only_good=True,use_val_metric_only=False,cfg=cfg) is None
    assert len(EVENTS)==before,"original negative path unexpectedly generated model calls"
    return "original Journal metric-only filtered buggy node and empty-valid set stopped with zero model calls"
if journal is not None:record("NATIVE_NEGATIVE_CONTROLS_NO_MODEL_CALLS",negative_controls)
fallback=[]
class LoggerHook(logging.Handler):
    def emit(self,x):
        msg=x.getMessage()
        if "Falling back" in msg or "Error in LLM selection" in msg:fallback.append(msg)
hook=LoggerHook()
def actual_model_decision():
    logger=logging.getLogger("ai_scientist.treesearch.journal")
    logger.addHandler(hook)
    logger.setLevel(logging.WARNING)
    try:
        before=len(EVENTS)
        chosen=j.get_best_node(only_good=True,use_val_metric_only=False,cfg=cfg)
        observed=EVENTS[before:]
        assert observed,"original method did not invoke an actual provider"
        assert not fallback,"original method fell back, so function-calling mechanism did not execute successfully: "+str(fallback)
        assert chosen is not None and chosen.id == "candidateA","invalid or buggy selection"
        tools=[c for ev in observed for c in ev.get("response",{}).get("tool_calls",[])]
        assert any(x.get("name")=="select_best_implementation" for x in tools),"no genuine native OpenAI function tool call in model response"
        usages=[ev["response"]["usage"] for ev in observed if ev.get("response",{}).get("usage")]
        assert usages and all(int(u.get("prompt_tokens",0))>0 and int(u.get("completion_tokens",0))>0 for u in usages),"missing provider-reported model tokens"
        assert all(ev.get("status")==200 for ev in observed),"non-200 provider call"
        return "original Journal model-driven function-call decision; selected "+chosen.id+", genuine tools, provider tokens "+str(usages)
    finally:
        logger.removeHandler(hook)
if journal is not None and any(c["name"]=="NATIVE_NEGATIVE_CONTROLS_NO_MODEL_CALLS" and c["status"]=="PASS" for c in CHECKS):
    record("NATIVE_JOURNAL_FORCED_TOOL_CALL_SELECTION",actual_model_decision)
def source_clean():
    assert git("rev-parse","HEAD")==PIN
    assert git("status","--porcelain=v1","--untracked-files=all")==""
    return "git pin and original source worktree unchanged"
record("ORIGINAL_AIS_POST_SOURCE_CLEAN",source_clean)
handler.shutdown()
receipt={"study":"Research2 Q1 nondecisive","original_commit":PIN,"local_model":"Qwen2.5-3B-Instruct Q4_K_M",
"real_model_id":MODEL_ID,"original_get_best_node_backend":"ollama/native original backend localhost:11434",
"provider_calls":EVENTS,"fallback_detected":fallback,"checks":CHECKS,
"count_pass":sum(x["status"]=="PASS" for x in CHECKS),"count_fail":sum(x["status"]=="FAIL" for x in CHECKS),
"full_original_AIS1_AIS5_certified":False,"decisive_AES_trials":0,"elapsed_seconds":round(time.monotonic()-run_start,2)}
p=OUT/"ais_native_model_selector_receipt.json"
p.write_text(json.dumps(receipt,sort_keys=True,indent=2,ensure_ascii=True)+"\n",encoding="utf-8")
print(json.dumps({"pass":receipt["count_pass"],"fail":receipt["count_fail"],"provider_call_count":len(EVENTS),"fallback":fallback},sort_keys=True))
sys.exit(1 if receipt["count_fail"] else 0)
