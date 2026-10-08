# Eon Native Browser Controller — Microsoft Playwright MCP

Status: v0.1 adapter for the ORIGINAL Eon Agent MCP, no new ChatGPT plugin link.
Project: Research #2 AES v2 methodology tournament.

## Installed backend
Microsoft's Apache-2.0 @playwright/mcp version 0.0.83, pinned in %LOCALAPPDATA%\EonMCP\browser-controller on the Office PC. Connects to an already-running Chrome session; no profile copy, no new account login. Original user profile is Chrome Profile 2. Engine is browser, exposed through original Eon eon_run and eon_catalog. Real tool handshake: 13 available upstream tools.

## One-time Chrome permission (CDP, no extension install)
In the existing Chrome Profile 2 window, visit:
chrome://inspect/#remote-debugging

Enable "Allow remote debugging for this browser instance". Chrome may ask to approve Eon's incoming connection. Allow only if you trust the agent: this permission gives access to signed-in tabs. Without it the Playwright connection fails with DevToolsActivePort file not found. This is a browser access permission, NOT a new ChatGPT plugin.

Alternative: install Microsoft's Playwright Extension IN PROFILE 2, from:
https://chromewebstore.google.com/detail/playwright-extension/mmlmfjhmonkocbjadbfplnigmagldckm
Then configure backend=chrome_extension and approve its connection once. Do not paste extension secrets into chat.

## Eon calls
1. eon_catalog(engine="browser",include_schema=true)
2. eon_run(engine="browser",action="status")
3. eon_run(engine="browser",action="tools") — list actual upstream schemas through native STDIO MCP
4. eon_run(engine="browser",action="browser_tabs",arguments={"action":"list"})
5. eon_run(engine="browser",action="browser_snapshot")
6. AFTER user approval: eon_run(engine="browser",action="configure",arguments={"allow_mutating_tools":true,"confirmed_by_user":true})
7. For real text and Enter submission:
eon_run(engine="browser",action="browser_type",arguments={"target":"<verified composer target>","text":"<authorized research handoff>","submit":true,"_eon_project_url":"https://chatgpt.com/g/g-p-6ac3614901ec8191b6ba5d00cfe424c5/project"})

The adapter strips the Eon-only _eon_project_url before forwarding to Playwright. It checks selected tab Page URL from a live accessibility snapshot within the SAME upstream MCP connection and refuses cross-project browser writes.

## Safety constraints
- No browser writes before explicit user confirmation.
- Never overwrite an existing unsent draft, press Enter blindly, or repeat an uncertain submission.
- Continuation requires a verified EON_HANDOFF_V1 and latest official Research #2 Drive/GitHub checkpoint.
- A new ChatGPT chat cannot bypass plan/model usage limits.
- No scientific AES v2 result is inferred from automation tests. Frozen six-rival tournament gates remain mandatory.
- Eon folder preference: G:\My Drive\Consciousness Formula Research; use engine=file_policy.
- Browser backend is device-local: available only when a compatible PC with its Chrome session is online.

## Verified vs outstanding
Unit tests: 7/7 PASS on native Playwright adapter. Original Python syntax checks PASS.
Backend install pin: PASS. Real Microsoft Playwright MCP STDIO handshake: PASS, 13 browser actions.
Real browser_tabs against current Chrome: BLOCKED until Chrome remote debugging or extension permission is enabled.
Actual text entry + submit + receipt on signed-in Research #2: NOT TESTED.
Actual unattended end-of-loop continuation is NOT enabled by this backend alone; the existing continuity watcher remains send-disabled until end-to-end testing.

Upstream source: https://github.com/microsoft/playwright-mcp.
Source under original Eon project: src/eon_playwright_browser.py; integration hooks in eon_nested_server.py and eon_relay_client.py. Tests: tests/test_eon_playwright_browser.py.
