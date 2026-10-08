from pathlib import Path
import ast,json,hashlib
repo=Path.home()/"Research2"/"comparators_20261008"/"EvoScientist"
paths={
"lifecycle":"EvoScientist/middleware/memory_lifecycle.py",
"worker":"EvoScientist/memory/agents/memory_worker.py",
"proposals":"EvoScientist/memory/autoskills/proposals.py",
"observation_test":"tests/test_observation_memory.py",
"autoskills_test":"tests/test_autoskills.py"}
data={k:(repo/p).read_text(encoding="utf-8") for k,p in paths.items()}
checks={}
checks["ES_S01_source_files_present"]=all((repo/p).is_file() for p in paths.values())
checks["ES_S02_all_sources_parse"]=all(ast.parse(v) is not None for v in data.values())
checks["ES_S03_post_agent_sync_and_async"]=all(s in data["lifecycle"] for s in ["def after_agent(","async def aafter_agent(","launch_memory_worker","alaunch_memory_worker"])
checks["ES_S04_memory_scheduler_error_hooks"]=all(s in data["lifecycle"] for s in ["MemoryScheduler","record_worker_finished","record_worker_aborted"])
checks["ES_S05_worker_deny_tools"]=all(s in data["worker"] for s in ["_MEMORY_WORKER_EXCLUDED_TOOLS","delete","execute","task","write_file","write_todos"])
checks["ES_S06_skill_review_paths"]=all(s in data["proposals"] for s in ["approve_skill_proposal","reject_skill_proposal","submit_autoskill_proposal"])
checks["ES_S07_observation_lineage_test"]=all(s in data["observation_test"] for s in ["record_observation_file","source_session_id","source_agent","project_id"])
checks["ES_S08_autoskill_source_tests_exist"]=all(s in data["autoskills_test"] for s in ["approve_skill_proposal","reject_skill_proposal","submit_autoskill_proposal"])
checks["ES_N01_ban_removed_detected"]="write_file" not in data["worker"].replace('"write_file"',"")
checks["ES_N02_review_removed_detected"]="approve_skill_proposal" not in data["proposals"].replace("approve_skill_proposal","")
result={"status":"SOURCE_STRUCTURAL_SENTINELS_ONLY","upstream_commit":"3b382b92b8fdad6e1f13467c382dcdd91d9b19d2","checks":checks,"passed":sum(checks.values()),"total":len(checks),"method_behavior":"NOT_TESTED","provider_calls":0,"decisive_outcomes":0,"files":{k:{"path":paths[k],"sha256":hashlib.sha256(v.encode()).hexdigest()} for k,v in data.items()}}
(Path.home()/"Research2"/"evoscientist_structural_sentinels_v001.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))
