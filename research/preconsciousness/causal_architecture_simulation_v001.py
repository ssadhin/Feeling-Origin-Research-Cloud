import numpy as np
from scipy.stats import pearsonr

MODELS = ("strict","homeostatic_bypass","parallel","recurrent_proxy")
TESTS = (("M","E",("I",)), ("M","F",("E",)), ("I","F",("E",)))

def residualize(y, X):
    X=np.asarray(X); y=np.asarray(y)
    Xd=np.column_stack([np.ones(len(y)),X])
    beta=np.linalg.lstsq(Xd,y,rcond=None)[0]
    return y-Xd@beta

def partial_r(d,a,b,cond):
    if not cond:
        return pearsonr(d[a],d[b])[0]
    ra=residualize(d[a],np.column_stack([d[x] for x in cond]))
    rb=residualize(d[b],np.column_stack([d[x] for x in cond]))
    return pearsonr(ra,rb)[0]

def simulate(model,n,seed):
    rng=np.random.default_rng(seed)
    M=rng.normal(size=n)
    ei=rng.normal(size=n); ee=rng.normal(size=n); ef=rng.normal(size=n)
    I=.8*M+ei
    if model=="strict":
        E=.8*I+ee
        F=.8*E+ef
    elif model=="homeostatic_bypass":
        E=.8*I+ee
        F=.8*E+.55*M+ef
    elif model=="parallel":
        E=.55*M+.55*I+ee
        F=.8*E+ef
    elif model=="recurrent_proxy":
        # Acyclic reduced-form proxy for a recurrent mature system.
        E=.45*M+.55*I+ee
        F=.45*I+.55*E+ef
    return {"M":M,"I":I,"E":E,"F":F}

def main():
    n=2000
    reps=500
    for model in MODELS:
        vals=[[] for _ in TESTS]
        for j in range(reps):
            d=simulate(model,n,100000+j)
            for k,(a,b,c) in enumerate(TESTS):
                vals[k].append(partial_r(d,a,b,c))
        for (a,b,c),v in zip(TESTS,vals):
            x=np.asarray(v)
            print(model, f"{a}-{b}|{','.join(c)}",
                  f"mean={x.mean():.6f}",
                  f"sd={x.std(ddof=1):.6f}",
                  f"p05={np.quantile(x,.05):.6f}",
                  f"p95={np.quantile(x,.95):.6f}",
                  f"Pr(|r|>.1)={np.mean(np.abs(x)>.1):.3f}")
if __name__=="__main__":
    main()
