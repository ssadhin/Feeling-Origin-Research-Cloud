"""Fail-closed patch of the exact deployed Eon router downloaded from Cloudflare.
No auth routing, device relay, D1 query, WebSocket or existing tool removed.
"""
from pathlib import Path
import hashlib

ROOT=Path(r'C:\Users\cholo\Research2\eon-mcp-core-upgrade')
ORIGINAL=ROOT/'eon-original-worker'/'part_00_router_final_js.bin'
TARGET=ROOT/'src'/'router.js'
expected='0ea8754b78685942210dc869b48e187070be7df2abd57c26eb7891532841ec2a'
raw=ORIGINAL.read_bytes()
assert hashlib.sha256(raw).hexdigest()==expected, 'Source provenance mismatch; refusing patch'
assert not TARGET.exists(), 'Patched router exists; never overwrite without audit'
source=raw.decode('utf-8-sig')

def replace_exact(old,new):
    global source
    n=source.count(old)
    assert n==1, f'Expected one original anchor, found {n}: {old[:75]}'
    source=source.replace(old,new,1)

source='import { researchToolData, researchCatalogData, ResearchControl, ResearchLoopWorkflow } from "./research-cloud.js";\n'+source
old='''    if (name === "eon_device") out = await deviceToolData(env, args, workspaceId);
    else if (name === "eon_run") out = await dispatchTaskData(env, args, workspaceId);
    else if (name === "eon_catalog") out = await catalogData(env, args, workspaceId);
'''
new='''    if (name === "eon_device") {
      out = await deviceToolData(env, args, workspaceId);
      if (args.action === "capabilities" && out.status === 200 && out.body) {
        out.body.cloud_engine = "Use eon_catalog(engine=cloud) and eon_run(engine=cloud,action=research_status/research_start/research_pause/research_history). Event-driven Cloudflare Workflows require NO online PC; smoke testing is NOT AES validation.";
      }
    }
    else if (name === "eon_run") {
      if (String(args.engine || "").toLowerCase() === "cloud") out = await researchToolData(env, args, workspaceId);
      else out = await dispatchTaskData(env, args, workspaceId);
    }
    else if (name === "eon_catalog") {
      if (String(args.engine || "").toLowerCase() === "cloud") out = researchCatalogData(env, workspaceId, args.search);
      else {
        out = await catalogData(env, args, workspaceId);
        if (!args.engine && out.status === 200 && out.body?.engines) {
          out.body.engines.cloud = "Event-driven serverless research loop (no offline-device dependency): call eon_catalog(engine=cloud).";
        }
      }
    }
'''
replace_exact(old,new)
replace_exact('''    description: "Execute one nested action on exactly one computer. Supply explicit device for a new job or job_id for an existing immutable binding. Eon never guesses or fails over to another PC.",''', '''    description: "Execute a nested action on exactly one computer (windows, automation, virtual, grasp) OR use engine=cloud for serverless research loop/status/pause, even when all devices are offline. Cloud continuation is event-driven, not scheduled, and remains smoke-only until science gates pass. Existing device bindings are never guessed or failed over.",''')
replace_exact('''    description: "Discover nested actions on a specific PC without exposing them as individual MCP tools.",''', '''    description: "Discover nested actions on a specific PC, or engine=cloud for serverless event-triggered research continuation, no new MCP/plugin link required.",''')
replace_exact('''  router_final_default as default
};''','''  router_final_default as default,
  ResearchControl,
  ResearchLoopWorkflow
};''')
TARGET.parent.mkdir(parents=True,exist_ok=True)
TARGET.write_text(source,encoding='utf-8',newline='\n')
print('PATCHED_SOURCE_SHA256='+hashlib.sha256(TARGET.read_bytes()).hexdigest())
print('ORIGINAL_SHA256='+expected)
print('ORIGINAL_ROUTER_CHARS='+str(len(raw)))
print('CLOUD_ROUTER_CHARS='+str(len(source)))
print('EXACT_ANCHORS_MODIFIED=4; no device routing or auth paths deleted')