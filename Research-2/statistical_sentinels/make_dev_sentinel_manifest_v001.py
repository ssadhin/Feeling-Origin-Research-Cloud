"""Produce Research #2 Eon-executed nondecisive sentinel manifest with source hashes."""
from pathlib import Path
from datetime import datetime, timezone
import sys,platform,hashlib,re,json,subprocess
base=Path(__file__).parent
source_files=["neutral_claim_gate_dev_v001.py",
              "neutral_claim_gate_mutation_dev_v001.py",
              "provider_usage_contract_dev_v001.py",
              "six_rival_power_sensitivity_dev_v001.py"]
tests={}
for f in source_files:
    p=base/f
    sha=hashlib.sha256(p.read_bytes()).hexdigest()
    r=subprocess.run([sys.executable,str(p)],capture_output=True,text=True,timeout=20,cwd=base)
    log=r.stdout+"\n"+r.stderr
    if r.returncode!=0:
        print(f,log)
        raise RuntimeError(f+" failed")
    match=re.search(r"Ran (\d+) tests",log)
    if f=="neutral_claim_gate_mutation_dev_v001.py":
        d=json.loads(r.stdout)
        assert d["all_detected"] and len(d["mutations"])==5
        outcome="5/5 mutants detected"
    elif match:
        assert "OK" in log
        outcome=f"{match.group(1)} unit tests passed"
    else:
        d=json.loads(r.stdout)
        assert d["tests_passed"]==d["tests_total"]==5
        outcome="5/5 planning checks passed"
    tests[f]={"sha256":sha,"exit_code":r.returncode,"outcome":outcome,
              "captured_stdout":r.stdout,"captured_stderr":r.stderr}
out={"kind":"RESEARCH_2_DEVELOPMENT_SENTINEL_MANIFEST",
     "utc_created_at":datetime.now(timezone.utc).isoformat(),
     "python":sys.version,"host_platform":platform.platform(),
     "device":"Eon Agent MCP / Home Laptop",
     "source_files":tests,
     "provider_inference_calls":0,
     "decisive_benchmark_calls":0,
     "phase5_preregistration_frozen":False,
     "claim":"NONDECISIVE SOURCE/LOGIC ONLY; NOT PROVIDER TELEMETRY OR METHOD EFFICACY"}
dst=base/"2026-10-08_eon_development_sentinel_manifest_v001.json"
dst.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")
print("MANIFEST",dst)
print("RESULTS",[(k,v["outcome"]) for k,v in tests.items()])
