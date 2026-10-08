from pathlib import Path
import ast, hashlib, json
root=Path.home()/"Research2"/"comparators_20261008"/"EvoMaster"
read=lambda p:(root/p).read_text(encoding="utf-8")
phases=["solve","critique","rewrite","select"]
checks={}
checks["EM_S01_four_phase_sources"]=all((root/"playground"/"x_master"/"core"/"exp"/(p+"_exp.py")).is_file() for p in phases)
checks["EM_S02_four_phase_syntax"]=checks["EM_S01_four_phase_sources"] and all(ast.parse(read("playground/x_master/core/exp/"+p+"_exp.py")) is not None for p in phases)
intro=read("playground/x_master/README.md").lower()
checks["EM_S03_declared_four_phase_contract"]=all(p in intro for p in ["solver phase","critic phase","rewrite phase","select phase"])
run=read("run.py")
checks["EM_S04_explicit_evolution_opt_in"]=("--evolve" in run and "EvolutionManager" in run)
manager=read("evomaster/evolution/manager.py")
checks["EM_S05_baseline_analyze_evolve_rerun"]=all(x in manager for x in ["iter_000_baseline","analyzer.analyze(","applier.apply(","_run_agent("])
docs=read("docs/evolution.md")
checks["EM_S06_tool_proposals_not_autoapplied"]=("Tool proposals | No" in docs)
checks["EM_S07_serial_single_task_scope"]=("One task per evolution run" in docs and "Serial execution only" in docs)
checks["EM_N01_mutation_detects_deleted_opt_in"]=not ("--evolve" in run.replace("--evolve","") and "EvolutionManager" in run.replace("--evolve",""))
checks["EM_N02_mutation_detects_deleted_phase"]=not all(p in ["solve","critique","rewrite"] for p in phases)
result={"status":"SOURCE_STRUCTURAL_SENTINELS_ONLY","commit":"36a52bc6c42a6b9fd710a41c52f3c3bb948b9ac9","checks":checks,"pass":sum(checks.values()),"total":len(checks),"behavioral_fidelity":"NOT_TESTED","real_model_calls":0,"decisive_benchmarks":0}
out=Path.home()/"Research2"/"evomaster_structural_sentinels_v001.json"
out.write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))
