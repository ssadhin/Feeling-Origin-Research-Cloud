#!/usr/bin/env python3
"""Independent Python replay of Parrotta post-primary trial-adjusted sensitivity.
Source Git blob 447fff57c91fb5ff761449d98d93737e26b1236c.
Run: python analysis/2026-10-11_0237_parrotta_trial_adjusted.py "Data_v3 - 2504.xlsx"
Dependencies: numpy, openpyxl. This is NONBLIND, exploratory, not proof of phenomenal P.
"""
import sys, hashlib, json
from collections import defaultdict
from pathlib import Path
import numpy as np
from openpyxl import load_workbook

EXPECTED = "447fff57c91fb5ff761449d98d93737e26b1236c"
def replay(path):
    data=Path(path).read_bytes()
    sha=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
    if sha!=EXPECTED: raise ValueError("Source Git blob mismatch: "+sha)
    wb=load_workbook(path,read_only=True,data_only=True)
    it=iter(wb.worksheets[0].values)
    header=next(it)
    by=defaultdict(list)
    nrows=0
    for values in it:
        row=dict(zip(header,values))
        by[(row["Exp"],row["SSID"])].append(row)
        nrows+=1
    wb.close()
    groups={"Intero":[],"Extero":[]}
    deficient=0
    for (exp,ssid),rows in by.items():
        rr=[r for r in rows if r["Session"]==2 and r["StimInt"] in (2,3,4) and r["Feedback"] in ("Faster","Slower")]
        X=np.array([[1.0,float(r["StimInt"]==3),float(r["StimInt"]==4),float(r["Feedback"]=="Faster"),float(r["Trial"])] for r in rr])
        if len(rr)!=12 or np.linalg.matrix_rank(X)<5:
            deficient+=1
            continue
        y1=np.array([float(r["LIK"])/4 for r in rr])
        y2=np.array([float(r["VAS"])/100 for r in rr])
        u=float(np.linalg.lstsq(X,y1,rcond=None)[0][3])
        i=float(np.linalg.lstsq(X,y2,rcond=None)[0][3])
        groups[exp].append((u-i,u,i))
    means={exp:np.mean(np.array(a),axis=0).tolist() for exp,a in groups.items()}
    state=20261012
    def rand():
        nonlocal state
        state=(1664525*state+1013904223)&0xffffffff
        return state/4294967296.0
    boots={"Intero":[],"Extero":[],"difference":[]}
    for _ in range(10000):
        vals={}
        for exp in ("Intero","Extero"):
            arr=groups[exp]
            vals[exp]=sum(arr[int(rand()*len(arr))][0] for _ in range(len(arr)))/len(arr)
            boots[exp].append(vals[exp])
        boots["difference"].append(vals["Intero"]-vals["Extero"])
    cis={k:np.quantile(v,[.025,.975]).tolist() for k,v in boots.items()}
    return {"git_blob":sha,"n_rows":nrows,"n_subjects":len(by),"rank_deficient":deficient,
            "means_D_LIK_VAS":means,"ci95":cis,"n_by_exp":{k:len(v) for k,v in groups.items()},
            "status":"post-primary nonblind sensitivity, not proof"}
if __name__=="__main__":
    if len(sys.argv)!=2: raise SystemExit("Pass source workbook path")
    print(json.dumps(replay(sys.argv[1]),indent=2))
