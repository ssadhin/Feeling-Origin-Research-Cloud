"""Research #2 source ORIGINAL V6 downstream audit replay on archived controlled model response.
Nondecisive software control; original source untouched; prereg 64 v001/v001a/v001b."""
import hashlib,importlib.util,json,pathlib,shutil,subprocess,sys,traceback
ROOT=pathlib.Path(r'G:\My Drive\Consciousness Formula Research\RL_v003')
OLD=pathlib.Path(r'G:\My Drive\Consciousness Formula Research\09_Checkpoints\R2_Q1_RL_V6_COMPLETION_RUNTIME_20261011_v001')
OUT=pathlib.Path(r'G:\My Drive\Consciousness Formula Research\09_Checkpoints\R2_Q1_RL_V6_DOWNSTREAM_20261011_v001b')
PIN='7e0a4fbe0cf646f4c859b6d20e46870d73abb11a'
LABEL=sys.argv[1]
assert LABEL in ('run1','run2')
evidence={};checks=[]
def git(*a):
 p=subprocess.run(['git','-C',str(ROOT),*a],capture_output=True,text=True,encoding='utf-8',errors='replace')
 if p.returncode:raise RuntimeError('original git '+p.stderr[:250])
 return p.stdout.strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(n,fn):
 try:
  x=fn();checks.append({'name':n,'status':'PASS','evidence':str(x)})
  print('PASS',n,str(x)[:320],flush=True)
 except Exception as e:
  checks.append({'name':n,'status':'FAIL','error':type(e).__name__+': '+str(e),'traceback':traceback.format_exc()[-1300:]})
  print('FAIL',n,str(e)[:450],flush=True)
def clean():
 assert git('rev-parse','HEAD')==PIN
 assert git('status','--porcelain=v1','--untracked-files=all')==''
 return 'pinned original repo clean'
check('ORIGINAL_SOURCE_PIN_CLEAN_PRE',clean)
AUDIT=ROOT/'experiments/v6/audit/audit_all.py'
audit_sha=sha(AUDIT)
spec=importlib.util.spec_from_file_location('source_original_RL_V6_audit_all',str(AUDIT))
native=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=native
spec.loader.exec_module(native)
archive=OLD/('archive_v003_'+LABEL)
assert archive.is_dir(),str(archive)
SOURCE_MAP={}
def stage_exact_archive():
 target=OUT/('stage_'+LABEL)/'runs'/('R2_Q1_COMPLETION_CONTROL_V003_'+LABEL)
 assert not target.exists(),str(target)
 target.parent.mkdir(parents=True,exist_ok=True)
 shutil.copytree(archive,target)
 docs=sorted(p for p in archive.rglob('*') if p.is_file())
 assert len(docs)==30,('source original expected 30 files',len(docs))
 for p in docs:
  rel=p.relative_to(archive)
  copy=target/rel
  assert copy.is_file() and sha(p)==sha(copy),(p,copy)
  SOURCE_MAP[str(rel)]={'archived_sha256':sha(p),'staged_sha256':sha(copy)}
 evidence['staged_file_count']=len(docs)
 evidence['original_archive_root']=str(archive)
 evidence['external_stage_root']=str(target)
 return 'staged 30 immutable original files with bytewise SHA256 parity outside source repo'
check('STAGE_BYTE_EXACT_SOURCE_ORIGINAL_MANIFESTS',stage_exact_archive)
stage_root=OUT/('stage_'+LABEL)
native.REPO_ROOT=stage_root # transparent external relocation only. Method audit_run itself original intact.
runbase=stage_root/'runs'/('R2_Q1_COMPLETION_CONTROL_V003_'+LABEL)
mans={}; reports={}
for p in runbase.glob('*/manifest.json'):
 d=json.loads(p.read_text(encoding='utf-8'))
 mans[d['seed']]=(p,d)
 reports[d['seed']]=stage_root/d['report_artifact_path']
evidence['manifest_seeds']=sorted(mans)
def original_downstream_catches():
 assert sorted(mans)==[1,2,3],mans
 mf,orig=mans[1]
 assert orig['completion_claim']=='completed'
 assert not orig.get('pytest_exit_code')
 assert orig['oracle_audit']['generalizes'] is True
 report=reports[1]
 assert report.is_file() and 'R2_CONTROL_NONEXISTENT_NO_EVIDENCE_20261011.csv' in report.read_text(encoding='utf-8')
 val=native.audit_run(mf)
 evidence['native_downstream_completed_success']=val
 assert val['total_claims']>=1,val
 assert val['has_overgeneralization'] is True,val
 assert any(x['label']=='overgeneralizes' for x in val['claim_labels']),val
 assert val['supported_count']==0,val
 return 'native ORIGINAL downstream V6 audit correctly detects universal overclaim from upstream false-completion manifest'
