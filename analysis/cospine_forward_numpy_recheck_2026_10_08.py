import numpy as np
from cospine_ds005883_loocv_measurement_rival_v001 import read_pairs
def fit(a,cols,z):
 x=np.column_stack([np.ones(len(a))]+[a[:,c] for c in cols])
 if np.linalg.matrix_rank(x)<x.shape[1]:return None
 return float(np.r_[1,[z[c] for c in cols]]@np.linalg.lstsq(x,a[:,1],rcond=None)[0])
for i in range(1,40):
 sid,pairs=read_pairs(i);p=np.array(pairs,float)
 a=np.column_stack((p,np.arange(1,16),np.r_[np.nan,p[:-1,0]],np.r_[np.nan,p[:-1,1]]))
 tr,te=a[:10],a[10:];s={k:0. for k in 'ABCDEF'}
 for z in te:
  b=fit(tr,[0],z);b=tr[:,1].mean() if b is None else b
  pred=[tr[:,1].mean(),b]
  for t,c in [(tr,[0,2]),(tr[1:],[0,4]),(tr[1:],[0,3]),(tr[1:],[0,3,4])]:
   q=fit(t,c,z);pred.append(b if q is None else q)
  for k,v in zip('ABCDEF',pred):s[k]+=(z[1]-v)**2
 print(sid,s)
