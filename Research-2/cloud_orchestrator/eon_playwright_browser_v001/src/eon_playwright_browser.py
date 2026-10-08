"""Open-source Playwright MCP as Eon's internal browser engine.

Microsoft @playwright/mcp 0.0.83 (Apache-2.0) is locally pinned.
Connects to user's ALREADY running Chrome:
  chrome_cdp: Chrome 144+ remote debugging permission (no extension).
  chrome_extension: official Playwright extension in specified Chrome profile.
Never launches an isolated browser, reads cookies, or installs another ChatGPT MCP.
"""
from __future__ import annotations
import asyncio
import importlib.util
import json
import os
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlparse

BROWSER_HOME = Path(os.getenv("LOCALAPPDATA", str(Path.home()))) / "EonMCP" / "browser-controller"
SETTINGS = BROWSER_HOME / "eon-browser.json"
PROFILE_DIR = Path(os.getenv("LOCALAPPDATA", str(Path.home()))) / "Google" / "Chrome" / "User Data"
EXTENSION_ID = "mmlmfjhmonkocbjadbfplnigmagldckm"
EXTENSION_URL = f"https://chromewebstore.google.com/detail/playwright-extension/{EXTENSION_ID}"
PROJECT_URL = "https://chatgpt.com/g/g-p-6ac3614901ec8191b6ba5d00cfe424c5/project"
PACKAGE_VERSION = "0.0.83"
NODE = Path("C:/Program Files/nodejs/node.exe")
CLI = BROWSER_HOME / "node_modules" / "@playwright" / "mcp" / "cli.js"
ALLOWED = frozenset({
    "browser_tabs", "browser_snapshot", "browser_navigate",
    "browser_click", "browser_type", "browser_press_key",
    "browser_wait_for", "browser_handle_dialog", "browser_hover",
    "browser_select_option", "browser_fill_form", "browser_take_screenshot",
    "browser_evaluate"
})
MUTATING = frozenset({
    "browser_navigate", "browser_click", "browser_type", "browser_press_key",
    "browser_handle_dialog", "browser_select_option", "browser_fill_form"
})
CONNECTIONS = {"chrome_cdp", "chrome_extension"}