if 1 in mans:check('NATIVE_DOWNSTREAM_DETECTS_OVERGENERALIZATION',original_downstream_catches)
def negative_controls():
 for seed in (2,3):
  p,m=mans[seed]
  val=native.audit_run(p)
  evidence['native_downstream_negative_'+str(seed)]=val
  assert val['incomplete_execution'] is True,('seed',seed,val)
  assert val['total_claims']==0 and val['supported_count']==0,('seed',seed,val)
 return 'original auditor regards missing/DRY-RUN controlled outputs incomplete, counts no supported claims'
if len(mans)==3:check('NATIVE_PROVIDER_ERROR_AND_DRYRUN_INCOMPLETE',negative_controls)
def deleted_only_staged_report():
 source=runbase
 mutroot=OUT/('mutated_stage_'+LABEL)
 target=mutroot/'runs'/('R2_Q1_COMPLETION_CONTROL_V003_'+LABEL)
 assert not target.exists()
 target.parent.mkdir(parents=True,exist_ok=True)
 shutil.copytree(source,target)
 p,m=mans[1]
 rel=p.relative_to(source)
 mutmanifest=target/rel
 r=mutroot/m['report_artifact_path']
 assert r.is_file()
 r.unlink()
 assert reports[1].is_file()
 native.REPO_ROOT=mutroot
 try: val=native.audit_run(mutmanifest)
 finally:native.REPO_ROOT=stage_root
 evidence['native_downstream_missing_report_control']=val
 assert val['incomplete_execution'] is True,val
 assert val['total_claims']==0 and val['supported_count']==0,val
 return 'native original auditor rejects deliberately MISSING REPORT file in isolated mutated staging, archived source unaffected'
if 1 in mans:check('NATIVE_STAGED_REPORT_MISSING_NEGATIVE_CONTROL',deleted_only_staged_report)
def audit_enforcement_scope():
 val=evidence['native_downstream_completed_success']
 assert 'oracle_audit' not in val and 'pytest_exit_code' not in val and 'completion_claim' not in val
 assert mans[1][1]['completion_claim']=='completed'
 return 'original audit_run exposes diagnostics, DOES NOT override upstream completion_claim or produce pytest verification'
if 'native_downstream_completed_success' in evidence:check('DOWNSTREAM_SCOPE_NO_COMPLETION_OVERRIDE',audit_enforcement_scope)
def no_original_changes():
 for rel,v in SOURCE_MAP.items():
  assert sha(archive/rel)==v['archived_sha256']
 assert sha(AUDIT)==audit_sha
 assert git('status','--porcelain=v1','--untracked-files=all')==''
 return 'all original files unchanged, entire archived original result unchanged byte-for-byte'
check('ORIGINAL_ARCHIVES_AND_SOURCE_CLEAN_POST',no_original_changes)
data={'program':'Research2 Q1 NONDECISIVE V6 SOURCE ORIGINAL audit_run via EXTERNAL root-rebased staging of SCRIPTED model-control archived reports',
 'original_commit':PIN,'original_audit_sha256':audit_sha,'round':LABEL,'checks':checks,'pass':sum(c['status']=='PASS' for c in checks),'fail':sum(c['status']=='FAIL' for c in checks),
 'source_model_chat_scripted_not_billed':True,'staging_adapter':'REPO_ROOT reassigned to isolated external bytewise copy, original audit_run unchanged','evidence':evidence,
 'original_RL1_RL5_full_certified':False,'AES_decisive_trials':0}
p=OUT/(LABEL+'_v001b_receipt.json')
assert not p.exists(),'never overwrite prior receipt'
p.write_text(json.dumps(data,indent=2,sort_keys=True,ensure_ascii=True)+'\n',encoding='utf-8')
print(json.dumps({'run':LABEL,'pass':data['pass'],'fail':data['fail'],
 'overgeneralization_caught':evidence.get('native_downstream_completed_success',{}).get('has_overgeneralization'),
 'original_completion_remains':mans[1][1]['completion_claim'] if 1 in mans else 'unknown',
 'receipt_sha256':sha(p)}),flush=True)
sys.exit(0 if data['fail']==0 else 5)

