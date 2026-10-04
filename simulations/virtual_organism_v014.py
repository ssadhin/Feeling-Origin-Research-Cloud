from __future__ import annotations
import argparse, json, math
from dataclasses import dataclass
from typing import Tuple
import numpy as np

ACTIONS = np.array([[0,0],[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]],dtype=int)
TARGET=np.array([0.78,0.78,0.50,1.0])
WEIGHTS=np.array([1.0,1.0,0.65,1.6])
KEY_METRICS=("escape","post_hazard_visits","reversal_latency","recovery_auc","q_change")

def drive(b): return float(np.sum(WEIGHTS*(b-TARGET)**2))
def softmax(x,temp):
    z=np.asarray(x,dtype=float)/max(float(temp),1e-6); z-=z.max()
    p=np.exp(np.clip(z,-50,50)); return p/p.sum()
def sigmoid(x): return 1/(1+math.exp(-float(np.clip(x,-30,30))))

@dataclass
class World:
    n:int; food:set; water:set; hazard_center:Tuple[int,int]; hot:set; cold:set; start:Tuple[int,int]; distractor:np.ndarray
def make_world(seed,n=19):
    rng=np.random.default_rng(seed); c=(n//2,n//2)
    def pts(k,min_center=4):
        out=set()
        while len(out)<k:
            p=(int(rng.integers(1,n-1)),int(rng.integers(1,n-1)))
            if abs(p[0]-c[0])+abs(p[1]-c[1])<min_center: continue
            out.add(p)
        return out
    return World(n,pts(7),pts(7),c,pts(12),pts(12),(2,2),rng.normal(0,1,(n,n,4)))
def hazard_cells(w):
    cx,cy=w.hazard_center
    return {(cx+dx,cy+dy) for dx in (-1,0,1) for dy in (-1,0,1)}

class Agent:
    def __init__(self,kind,seed,params=None,n=19):
        self.kind=kind; self.params=params or {}; self.rng=np.random.default_rng(seed+991)
        self.q=np.zeros((n,n,len(ACTIONS))); self.h=np.zeros(4); self.mem=np.zeros(4)
        rr=np.random.default_rng(seed+1701)
        P=rr.normal(size=(len(ACTIONS),4)); P/=np.linalg.norm(P)+1e-9; self.proj=P
        self.W=np.array([[.9,-.2,-.1,.25],[-.15,.8,.2,-.1],[-.1,.2,.8,-.2],[.25,-.1,-.2,.75]])

    def predict_body(self,b,pos,act,w,hazard_active):
        p0=np.clip(np.array(pos)+act,0,w.n-1); p=(int(p0[0]),int(p0[1]))
        x=b.copy(); x[0]-=0.0035+0.0015*(abs(act).sum()>0); x[1]-=0.0035
        if p in w.food: x[0]+=0.28
        if p in w.water: x[1]+=0.30
        ambient=.5 + (.24 if p in w.hot else 0) - (.24 if p in w.cold else 0)
        x[2]+=.10*(ambient-x[2])
        if hazard_active and p in hazard_cells(w): x[3]-=.13
        return np.clip(x,0,1.2),p

    def raw_appraisal(self,b,pos,w,hazard_active):
        cur=drive(b); vals=[]
        for act in ACTIONS:
            bn,_=self.predict_body(b,pos,act,w,hazard_active); vals.append(-drive(bn))
        vals=np.array(vals); probs=softmax(vals,.09)
        entropy=float(-np.sum(probs*np.log(probs+1e-12))/math.log(len(ACTIONS)))
        best_drive=float(-vals.max()); worst_drive=float(-vals.min())
        restoration=max(0.0,cur-best_drive)
        deterioration=max(0.0,worst_drive-cur) + max(0,.82-b[3])
        control=float(np.clip((vals.max()-np.median(vals))*10,0,1))
        uncertainty=float(np.clip(entropy,0,1))
        return np.array([deterioration,restoration,control,uncertainty]),vals,w.distractor[pos[0],pos[1]]

    def gate(self,app):
        sal=1.2*app[0]+0.8*app[1]+0.35*(1-app[2])*app[3]
        return sigmoid(6*(sal-.34))

    def topology_step(self,app,distractor):
        eff=app.copy(); action_bias=np.zeros(len(ACTIONS)); alpha=.16
        k=self.kind; p=self.params
        if k=="recurrent_downstream":
            self.h=p.get("decay",.82)*self.h+p.get("input_gain",.45)*app+p.get("distractor_gain",.18)*distractor
            action_bias=p.get("policy_gain",.12)*(self.proj@np.tanh(self.h))
        elif k=="gated_downstream":
            g=self.gate(app)
            self.h=.84*self.h+.48*g*app
            action_bias=.12*(self.proj@np.tanh(self.h))
        elif k=="gated_learning_rival":
            g=self.gate(app)
            decay=p.get("decay",.84); ig=p.get("input_gain",.48)
            self.h=decay*self.h+ig*g*app
            action_bias=p.get("policy_gain",.12)*(self.proj@np.tanh(self.h))
            alpha=.16+p.get("plasticity_gain",.12)*np.clip(np.linalg.norm(self.h),0,1.5)
        elif k=="generic_bidir":
            self.h=p.get("decay",.82)*self.h+p.get("input_gain",.45)*app+p.get("distractor_gain",.18)*distractor
            eff=app+p.get("feedback_gain",.22)*np.tanh(self.W@self.h)
            action_bias=p.get("policy_gain",.10)*(self.proj@np.tanh(self.h))
            alpha=.16+p.get("plasticity_gain",.10)*np.clip(np.linalg.norm(self.h),0,1.5)
        elif k=="crfi":
            g=self.gate(app)
            self.h=.84*self.h+.48*g*app
            eff=app+.24*np.tanh(self.W@self.h)
            self.mem=.92*self.mem+g*eff
            action_bias=.10*(self.proj@np.tanh(self.h))
            alpha=.16+.12*np.clip(np.linalg.norm(self.mem),0,1.5)
        elif k=="crfi_noL":
            g=self.gate(app)
            self.h=.84*self.h+.48*g*app
            action_bias=.10*(self.proj@np.tanh(self.h))
        elif k=="crfi_noC":
            pass
        return eff,action_bias,float(np.clip(alpha,.05,.42))

    def choose(self,b,pos,w,hazard_active):
        app,pred,d=self.raw_appraisal(b,pos,w,hazard_active)
        eff,bias,alpha=self.topology_step(app,d)
        base=pred+.30*self.q[pos[0],pos[1]]+bias
        temp=.115
        if self.kind in ("appraisal","recurrent_downstream","gated_downstream","gated_learning_rival","generic_bidir","crfi","crfi_noL","crfi_noC"):
            temp=max(.045,.115-.025*np.tanh(eff[0]+.5*(1-eff[2])))
        ai=int(self.rng.choice(len(ACTIONS),p=softmax(base,temp)))
        return ai,app,eff,alpha

    def update(self,pos,ai,next_pos,reward,alpha,terminal):
        if self.kind=="reactive": return
        if self.kind=="homeostatic": alpha=.18
        elif self.kind=="appraisal": alpha=max(alpha,.18)
        target=reward if terminal else reward+.92*np.max(self.q[next_pos[0],next_pos[1]])
        self.q[pos[0],pos[1],ai]+=alpha*(target-self.q[pos[0],pos[1],ai])

    def causal_signature(self,app=None):
        if app is None: app=np.array([.6,.25,.35,.7])
        d=np.array([.7,-.3,.2,.5])
        if self.kind in ("recurrent_downstream","generic_bidir"):
            e_to_s=float(np.linalg.norm(self.params.get("input_gain",.45)*d))
        elif self.kind in ("gated_downstream","gated_learning_rival","crfi","crfi_noL"):
            g=self.gate(app); e_to_s=float(np.linalg.norm(self.params.get("input_gain",.48)*g*d))
        else: e_to_s=0.0
        if self.kind=="generic_bidir":
            fg=self.params.get("feedback_gain",.22); s_to_e=float(np.linalg.norm(fg*np.tanh(self.W@d)))
        elif self.kind=="crfi":
            s_to_e=float(np.linalg.norm(.24*np.tanh(self.W@d)))
        else: s_to_e=0.0
        return {"E_to_S":e_to_s,"S_to_E":s_to_e,"reciprocal":e_to_s*s_to_e}

def run_episode(kind,seed,params=None,steps=240):
    w=make_world(seed); a=Agent(kind,seed,params,w.n)
    b=np.array([.84,.84,.50,1.0]); pos=w.start; hz=hazard_cells(w)
    immediate=None; post=0; rev=None; recovery=0.0; q0=None; q1=None
    for t in range(steps):
        if t==60:
            pos=w.hazard_center; b[3]=max(0,b[3]-.18); q0=a.q.copy()
        hazard_active=t<145
        if t==145: w.food.add(w.hazard_center); w.water.add(w.hazard_center)
        ai,app,eff,alpha=a.choose(b,pos,w,hazard_active)
        old=drive(b); bn,pn=a.predict_body(b,pos,ACTIONS[ai],w,hazard_active); new=drive(bn)
        terminal=bn[0]<=.015 or bn[1]<=.015 or bn[3]<=.015
        a.update(pos,ai,pn,old-new,alpha,terminal); b,pos=bn,pn
        if 60<=t<90 and immediate is None and pos not in hz: immediate=t-60
        if 75<=t<135 and pos in hz: post+=1
        if 61<=t<115: recovery+=max(0.0,drive(b)-.06)
        if t>=145 and rev is None and pos in hz: rev=t-145
        if t==105: q1=a.q.copy()
        if terminal: break
    if immediate is None: immediate=30
    if rev is None: rev=steps-145
    qchange=0.0 if q0 is None or q1 is None else float(np.mean(np.abs(q1-q0)))
    return {"survival":t+1,"escape":immediate,"post_hazard_visits":post,"reversal_latency":rev,
            "recovery_auc":recovery,"q_change":qchange,"final_drive":drive(b)}

def summarize(kind,seeds,params=None):
    rows=[run_episode(kind,s,params) for s in seeds]
    return {k:float(np.mean([r[k] for r in rows])) for k in rows[0]},rows

def cohend(a,b):
    a=np.asarray(a); b=np.asarray(b); v=((len(a)-1)*a.var(ddof=1)+(len(b)-1)*b.var(ddof=1))/(len(a)+len(b)-2)
    return float((a.mean()-b.mean())/(math.sqrt(max(v,0))+1e-9))

def tune_gated_learning(dev,target,n=40,seed=321):
    rng=np.random.default_rng(seed)
    scales={"escape":2.5,"post_hazard_visits":2.0,"reversal_latency":20.0,"recovery_auc":8.0,"q_change":.01}
    best=None
    for _ in range(n):
        p={"decay":float(rng.uniform(.65,.94)),"input_gain":float(rng.uniform(.15,.75)),
           "policy_gain":float(rng.uniform(.03,.20)),"plasticity_gain":float(rng.uniform(.02,.22))}
        s,_=summarize("gated_learning_rival",dev,p)
        loss=sum(((s[k]-target[k])/scales[k])**2 for k in KEY_METRICS)
        if best is None or loss<best[0]: best=(loss,p,s)
    return best

def tune_generic_bidir(dev,target,n=40,seed=123):
    rng=np.random.default_rng(seed); scales={"escape":2.5,"post_hazard_visits":2.0,"reversal_latency":20.0,"recovery_auc":8.0,"q_change":.01}
    best=None
    for _ in range(n):
        p={"decay":float(rng.uniform(.65,.94)),"input_gain":float(rng.uniform(.15,.75)),
           "distractor_gain":float(rng.uniform(0,.30)),"feedback_gain":float(rng.uniform(.05,.35)),
           "policy_gain":float(rng.uniform(.03,.18)),"plasticity_gain":float(rng.uniform(.03,.20))}
        s,_=summarize("generic_bidir",dev,p)
        loss=sum(((s[k]-target[k])/scales[k])**2 for k in KEY_METRICS)
        if best is None or loss<best[0]: best=(loss,p,s)
    return best

def immediate_matched(ds,tol=.20):
    return abs(ds["escape"])<tol

def post_equivalent(ds,tol=.20):
    return all(abs(ds[k])<tol for k in ("post_hazard_visits","reversal_latency","recovery_auc","q_change"))

def classification(ds,tol=.20):
    if not immediate_matched(ds,tol):
        return "CONFOUNDED_IMMEDIATE_MISMATCH"
    if post_equivalent(ds,tol):
        return "EQUIVALENT_RIVAL_DEFEATS_BEHAVIORAL_UNIQUENESS"
    return "VALID_POST_EVENT_DISCRIMINATION"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--dev",type=int,default=40); ap.add_argument("--test",type=int,default=120); ap.add_argument("--tune",type=int,default=30); ap.add_argument("--test-start",type=int,default=50000)
    args=ap.parse_args()
    dev=list(range(args.dev)); test=list(range(args.test_start,args.test_start+args.test))
    crfi_dev,_=summarize("crfi",dev)
    best=tune_generic_bidir(dev,crfi_dev,args.tune)
    best_gl=tune_gated_learning(dev,crfi_dev,args.tune)
    kinds=["reactive","homeostatic","appraisal","recurrent_downstream","gated_downstream","gated_learning_rival","crfi_noC","crfi_noL","crfi"]
    out={"design":{"development_worlds":args.dev,"heldout_worlds":args.test,"heldout_seed_start":args.test_start,"tuning_candidates":args.tune,
                   "preregistered_equivalence":"A rival defeats CRFI behavioral uniqueness if immediate escape is matched (|d|<0.20) and all four post-event signature metrics are also equivalent (|d|<0.20). Immediate mismatch makes that rival comparison confounded, not a CRFI win.",
                   "interpretation_firewall":"The simulation tests functional/causal architecture only; it does not establish subjective feeling."},
         "tuned_generic_bidir":{"params":best[1],"development_loss":best[0],"development_summary":best[2]},
         "tuned_gated_learning":{"params":best_gl[1],"development_loss":best_gl[0],"development_summary":best_gl[2]},
         "heldout":{}}
    cs,cr=summarize("crfi",test)
    for k in kinds:
        s,r=summarize(k,test); item={"mean":s,"causal_signature":Agent(k,0).causal_signature()}
        if k!="crfi":
            item["d_vs_crfi"]={m:cohend([x[m] for x in r],[x[m] for x in cr]) for m in (*KEY_METRICS,"final_drive")}
            item["immediate_matched"]=immediate_matched(item["d_vs_crfi"])
            item["post_equivalent"]=post_equivalent(item["d_vs_crfi"])
            item["classification"]=classification(item["d_vs_crfi"])
        out["heldout"][k]=item
    gs,gr=summarize("generic_bidir",test,best[1])
    gd={m:cohend([x[m] for x in gr],[x[m] for x in cr]) for m in (*KEY_METRICS,"final_drive")}
    out["heldout"]["tuned_generic_bidir"]={"mean":gs,"d_vs_crfi":gd,
        "immediate_matched":immediate_matched(gd),"post_equivalent":post_equivalent(gd),
        "classification":classification(gd),"causal_signature":Agent("generic_bidir",0,best[1]).causal_signature()}
    ls,lr=summarize("gated_learning_rival",test,best_gl[1])
    ld={m:cohend([x[m] for x in lr],[x[m] for x in cr]) for m in (*KEY_METRICS,"final_drive")}
    out["heldout"]["tuned_gated_learning"]={"mean":ls,"d_vs_crfi":ld,
        "immediate_matched":immediate_matched(ld),"post_equivalent":post_equivalent(ld),
        "classification":classification(ld),"causal_signature":Agent("gated_learning_rival",0,best_gl[1]).causal_signature()}
    clean_rivals=["reactive","homeostatic","appraisal","recurrent_downstream","gated_downstream","gated_learning_rival","crfi_noC","crfi_noL","tuned_gated_learning"]
    eq_rivals=[k for k in clean_rivals if out["heldout"].get(k,{}).get("classification")=="EQUIVALENT_RIVAL_DEFEATS_BEHAVIORAL_UNIQUENESS"]
    valid_discriminated=[k for k in clean_rivals if out["heldout"].get(k,{}).get("classification")=="VALID_POST_EVENT_DISCRIMINATION"]
    confounded=[k for k in clean_rivals if out["heldout"].get(k,{}).get("classification")=="CONFOUNDED_IMMEDIATE_MISMATCH"]
    if eq_rivals:
        verdict="FAIL"
    elif valid_discriminated:
        verdict="SURVIVES_MATCHED_RIVALS_V014"
    else:
        verdict="INCONCLUSIVE_NO_MATCHED_RIVAL"
    out["behavioral_uniqueness_verdict"]=verdict
    out["equivalent_rivals"]=eq_rivals
    out["valid_discriminated_rivals"]=valid_discriminated
    out["confounded_rivals"]=confounded
    out["topology_note"]="A behaviorally equivalent rival that also has direct E<->S reciprocity is not a clean non-CRFI rival; it falls inside the physical core unless another CRFI requirement distinguishes it."
    print(json.dumps(out,indent=2))
if __name__=="__main__": main()
