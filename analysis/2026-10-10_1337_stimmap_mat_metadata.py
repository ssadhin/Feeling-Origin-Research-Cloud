#!/usr/bin/env python3
"""Pinned stimMAP MATLAB metadata-only schema audit; never load pain outcomes."""
import base64, hashlib, io, json, urllib.request
from scipy.io import whosmat, loadmat

REPO = "canlab/stimMAP_2025"
REF = "6c419ffc8a5d242b00ff95106aacb250365d3715"
FIELDS = ("Experiment_type", "Electrode_location", "sub_current", "session", "protocol_selction")
paths = [
    "Session 0/Calibration/Results/sub-01/sub-01_Calibration.mat",
    "Session 1/Pain before tDCS/Results/sub-01/sub-01_ses-01/sub-01_ses-01_run-01.mat",
    "Session 1/Pain after tDCS/Results/sub-01/sub-01_ses-01/sub-01_ses-01_run-01.mat",
]
for subject in (1, 2):
    for session in (1, 2, 3):
        stem = f"sub-{subject:02d}_ses-{session:02d}"
        label = "tDCS induced sensation" + ("" if session == 3 else "s")
        paths.append(f"Session {session}/{label}/Results/sub-{subject:02d}/{stem}/{stem}-total.mat")

def fetch(path):
    from urllib.parse import quote
    url = f"https://api.github.com/repos/{REPO}/contents/" + quote(path, safe="/") + f"?ref={REF}"
    req = urllib.request.Request(url, headers={"User-Agent": "feeling-origin-mat-audit"})
    with urllib.request.urlopen(req, timeout=30) as response:
        record = json.load(response)
    data = base64.b64decode(record["content"])
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert blob == record["sha"], path
    return data, blob

def normalize(x):
    if hasattr(x, "tolist"):
        x = x.tolist()
    if isinstance(x, list):
        return [normalize(y) for y in x]
    if isinstance(x, bytes):
        return x.decode("utf-8", "replace")
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    return str(x)

results = []
for path in paths:
    data, sha = fetch(path)
    names = [name for name, shape, dtype in whosmat(io.BytesIO(data))]
    values = loadmat(io.BytesIO(data), variable_names=FIELDS, simplify_cells=True)
    selected = {k: normalize(values[k]) for k in FIELDS if k in values}
    results.append({"path": path, "blob_sha": sha, "variables": len(names),
                    "selected_metadata": selected,
                    "assignment_names": [n for n in names if any(
                        term in n.lower() for term in ("anodal", "cathodal", "sham", "polarity", "allocation", "treatment"))]})
print(json.dumps({"source_commit": REF, "scope": "schema and selected metadata ONLY",
                  "files": results, "causal_status": "No polarity contrast without verified assignment"}, indent=2))
