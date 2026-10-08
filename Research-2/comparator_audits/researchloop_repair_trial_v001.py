from pathlib import Path
import hashlib,ast,json,yaml,difflib,subprocess
root=Path.home()/"Research2"/"repair_trials"/"ResearchLoop_encoding_v001"
files={
"tests/researchloop/test_smoke_harness_contract.py":"py",
"tests/researchloop/test_reproduction_registry.py":"py",
"docs/research/V0/reproduction/REPRODUCTION_LEDGER.yaml":"yaml",
"docs/research/V0/reproduction/smoke_specs/PROVENANCE_ONLY.yaml":"yaml"}
def sha(b):return hashlib.sha256(b).hexdigest()
manifest={"status":"DEVELOPMENT_ONLY_SYNTAX_REPAIR_NOT_SEMANTIC_APPROVAL","original_commit":"7e0a4fbe0cf646f4c859b6d20e46870d73abb11a","files":[],"decisive_runs":0}
for rel,kind in files.items():
 p=root/rel; orig=p.read_bytes()
 decoded=orig.decode("gb18030")
 lines=decoded.splitlines(keepends=True)
 changed=[]
 for i,line in enumerate(lines):
  stripped=line.rstrip("\r\n")
  if kind=="py" and stripped.count('"')%2 and stripped.rstrip().endswith(",") and 'blocker_policy' in stripped or (kind=="py" and stripped.count('"')%2 and "ReproductionTarget(" in stripped):
   newline=line[len(stripped):]
   if stripped.endswith(","): stripped=stripped[:-1]+'",'
   changed.append(i+1);lines[i]=stripped+newline
  elif kind=="yaml" and ('fair_comparison_boundary:' in stripped or 'blocker_policy:' in stripped) and stripped.count('"')%2:
   newline=line[len(stripped):]
   lines[i]=stripped+'"'+newline; changed.append(i+1)
 fixed=''.join(lines)
 try:
  if kind=="py": ast.parse(fixed,filename=rel)
  else: yaml.safe_load(fixed)
  syntax="PASS"
 except Exception as e: syntax=type(e).__name__+":"+str(e)[:200]
 out=fixed.encode("utf-8")
 p.write_bytes(out)
 orig_git=subprocess.run(["git","-C",str(root),"rev-parse","HEAD:"+rel],capture_output=True,text=True)
 manifest["files"].append({"path":rel,"original_sha256":sha(orig),"original_git_blob":orig_git.stdout.strip(),"repaired_sha256":sha(out),"decoded":"gb18030_to_utf8","inserted_closing_quote_lines":changed,"syntax_or_yaml_parse":syntax,"semantic_fidelity":"UNDETERMINED"})
print(json.dumps(manifest,ensure_ascii=True,indent=2))
dst=Path.home()/"Research2"/"researchloop_repair_trial_v001_manifest.json"
dst.write_text(json.dumps(manifest,ensure_ascii=True,indent=2),encoding="utf-8")
