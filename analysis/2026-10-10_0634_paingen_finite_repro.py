#!/usr/bin/env python3
"""Pinned Paingen finite-QC reproducibility audit; no phenomenal inference.
Usage: python analysis/2026-10-10_0634_paingen_finite_repro.py SOURCE.csv
Source blob 539a7bdeb9a324afc20d064a458979b43594c456
Frozen protocol: protocols/2026-10-10_0537_paingen_independent_qc_prefreeze.md
Python >=3.9, standard library only. RNG xorshift32, not Python random.Random.
"""
import csv, hashlib, io, json, math, sys
from collections import defaultdict
from statistics import mean

PIN="539a7bdeb9a324afc20d064a458979b43594c456"
N=10000

def sha_blob(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

class RNG:
    def __init__(self,seed): self.s=seed & 0xffffffff
    def rand(self):
        x=self.s
        x^=(x<<13)&0xffffffff
        x^=x>>17
        x^=(x<<5)&0xffffffff
        self.s=x&0xffffffff
        return self.s/4294967296.0

def test(vals):
    n=len(vals)
    if n<2: raise ValueError("insufficient families")
    obs=mean(vals); rng=RNG(20261010); boots=[]
    for _ in range(N):
        boots.append(sum(vals[int(rng.rand()*n)] for _ in range(n))/n)
    boots.sort(); rng=RNG(20261011); extreme=0
    for _ in range(N):
        z=sum(x*(-1 if rng.rand()<.5 else 1) for x in vals)/n
        extreme+=(abs(z)>=abs(obs))
    return dict(n_families=n,mean_D=obs,CI95=[boots[249],boots[9749]],
                p_two_sided=(extreme+1)/(N+1),extreme=extreme)

def summarize(pairs):
    fam=defaultdict(list)
    for p in pairs: fam[p["family"]].append(p["D"])
    return dict(n_pairs=len(pairs),**test([mean(fam[k]) for k in sorted(fam)]))

def audit(raw):
    sha=sha_blob(raw)
    if sha!=PIN: raise ValueError("pinned source blob mismatch "+sha)
    rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    required={"participant_ID","family_ID","heat","stimLvl","prodicaine","Yint","Yunp"}
    if not rows or not required.issubset(rows[0]): raise ValueError("missing columns")
    groups=defaultdict(dict); people=set(); allfam=set()
    for r in rows:
        people.add(r["participant_ID"]);allfam.add(r["family_ID"])
        key=(r["participant_ID"],r["heat"],r["stimLvl"]); arm=r["prodicaine"]
        if arm not in ("0","1") or arm in groups[key]:
            raise ValueError("duplicate or unknown condition "+str((key,arm)))
        groups[key][arm]=r
    pairs=[]; exc=dict(unmatched=0,nonfinite=0,family_mismatch=0)
    for g in groups.values():
        if "0" not in g or "1" not in g:
            exc["unmatched"]+=1;continue
        a,b=g["0"],g["1"]
        if a["family_ID"]!=b["family_ID"]:
            exc["family_mismatch"]+=1;continue
        try: i0,u0,i1,u1=[float(x) for x in
            (a["Yint"],a["Yunp"],b["Yint"],b["Yunp"])]
        except (ValueError,TypeError):
            exc["nonfinite"]+=1;continue
        if not all(map(math.isfinite,(i0,u0,i1,u1))):
            exc["nonfinite"]+=1;continue
        pairs.append(dict(family=a["family_ID"],heat=a["heat"],level=a["stimLvl"],
            D=(u0-u1)-(i0-i1),dU=u0-u1,dI=i0-i1,I0=i0,I1=i1,U0=u0,U1=u1))
    fam=defaultdict(list)
    for p in pairs: fam[p["family"]].append(p)
    keys=sorted(fam)
    fmeans=[mean([p["D"] for p in fam[k]]) for k in keys]
    out=dict(source_git_blob_sha=sha,rows=len(rows),participants=len(people),
        source_families=len(allfam),groups=len(groups),exclusions=exc,
        valid_pairs=len(pairs),valid_families=len(fam),overall=summarize(pairs))
    out["overall"]["mean_dU"]=mean([mean([p["dU"] for p in fam[k]]) for k in keys])
    out["overall"]["mean_dI"]=mean([mean([p["dI"] for p in fam[k]]) for k in keys])
    out["by_heat"]={h:summarize([p for p in pairs if p["heat"]==h]) for h in ("0","1")}
    out["by_level"]={h:summarize([p for p in pairs if p["level"]==h]) for h in ("3","4","5")}
    out["cyclic_family_folds_NOT_OOS"]=[
        dict(fold=j,n=len(fmeans[j::5]),D=mean(fmeans[j::5])) for j in range(5)]
    out["zero_counts"]={k:sum(p[k]==0 for p in pairs) for k in ("I0","I1","U0","U1")}
    out["status"]="negative affect-minus-intensity contrast; not causal M or phenomenal proof"
    return out

if __name__=="__main__":
    if len(sys.argv)!=2: raise SystemExit("usage: python script.py SOURCE.csv")
    with open(sys.argv[1],"rb") as f: result=audit(f.read())
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
