#!/usr/bin/env python3
# Research2 Relay5 P14/P15 source-derived budget-shadow audit (not native Environment)
import json,sys
C={'generate':8,'observe':8,'compare':10,'residual':6,'negative_control':8,'ancestor':8,'equivalence':10,'ood':14,'mist':10}
P14=('generate','observe','compare','residual','generate','negative_control','ancestor','equivalence','ood')
P15=('generate','observe','mist','compare','residual','generate','negative_control','ancestor','equivalence','ood')
budgets=(0,70,76,80,90,100)
def simulate(seq,b):
 t=[];sk=[];rem=b
 for a in seq:
  if rem>=C[a]: rem-=C[a];t.append(a)
  else:sk.append(a)
 return {'trace':t,'skipped':sk,'spent':b-rem,'remaining':rem}
def oracle(seq,b,target):return sum(C[x] for x in seq[:seq.index(target)+1])<=b
cases={str(b):{'P14':simulate(P14,b),'P15':simulate(P15,b),'P15_no_MIST':simulate(tuple(a for a in P15 if a!='mist'),b)} for b in budgets}
checks={
 'B0_no_actions':all(not cases['0'][p]['trace'] for p in ('P14','P15')),
 'B70_P14_equiv':'equivalence' in cases['70']['P14']['trace'],
 'B70_P15_equiv_censored':'equivalence' not in cases['70']['P15']['trace'],
 'B76_both_equiv':all('equivalence' in cases['76'][p]['trace'] for p in ('P14','P15')),
 'B80_P14_ood':'ood' in cases['80']['P14']['trace'],
 'B80_P15_ood_censored':'ood' not in cases['80']['P15']['trace'],
 'B90_both_ood':all('ood' in cases['90'][p]['trace'] for p in ('P14','P15')),
 'B100_both_full':all(len(cases['100'][p]['trace'])==len(seq) for p,seq in (('P14',P14),('P15',P15))),
 'MIST_mutation_matches_P14':all(cases[str(b)]['P15_no_MIST']['trace']==cases[str(b)]['P14']['trace'] for b in budgets),
 'independent_prefix_oracle':all((t in cases[str(b)][p]['trace'])==oracle(seq,b,t) for b in budgets for p,seq in (('P14',P14),('P15',P15)) for t in ('equivalence','ood')),
 'resource_bounds':all(0<=cases[str(b)][p]['spent']<=b for b in budgets for p in ('P14','P15'))
}
result={'source_commit':'633fc711e34e9bf1be37f5760147a5918276d31a','source_blobs':['47fc8c9f2d85646ade45b846d49efbd2db8d93c4','7fa1ff5a1455e498b1c6534c981c4c1a1b903da8'],'cases':cases,'checks':checks,'passed':sum(checks.values()),'total':len(checks),'limit':'source-derived schedule only; not native module or 19C certificate'}
print(json.dumps(result,sort_keys=True,separators=(',',':')))
if not all(checks.values()):sys.exit(1)
