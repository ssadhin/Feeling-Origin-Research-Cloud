#!/usr/bin/env python3
"""Research #2 Q1: native InternAgent hybrid memory, signed guidance & persistence."""
import hashlib, json, os, pathlib, subprocess, sys, tempfile, time, traceback

HERE = pathlib.Path(__file__).resolve().parents[2]
OUT = HERE / "research2" / "qualification" / "output-internagent-taskmem-v001"
OUT.mkdir(parents=True, exist_ok=True)
SOURCE = pathlib.Path(os.environ["R2_INTERNAGENT_ORIGINAL"])
PIN = "fa8c3eedfa9751d3752ea6eb49220b303ac2397d"
start = time.monotonic()
rows = []
guidance = {}
def git(*args):
    p = subprocess.run(["git","-C",str(SOURCE),*args],capture_output=True,text=True)
    if p.returncode: raise RuntimeError(p.stderr[-600:])
    return p.stdout.strip()
def probe(name, fn):
    try:
        detail=fn()
        rows.append({"name":name,"status":"PASS","evidence":str(detail)})
        print("PASS",name,detail,flush=True)
        return True
    except Exception as e:
        rows.append({"name":name,"status":"FAIL","error":type(e).__name__+": "+str(e),"traceback":traceback.format_exc()[-1800:]})
        print("FAIL",name,type(e).__name__,str(e),flush=True)
        return False
memory=None
source_hashes={}
def import_original():
    global memory
    assert git("rev-parse","HEAD")==PIN
    assert not git("status","--porcelain=v1","--untracked-files=all")
    for rel in ("internagent/mas/memory/task_memory.py","internagent/mas/memory/retriever.py","internagent/mas/models/embedding_models.py"):
        source_hashes[rel]=hashlib.sha256((SOURCE/rel).read_bytes()).hexdigest()
    sys.path.insert(0,str(SOURCE))
    import internagent.mas.memory.task_memory as taskmem
    memory=taskmem
    return "entire original source package import; SHA pinned exact clean commit"
if probe("PINNED_ORIGINAL_DIRECT_IMPORT",import_original):
    def exercise():
        def rec(identifier,label,name,desc):
            return memory.TaskMemRecord(record_id=identifier,name=name,title=name,description=desc,
                  statement=desc,method=desc,baseline_results={"score":50.0},
                  improved_results={"score":40.0 if label<0 else 65.0},
                  label=label,overall_improvement_rate=-20.0 if label<0 else 30.0,
                  success=label>0)
        with tempfile.TemporaryDirectory(prefix="r2_ia_taskmem_") as d:
            path=pathlib.Path(d)
            cold=memory.TaskMemoryLayer(memory_dir=str(path/"empty"),embedding_config={"model_type":"local","model_name":"sentence-transformers/all-MiniLM-L6-v2"})
            none=cold.generate_guidance_prompt("avalanche sensor overheat calibration",top_k=1,alpha=1.0)
            assert "No similar records found" in none,"cold-memory negative control failed"
            m=memory.TaskMemoryLayer(memory_dir=str(path/"history"),embedding_config={"model_type":"local","model_name":"sentence-transformers/all-MiniLM-L6-v2"})
            fixtures=[
              rec("NEG_A",-1,"avalanche overheat failure","avalanche cascade overheat noise intervention harmful"),
              rec("NEG_B",-1,"retinal artifact failure","retinal polarization artifact correction unusable"),
              rec("POS_A",1,"battery calibration improvement","battery thermopile calibration stability improves performance"),
              rec("POS_B",1,"satellite diffraction improvement","satellite diffraction correction spectral performance improves"),
            ]
            m.records=fixtures
            m.retriever.build_index(m.records,[m._extract_text(z) for z in m.records])
            q_neg="avalanche cascade overheat noise intervention harmful"
            q_pos="battery thermopile calibration stability improves performance"
            bad=m.retrieve_similar_records(q_neg,top_k=1,alpha=1.0)
            good=m.retrieve_similar_records(q_pos,top_k=1,alpha=1.0)
            assert bad and bad[0][0].label==-1,"failed-record retrieval mismatch "+str([(r.record_id,v) for r,v in bad])
            assert good and good[0][0].label==1,"successful-record retrieval mismatch "+str([(r.record_id,v) for r,v in good])
            neg=m.generate_guidance_prompt(q_neg,top_k=1,alpha=1.0)
            pos=m.generate_guidance_prompt(q_pos,top_k=1,alpha=1.0)
            assert "REJECT" in neg and "NEG_A" in neg,"source negative guidance not present "+neg[:500]
            assert "ACCEPT" in pos and "POS_A" in pos,"source positive guidance not present "+pos[:500]
            m._save_memory()
            fresh=memory.TaskMemoryLayer(memory_dir=str(path/"history"),embedding_config={"model_type":"local","model_name":"sentence-transformers/all-MiniLM-L6-v2"})
            assert len(fresh.records)==4,"native memory reload lost records"
            neg2=fresh.generate_guidance_prompt(q_neg,top_k=1,alpha=1.0)
            pos2=fresh.generate_guidance_prompt(q_pos,top_k=1,alpha=1.0)
            assert "REJECT" in neg2 and "ACCEPT" in pos2,"persistent sign-guidance changed after reload"
            guidance.update({"empty":none,"negative":neg,"positive":pos,"negative_reopened":neg2,"positive_reopened":pos2,
                      "negative_record_id":bad[0][0].record_id,"positive_record_id":good[0][0].record_id})
            return "original FAISS vector+BM25 build, opposite evidence-guidance, cold-start negative, persisted/reloaded stable"
    probe("TASKMEM_NATIVE_NEGATIVE_POSITIVE_RETRIEVAL_PERSISTENCE",exercise)
def source_clean():
    assert git("rev-parse","HEAD")==PIN
    assert not git("status","--porcelain=v1","--untracked-files=all")
    return "original source commit and all tracked/untracked files clean"
probe("ORIGINAL_SOURCE_POST_CLEAN",source_clean)
obj={"program":"Research2","phase":"Q1_nondecisive","original_commit":PIN,"source_hashes":source_hashes,
  "encoder":"sentence-transformers/all-MiniLM-L6-v2","native_module":"InternAgent TaskMemoryLayer, HybridRetriever, EmbeddingModel",
  "checks":rows,"guidance":guidance,
  "pass":sum(x["status"]=="PASS" for x in rows),"fail":sum(x["status"]=="FAIL" for x in rows),
  "full_19C_IA1_IA5_certified":False,"decisive_AES_trials":0,
  "elapsed_seconds":round(time.monotonic()-start,2)}
p=OUT/"internagent_taskmem_native_receipt.json"
p.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=True)+"\n",encoding="utf-8")
print(json.dumps({"pass":obj["pass"],"fail":obj["fail"],"original_source_unchanged":True if rows[-1]["status"]=="PASS" else False},sort_keys=True))
sys.exit(1 if obj["fail"] else 0)
