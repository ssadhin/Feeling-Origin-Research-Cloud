#!/usr/bin/env python3
"""Research #2 source-native, nondecisive InternAgent memory qualification on GitHub."""
import asyncio, hashlib, importlib.util, json, os, pathlib, platform, sys, tempfile, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "research2" / "qualification" / "output-internagent"
OUT.mkdir(parents=True, exist_ok=True)
PIN = "fa8c3eedfa9751d3752ea6eb49220b303ac2397d"
FILE = "internagent/mas/memory/memory_manager.py"
SOURCE = f"https://raw.githubusercontent.com/InternScience/InternAgent/{PIN}/{FILE}"
EXPECTED_BLOB = "19445653f88b945d0fad8dcf5250c6e219f97b44"
checks = []
start = time.monotonic()
module = None

def check(name, f):
    try:
        evidence = f()
        checks.append({"name": name, "result": "PASS", "evidence": evidence})
    except Exception as e:
        checks.append({"name": name, "result": "FAIL", "error": type(e).__name__ + ": " + str(e)})

def load_original():
    global module
    with urllib.request.urlopen(SOURCE, timeout=25) as response:
        data = response.read()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert blob == EXPECTED_BLOB, f"blob mismatch {blob}"
    with tempfile.TemporaryDirectory() as d:
        source_path = pathlib.Path(d) / "memory_manager.py"
        source_path.write_bytes(data)
        spec = importlib.util.spec_from_file_location("internagent_r2_pinned", str(source_path))
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    return f"unchanged source from {PIN}; verified original Git blob SHA1 {blob}"

check("PINNED_ORIGINAL_BLOB_AND_DIRECT_IMPORT", load_original)

async def test_mem():
    m = module.InMemoryMemoryManager()
    await m.startup()
    await m.save_session("A", {"id": "A", "research_goal": "failure challenge"})
    await m.save_session("B", {"id": "B", "research_goal": "independent positive"})
    await m.save_hypothesis("neg", {"session_id": "A", "outcome": "negative"})
    await m.save_hypothesis("pos", {"session_id": "B", "outcome": "positive"})
    assert (await m.get_hypotheses_by_session("A"))[0]["outcome"] == "negative"
    assert (await m.get_hypotheses_by_session("B"))[0]["outcome"] == "positive"
    summary = {s["id"]: s for s in await m.list_sessions()}
    assert summary["A"]["hypothesis_count"] == 1 and summary["B"]["hypothesis_count"] == 1
    assert await m.delete_session("A") is True
    assert await m.get_hypothesis("neg") == {}
    assert (await m.get_hypothesis("pos"))["outcome"] == "positive"
    cold = module.InMemoryMemoryManager()
    assert await cold.get_hypotheses_by_session("B") == []
    return "positive/negative hypotheses; session isolation; deletion and cold-start negative control"

check("NATIVE_INMEMORY_HYPOTHESIS_PERSISTENCE", lambda: asyncio.run(test_mem()))

async def test_fs():
    with tempfile.TemporaryDirectory(prefix="r2_ia_") as folder:
        m = module.FileSystemMemoryManager(data_dir=folder, task_name="r2")
        await m.save_session("one", {"id": "one", "research_goal": "persistent task"})
        await m.save_hypothesis("h0", {"session_id": "one", "outcome": "failed"})
        await m.save_hypothesis("h1", {"session_id": "one", "outcome": "successful"})
        other = module.FileSystemMemoryManager(data_dir=folder, task_name="r2")
        assert (await other.get_session("one"))["research_goal"] == "persistent task"
        assert {h["outcome"] for h in await other.get_hypotheses_by_session("one")} == {"failed", "successful"}
        assert await other.delete_session("one") is True
        assert await other.get_session("one") == {}
    return "original file-backed manager: negative/positive history survives new object, then delete"

check("NATIVE_FILE_MEMORY_REOPEN", lambda: asyncio.run(test_fs()))

obj = {
    "program": "Research2", "phase": "Q1_nondecisive", "exact_original_commit": PIN,
    "original_source_file": FILE, "expected_git_blob_sha1": EXPECTED_BLOB,
    "runtime": sys.version.split()[0], "platform": platform.platform(),
    "cpu_count": os.cpu_count(), "elapsed_seconds": round(time.monotonic()-start, 3),
    "full_19C_certified": False, "decisive_AES_trials": 0,
    "pass": sum(x["result"]=="PASS" for x in checks),
    "fail": sum(x["result"]=="FAIL" for x in checks), "checks": checks,
}
p = OUT / "internagent_cloud_receipt.json"
p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(obj, sort_keys=True))
sys.exit(1 if obj["fail"] else 0)
