from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument("--dev",type=int,default=40)
p.add_argument("--test",type=int,default=120)
p.add_argument("--tune",type=int,default=30)
p.add_argument("--test-start",type=int,default=50000)
args=p.parse_args()

cmd=[
    sys.executable,"simulations/virtual_organism_v014.py",
    "--dev",str(args.dev),"--test",str(args.test),"--tune",str(args.tune),
    "--test-start",str(args.test_start)
]
r=subprocess.run(cmd,text=True,capture_output=True)
print(r.stdout)
if r.stderr:
    print(r.stderr,file=sys.stderr)
out=Path("results"); out.mkdir(exist_ok=True)
(out/"virtual-organism-v014.json").write_text(r.stdout,encoding="utf-8")
if r.returncode:
    raise SystemExit(r.returncode)
