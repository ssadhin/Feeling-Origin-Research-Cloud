from __future__ import annotations
import argparse, contextlib, importlib.util, io
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--trials", type=int, default=2500)
args = parser.parse_args()
trials = max(1, min(args.trials, 100000))

spec = importlib.util.spec_from_file_location("ablation", "simulations/crfi_ablation_v013.py")
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)
mod.NTRIALS = trials

out = Path("results")
out.mkdir(exist_ok=True)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    mod.main()
text = buf.getvalue()
print(text)
(out / "ablation.txt").write_text(text, encoding="utf-8")
