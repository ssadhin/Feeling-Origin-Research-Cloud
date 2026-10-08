# Eon Agent MCP — native cloud research continuation (one existing link)

**Not another plugin or MCP endpoint.** This is an additive upgrade of the original production `eon-mcp-agent` Cloudflare Worker, preserving Eon's workspace authentication, EON_DB, DeviceHub, and the exact three existing top-level tools (`eon_device`, `eon_run`, `eon_catalog`). The installed device relays remain intact.

## How ChatGPT discovers it

- `eon_catalog(engine="cloud", include_schema=true)` lists the cloud research actions.
- `eon_run(engine="cloud", action="research_capabilities")` explains the available cloud capability and its limitations.
- `eon_run(engine="cloud", action="research_start", arguments={"mode":"smoke"})` starts three cloud-only continuation cycles without an hourly schedule or any online computer. Each unresolved loop triggers the next Workflows instance immediately. The third loop ends `PAUSED_BUDGET`, not success.
- `eon_run(engine="cloud", action="research_status")` reads the current durable progress.
- `eon_run(engine="cloud", action="research_history")` reads archived smoke event history.
- `eon_run(engine="cloud", action="research_pause")` pauses further progression.

The `eon_device(action="capabilities")` response also advertises the cloud engine. Cloud calls bypass the per-PC routing gate, while ordinary device actions preserve their existing immutable device binding.

## Scientific honesty

The first deployed version MUST use `RESEARCH_MODE=smoke`. It contains **no autonomous OpenAI calls, no source-native competitor executions, and no prospective AES-v2 evidence**. It proves only the event-driven continuation infrastructure; it cannot validate AES superiority. A future version must implement genuine cloud-only research tools, provenance, source-native competitor tests, model/provider budget parity and independent defender reviews. Only after scientific protocols are frozen and authorized may live research be enabled; `GOAL_MET` must never be inferred from smoke outputs or an LLM assertion.

## Preservation / rollback

The exact deployed original Eon router before editing was downloaded from Cloudflare Scripts API as a multipart response, saved at `eon-original-worker/part_00_router_final_js.bin`, SHA-256 `0ea8754b78685942210dc869b48e187070be7df2abd57c26eb7891532841ec2a`. The patched router build is versioned separately and always preserve these original bytes and runtime bindings. The live Worker deployment version must be recorded before any upgrade, and post-deployment Eon connectivity verified; on failure roll back the prior Cloudflare version.

No new ChatGPT plugin connection, no new MCP link, no device relay requirement for cloud continuation; credentials do not appear in source code.