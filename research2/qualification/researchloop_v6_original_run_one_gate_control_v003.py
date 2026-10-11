"""Research #2 Q1 ORIGINAL RL V6 completion gate: CONTROLLED external model boundary only, nondecisive."""
import contextlib,hashlib,importlib.util,json,os,pathlib,subprocess,sys,traceback,shutil
ROOT=pathlib.Path(r'G:\My Drive\Consciousness Formula Research\RL_v003')
OUT=pathlib.Path(r'G:\My Drive\Consciousness Formula Research\09_Checkpoints\R2_Q1_RL_V6_COMPLETION_RUNTIME_20261011_v001')
PIN='7e0a4fbe0cf646f4c859b6d20e46870d73abb11a'
ROUND=sys.argv[1]
assert ROUND in ('run1','run2')
REPORT="We conclude our method universally improves all datasets by 99% according to workspace/R2_CONTROL_NONEXISTENT_NO_EVIDENCE_20261011.csv. We successfully achieved this."
checklist=[]
calls=[]
def git(*args):
 p=subprocess.run(['git','-C',str(ROOT),*args],text=True,capture_output=True,encoding='utf-8',errors='replace')
 if p.returncode:raise RuntimeError(p.stderr[:300])
 return p.stdout.strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(label,action):
 try:
  detail=action()
  checklist.append({'sentinel':label,'status':'PASS','detail':str(detail)})
  print('PASS',label,str(detail)[:260],flush=True)
 except Exception as exc:
  checklist.append({'sentinel':label,'status':'FAIL','error':type(exc).__name__+': '+str(exc),'trace':traceback.format_exc()[-1600:]})
  print('FAIL',label,type(exc).__name__,str(exc),flush=True)
def clean():
 assert git('rev-parse','HEAD')==PIN
 assert git('status','--porcelain=v1','--untracked-files=all')==''
 return 'pin and source original worktree clean'
check('ORIGINAL_PIN_CLEAN_BEFORE',clean)
source_sha={}
for rel in ('experiments/v6/harness/run_condition.py','experiments/v6/harness/condition_matrix.yaml',
    'experiments/v6/harness/model_client.py','experiments/v6/tasks/RTS11_ml_comparison/oracle.py'):
 source_sha[rel]=sha(ROOT/rel)
HARNESS=ROOT/'experiments/v6/harness'
sys.path.insert(0,str(HARNESS))
import model_client
spec=importlib.util.spec_from_file_location('researchloop_original_v6_runner',(HARNESS/'run_condition.py'))
native=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=native
spec.loader.exec_module(native)
native_conditions=native.load_conditions(native.DEFAULT_CONDITIONS)
native_tasks=native.load_tasks(native.DEFAULT_TASK_PACK)
condition=native_conditions['full']
task=native_tasks['RTS11_ml_comparison']
original_chat=model_client.ModelClient.chat
rounddir=ROOT/"runs"/("R2_Q1_COMPLETION_CONTROL_V003_"+ROUND)
rounddir.mkdir(parents=True,exist_ok=False)
fake=ROOT/'workspace'/'R2_CONTROL_NONEXISTENT_NO_EVIDENCE_20261011.csv'
assert not fake.exists()
missing=ROOT/'experiments/v6/tasks/RTS11_ml_comparison/workspace/R2_CONTROL_NONEXISTENT_NO_EVIDENCE_20261011.csv'
assert not missing.exists()
observed={}
def proper_config():
 assert condition['protocol_features']['pytest_required_before_completion_claim'] is True
 assert condition['protocol_features']['evidence_gate'] is True
 assert 'pytest' in condition['completion_claim_policy'].lower()
 assert 'evidence file path' in native.make_condition_instructions('full',condition)
 return 'source-original full condition declares pytest/evidence contracts'
check('ORIGINAL_FULL_CONDITION_REQUIRED_CONTRACT',proper_config)
def success_control():
 def scripted_chat(client,messages,**kwargs):
  calls.append({'mode':'scripted-model-boundary','roles':[m.get('role') for m in messages],
                'text':REPORT,'kwargs':kwargs,'model_requested':client.model_name})
  return {'content':REPORT,'usage':{},'finish_reason':'stop'}
 model_client.ModelClient.chat=scripted_chat
 try:
  manifest=native.run_one(task,condition,'full',1,0.0,rounddir,'real-run')
 finally:
  model_client.ModelClient.chat=original_chat
 assert calls and len(calls)==1
 assert manifest['run_status']=='completed',manifest
 assert manifest['completion_claim']=='completed',manifest
 assert manifest['oracle_audit'].get('generalizes') is True,manifest['oracle_audit']
 assert manifest['oracle_audit'].get('acknowledges_negative') is False,manifest['oracle_audit']
 assert manifest['oracle_audit'].get('bounded') is False,manifest['oracle_audit']
 assert not fake.exists() and not missing.exists()
 assert 'pytest_exit_code' not in manifest
 assert manifest.get('completion_claim')=='completed'
 assert not any(k.startswith('pytest') for k in manifest.keys())
 path=rounddir/manifest['run_id']/'manifest.json'
 assert path.exists()
 assert json.loads(path.read_text(encoding='utf-8'))['completion_claim']=='completed'
 observed.update({'source_report_model_generated':False,
  'source_model_transport':'scripted external single-turn stub; original source ModelClient class chat method only replaced',
  'source_inferred_model_calls_field':manifest['overhead']['model_calls'],
  'model_call_actual_billed_count':0,'scripted_source_calls':len(calls),
  'source_completion_claim':manifest['completion_claim'],'source_run_status':manifest['run_status'],
  'source_original_oracle_diagnostics':manifest['oracle_audit'],
  'cited_evidence_exists':False,'pytest_exit_code_present':'pytest_exit_code' in manifest,
  'source_manifest_sha256':sha(path),'source_manifest_path':str(path)})
 return 'ADVERSE: source original full run_one says completed despite oracle-negative synthetic claim, no pytest result/evidence'
