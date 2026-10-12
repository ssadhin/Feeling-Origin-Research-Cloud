import json
from pathlib import Path
x=json.loads((Path(__file__).parent/'OBSERVED_COMPACT.json').read_text())
assert len(x['runs'])==2
assert all(r['passed']==r['total']==16 for r in x['runs'])
assert x['independent_verification']['passed']==18
assert x['mutations']['detected']==4
print('Compact receipt consistent; not a native rerun')
