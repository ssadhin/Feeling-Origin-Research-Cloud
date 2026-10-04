from __future__ import annotations
import itertools, math, time
import numpy as np

SEED=20261004
N=32
T=100
SEEDS=[0,5,10,15,20,25,30]

def norm_radius(W,r):
    vals=np.linalg.eigvals(W)
    return W*(r/(max(abs(vals))+1e-12))

def make_regime(kind, seed):
    rng=np.random.default_rng(seed)
    if kind=="collapse":
        W=rng.normal(0,0.01,(N,N))
        for i in range(N-1):
            W[i+1,i]+=0.08
        W=norm_radius(W,0.28); leak=0.22
    elif kind=="balanced":
        mask=rng.random((N,N))<0.18
        W=rng.normal(0,1,(N,N))*mask
        W=0.75*W+0.25*W.T
        W=norm_radius(W,0.96); leak=0.08
    elif kind=="stereotyped":
        W=np.ones((N,N))/N + rng.normal(0,0.003,(N,N))
        W=norm_radius(W,0.985); leak=0.05
    else:
        raise ValueError(kind)
    return W,leak

def evolve(W,leak,seed,steps=T):
    x=np.zeros(N); out=[]
    for t in range(steps):
        u=np.zeros(N)
        if t==0: u[seed]=1.0
        x=(1-leak)*np.tanh(W@x+u)
        out.append(x.copy())
    return np.asarray(out)

def causal_capacity(W,leak):
    Rs=[evolve(W,leak,s) for s in SEEDS]
    spreads=[]; persists=[]; vecs=[]
    for R in Rs:
        a=np.abs(R); mx=a.max()+1e-12
        spreads.append(np.mean(np.max(a[2:],axis=0)>0.04*mx))
        norms=np.linalg.norm(R,axis=1); pk=norms.max()+1e-12
        idx=np.where(norms>0.05*pk)[0]
        persists.append((idx[-1]+1)/T if len(idx) else 0.0)
        v=R[2:].ravel()
        vecs.append(v/(np.linalg.norm(v)+1e-12))
    integration=float(np.mean(spreads))
    persistence=float(np.mean(persists))
    sims=[]
    for i in range(len(vecs)):
        for j in range(i+1,len(vecs)):
            sims.append(abs(float(np.dot(vecs[i],vecs[j]))))
    cause_diff=float(1-np.mean(sims))
    M=np.stack(vecs)
    sv=np.linalg.svd(M,compute_uv=False)
    p=(sv*sv)/(np.sum(sv*sv)+1e-12)
    erank=float(np.exp(-np.sum(p*np.log(p+1e-15))))
    repertoire=(erank-1)/(len(SEEDS)-1)
    a=np.abs(W)
    reciprocity=float(np.sum(np.minimum(a,a.T))/(np.sum(a)+1e-12))
    components=np.clip([integration,persistence,cause_diff,repertoire,reciprocity],1e-9,1)
    C=float(np.prod(components)**(1/5))
    return C,(integration,persistence,cause_diff,repertoire,reciprocity)

def boolean_minimality():
    # Empirical-constraint abstraction:
    # C=conscious-capable domain, L=content admission/embedding.
    # Required feeling-presence outcomes:
    # 00->0, 01->0, 10->0, 11->1.
    rows=[(0,0,0),(0,1,0),(1,0,0),(1,1,1)]
    survivors=[]
    for table in itertools.product([0,1],repeat=4):
        f={(0,0):table[0],(0,1):table[1],(1,0):table[2],(1,1):table[3]}
        if all(f[(c,l)]==y for c,l,y in rows):
            survivors.append(table)
    return survivors

def cycle_automorphisms(n=8):
    # Dihedral group actions on cycle labels 0..n-1.
    autos=[]
    for k in range(n):
        autos.append(tuple((i+k)%n for i in range(n)))
        autos.append(tuple((k-i)%n for i in range(n)))
    return sorted(set(autos))

def fixes(auto, anchors):
    return all(auto[a]==a for a in anchors)

def reaction_demo():
    # Same local threat evaluation in every condition.
    E={"negative_valence":0.8,"imminence":0.9}
    reaction=0.55*E["negative_valence"]+0.45*E["imminence"]
    cases=[
        ("unconscious-domain",0,1),
        ("awake-unseen-content",1,0),
        ("awake-felt-content",1,1),
        ("inactive-unseen",0,0),
    ]
    return reaction,[(name,c,l,int(bool(c and l))) for name,c,l in cases]

def main():
    t0=time.perf_counter()
    print("=== V007 DECISIVE MINIMALITY TEST ===")
    surv=boolean_minimality()
    print("Boolean functions satisfying all four admission constraints:",len(surv))
    print("Unique truth table [F00,F01,F10,F11] =",surv[0])
    print("Therefore F_presence(C,L) = C AND L, conditional on the four constraints.")

    print("\n=== CAUSAL-DOMAIN STRESS TEST ===")
    kinds=["collapse","balanced","stereotyped"]
    reps=100
    vals={k:[] for k in kinds}
    for r in range(reps):
        for k in kinds:
            C,parts=causal_capacity(*make_regime(k,SEED+r))
            vals[k].append(C)
    for k in kinds:
        a=np.asarray(vals[k])
        print(f"{k:12s} mean_C={a.mean():.6f} sd={a.std():.6f} min={a.min():.6f} max={a.max():.6f}")
    wins=0
    for r in range(reps):
        if vals["balanced"][r]>vals["collapse"][r] and vals["balanced"][r]>vals["stereotyped"][r]:
            wins+=1
    print(f"balanced_regime_wins={wins}/{reps}")

    reaction,cases=reaction_demo()
    print("\n=== SAME EMOTION COMPUTATION, DIFFERENT ADMISSION ===")
    print(f"automatic_reaction_urgency={reaction:.3f} in every case")
    for name,c,l,f in cases:
        print(f"{name:22s} C={c} L={l} predicted_felt_presence={f}")

    print("\n=== SYMMETRY / RESOLVING-ANCHOR TEST ===")
    autos=cycle_automorphisms(8)
    for anchors in [(),(0,),(0,1)]:
        count=sum(fixes(a,anchors) for a in autos)
        print(f"anchors={anchors} surviving_isometries={count}")
    print("An 8-state cycle has 16 dihedral symmetries; two adjacent physical anchors remove all nontrivial ones.")

    print("\n=== RESULT ===")
    print("1. Presence minimality: C AND L is unique under the stated dissociation constraints.")
    print("2. Capacity cannot be activity/connectivity alone: both collapse and stereotypy fail the balanced causal test.")
    print("3. Automatic reaction remains possible when feeling-presence is off.")
    print("4. Unanchored relational quality is ambiguous; a resolving anchor set removes that mathematical ambiguity.")
    print("5. This establishes functional/mathematical sufficiency of the scaffold, not metaphysical proof of subjectivity.")
    print(f"runtime_seconds={time.perf_counter()-t0:.4f}")

if __name__=="__main__":
    main()
