from __future__ import annotations
import itertools, time
import numpy as np

# A finite physical system with 6 internal states and 3 interventions.
# T1 and T2 have exactly the same physics. They differ only by a stipulated
# qualia labeling that has no causal effect on transitions or observations.

rng=np.random.default_rng(20261004)
S=6
A=3

# Physical transition kernels P(s'|s,a)
P=rng.random((A,S,S))
P=P/P.sum(axis=2,keepdims=True)

# Physical observation kernel P(o|s), e.g. report/action/body output
O=rng.random((S,4))
O=O/O.sum(axis=1,keepdims=True)

# Two phenomenal interpretations, causally inert by construction
q1=np.array(["red","green","pain","neutral","warm","cold"],dtype=object)
q2=np.array(["green","red","neutral","pain","cold","warm"],dtype=object)

def physical_distribution(initial, actions):
    dist=np.zeros(S); dist[initial]=1.0
    obs=[]
    for a in actions:
        dist=dist@P[a]
        obs.append(dist@O)
    return np.asarray(obs)

def tv(p,q):
    return 0.5*np.abs(p-q).sum()

def main():
    t=time.perf_counter()
    max_tv=0.0
    checked=0
    # Exhaust all initial states and every intervention sequence up to length 5.
    for initial in range(S):
        for L in range(1,6):
            for actions in itertools.product(range(A),repeat=L):
                # T1 and T2 share identical P and O, hence identical observables.
                d1=physical_distribution(initial,actions)
                d2=physical_distribution(initial,actions)
                max_tv=max(max_tv,tv(d1,d2))
                checked+=1

    print("=== V009 EMPIRICAL-EQUIVALENCE / ZOMBIE NO-GO TEST ===")
    print("physical states:",S," interventions:",A)
    print("phenomenal labeling T1:",list(q1))
    print("phenomenal labeling T2:",list(q2))
    print("experiment sequences checked:",checked)
    print("maximum total-variation distance between ALL physical predictions:",max_tv)
    print()
    print("Result:")
    print("If the phenomenal permutation is stipulated to have no causal effect,")
    print("no physical intervention/observation can discriminate T1 from T2.")
    print("Therefore simulation cannot prove or disprove a causally inert qualia permutation.")
    print()
    print("To make consciousness scientifically identifiable, at least one of these must hold:")
    print("A) phenomenal differences are themselves physical/causal differences; or")
    print("B) phenomenal differences have causal effects that enter measurable dynamics.")
    print("Under physical causal closure, A is the parsimonious bridge premise.")
    print(f"runtime_seconds={time.perf_counter()-t:.6f}")

if __name__=="__main__":
    main()