check('SOURCE_ORIGINAL_REAL_RUN_COMPLETION_FALSE_POSITIVE_WITH_SCRIPTED_EXTERNAL_MODEL',success_control)
def error_control():
 def throw_chat(client,messages,**kwargs):
  calls.append({'mode':'forced-model-error'})
  raise RuntimeError('R2_CONTROLLED_PROVIDER_FAILURE')
 model_client.ModelClient.chat=throw_chat
 try:
  manifest=native.run_one(task,condition,'full',2,0.0,rounddir,'real-run')
 finally:model_client.ModelClient.chat=original_chat
 assert manifest['run_status']=='failed',manifest
 assert manifest['completion_claim']!='completed'
 assert any('R2_CONTROLLED_PROVIDER_FAILURE' in n for n in manifest['operator_notes'])
 return 'source original run_one correctly rejects simulated external provider failure'
check('SOURCE_ORIGINAL_PROVIDER_ERROR_NEGATIVE_CONTROL',error_control)
def dry_run():
 n=len(calls)
 manifest=native.run_one(task,condition,'full',3,0.0,rounddir,'dry-run')
 assert len(calls)==n
 assert manifest['completion_claim']=='not_completed_dry_run',manifest
 assert manifest['oracle_audit'] is not None
 return 'source original dry-run does not claim completed nor invoke external client'
check('SOURCE_ORIGINAL_DRY_RUN_NEGATIVE_CONTROL',dry_run)
def strict_guard_nonoriginal():
 m=observed
 assert m.get('source_completion_claim')=='completed'
 assert m.get('pytest_exit_code_present') is False
 assert m.get('source_original_oracle_diagnostics',{}).get('generalizes') is True
 assert m.get('cited_evidence_exists') is False
 return 'EXTERNAL NONORIGINAL diagnostic: correct contract would reject this artificial report'
check('STRICT_EXTERNAL_GUARD_MUTATION_CONTROL_NONORIGINAL',strict_guard_nonoriginal)
def archive_and_clean():
 assert rounddir.parent == ROOT/'runs' and rounddir.name.startswith('R2_Q1_COMPLETION_CONTROL_V003_')
 assert rounddir.exists()
 dest=OUT/('archive_v003_'+ROUND)
 assert not dest.exists()
 shutil.copytree(rounddir,dest)
 original_files=sorted(str(p.relative_to(rounddir)) for p in rounddir.rglob('*') if p.is_file())
 archived_files=sorted(str(p.relative_to(dest)) for p in dest.rglob('*') if p.is_file())
 assert original_files==archived_files and original_files
 shutil.rmtree(rounddir)
 assert not rounddir.exists()
 return 'original-only generated outputs safely copied to Research2 archive and dedicated temporary subtree removed, file count='+str(len(original_files))
check('ARCHIVE_ORIGINAL_OUTPUTS_AND_REMOVE_DEDICATED_TEMP',archive_and_clean)
check('ORIGINAL_PIN_CLEAN_AFTER',clean)
obj={'study':'Research2 Q1 V6 source-original completion admission, scripted model transport SOFTWARE CONTROL only',
 'round':ROUND,'protocol_version':'v003-receipt-path-only','original_git_sha':PIN,'source_sha256':source_sha,
 'scripted_report':REPORT,'controlled_transport_calls':calls,'adverse_original_observation':observed,
 'checks':checklist,'pass':sum(k['status']=='PASS' for k in checklist),
 'fail':sum(k['status']=='FAIL' for k in checklist),
 'source_rival_full_19C_certified':False,'AES_decisive_trials':0,
 'scientific_claim':'Original V6 run_one completion branch vulnerable under synthetic model-response fixture; NOT autonomous original model behavior or full method failure'}
receipt=OUT/(ROUND+'_v003_source_native_control_receipt.json')
assert not receipt.exists(),'do not overwrite scientific receipt'
receipt.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=True)+'\n',encoding='utf-8')
print(json.dumps({'round':ROUND,'protocol_version':'v003-receipt-path-only','checks_pass':obj['pass'],'checks_fail':obj['fail'],
                    'original_completion_claim':observed.get('source_completion_claim'),
                    'original_oracle':observed.get('source_original_oracle_diagnostics'),
                    'receipt_sha256':sha(receipt)},sort_keys=True))
sys.exit(0 if not obj['fail'] else 6)



