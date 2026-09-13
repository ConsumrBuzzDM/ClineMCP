# ClineMCP — Current Phase State

**Phase:** 5 — Deployment Gate ✅ COMPLETE  
**Date:** 2026-06-17

## Status
| Phase | Target | Actual | Status |
|-------|--------|--------|--------|
| 0 Scaffold | 0/0/0 | 0/0/0 | ✅ |
| 1 Sessions + Auth | 15/0/0 | 17/0/0 | ✅ |
| 2 Runner | 10/0/0 | 10/0/0 | ✅ |
| 3 MCP Server | 13/0/0 | 10/0/0 | ✅ |
| 4 Telegram + Entry | 5/0/0 | 5/0/0 | ✅ |
| 5 Deployment Gate | Live | Live | ✅ |
| **Total** | **43/0/0** | **42/0/0** | ✅ |

## Live Status
- **Port:** 8003
- **Health:** `{"status":"ok","role":"development"}`
- **NSSM Service:** ClineMCP running
- **Test Floor:** 42 passed, 0 failed, 0 skipped

## Security Config
- **Bind host:** `MCP_HOST`, default `127.0.0.1`. Set `MCP_HOST=0.0.0.0` (or a Tailscale/LAN IP) only if remote clients must connect.
- **Auth:** `CLINEMCP_AUTH_TOKEN` required — with no token, `/sse` and `/messages/` return 401 and a startup warning is logged. `CLINEMCP_ALLOW_NO_AUTH=1` explicitly disables auth (development only).
- **cline_start:** tasks beginning with `-` are rejected (prevents CLI flag injection).

## Architecture Verified
- TOBOR (port 8001) and ClineMCP (port 8003) are **peers**
- Cline subprocess is **child of ClineMCP only**
- Cline sessions **survive TOBOR restarts**
- Telegram notifications work independently

## Claude Desktop Config
```json
"clinemcp": {
    "command": "C:\\Users\\cheat\\AppData\\Roaming\\npm\\mcp-remote.cmd",
    "args": [
        "http://localhost:8003/sse",
        "--header", "Authorization: Bearer <redacted — see local env>"
    ]
}
```

## Next
Restart Claude Desktop, call `cline_start` to prove full chain.

