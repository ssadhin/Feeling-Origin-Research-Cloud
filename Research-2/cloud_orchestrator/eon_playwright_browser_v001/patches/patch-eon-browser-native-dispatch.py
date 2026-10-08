from pathlib import Path
import ast,shutil
root=Path(r"G:\My Drive\Untitled folder\agente M MCP server")
backup=Path(r"G:\My Drive\Consciousness Formula Research\EonBrowserUpgradeBackup_v001")
if backup.exists() and not (backup/"eon_nested_server.py").exists():raise SystemExit("Unexpected backup contents")
backup.mkdir(parents=True,exist_ok=True)
p=root/"src/eon_nested_server.py"
s=p.read_text(encoding="utf-8")
a='''    if canonical in {"continuity", "chat_continuity"}:'''
b='''    if canonical in {"browser", "playwright"}:
        from eon_playwright_browser import run as browser_run
        return _jsonable(await browser_run(a, arguments))
    if canonical in {"continuity", "chat_continuity"}:'''
assert s.count(a)==1,("dispatch",s.count(a))
if not (backup/p.name).exists():shutil.copy2(p,backup/p.name)
s=s.replace(a,b)
a='''"engines": ["windows", "automation", "virtual", "grasp"],'''
b='''"engines": ["windows", "automation", "virtual", "grasp", "browser"],'''
assert s.count(a)==1,("capabilities",s.count(a))
s=s.replace(a,b)
a='''    raise ValueError("Unknown engine. Use windows, automation, virtual, or grasp.")'''
b='''    raise ValueError("Unknown engine. Use windows, automation, virtual, grasp, or browser.")'''
assert s.count(a)==2,("error",s.count(a))
s=s.replace(a,b)
ast.parse(s)
p.write_text(s,encoding="utf-8")
q=root/"src/eon_relay_client.py"
t=q.read_text(encoding="utf-8")
a='''    if e in {"continuity", "chat_continuity"}:'''
b='''    if e in {"browser", "playwright"}:
        from eon_playwright_browser import catalog as browser_catalog
        return browser_catalog(search, include_schema)
    if e in {"continuity", "chat_continuity"}:'''
assert t.count(a)==1,("catalog",t.count(a))
shutil.copy2(q,backup/q.name)
t=t.replace(a,b)
ast.parse(t)
q.write_text(t,encoding="utf-8")
print("EON_NATIVE_BROWSER_ENGINE_PATCHED_IN_PLACE")
print("BACKUP",str(backup))
