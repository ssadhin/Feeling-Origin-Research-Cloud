from __future__ import annotations
import json, os, platform, time
from pathlib import Path
import numpy as np

out = Path("results")
out.mkdir(exist_ok=True)
t0 = time.perf_counter()
rng = np.random.default_rng(20261004)
a = rng.normal(size=(1400, 1400))
b = rng.normal(size=(1400, 1400))
c = a @ b
elapsed = time.perf_counter() - t0
payload = {
    "python": platform.python_version(),
    "platform": platform.platform(),
    "numpy": np.__version__,
    "matrix_shape": [1400, 1400],
    "checksum": float(c[0,0] + c[-1,-1]),
    "compute_seconds": elapsed,
    "github_run_id": os.getenv("GITHUB_RUN_ID"),
}
(out / "smoke.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
print(json.dumps(payload, indent=2))
