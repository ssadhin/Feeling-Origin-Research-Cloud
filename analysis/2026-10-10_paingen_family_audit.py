import csv,sys,random,statistics as st
from collections import defaultdict
# Paingen audit; source blob 539a7bdeb9a324afc20d064a458979b43594c456
# Frozen protocol: protocols/2026-10-10_0433_paingen_preoutcome.md
with open(sys.argv[1],encoding="utf-8-sig") as f: rows=list(csv.DictReader(f))
p=defaultdict(dict)
for r in rows: p[r["participant_ID"],r["heat"],r["stimLvl"]][r["prodicaine"]]=r
f=defaultdict(list); excluded=defaultdict(int)
for v in p.values():
    if "0" not in v or "1" not in v: excluded["unpaired"]+=1;continue
    a,b=v["0"],v["1"]
    try: I0,U0,I1,U1=[float(x) for x in (a["Yint"],a["Yunp"],b["Yint"],b["Yunp"])]
    except ValueError: excluded["missing"]+=1;continue
    f[a["family_ID"]].append((U0-U1)-(I0-I1))
a=[st.mean(v) for v in f.values()]; n=len(a); obs=st.mean(a)
g=random.Random(20261010)
boot=sorted(st.mean(g.choices(a,k=n)) for _ in range(10000))
g=random.Random(20261011)
extreme=sum(abs(st.mean([x*g.choice((-1,1)) for x in a]))>=abs(obs) for _ in range(10000))
print(dict(rows=len(rows),families=n,paired=sum(map(len,f.values())),excluded=dict(excluded),meanD=obs,CI95=(boot[249],boot[9749]),signflip_p=(extreme+1)/10001))
# Python RNG differs from xorshift32; CI/p are independently seeded sensitivity, not exact frozen resampling.
