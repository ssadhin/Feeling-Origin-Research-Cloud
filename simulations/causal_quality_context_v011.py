from __future__ import annotations
import math, time
import numpy as np

N=8
H=2
TARGET=3
ANCHORS=(1,5,7)

def jsd(p,q):
    p=np.asarray(p,float); q=np.asarray(q,float)
    p=p/(p.sum()+1e-15); q=q/(q.sum()+1e-15)
    m=.5*(p+q)
    def kl(a,b):
        mask=a>0
        return float(np.sum(a[mask]*np.log2(a[mask]/(b[mask]+1e-15))))
    return .5*kl(p,m)+.5*kl(q,m)

def metric(p,q):
    return math.sqrt(max(jsd(p,q),0.0))

def base_kernel():
    P=np.zeros((N,N))
    for i in range(N):
        P[i,i]=.34
        P[i,(i+1)%N]=.34
        P[i,(i-1)%N]=.20
        P[i,(i+2)%N]=.12
    return P/P.sum(axis=1,keepdims=True)

def deform_context(P):
    Q=P.copy()
    # Keep the instantaneous content-state identity TARGET exactly the same,
    # but change what entering that state causally leads to in this context.
    Q[TARGET]=0
    Q[TARGET,TARGET]=.15
    Q[TARGET,4]=.05
    Q[TARGET,6]=.45
    Q[TARGET,7]=.35
    Q[TARGET]/=Q[TARGET].sum()
    return Q

def traj(P,start):
    v=np.zeros(N); v[start]=1
    out=[]
    for _ in range(H):
        v=v@P
        out.append(v.copy())
    z=np.concatenate(out)
    return z/z.sum()

def dmat(P):
    K=[traj(P,i) for i in range(N)]
    return np.array([[metric(K[i],K[j]) for j in range(N)] for i in range(N)])

def unique_rows(X,tol=1e-10):
    rows=[]
    for x in X:
        if not any(np.max(np.abs(x-r))<tol for r in rows):
            rows.append(x)
    return len(rows)

def main():
    t0=time.perf_counter()
    P=base_kernel()
    Q=deform_context(P)
    D1=dmat(P); D2=dmat(Q)
    X1=D1[:,ANCHORS]; X2=D2[:,ANCHORS]
    shifts=np.linalg.norm(X2-X1,axis=1)

    print("=== V011 CLEAN CONTEXT-DEFORMATION TEST ===")
    print("anchors=",ANCHORS)
    print("states resolved before deformation:",unique_rows(X1),"/",N)
    print("local content identity held fixed: state",TARGET)
    print("target coordinate before:",np.round(X1[TARGET],6).tolist())
    print("target coordinate after :",np.round(X2[TARGET],6).tolist())
    print(f"target causal-coordinate shift={shifts[TARGET]:.6f}")
    controls=np.delete(shifts,TARGET)
    print(f"mean non-target shift={controls.mean():.6f}")
    print(f"target/mean-control shift ratio={shifts[TARGET]/(controls.mean()+1e-12):.3f}")
    print()
    print("Local-pattern-only prediction: NO qualitative change, because local identity is fixed.")
    print("Causal-context prediction: qualitative change, because the intervention trajectory changed.")
    print("This gives a clean discriminating experimental design.")
    print("It does not by itself prove that causal coordinates are subjective experience.")
    print(f"runtime_seconds={time.perf_counter()-t0:.6f}")

if __name__=="__main__":
    main()
