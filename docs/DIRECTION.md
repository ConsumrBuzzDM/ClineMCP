# ClineMCP - Direction

*Drafted 2026-09-22 by devin (Tower) from the repo's own docs - needs Robert's review before it is treated as intent.*

## Purpose

Standalone MCP server managing Cline CLI sessions as observable, persistent,
self-reporting processes - a peer of TOBOR, not a child. Cline runs as a
subprocess of ClineMCP so sessions survive TOBOR restarts. Port 8003.

## Current state

FastAPI + mcp SDK + aiosqlite session persistence; binding contract floor of
76/0/0 pytest results (`AGENT_CONTRACT.md`); sessions persisted before
subprocess start; crash-recovery marks stale "running" sessions failed on
startup.

## Next steps

1. Maintenance + phase work via `docs/directives/` per the contract.
2. Keep the 76-test floor - a count drift is a STOP, not a fix target
   (`AGENT_CONTRACT.md`).

## Definition of done

`uv run pytest --tb=no -q` reports the contract's exact floor; sessions persist
and self-report across restarts.

## Do not

- `asyncio.create_subprocess_exec` only - never `shell=True`.
- One active Cline session at a time (MVP constraint).
- ADRs in `docs/adr/` are permanently locked once committed.

## Sources of truth

- `AGENT_CONTRACT.md` (binding pre-flight contract), `AGENTS.md`,
  `docs/ROADMAP.md`, `docs/adr/`.
