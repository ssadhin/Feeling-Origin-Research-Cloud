#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,statistics,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import benchmark_v001_1 as core

GEN2=("P14","P15","P16","P17","P18")
BASELINES=core.POLICIES
POLICIES=BASELINES+GEN2

def vals_gap(s):
    vals=sorted(s.scores.values(),reverse=True)
    best=vals[0] if vals else 0.0
    gap=vals[0]-vals[1] if len(vals)>1 else 99.0
    return best,gap

def run_gen2(env,pid):
    s=env.state
    def act(a,**kw): return env.act(a,**kw)
    if pid in BASELINES:
        return core._run_public_policy(env,pid)

    if pid=="P14":
        for a in ("generate","observe","compare","residual","generate","negative_control","ancestor","equivalence","ood"):
            if env.can(a): act(a)

    elif pid=="P15":
        for a in ("generate","observe","mist","compare","residual","generate","negative_control","ancestor","equivalence","ood"):
            if env.can(a): act(a)

    elif pid=="P16":
        act("generate"); act("observe")
        best,gap=vals_gap(s)
        if best<1.0 or gap<0.45:
            if env.can("residual"): act("residual")
            if env.can("generate"): act("generate")
        elif gap<0.9 and env.can("compare"):
            act("compare")
        for a in ("negative_control","ancestor","equivalence"):
            if env.can(a): act(a)
        if "nonidentifiable" in s.detected:
            return
        best,gap=vals_gap(s)
        if gap<0.75 and env.can("intervene"):
            act("intervene")
        if env.can("software_test"): act("software_test")
        if env.can("ood"): act("ood")
        if env.can("observe"): act("observe")

    elif pid=="P17":
        act("generate"); act("observe")
        n0=len(s.candidates)
        best,gap=vals_gap(s)
        if best<1.2 or gap<0.8:
            if env.can("residual"): act("residual")
            if env.can("generate"): act("generate")
        best,gap=vals_gap(s)
        if (len(s.candidates)<=n0 or gap<0.9) and env.can("ancestor"):
            act("ancestor")
        if env.can("compare"): act("compare")
        best,gap=vals_gap(s)
        if gap<1.0 and env.can("equivalence"):
            act("equivalence")
        if "nonidentifiable" in s.detected:
            return
        best,gap=vals_gap(s)
        if gap<0.75 and env.can("intervene"):
            act("intervene")
        for a in ("negative_control","software_test","sensitivity","multiverse","ood"):
            if env.can(a): act(a)
        if env.can("observe"): act("observe")

    elif pid=="P18":
        act("generate"); act("observe")
        best,gap=vals_gap(s)
        if best<1.0:
            act("residual") if env.can("residual") else None
            act("generate") if env.can("generate") else None
        elif gap<0.7 and env.can("compare"):
            act("compare")
        for a in ("negative_control","ancestor"):
            if env.can(a): act(a)
        best,gap=vals_gap(s)
        if gap<1.0 and env.can("equivalence"):
            act("equivalence")
        if "nonidentifiable" in s.detected:
            return
        selected,conf=core.public_decision(s)
        best,gap=vals_gap(s)
        if conf<0.82 or gap<0.75:
            if env.can("intervene"): act("intervene")
            if env.can("software_test"): act("software_test")
        selected,conf=core.public_decision(s)
        if conf>=0.80 and env.can("ood"): act("ood")
        if env.can("observe"): act("observe")
    else:
        raise KeyError(pid)

def score(world,pid):
    env=core.Environment(world,pid)
    run_gen2(env,pid)
    s=env.state
    selected,confidence=core.public_decision(s)
    if "NONIDENTIFIABLE" in world.components:
        correct=selected=="UNDERDETERMINED"
    else:
        correct=selected==world.truth or selected in world.equivalent
    fp=(not correct) and confidence>=.80
    miss=world.requires_generation and selected==world.truth
    traps=set(world.traps)
    detect=True if not traps else bool(traps & s.detected)
    brier=(confidence-(1.0 if correct else 0.0))**2
    return dict(policy=pid,world_id=world.world_id,components="+".join(world.components),correct=int(correct),false_positive=int(fp),missing_recovery=int(miss),confidence=confidence,brier=brier,failure_detected=int(detect),spent=s.spent,budget_remaining=s.budget,selected=selected,truth=world.truth,history="|".join(s.history))

def run(split,n):
    return [score(w,p) for w in core.iter_worlds(split,n) for p in POLICIES]

def summarize(rows):
    out={}
    for p in POLICIES:
        rr=[r for r in rows if r['policy']==p]; n=len(rr)
        out[p]={
            'episodes':n,'accuracy':sum(r['correct'] for r in rr)/n,
            'false_positive_rate':sum(r['false_positive'] for r in rr)/n,
            'mean_brier':statistics.mean(r['brier'] for r in rr),
            'mean_cost':statistics.mean(r['spent'] for r in rr),
            'failure_detection_rate':sum(r['failure_detected'] for r in rr)/n,
            'missing_recovery_rate_unconditional':sum(r['missing_recovery'] for r in rr)/n,
        }
    front=[]
    for p,a in out.items():
        dominated=False
        for q,b in out.items():
            if q==p: continue
            no_worse=(b['accuracy']>=a['accuracy'] and b['false_positive_rate']<=a['false_positive_rate'] and b['mean_brier']<=a['mean_brier'] and b['mean_cost']<=a['mean_cost'])
            better=(b['accuracy']>a['accuracy'] or b['false_positive_rate']<a['false_positive_rate'] or b['mean_brier']<a['mean_brier'] or b['mean_cost']<a['mean_cost'])
            if no_worse and better: dominated=True; break
        if not dominated: front.append(p)
    return {'policies':out,'pareto_front':front}

def selftest():
    w=core.make_world('NONIDENTIFIABLE',123)
    e=core.Environment(w,'P14'); run_gen2(e,'P14'); sel,_=core.public_decision(e.state)
    assert sel=='UNDERDETERMINED', (sel,e.state.history,e.state.detected)
    w=core.make_world('REJECTED_ANCESTOR_RECOVERY',124)
    e=core.Environment(w,'P17'); run_gen2(e,'P17'); assert e.state.spent<=core.BUDGET
    assert score(core.make_world('HYBRID_TRUTH',125),'P18')==score(core.make_world('HYBRID_TRUTH',125),'P18')
    print('SELF_TEST_PASS_GEN2')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--self-test',action='store_true')
    ap.add_argument('--split',choices=('train','validation','locked_test','ood'),default='validation')
    ap.add_argument('--n-per-class',type=int,default=250)
    ap.add_argument('--out',type=Path,default=Path('v002.csv'))
    ap.add_argument('--summary',type=Path,default=Path('v002_summary.json'))
    a=ap.parse_args()
    if a.self_test: selftest(); return
    rows=run(a.split,a.n_per_class); a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    s=summarize(rows)
    s.update(split=a.split,n_per_class=a.n_per_class,claim_ceiling='Frozen Generation-2 evaluation. Interpret split according to preregistered claim ceiling.')
    a.summary.write_text(json.dumps(s,indent=2),encoding='utf-8')
    print(json.dumps(s,indent=2))
if __name__=='__main__': main()
