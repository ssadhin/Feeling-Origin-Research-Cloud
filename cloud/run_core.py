from __future__ import annotations
import subprocess, sys
from pathlib import Path

scripts = [
    "decisive_minimality_v007.py",
    "rival_constraints_v008.py",
    "empirical_equivalence_nogo_v009.py",
    "causal_quality_context_v011.py",
    "reentrant_feeling_v012.py",
]
out = Path("results")
out.mkdir(exist_ok=True)
log = []
for script in scripts:
    p = subprocess.run([sys.executable, f"simulations/{script}"], text=True, capture_output=True)
    block = f"===== {script} =====\nSTDOUT\n{p.stdout}\nSTDERR\n{p.stderr}\nEXIT={p.returncode}\n"
    print(block)
    log.append(block)
    if p.returncode != 0:
        (out / "core-suite.txt").write_text("\n".join(log), encoding="utf-8")
        raise SystemExit(p.returncode)
(out / "core-suite.txt").write_text("\n".join(log), encoding="utf-8")
