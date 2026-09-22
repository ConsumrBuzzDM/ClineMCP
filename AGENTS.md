# AGENTS.md — Guide for AI Agents Working on ClineMCP

This file gives AI agents (Claude, Gemini CLI, Devin, Cursor, etc.) the
essential context for working on this repo: project layout, commands,
conventions, and behavioral guidelines. Read this before starting work.
See also `C:\Github\Agents\CONVENTIONS.md` for conventions that apply across
all of Robert's repos, and `AGENT_CONTRACT.md` in this repo for the binding
pre-flight contract.

---

## Project

Standalone MCP server for managing Cline CLI sessions as observable,
persistent, self-reporting processes. ClineMCP is a **peer of TOBOR, not a
child** — Cline runs as a subprocess of ClineMCP itself, so sessions survive
TOBOR restarts.

- **Language:** Python 3.12 (`>=3.12,<3.13`)
- **Framework:** FastAPI, `mcp` SDK, `aiosqlite` (session persistence)
- **Package manager:** uv
- **Test framework:** pytest (async), pytest-cov
- **Linter:** ruff (line length 100)
- **Port:** 8003

## Repo layout

```
clinemcp/                  main package
config/                    configuration
docs/adr/                  Architecture Decision Records (read-only, see below)
logs/
scripts/
tests/
sessions.db                SQLite session store
AGENT_CONTRACT.md           binding pre-flight contract (read before changes)
```

## Current state & next steps

The SDD (`docs/sdd/ClineMCP_SDD_v0_1.md`) describes the v0.1 MVP scope;
it's a fixed design spec, not a living tracker. Real growth since has
gone well past "Phase 0" (76 tests now, not the 40 the contract
originally targeted — fixed 2026-09-22) — a FastAPI MCP server,
Telegram notifications, session enrichment, an `mcp.server.lowlevel`
migration, and upstream merges (agent_type routing, a fail-closed auth
security fix). No single doc tracks post-MVP state; `docs/adr/` (read-
only, append-only) is the closest thing to a change log — check there
and `git log` for what's actually landed beyond the SDD's original
scope. `DirectiveQueueMCP` tracks live/queued work in
`docs/directives/`.

## Setup

```bash
uv sync
cp .env.example .env   # fill in required values; .env.local also supported
```

## Commands

```bash
uv run pytest --tb=no -q      # pre-flight — must report 76 passed, 0 failed, 0 skipped
ruff check .
```

**If the pytest count differs from the contract's target, STOP** —
per `AGENT_CONTRACT.md`, do not proceed until investigated.

## Architectural constraints (from AGENT_CONTRACT.md — binding)

- `asyncio.create_subprocess_exec` only — **never** `shell=True`.
- One active Cline session at a time (MVP constraint).
- `--auto-approve true` always.
- Sessions are persisted to SQLite *before* the subprocess starts.
- On startup, any sessions still marked "running" are marked failed
  (crash recovery).
- All ADRs in `docs/adr/` are **read-only** — permanently locked once
  committed. If a design needs to change, write a new ADR rather than
  editing an existing one.

---

## Commit conventions

- **Commit every change** with a descriptive message focused on why, not
  just what.
- **Push to GitHub** after committing — Robert reviews after the fact, not
  gating each push.
- **Do not amend prior commits. Do not force-push.** The git history is an
  audit trail, not a draft — once pushed, it's immutable. Local-only commits
  that haven't been pushed yet may be amended freely.
- **Robert also commits directly himself**, interleaved with agent commits.
  This is expected behavior, not an anomaly. When investigating git history
  anomalies or unexplained intermediate commits, consider that Robert may
  have committed them manually before assuming a hook, parallel session, or
  tooling bug.

## Never trust agent completion summaries

Agent-reported completion is a hypothesis until independently verified
against actual pasted output. A completion report claiming success is not
itself evidence of success. Concretely:

- Every completion report includes real, pasted command output, not
  paraphrased summaries.
- Numbers (test counts, coverage percentages, lint results) are the actual
  tool output, not a restated approximation.
- Check `git status` and `git diff` before committing to verify what
  actually changed.
- Check `git reflog` when verifying a prior session's claimed work, not
  just `git log` — `log` shows the current state of history, but doesn't
  reveal amended/rewritten commits the way `reflog` can.
- Where a finding corrects an earlier assumption, the correction is made
  **in place, marked explicitly** ("SUPERSEDED," "CORRECTED"), not silently
  edited.

## Behavioral guidelines

### Think before coding

- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### Simplicity first

- Minimum code that solves the problem. Nothing speculative.
- No features beyond what was asked. No abstractions for single-use code.
- If you write 200 lines and it could be 50, rewrite it.

### Surgical changes

- Touch only what you must. Don't "improve" adjacent code, comments, or
  formatting. Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.
- Every changed line should trace directly to the user's request.

### Goal-driven execution

- "Fix the bug" → write a test that reproduces it, then make it pass.
- "Refactor X" → ensure tests pass before and after.
- Run `uv run pytest --tb=no -q` before committing. Real test output, not
  paraphrased summaries, is the standard.

## Documentation files

- `README.md` — overview, features, dev setup
- `AGENT_CONTRACT.md` — binding pre-flight contract (test floor,
  architectural constraints)
- `docs/adr/` — Architecture Decision Records (read-only)
- `AGENTS.md` — this file

## Common pitfalls

1. **Using `shell=True` for the Cline subprocess.** Forbidden by
   `AGENT_CONTRACT.md` — always use `asyncio.create_subprocess_exec`.
2. **Starting a second concurrent session.** MVP supports one active
   session only.
3. **Editing an existing ADR.** ADRs in `docs/adr/` are permanent —
   write a new one instead.
