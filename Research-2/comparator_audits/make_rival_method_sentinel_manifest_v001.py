from pathlib import Path
import sys, subprocess, hashlib, json, datetime, platform
base=Path.home()/"Research2"
scripts=[
 "evoscientist_scheduler_original_behavior_v001.py",
 "evoscientist_scheduler_mutation_dev_v001.py",
 "evomaster_selector_original_behavior_v001.py",
 "evomaster_selector_mutation_v001.py"]
rows=[]
for name in scripts:
    path=base/name
    run=subprocess.run([sys.executable,str(path)],capture_output=True,text=True,timeout=20,cwd=base)
    assert run.returncode==0,(name,run.stdout,run.stderr)
    rows.append({"script":name,"source_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                 "exit_code":run.returncode,
                 "stdout":run.stdout,"stderr":run.stderr[:2500]})
record={"kind":"R2_PRE_FREEZE_COMPARATOR_METHOD_SENTINELS",
        "recorded_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "host_platform":platform.platform(),"python":sys.version.split()[0],
        "rivals":["EvoScientist","EvoMaster"],"runs":rows,
        "policy_fidelity":"PARTIAL_METHOD_ONLY","decisive_benchmarks_run":0,
        "provider_api_calls":0,"secrets_recorded":False}
output=base/"2026-10-08_eon_rival_method_sentinels_v001.json"
output.write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding="utf-8")
print(json.dumps({"result":"4_DEVELOPMENT_SENTINELS_PASSED","output":str(output),"files":len(rows),"decisive_benchmarks_run":0}))
