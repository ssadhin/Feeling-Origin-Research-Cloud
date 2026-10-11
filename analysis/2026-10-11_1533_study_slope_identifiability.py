import numpy as np
from scipy.stats import t
rng=np.random.default_rng(20261011)
j=np.repeat(np.arange(16),25); g=(j>=8).astype(float)
x=rng.normal(size=400); e=rng.normal(scale=.4,size=400)
ya=.2+.5*x+.3*g*x+e
u=.3*(np.arange(16)>=8); yb=.2+.5*x+u[j]*x+e
assert np.array_equal(ya,yb)
D=np.column_stack([(j==k).astype(float) for k in range(1,16)])
X=np.column_stack([np.ones(400),D,g,x,g*x])
Z=np.column_stack([X]+[(j==k).astype(float)*x for k in range(16)])
b=np.linalg.lstsq(X,ya,rcond=None)[0]
rank=np.linalg.matrix_rank(X); rankZ=np.linalg.matrix_rank(Z)
se=np.sqrt(np.sum((ya-X@b)**2)/(400-rank)*np.linalg.pinv(X.T@X)[-1,-1])
print(dict(n=400,rank=rank,rank_full=rankZ,beta=b[-1],t=b[-1]/se,p=2*t.sf(abs(b[-1]/se),400-rank),maxdiff=np.max(np.abs(ya-yb))))
