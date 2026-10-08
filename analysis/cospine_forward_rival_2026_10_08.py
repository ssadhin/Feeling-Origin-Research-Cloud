#!/usr/bin/env python3
"""Exploratory forward-trial rival audit; no phenomenal inference."""
import json, math
from cospine_ds005883_loocv_measurement_rival_v001 import read_pairs

def predict(rows, cols, z):
    p=len(cols)+1
    X=[[1.0]+[r[j] for j in cols] for r in rows]
    a=[[sum(v[i]*v[j] for v in X) if j<p else sum(v[i]*r[1] for v,r in zip(X,rows)) for j in range(p+1)] for i in range(p)]
    for j in range(p):
        k=max(range(j,p),key=lambda k:abs(a[k][j]))
        if abs(a[k][j])<1e-9: return None
        a[j],a[k]=a[k],a[j]
        v=a[j][j];a[j]=[u/v for u in a[j]]
        for i in range(p):
            if i==j: continue
            v=a[i][j];a[i]=[u-v*w for u,w in zip(a[i],a[j])]
    b=[r[-1] for r in a]
    return b[0]+sum(b[i+1]*z[c] for i,c in enumerate(cols))

def subject(i):
    sid,pairs=read_pairs(i)
    rows=[[x,y,j+1,pairs[j-1][1] if j else float('nan')] for j,(x,y) in enumerate(pairs)]
    train,test=rows[:10],rows[10:]
    mean=sum(r[1] for r in train)/10
    ss={k:0.0 for k in 'ABCD'}
    fb={k:0 for k in 'BCD'}
    for z in test:
        b=predict(train,[0],z)
        if b is None: b=mean;fb['B']+=1
        c=predict(train,[0,2],z)
        if c is None: c=b;fb['C']+=1
        d=predict(train[1:],[0,3],z)
        if d is None: d=b;fb['D']+=1
        for k,yhat in zip('ABCD',[mean,b,c,d]): ss[k]+=(z[1]-yhat)**2
    return {'subject':sid,'SSE':ss,'fallback':fb}

if __name__=='__main__':
    out=[subject(i) for i in range(1,40)]
    s={k:sum(r['SSE'][k] for r in out) for k in 'ABCD'}
    wins={k:sum(r['SSE'][k]<r['SSE']['B']-1e-9 for r in out) for k in 'CD'}
    print(json.dumps({'source':'037ed267e7f7f2024a5fe3d0e8fb4759f7f67bdd',
      'n_test':195,'SSE':s,'RMSE':{k:math.sqrt(v/195) for k,v in s.items()},
      'D_vs_B_improvement':1-s['D']/s['B'],'C_D_subject_wins':wins,
      'threshold_D_pass':(1-s['D']/s['B']>=.05 and wins['D']>20),
      'subjects':out},indent=2))
