"""Research2 R1 P14/P15 public-TRAIN exact full upstream source module import; v002 metric reconciliation."""
import collections,hashlib,json,pathlib,sys,traceback
ROOT=pathlib.Path(r'G:\My Drive\Consciousness Formula Research\09_Checkpoints\R2_Q1_R1_EXACT_NATIVE_IMPORT_20261012_v001')
SRC=ROOT/'pinned_source';ROUND=sys.argv[1];assert ROUND in ('run1','run2')
sys.path.insert(0,str(SRC))
import benchmark_v001_1 as core
import benchmark_v002 as gen2
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blob(p):
 b=p.read_bytes();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
checks=[]
def check(name,fn):
 try:
  value=fn();checks.append({'name':name,'status':'PASS','detail':str(value)});print('PASS',name,str(value)[:400],flush=True)
 except Exception as e:
  checks.append({'name':name,'status':'FAIL','detail':str(e),'traceback':traceback.format_exc()[-1000:]});print('FAIL',name,str(e)[:500],flush=True)
def source():
 p=SRC/'benchmark_v001_1.py';q=SRC/'benchmark_v002.py'
 assert blob(p)=='7fa1ff5a1455e498b1c6534c981c4c1a1b903da8'
 assert blob(q)=='47fc8c9f2d85646ade45b846d49efbd2db8d93c4'
 return 'source originals imported, Git blobs unmodified'
check('BLOB_EXACT_MODULES_BEFORE',source)
stats={a:dict(present=0,selected=0,correct=0,costs=collections.Counter()) for a in 'ABCD'}
disc=collections.Counter()
path=ROOT/(ROUND+'_v002_raw_2200x4.jsonl')
assert not path.exists(),'preserve prior results'
def evaluate(world,a):
 label='P15' if a=='D' else 'P14'
 env=core.Environment(world,label)
 if a=='C':
  native_act=env.act
  def intervene(act,**kw):
   if act!='mist':return native_act(act,**kw)
   rng=env._rng.getstate()
   try:return native_act(act,**kw)
   finally:env._rng.setstate(rng)
  env.act=intervene
 gen2.run_gen2(env,'P14' if a=='A' else 'P15')
 selected,confidence=core.public_decision(env.state)
 correct=int(selected=='UNDERDETERMINED' if 'NONIDENTIFIABLE' in world.components else (selected==world.truth or selected in world.equivalent))
 return dict(present=int(world.requires_generation and world.truth in env.state.candidates),
             selected_truth=int(world.requires_generation and selected==world.truth),
             correct=correct,selected=selected,spent=env.state.spent,history=tuple(env.state.history))
n=0;n_gen=0
with path.open('w',encoding='utf-8',newline='\n') as fp:
 for w in core.iter_worlds('train',100):
  n+=1;n_gen+=int(w.requires_generation)
  item={'world':w.world_id,'requires_generation':w.requires_generation}
  for a in 'ABCD':
   x=evaluate(w,a);item[a]=x
   for k,field in [('present','present'),('selected','selected_truth'),('correct','correct')]:
    stats[a][k]+=x[field]
   stats[a]['costs'][x['spent']]+=1
  for x,y,label in [('A','B','A_B_present'),('A','C','A_C_present'),('D','B','D_B_present')]:
   disc[label]+=int(item[x]['present']!=item[y]['present'])
  disc['A_C_selected']+=int(item['A']['selected']!=item['C']['selected'])
  fp.write(json.dumps(item,sort_keys=True,separators=(',',':'))+'\n')
summary={'n':n,'generation':n_gen,'counts':{a:{**{k:v for k,v in stats[a].items() if k!='costs'},'costs':dict(stats[a]['costs'])} for a in 'ABCD'},
         'discord':dict(disc),'raw_sha256':h(path),'frozen_original_git':'633fc711e34e9bf1be37f5760147a5918276d31a'}
def population():
 assert (n,n_gen,len(core.WORLD_CLASSES))==(2200,400,22);return (n,n_gen)
check('PUBLIC_TRAIN_POPULATION',population)
def primary():
 got=tuple(stats[a]['present'] for a in 'ABCD')
 assert got==(343,327,343,344),got
 assert disc['A_C_present']==0,disc
 assert disc['A_B_present']>0 and disc['D_B_present']>0,disc
 return {'candidate_recovery':got,'discordances':dict(disc)}
check('PRIOR_V024_PRIMARY_CANDIDATE_RECOVERY',primary)
def secondary():
 expected_selected=(328,309,319,320)
 expected_correct=(2123,2106,2115,2117)
 got_selected=tuple(stats[a]['selected'] for a in 'ABCD')
 got_correct=tuple(stats[a]['correct'] for a in 'ABCD')
 assert got_selected==expected_selected,(got_selected,expected_selected)
 assert got_correct==expected_correct,(got_correct,expected_correct)
 return {'final_selected_truth':got_selected,'accuracy':got_correct}
check('SOURCE_EXACT_SECONDARY_TERMINAL_DECISIONS',secondary)
def costs():
 for a in 'ABCD':
  assert stats[a]['costs']=={80 if a=='A' else 90:2200},(a,stats[a]['costs'])
 return {a:dict(stats[a]['costs']) for a in 'ABCD'}
check('SOURCE_EXACT_ACTION_COSTS',costs)
check('ORIGINAL_GIT_BLOBS_IDENTICAL_AFTER',source)
d={'status':'nondecisive source-native R1 metric reconciliation v002','run':ROUND,
   'source_original_imported':True,'counterfactual_C_original_contestant':False,
   'summary':summary,'checks':checks,'passes':sum(x['status']=='PASS' for x in checks),'fails':sum(x['status']=='FAIL' for x in checks),
   'claim_ceiling':'Research 1 P14/P15 public TRAIN metric reconciliation, NOT AES tournament','decisive_AES_trials':0}
out=ROOT/(ROUND+'_v002_receipt.json');assert not out.exists()
out.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'round':ROUND,'passes':d['passes'],'fails':d['fails'],'summary':summary,'receipt_sha256':h(out)},sort_keys=True))
sys.exit(0 if d['fails']==0 else 5)

