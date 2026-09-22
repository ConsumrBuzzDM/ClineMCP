# ClineMCP — Roadmap

*Last updated: 2026-09-22 by robert-claude (Tower)*

## Purpose

A standalone MCP server that manages Cline CLI sessions as observable,
persistent, self-reporting processes. It exists specifically so Cline
sessions survive TOBOR restarts — ClineMCP is a peer of TOBOR, not a
child, running Cline as its own subprocess rather than TOBOR's.

## Current maturity

Real, actively-developed infrastructure — well past its original v0.1
MVP scope. 76 passing tests (contract fixed 2026-09-22; previously
documented as 40, stale since the project grew). FastAPI + `mcp` SDK +
`aiosqlite` for session persistence.

## Phase history

| When | What |
|---|---|
| — | v0.1 MVP built per `docs/sdd/ClineMCP_SDD_v0_1.md` (Phase 0 target: 40 tests) |
| Since | FastAPI MCP server, Telegram notifications, session enrichment, an `mcp.server.lowlevel` migration |
| Since | Upstream merges: agent_type routing, provider-prefix parsing, a fail-closed auth security fix |
| 2026-09-22 | `AGENT_CONTRACT.md`'s stale "40 passed" pre-flight gate corrected to the real count (76) — `ClineMCP_ContractTestFloorDrift_Directive.md`, Done |

## Active / Queued

Nothing currently queued. Check `docs/directives/` / `DirectiveQueueMCP`
for anything newer than this note.

## Candidate next phases

1. **A living state doc.** No single document tracks what's landed
   since the v0.1 SDD — `docs/adr/` (read-only, append-only) is the
   closest thing to a change log, but it's not a quick-read summary.
   A `docs/state/current.md`-style doc (matching the pattern used in
   TeleseroAdminSuite2026, ConvosoMCP, CBTowerAnsible) would make future
   "what's actually built here" questions answerable in one read instead
   of a `git log` archaeology pass. Not urgent, but a real, recurring
   cost every time an agent (or Robert) needs to answer that question.
2. **ADR backfill check.** Worth a quick audit: does every major
   post-MVP change (the FastAPI server, Telegram notifications, the
   `mcp.server.lowlevel` migration) have a corresponding ADR, or did
   some real architectural decisions land without one? If gaps exist,
   a retroactive ADR captures the "why" before it's lost to memory.

## Constraints & gotchas for future dispatches

- **`docs/adr/` is read-only / append-only** per `AGENT_CONTRACT.md` —
  never edit an existing ADR, only add new ones.
- **`AGENT_CONTRACT.md`'s pre-flight gate is binding language** every
  dispatched session is told to follow literally ("if count differs:
  STOP"). If a future directive intentionally changes test count
  expectations, say so explicitly in the directive text — otherwise a
  dispatched session may halt on the very drift it's meant to fix (this
  happened 2026-09-22, worth remembering as a pattern).
- No live-service or sibling-repo dependencies have caused dispatch
  problems here — nothing special beyond the two points above.

## Open questions

None currently open.

```yaml roadmap
status: draft
approved: ""
reviewed: "2026-09-22"
replan_after_days: 14
stop_if: "ClineMCP's documented architecture, state, and all post-MVP decisions are captured in living docs and ADRs — future agents can answer 'what's actually built here' in one read."
milestones:
  - id: M1
    title: Documentation & ADR backfill
    status: pending
    exit:
      - file: "docs/state/current.md"
      - grep:
          path: "docs/adr"
          pattern: "FastAPI|Telegram|mcp.server.lowlevel"
    steps:
      - id: M1.1
        title: Create living state documentation
        kind: docs
        size: M
        status: pending
        directive: ""
        detail: "Create `docs/state/current.md` as a living summary of what's actually built in ClineMCP since the v0.1 SDD — following the pattern used in TeleseroAdminSuite2026, ConvosoMCP, CBTowerAnsible. Covers FastAPI server, Telegram notifications, session enrichment, and mcp.server.lowlevel migration. Not urgent, but answers a recurring question agents ask."
        accept:
          - file: "docs/state/current.md"
      - id: M1.2
        title: Audit post-MVP ADRs
        kind: docs
        size: S
        status: pending
        directive: ""
        detail: "Quick audit: confirm every major post-MVP change (FastAPI server, Telegram notifications, mcp.server.lowlevel migration, agent_type routing, provider-prefix parsing, auth security fix) has a corresponding ADR. If gaps exist, write retroactive ADRs to capture the 'why' before it's lost to memory."
        accept:
          - grep:
              path: "docs/adr"
              pattern: "README"
```
