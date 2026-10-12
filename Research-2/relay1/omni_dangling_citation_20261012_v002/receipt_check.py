from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
raw=(p/'raw_v002_run1.json').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='90d11ba8200a31610eb850e6118a072df870d2cbf63792c1ec8f3cac7547ca59'
r=json.loads(raw)
assert r['passed']==14 and all(r['checks'].values())
print('Verified 14/14 offline source-fidelity controls')