def config() -> dict[str, Any]:
    default = {"backend": "chrome_cdp", "profile": "Profile 2",
               "project_url": PROJECT_URL, "allow_mutating_tools": False}
    if SETTINGS.exists():
        data = json.loads(SETTINGS.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("BROWSER_CONFIG_CORRUPT")
        default.update({k: v for k, v in data.items() if k in default})
    if default["backend"] not in CONNECTIONS:
        raise ValueError("BROWSER_BACKEND_INVALID")
    if default["profile"] not in ("Default",) and not re.fullmatch(r"Profile [0-9]{1,3}", str(default["profile"])):
        raise ValueError("BROWSER_PROFILE_INVALID")
    validate_project(default["project_url"])
    return default


def validate_project(url: str) -> str:
    if not isinstance(url, str) or len(url) > 500:
        raise ValueError("BROWSER_PROJECT_URL_INVALID")
    u = urlparse(url)
    if u.scheme != "https" or u.netloc.lower() != "chatgpt.com":
        raise ValueError("BROWSER_PROJECT_HOST_INVALID")
    if not re.fullmatch(r"/g/g-p-[a-f0-9]{32}/project", u.path):
        raise ValueError("BROWSER_PROJECT_PATH_INVALID")
    return url


def project_match(observed: str, expected: str) -> bool:
    """Must be exact project ID, not just matching a ChatGPT hostname."""
    try:
        path = urlparse(observed)
        e = urlparse(validate_project(expected))
    except ValueError:
        return False
    project_id = e.path.split("/")[2]
    return (path.scheme == "https" and path.netloc.lower() == "chatgpt.com"
            and re.match(r"^/g/"+re.escape(project_id)+r"(?:-[a-z0-9-]+)?/(?:project|c/)", path.path) is not None)


def extension_installed(profile: str) -> bool:
    target = PROFILE_DIR / profile / "Extensions" / EXTENSION_ID
    return target.exists() and any(target.glob("*/manifest.json"))


def package_version() -> str | None:
    file = CLI.parent / "package.json"
    if not file.exists():
        return None
    try:
        value = json.loads(file.read_text(encoding="utf-8")).get("version")
        return value if isinstance(value,str) else None
    except Exception:
        return None


def status() -> dict[str, Any]:
    c = config()
    ver = package_version()
    return {
        "engine": "browser", "upstream": "microsoft/playwright-mcp",
        "upstream_version": ver, "expected_version": PACKAGE_VERSION,
        "license": "Apache-2.0",
        "installed_and_pinned": ver == PACKAGE_VERSION and NODE.exists() and CLI.exists(),
        "browser_session": "EXISTING signed-in Chrome; Eon never launches a new profile",
        "backend": c["backend"], "chrome_profile": c["profile"],
        "extension_installed_in_chrome_profile": extension_installed(c["profile"]),
        "extension_store": EXTENSION_URL,
        "cdp_one_time_permission_page": "chrome://inspect/#remote-debugging",
        "project_url": c["project_url"],
        "mutating_actions_authorized": c["allow_mutating_tools"],
        "note": "Enable Chrome remote debugging once, or install Microsoft's Playwright Extension into this profile and approve the connection; never bypass ChatGPT usage limits."
    }


def argv(c: dict[str, Any]) -> list[str]:
    if package_version() != PACKAGE_VERSION or not NODE.exists():
        raise RuntimeError("PINNED_MICROSOFT_PLAYWRIGHT_MCP_NOT_INSTALLED")
    if c["backend"] == "chrome_extension":
        if not extension_installed(c["profile"]):
            raise RuntimeError("PLAYWRIGHT_EXTENSION_REQUIRED_IN_PROFILE_"+c["profile"]+" — "+EXTENSION_URL)
        return [str(CLI), "--extension", "--profile-dir-name", str(c["profile"])]
    return [str(CLI), "--cdp-endpoint=chrome"]


def _content_result(result) -> dict[str, Any]:
    content = []
    for item in getattr(result, "content", []):
        typ = getattr(item, "type", None)
        if typ == "text":
            t = str(getattr(item, "text", ""))
            content.append({"type": "text", "text": t[:80000]})
        else:
            content.append({"type": str(typ), "note": "Binary media not forwarded in Eon text response"})
    return {"error": bool(getattr(result,"is_error", False)), "content": content}


def snapshot_page_url(result) -> str | None:
    """Extract URL ONLY from the Playwright MCP page metadata, not user text."""
    lines = "\n".join(str(getattr(c, "text", "")) for c in getattr(result, "content", [])
                      if getattr(c,"type",None)=="text")
    for line in lines.splitlines()[:18]:
        match = re.fullmatch(r"\s*-\s*Page URL:\s*(https://\S+)\s*", line)
        if match:
            return match.group(1)
    return None


async def _playwright(action: str, arguments: dict[str, Any], guard_project: str | None = None):
    """Native STDIO MCP client, not an additional ChatGPT plugin/connector."""
    from fastmcp import Client
    from fastmcp.client.transports import StdioTransport
    c = config()
    t = StdioTransport(command=str(NODE), args=argv(c), cwd=str(BROWSER_HOME))
    client = Client(t, timeout=35, init_timeout=20)
    async with client:
        if action == "__list_tools__":
            tools = await client.list_tools()
            return {"tools": [{
                "name": tool.name, "description": (tool.description or "")[:1200],
                "schema": getattr(tool, "input_schema", None) or getattr(tool, "inputSchema", None)
            } for tool in tools if tool.name in ALLOWED]}
        if guard_project:
            if action == "browser_navigate":
                if not project_match(str(arguments.get("url", "")), guard_project):
                    raise PermissionError("CANNOT_NAVIGATE_OUTSIDE_RESEARCH_PROJECT")
            else:
                snap = await client.call_tool("browser_snapshot", {})
                page_url = snapshot_page_url(snap)
                if not page_url or not project_match(page_url, guard_project):
                    raise PermissionError("CURRENT_PLAYWRIGHT_TAB_NOT_VERIFIED_AS_RESEARCH_PROJECT")
        output = await client.call_tool(action, arguments)
        return _content_result(output)


def catalog(search: str | None=None, include_schema: bool=True) -> dict[str, Any]:
    acts = [
        ("status", "Check installed backend, Chrome profile, one-time authorization readiness; never touches tabs."),
        ("configure", "Choose chrome_cdp or chrome_extension and exact Chrome Profile 2/project; optional explicit approval for mutating tools."),
        ("tools", "List underlying official Playwright MCP browser tools and schemas."),
    ]
    acts += [(x, "Delegated Microsoft Playwright MCP browser tool (real DOM-backed interaction), exact upstream arguments.") for x in sorted(ALLOWED)]
    q = (search or "").lower()
    acts = [{"action":name,"description":desc,
             **({"arguments_schema":{"type":"object","description":"See browser.tools for exact upstream arguments"}} if include_schema else {})}
            for name,desc in acts if not q or q in name or q in desc.lower()]
    return {"engine":"browser","actions":acts,"upstream":"Microsoft Playwright MCP 0.0.83 (Apache-2.0)",
            "browser_profile":"Profile 2", "extra_chatgpt_mcp_required":False,
            "requires_one_time_Chrome_permission":True,
            "notes":"Mutation tools are off until explicitly configured. Do not use to evade plan/message limits."}


def _set_config(arguments: dict[str, Any]) -> dict[str, Any]:
    c=config()
    if "backend" in arguments:
        if arguments["backend"] not in CONNECTIONS:
            raise ValueError("CHOOSE_chrome_cdp_OR_chrome_extension")
        c["backend"]=arguments["backend"]
    if "profile" in arguments:
        profile=arguments["profile"]
        if profile not in ("Default",) and not re.fullmatch(r"Profile [0-9]{1,3}", str(profile)):
            raise ValueError("CHROME_PROFILE_INVALID")
        c["profile"]=profile
    if "project_url" in arguments:
        c["project_url"]=validate_project(arguments["project_url"])
    if "allow_mutating_tools" in arguments:
        if arguments.get("confirmed_by_user") is not True:
            raise ValueError("EXPLICIT_USER_CONFIRMATION_REQUIRED_TO_CHANGE_BROWSER_WRITES")
        c["allow_mutating_tools"]=bool(arguments["allow_mutating_tools"])
    BROWSER_HOME.mkdir(parents=True, exist_ok=True)
    temp=SETTINGS.with_suffix(".tmp")
    temp.write_text(json.dumps(c,indent=2),encoding="utf-8")
    os.replace(temp,SETTINGS)
    return status()


async def run(action: str, arguments: dict[str, Any] | None=None):
    arguments=arguments or {}
    if action == "status":
        return status()
    if action == "configure":
        return _set_config(arguments)
    if action == "tools":
        return await _playwright("__list_tools__",{})
    if action not in ALLOWED:
        raise ValueError("UNRECOGNIZED_OR_DISALLOWED_PLAYWRIGHT_ACTION")
    # Only source-native browser actions, no arbitrary evaluate (which allows JS
    # execution against signed-in sites) until user grants explicit browser writes.
    sensitive = action in MUTATING or action == "browser_evaluate" or (
        action == "browser_tabs" and arguments.get("action") not in ("list", None))
    guard = None
    if sensitive:
        if not config()["allow_mutating_tools"]:
            raise PermissionError("BROWSER_MUTATION_NOT_AUTHORIZED")
        # For all writes and evaluate, independently verify the browser tab.
        # A caller-supplied project URL alone is NOT sufficient evidence.
        if arguments.pop("_eon_project_url", None) != config()["project_url"]:
            raise PermissionError("EXACT_RESEARCH_PROJECT_URL_CONFIRMATION_REQUIRED")
        guard = config()["project_url"] if action != "browser_tabs" else None
    try:
        return await asyncio.wait_for(_playwright(action,arguments,guard),timeout=95)
    except asyncio.TimeoutError as e:
        raise RuntimeError("PLAYWRIGHT_MCP_BROWSER_TIMEOUT_OR_APPROVAL_REQUIRED") from e


def test_offline() -> dict[str, Any]:
    assert project_match("https://chatgpt.com/g/g-p-6ac3614901ec8191b6ba5d00cfe424c5-research-2/c/a",PROJECT_URL)
    assert project_match(PROJECT_URL,PROJECT_URL)
    assert not project_match("https://example.org/g/g-p-6ac3614901ec8191b6ba5d00cfe424c5/project",PROJECT_URL)
    assert not project_match("https://chatgpt.com/g/g-p-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/project",PROJECT_URL)
    assert argv({"backend":"chrome_cdp", "profile":"Profile 2"})[-1]=="--cdp-endpoint=chrome" if package_version() == PACKAGE_VERSION else True
    return {"ok":True,"name":"Microsoft Playwright MCP Eon browser adapter","test":"PASS","browser_interaction":False}
