# ClineMCP — Fix AGENT_CONTRACT.md's Stale Test-Floor Gate

*September 2026 | Read fully before executing anything.*

---

> STOP: `uv run pytest --tb=no -q` — verify the real count yourself
> before touching anything (verified 2026-09-22: **76 passed**, not
> the 40 `AGENT_CONTRACT.md` currently mandates).
>
> **This mismatch is expected — it's the exact thing this directive
> exists to fix, not a reason to halt.** `AGENT_CONTRACT.md`'s own
> pre-flight section says "if count differs: STOP," which — read
> literally, on its own, before you've seen this directive — would
> tell you to abort here. Don't. That instruction is itself the stale
> thing being corrected. Proceed with the fix in §1.

---

## §0 Context

`AGENT_CONTRACT.md`'s "Pre-flight (MANDATORY)" section states, in
binding language every agent session is told to follow literally:

> `uv run pytest --tb=no -q`
> Must report: 40 passed, 0 failed, 0 skipped (Phase 0 target)
> **If count differs: STOP.**

`AGENTS.md`'s Commands section repeats the same "40 passed" figure.
The real current count, run directly, is **76 passed** — the contract
was never updated as the project grew past its "Phase 0" baseline
(git log shows substantial work since: FastAPI MCP server, Telegram
notifications, session enrichment, an `mcp.server.lowlevel` migration,
upstream merges for agent_type routing and a security fix). Taken
literally, this contract tells every future agent session to halt on
its very first mandated command, because 76 ≠ 40.

This is a documentation-drift bug, not a code bug — nothing about the
test suite itself needs to change.

## 1. Scope

1. **`AGENT_CONTRACT.md`**: update "Must report: 40 passed, 0 failed,
   0 skipped (Phase 0 target)" to the real, current count (re-verify
   at execution time — do not just copy 76 from this directive, in
   case more work has landed since it was written).
2. **`AGENTS.md`**: same fix in the Commands section's comment.
3. Check whether any other doc in the repo cites the stale "40" figure
   (`grep -rn "40 passed" .` from the repo root, excluding `.venv`)
   and fix any you find, same way.

## 2. What NOT to do

- Do not touch any file under `docs/adr/` — permanently locked per
  `AGENT_CONTRACT.md`'s own rule, and this isn't an architectural
  decision, just a stale number.
- Do not change what the pre-flight check verifies (still "0 failed,
  0 skipped," still run before every session) — only the expected
  count.
- Do not investigate or "fix" why the count grew — that's just the
  project's real history; this directive corrects the documentation
  to match reality, not the other way around.

## 3. Completion Criteria

- [ ] `AGENT_CONTRACT.md` and `AGENTS.md` both state the real, freshly-verified pass count
- [ ] `grep -rn "40 passed"` (or whatever the old figure was) returns nothing left uncorrected
- [ ] `docs/adr/` untouched
- [ ] Committed: `docs: fix stale test-floor count in AGENT_CONTRACT.md/AGENTS.md`

## 4. Quick Reference

| Key | Value |
|---|---|
| Status | Draft |
| Assigned to | devin |
| Test baseline | 76 passed (2026-09-22) — re-verify, don't trust this number blindly |
| Do not touch | `docs/adr/` (read-only) |
| Branch | - |
| Commit | `docs: fix stale test-floor count in AGENT_CONTRACT.md/AGENTS.md` |

*ClineMCP Directive | September 2026*

<!-- queue:start -->
## Queue

| Field | Value |
|---|---|
| Status | Draft |
| Assigned to | devin |
| Branch | - |
| Base branch | main |

**Status log**
- 2026-09-22 · robert-claude · none → Draft — AGENT_CONTRACT.md's mandatory pre-flight gate says "40 passed... if count differs: STOP" but the real count (verified directly) is 76 passed. Every future agent session following the contract literally would halt on its first command.
<!-- queue:end -->
