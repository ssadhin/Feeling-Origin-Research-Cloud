# Eon Research #2 cloud continuation — v0.1 prototype

**Status:** cloud-native continuation coordinator and bounded source-inventory agent, NOT a full autonomous research scientist, NOT an Eon device worker, NOT evidence of AES superiority. Eon's existing Cloudflare WebSocket relay cannot execute desktop actions if all devices are offline. This project is a separate Worker + durable Workflow within the same Cloudflare ecosystem; Eon MCP is used to install, deploy and diagnose it. The Eon core/relay remains untouched.

## Contract

- No cron schedule. An authorized `POST /admin/start` creates loop 0; after a verified `CONTINUE`, Cloudflare Workflows automatically creates a deterministic-ID immediate successor for loop N+1.
- The Durable Object stores authoritative chain state, serial order, immutable per-loop ledger and user pause. Duplicate or out-of-order reports fail closed. Audit replays cannot skip sequence.
- State `PAUSED_BUDGET` means **goal not yet met**, not a scientific verdict. The prototype intentionally stops after a bounded number of loops to prevent unexpected spending. `BLOCKED` also does not mean goal resolved.
- `smoke`: three free/deterministic cloud-only loops, ending in budget pause, without OpenAI or Google/GitHub tokens. This validates trigger and cloud persistence only, not science or offline physical testing.
- `live`: requires cloud OpenAI, Google Drive OAuth refresh credentials, GitHub repo PAT. It reads the latest canonical 17 status each loop and chooses a narrow source-inventory audit over one of six SHA-pinned official rivals. Each verified audit is **create-only** committed to Research-2/cloud_orchestrator/loops/... in the canonical GitHub branch. The action cannot run arbitrary model-proposed shell commands or declare methodology superiority.
- No full competitor fidelity, independent defender, provider parity, OOD tournament, executable frozen AES contestant, or final decision engine is implemented. Live mode therefore **must not be interpreted as capable of completing the entire AES v2 methodology tournament autonomously**. A later version would need a separate vetted cloud CI/sandbox runner, source-native fixtures, cost metering, and independent human review under frozen gates. The v0.1 step engine deliberately halts when narrow available audit capabilities are exhausted.

## Deploy (Cloudflare account; no Eon laptop needed once deployed)

1. `npm install` and `npm test` (Node 18+).
2. `npx wrangler deploy` (dedicated Worker name `eon-research2-cloud-loop`; do not overwrite Eon relay Worker).
3. `npx wrangler secret put ADMIN_TOKEN` (cryptographically random, owner-only; required for `/admin/*`). No public start route. Never paste secret in chat or put it in repo.
4. Before **live** operation, create scoped Google OAuth client+refresh token with Drive/Docs read permission, GitHub fine-grained token limited to authorized Research #2 repo plus official public source reads, and an OpenAI API key. Set secrets `OPENAI_API_KEY`, `GITHUB_TOKEN`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`. Set Worker `RESEARCH_MODE=live` in config and redeploy. The user must approve API spending and provider permissions first. This version defaults to `smoke`, and doesn't autonomously start on deploy.
5. With authorized token, `POST /admin/start` (no body required), `GET /admin/status`, `POST /admin/pause`. `GET /health` is public and reveals only non-sensitive mode/status.
6. Cloud continuation uses Cloudflare Workflows + SQLite Durable Object. Check Worker/Workflow logs and the GitHub immutable per-run ledger. No machine-hosted long-running background process is required.

## Scientific and operational limits

- Every run is a *bounded action episode*. A scheduled/condition watch in ChatGPT is not used.
- `PAUSED_BUDGET` / `BLOCKED` are barriers, never PASS. No LLM-supplied `GOAL_MET` outcome is accepted in this version. Human-reviewed prospective certification and a new executor version are required before enabling final automatic verdict, preserving scientific honesty.
- Transparent cost ceilings: `MAX_LOOPS=12` default for live, hard cap 100; one OpenAI call (plus necessary source/data calls) per loop; no other cloud compute. This is a safety limit, not a scientific stopping criterion. Follow-up requires an authorized new run/version, not misrepresenting limits as success.
- Current prototype checks only pinned-source tree manifests. A source inventory is not a source-native fidelity test. It does not execute scientific research on a disconnected Eon desktop.
- Current GitHub create-only replay handling assumes identical retained events; the workflow instance idempotence protects successor duplication. The tool cannot verify true independent defender signatures.
- Remote source trust and OAuth scope/consent must be reviewed before live mode.

## Why this is alongside Eon, not inside the device agent

`eon_device` reports Eon's Cloudflare Worker relay and device-bound outbound WebSocket sessions. That relay only forwards to online devices, so editing its local automation engine would not satisfy the *all devices offline* condition. Cloudflare Workflows runs server-side independently and is the intended cloud continuation layer. Eon MCP is an installer and optional troubleshooting connector.

## Artifacts

- `src/index.js`: cloud Workflow, Durable Object, Google/GitHub/OpenAI integration, admin endpoint.
- `src/decision.mjs`: fixed pinned universe and conservative state machine.
- `test/decision.test.mjs`: six fail-closed tests.
- `wrangler.jsonc`, `package.json`: Cloudflare deployment.

### Versioning

v0.1 = coordinator/source inventory. No effect on frozen 19C/19G/19H gate documents or Research #2 17S status unless explicitly recorded as a tooling artifact. Do not add evidence of AES superiority from this infrastructure alone.