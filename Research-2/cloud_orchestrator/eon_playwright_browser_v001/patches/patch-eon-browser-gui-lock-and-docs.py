from pathlib import Path
import ast
root=Path(r"G:\My Drive\Untitled folder\agente M MCP server")
p=root/"src/eon_nested_server.py"
s=p.read_text(encoding="utf-8")
a='''    if canonical in {"automation", "virtual"}:
        return True'''
b='''    if canonical in {"automation", "virtual", "browser", "playwright"}:
        return True'''
assert s.count(a)==1
s=s.replace(a,b)
ast.parse(s)
p.write_text(s,encoding="utf-8")
readme=root/"README.md"
r=readme.read_text(encoding="utf-8")
heading="## Native open-source Chrome browser control"
if heading not in r:
 r += "\n"+heading+"\n\nThe existing Eon MCP connection now exposes eon_catalog(engine=browser) and eon_run(engine=browser,action=...). Microsoft @playwright/mcp@0.0.83 is installed locally under %LOCALAPPDATA%\\EonMCP\\browser-controller and connects to the existing Chrome instance (default chrome_cdp, optional Chrome Profile 2 Playwright Extension); never copies cookies, starts a separate Chrome profile, or adds a ChatGPT connector. Full setup, one-time Chrome permission, type/Enter/browser_click examples, and safeguards: docs/EON_NATIVE_BROWSER_CONTROLLER.md. Browser writes require explicit authorization and selected Research #2 page verification. Browser automation is not evidence of AES v2 validity.\n"
 readme.write_text(r,encoding="utf-8")
agents=root/"AGENTS.md"
t=agents.read_text(encoding="utf-8")
instruction="## Browser controller: existing Chrome and research continuity"
if instruction not in t:
 t += "\n"+instruction+"\n\nWhen the user asks Eon to type/click/press Enter in Chrome, prefer the native browser engine backed by Microsoft's pinned Playwright MCP; do not blindly send Windows UIA keystrokes. Use only the user's original signed-in Chrome session with its own browser permission. Call eon_catalog(engine=browser) and eon_run(engine=browser,action=status/tools). If remote debugging is disabled, instruct user to enable it at chrome://inspect/#remote-debugging or install the official Playwright Extension in the correct profile. Never attempt Chrome profile copying, permission bypass, cross-project writes, silent overwrite of a draft, or retries after ambiguous message submissions. The Research #2 scientific state is determined from canonical Drive/GitHub and frozen protocols, NOT from the browser automation ledger.\n"
 agents.write_text(t,encoding="utf-8")
print("EON_BROWSER_GUI_LOCK_AND_DOCS_UPDATED")
