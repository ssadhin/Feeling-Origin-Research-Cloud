"""Source-derived cache-signature reproduction; public synthetic data only.
Pinned upstream EvoScientist/EvoScientist 3b382b92b8fdad6e1f13467c382dcdd91d9b19d2
store.py Git blob 9294ecf238875e71722819a74cb67f331bbefe58.
Cache implementation below preserves original upstream logic; parser is an adapter.
This is NOT a native application or 19C certification.
"""
from pathlib import Path
from collections import OrderedDict
from threading import Lock
import tempfile, os, json

_file_parse_cache = OrderedDict()
_cache_lock = Lock()

def _parse_observation_search_document(*, root, path):
    raw = path.read_text()
    return raw.split("summary: ",1)[1].split("\n",1)[0] if "summary: " in raw else None

def _parse_with_cache(root, path, touched):
    key = str(path)
    try:
        st = path.stat()
    except OSError:
        return None
    signature = (st.st_mtime_ns, st.st_size)
    with _cache_lock:
        cached = _file_parse_cache.get(key)
        if cached is not None and cached[0] == signature:
            _file_parse_cache.move_to_end(key)
            touched.add(key)
            return cached[1]
    parsed_document = _parse_observation_search_document(root=root, path=path)
    if parsed_document is None:
        return None
    with _cache_lock:
        _file_parse_cache[key] = (signature, parsed_document)
        _file_parse_cache.move_to_end(key)
        touched.add(key)
    return parsed_document

with tempfile.TemporaryDirectory() as d:
    p=Path(d)/"observation.md"
    a="---\nsummary: SAME_A\n---\n"
    b="---\nsummary: SAME_B\n---\n"
    assert len(a)==len(b)
    p.write_text(a)
    first=_parse_with_cache(Path(d),p,set())
    st=p.stat()
    p.write_text(b)
    os.utime(p,ns=(st.st_atime_ns,st.st_mtime_ns))
    stale=_parse_with_cache(Path(d),p,set())
    _file_parse_cache.clear()
    fresh=_parse_with_cache(Path(d),p,set())
    result={"initial":first,"same_signature_cached":stale,"after_clear":fresh,
            "pass":first=="SAME_A" and stale=="SAME_A" and fresh=="SAME_B"}
    print(json.dumps(result,sort_keys=True))
    assert result["pass"]
