#!/usr/bin/env python3
"""Research #2 cloud-side pinned ResearchLoop baseline audit, development only."""
from __future__ import annotations
import ast
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
from datetime import datetime, timezone

SHA = "7e0a4fbe0cf646f4c859b6d20e46870d73abb11a"
ROOT = Path(os.environ.get("RUNNER_TEMP", "/tmp")) / "r2_researchloop_upstream_20261011_v002"
OUT = Path("research2/cloud_qualification/artifacts/rl-original-suite-v002")
OUT.mkdir(parents=True, exist_ok=True)
def cmd(args, *, cwd=None, timeout=300, capture=True, env=None):
    cp = subprocess.run(args, cwd=cwd, timeout=timeout, stdout=subprocess.PIPE if capture else None,
                        stderr=subprocess.STDOUT if capture else None, text=True, errors="replace", env=env)
    return cp.returncode, cp.stdout or ""
def git(*args, cwd=ROOT):
    code, value=cmd(["git","-C",str(cwd),*args], timeout=180)
    if code: raise RuntimeError(f"git command failed: {args}, {value[-500:]}")
    return value.strip()
receipt={"correction_from_v001":"v001 Python AST reporting reused stale prior variable after malformed UTF8. v002 explicitly initializes text=None and fails AST for malformed Python source; original v001 remains immutable.",
         "purpose":"Research2 nondecisive qualification check, not full method fidelity",
         "source":"plan-lab-szu/ResearchLoop", "pin":SHA,
         "start_utc":datetime.now(timezone.utc).isoformat(),
         "host":{"platform":platform.platform(),"python":sys.version,"cpu_count":os.cpu_count()},
         "original_pinned_source_modified":False,
         "model_calls":0,"provider_api_calls":0,"scientific_decisive_trials":0}
try:
    ROOT.mkdir(exist_ok=False)
    git("init",str(ROOT),cwd=ROOT)
    git("remote","add","origin","https://github.com/plan-lab-szu/ResearchLoop.git")
    git("fetch","--depth=1","--filter=blob:none","origin",SHA)
    git("checkout","--detach","FETCH_HEAD")
    head=git("rev-parse","HEAD")
    before=git("status","--porcelain")
    receipt["source_pin_verified"]=(head==SHA)
    receipt["source_clean_before"]=not bool(before)
    if head != SHA or before: raise RuntimeError("wrong or dirty upstream git snapshot")
    utf8_records=[]
    paths=git("ls-files").splitlines()
    text_paths=sorted(x for x in paths if x.lower().endswith((".py",".yaml",".yml",".md",".txt")) and (
        (x.startswith("tests/researchloop/test_") and x.endswith(".py"))
        or x.startswith("docs/research/V0/reproduction/")
        or x.startswith("docs/research/V1/")))
    for p in text_paths:
        b=(ROOT/p).read_bytes()
        blob=git("hash-object","--",p)
        index=git("rev-parse",":0:"+p)
        decode_error=None
        text=None
        try: text=b.decode("utf-8","strict")
        except UnicodeDecodeError as e: decode_error={"offset":e.start,"end":e.end,"reason":e.reason}
        parse_ok=None
        if p.startswith("tests/researchloop/"):
            if decode_error is not None:
                parse_ok=False
            else:
                try: ast.parse(text)
                except SyntaxError: parse_ok=False
                else: parse_ok=True
        utf8_records.append({"path":p,"utf8_valid":decode_error is None,
                             "decode_error":decode_error,"python_ast_valid":parse_ok,
                             "git_blob":blob,"index_blob":index,"blob_matches":blob==index,
                             "sha256":hashlib.sha256(b).hexdigest()})
    receipt["utf8_scan"]={"files":len(text_paths),
      "invalid_files":[x for x in utf8_records if not x["utf8_valid"]],
      "index_byte_identical":all(x["blob_matches"] for x in utf8_records),
      "controls":{"utf8_plain":"ascii".encode().decode("utf-8")=="ascii",
                 "ff_byte_rejected":None}}
    try: bytes([255]).decode("utf-8")
    except UnicodeDecodeError: receipt["utf8_scan"]["controls"]["ff_byte_rejected"]=True
    else: receipt["utf8_scan"]["controls"]["ff_byte_rejected"]=False
    (OUT/"per_file_utf8.json").write_text(json.dumps(utf8_records,indent=2),encoding="utf-8")
    env=os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"]="1"
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"]="1"
    args=[sys.executable,"-m","pytest","tests/researchloop","-q","--tb=short",
          "-p","no:cacheprovider","--basetemp",str(OUT.resolve()/"pytest_tmp")]
    try:
        code,stdout=cmd(args,cwd=ROOT,env=env,timeout=240)
    except subprocess.TimeoutExpired as ex:
        code=124; stdout=str(ex)
    (OUT/"raw_pytest_output.txt").write_text(stdout,encoding="utf-8")
    receipt["original_full_pytest_suite"]={"exit_code":code,
        "command":" ".join(args),"output_sha256":hashlib.sha256(stdout.encode()).hexdigest(),
        "collection_errors":len(re.findall(r"^ERROR tests/researchloop/",stdout,re.M)),
        "passed_count":int(re.search(r"(\d+) passed",stdout).group(1)) if re.search(r"(\d+) passed",stdout) else None,
        "failed_count":int(re.search(r"(\d+) failed",stdout).group(1)) if re.search(r"(\d+) failed",stdout) else None}
    after=git("status","--porcelain")
    receipt["source_clean_after"]=not bool(after)
    receipt["invalid_python_tests_ast_rejected"]=all(x["python_ast_valid"] is False for x in utf8_records if x["path"].startswith("tests/researchloop/") and not x["utf8_valid"])
    assert receipt["invalid_python_tests_ast_rejected"], "AST decoder regression"
    receipt["original_pinned_source_modified"]=bool(after)
    receipt["gate_status"]="BLOCKED" if code != 0 else "UPSTREAM_SUITE_PASS_ONLY"
    receipt["controls_pass"]=all(receipt["utf8_scan"]["controls"].values())
    assert receipt["source_clean_after"] and receipt["controls_pass"] and receipt["utf8_scan"]["index_byte_identical"]
except Exception as exc:
    receipt["gate_status"]="EXECUTION_ERROR"
    receipt["execution_error"]=str(exc)
    print("EXECUTION_ERROR",str(exc),file=sys.stderr)
finally:
    receipt["finish_utc"]=datetime.now(timezone.utc).isoformat()
    data=json.dumps(receipt,indent=2,ensure_ascii=False)+"\n"
    (OUT/"receipt.json").write_text(data,encoding="utf-8")
    sha={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file()}
    (OUT/"sha256_manifest.json").write_text(json.dumps(sha,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in receipt.items() if k not in ("host",)},indent=2)[:6000])
if receipt["gate_status"] == "EXECUTION_ERROR":
    sys.exit(2)
if not receipt.get("source_clean_after") or not receipt.get("controls_pass"):
    sys.exit(3)
