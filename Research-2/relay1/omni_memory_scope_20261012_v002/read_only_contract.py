import ast,hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent
names={"verify_original.py":"d2f31134d3836e88989de479fadfcd3308e7fc26","acceptance_original.py":"09c0073f60e51ac31638f00a959fbb8d45b86bae"}
def gitsha(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+bytes([0])+b).hexdigest()
for n,expected in names.items():
    assert gitsha((p/n).read_bytes())==expected
v=(p/"verify_original.py").read_text()
a=(p/"acceptance_original.py").read_text()
assert "audit_memory_findings(store.db)" in v
assert "report.memory_unsupported" not in a
assert "report.grounding_rate < self.min_grounding" in a
print(json.dumps({"original_blobs":2,"memory_gate_in_acceptance":False,"aggregate_grounding_gate":True}))
