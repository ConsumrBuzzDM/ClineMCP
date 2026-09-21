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
