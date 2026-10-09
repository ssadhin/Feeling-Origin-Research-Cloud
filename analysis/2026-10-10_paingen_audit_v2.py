import csv,sys,math,statistics as st
from collections import defaultdict
# Reproduce Paingen family-weighted primary test, input CSV blob 539a7bdeb9a324afc20d064a458979b43594c456
def rng(seed):
 s=seed&0xffffffff
 while True:
  s^=(s<<13)&0xffffffff;s^=s>>17;s^=(s<<5)&0xffffffff;s&=0xffffffff
  yield s/4294967296
with open(sys.argv[1],encoding="utf-8-sig") as f: rows=list(csv.DictReader(f))
pairs=defaultdict(dict)
for x in rows:
 k=(x["participant_ID"],x["heat"],x["stimLvl"])
 if x["prodicaine"] in pairs[k]:raise ValueError("duplicate")
 pairs[k][x["prodicaine"]]=x
fam=defaultdict(list);missing=unpaired=0
for p in pairs.values():
 if "0" not in p or "1" not in p:unpaired+=1;continue
 a,b=p["0"],p["1"]
 try:
  i,u,j,v=map(float,(a["Yint"],a["Yunp"],b["Yint"],b["Yunp"]))
  if not all(map(math.isfinite,(i,u,j,v))):raise ValueError()
 except ValueError:missing+=1;continue
 fam[a["family_ID"]].append((u-v)-(i-j))
vals=[st.mean(x) for x in fam.values()];n=len(vals);obs=st.mean(vals)
g=rng(20261010);boot=sorted(sum(vals[int(next(g)*n)] for _ in range(n))/n for _ in range(10000))
g=rng(20261011)
ext=sum(abs(sum(x*(1 if next(g)>=.5 else -1) for x in vals)/n)>=abs(obs)-1e-15 for _ in range(10000))
print(dict(rows=len(rows),valid_cells=sum(map(len,fam.values())),families=n,unpaired=unpaired,missing=missing,D=obs,CI95=(boot[249],boot[9749]),p=(ext+1)/10001))
