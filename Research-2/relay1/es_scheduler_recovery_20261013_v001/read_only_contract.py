#!/usr/bin/env python3
"""Read-only original-source contract check for Relay1 scheduler audit."""
import ast, hashlib, pathlib, sys
p = pathlib.Path(sys.argv[1])
b = p.read_bytes()
sha = hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
assert sha == "32720fd2cb706cacc9297e79cf0f628ac5d660a0", sha
tree = ast.parse(b.decode("utf-8"))
source = b.decode("utf-8")
assert "self._pending.pop(key)" in source
assert "self._launch_linker(context)" in source
assert "if not self._has_active_workers(key.memory_dir)" in source
assert "logger.warning(\"Failed to launch observation linker\"" in source
assert "self._pending.setdefault(key, set()).update(context.observation_ids)" in source
assert "record_worker_aborted" in source
assert "tuple(sorted(observation_ids))" in source
print("PINNED_SOURCE_CONTRACT_PASS", sha, "nodes", len(list(ast.walk(tree))))
