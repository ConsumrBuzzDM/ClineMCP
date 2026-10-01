> **RETIRED 2026-10-01.** ClineMCP is retired and kept for preservation only; no new work.
> Reason: folded into AgentFlow, which now owns agent session launching and supervision. No
> AgentFlow package maps one-to-one onto Cline session management, so see AgentFlow
> (https://github.com/rfd62794/AgentFlow) for the replacement. The code below is untouched. The
> sections below describe the repo as it was and are historical.

# ClineMCP

Standalone MCP server for managing Cline CLI sessions.

## Overview

ClineMCP manages Cline CLI sessions as observable, persistent, self-reporting processes. Cline runs as a child of ClineMCP, not as a subprocess of TOBOR, allowing sessions to survive TOBOR restarts.

## Features

- Session persistence via SQLite
- Telegram notifications on completion
- Bearer token authentication
- NSSM service deployment
- One active session at a time (MVP)

## Configuration

Set in `.env.local` (see `.env.example`):

| Variable | Default | Notes |
|----------|---------|-------|
| `MCP_HOST` | `127.0.0.1` | Bind host. Use `0.0.0.0` or a specific LAN/Tailscale IP only if remote clients must connect. |
| `MCP_PORT` | `8003` | Bind port. |
| `CLINEMCP_AUTH_TOKEN` | — | Required. With no token configured, `/sse` and `/messages/` return 401 (fail closed). |
| `CLINEMCP_ALLOW_NO_AUTH` | unset | Set to `1` to explicitly allow unauthenticated requests when no token is configured (development only). |

## Development

```bash
uv sync
uv run pytest --tb=no -q
```

## Architecture

See `docs/adr/` for Architectural Decision Records.
