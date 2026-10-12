"""Research #2 v001: exactly pinned Research1 Python original module import; public TRAIN ONLY.
Preregistered Google Drive #95, 2026-10-12. Controls not native contestants."""
import hashlib,json,pathlib,subprocess,sys,traceback,collections,random
ROOT=pathlib.Path(r'G:\My Drive\Consciousness Formula Research\09_Checkpoints\R2_Q1_R1_EXACT_NATIVE_IMPORT_20261012_v001')
SRC=ROOT/'pinned_source'
RUN=sys.argv[1]
assert RUN in ('run1','run2')
sys.path.insert(0,str(SRC))
import benchmark_v001_1 as core
import benchmark_v002 as gen2
checks=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def gitblob(p):
 b=p.read_bytes()
 return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def check(n,fn):
 try:
  detail=fn()
  checks.append({'check':n,'status':'PASS','detail':str(detail)})
  print('PASS '+n+' '+str(detail)[:400],flush=True)
 except Exception as e:
  checks.append({'check':n,'status':'FAIL','error':str(e),'traceback':traceback.format_exc()[-1100:]})
  print('FAIL '+n+' '+str(e)[:400],flush=True)
def exact_sources():
 files=[('benchmark_v001_1.py','7fa1ff5a1455e498b1c6534c981c4c1a1b903da8'),
        ('benchmark_v002.py','47fc8c9f2d85646ade45b846d49efbd2db8d93c4')]
 for name,want in files:assert gitblob(SRC/name)==want,(name,gitblob(SRC/name))
 assert core.Environment.__module__=='benchmark_v001_1'
 assert gen2.run_gen2.__module__=='benchmark_v002'
 return 'two EXACT original Research1 Git blobs and imports, not transcribed helpers'
check('ORIGINAL_SOURCE_EXACT_HASH_AND_IMPORT',exact_sources)
env_data={}
def run_arm(w,arm):
 schedule='P14' if arm=='A' else 'P15'
 env=core.Environment(w,'P15' if arm=='D' else 'P14')
 if arm=='C':
  original=env.act
  def isolate_mist_rng(action,**kw):
   if action=='mist':
    old=env._rng.getstate()
    try:return original(action,**kw)
    finally:env._rng.setstate(old)
   return original(action,**kw)
  env.act=isolate_mist_rng # explicitly nonoriginal counterfactual at instance boundary
 gen2.run_gen2(env,schedule)
 sel,conf=core.public_decision(env.state)
 good=sel=='UNDERDETERMINED' if 'NONIDENTIFIABLE' in w.components else (sel==w.truth or sel in w.equivalent)
 return {'selected':sel,'correct':int(good),'missing_recovery':int(w.requires_generation and sel==w.truth),
         'spent':env.state.spent,'actions':tuple(env.state.history),
         'confidence':conf,'world_id':w.world_id}
stats={a:{'correct':0,'recovery':0,'costs':collections.Counter(),'world_count':0} for a in 'ABCD'}
discord={'B_A_recovery':0,'C_A_recovery':0,'C_A_selection':0,'D_B_recovery':0,'C_A_correct':0}
raw=ROOT/(RUN+'_raw_2200x4.jsonl')
assert not raw.exists(),'do not overwrite raw evidence'
n=0; n_generation=0
try:
 with raw.open('w',encoding='utf-8',newline='\n') as f:
  for w in core.iter_worlds('train',100):
   n+=1
   n_generation+=int(w.requires_generation)
   row={'world_id':w.world_id,'requires_generation':w.requires_generation}
   for a in 'ABCD':
    x=run_arm(w,a)
    assert x['world_id']==w.world_id
    row[a]=x
    stats[a]['correct']+=x['correct'];stats[a]['recovery']+=x['missing_recovery']
    stats[a]['costs'][x['spent']]+=1;stats[a]['world_count']+=1
   discord['B_A_recovery']+=int(row['B']['missing_recovery']!=row['A']['missing_recovery'])
   discord['C_A_recovery']+=int(row['C']['missing_recovery']!=row['A']['missing_recovery'])
   discord['C_A_selection']+=int(row['C']['selected']!=row['A']['selected'])
   discord['D_B_recovery']+=int(row['D']['missing_recovery']!=row['B']['missing_recovery'])
   discord['C_A_correct']+=int(row['C']['correct']!=row['A']['correct'])
   # keep original exact action histories and no post-outcome per-case exclusions
   f.write(json.dumps(row,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n')
except Exception as e:
 print('EXECUTION_FAILED '+type(e).__name__+' '+str(e),flush=True)
 raise
env_data={'classes':len(core.WORLD_CLASSES),'n_worlds':n,'n_generation':n_generation,
          'counts':{a:{'correct':stats[a]['correct'],'recovery':stats[a]['recovery'],
                      'costs':dict(stats[a]['costs'])} for a in 'ABCD'},
          'discordance':discord,'raw_sha256':sha(raw),
          'original_source_sha256':{p.name:sha(p) for p in SRC.glob('benchmark_*.py')}}
def nworld():
 assert n==2200 and len(core.WORLD_CLASSES)==22 and n_generation==400
 return (n,n_generation)
check('ORIGINAL_TRAIN_WORLD_POPULATION',nworld)
def reference():
 expected={a:(corr,reco) for a,corr,reco in [('A',2123,343),('B',2106,327),('C',2115,343),('D',2117,344)]}
 observed={a:(stats[a]['correct'],stats[a]['recovery']) for a in 'ABCD'}
 assert observed==expected,(observed,expected)
 return observed
check('PREDECLARED_COMPARE_TRANSCRIPTION_COUNTS',reference)
def costs():
 for a in 'ABCD':
  want=80 if a=='A' else 90
  assert stats[a]['costs']=={want:2200},(a,stats[a]['costs'])
 return {a:dict(stats[a]['costs']) for a in 'ABCD'}
check('ACTION_RESOURCE_COST_PARITY',costs)
def rng_recovery():
 assert discord['C_A_recovery']==0,discord
 assert discord['C_A_selection']==0,discord
 assert discord['C_A_correct']>0,discord
 return discord
check('MIST_RNG_COUNTERFACTUAL_DISCORDANCE',rng_recovery)
def label():
 assert discord['B_A_recovery']>0 and discord['D_B_recovery']>0,discord
 return discord
check('POLICY_LABEL_RNG_COUPLING_IDENTIFIED',label)
def exact_end():
 return exact_sources()
check('ORIGINAL_SOURCE_IDENTICAL_AFTER',exact_end)
summary={'protocol':'Research2 R1 exact original module import v001 nondecisive','commit':'633fc711e34e9bf1be37f5760147a5918276d31a',
         'run':RUN,'control_C_original':False,'only_split':'train',
         'notes':'P14/P15 label-seeded stochastic streams differ; source-exact core and gen2 imported; AES v2 NEVER RUN',
         'observations':env_data,'checks':checks,'passes':sum(z['status']=='PASS' for z in checks),'fails':sum(z['status']=='FAIL' for z in checks),
         'decisive_AES_runs':0}
out=ROOT/(RUN+'_receipt.json')
assert not out.exists()
out.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n',encoding='utf-8')
print(json.dumps({'run':RUN,'passes':summary['passes'],'fails':summary['fails'],'observed':env_data['counts'],
                 'discordance':discord,'raw_sha256':env_data['raw_sha256'],'receipt_sha256':sha(out)},sort_keys=True),flush=True)
sys.exit(0 if summary['fails']==0 else 5)

