# Repository Readiness Audit

Baseline: tag `ada08-baseline` (commit `53d91b6`). Audited before any agent run and before any readiness improvement.

Formula: `weighted = (score / 5) x weight`. Total is out of 100.

## BEFORE

| Dimension | Score 0-5 | Weighted | Evidence | Main Gap |
|---|---:|---:|---|---|
| Entry Point & Navigation | 2 | 6 /15 | `README.md` lists the three main files (`src/calculator.py`, `tests/test_calculator.py`, `SPEC.md`). | No entry-point map, no change guide, no list of places not to touch. The agent must infer where a new function belongs. |
| Agent Instructions | 0 | 0 /15 | No `AGENTS.md`, `CLAUDE.md` or any other agent instruction file exists. | No source-of-truth order, no rules, no Definition of Done, no stop conditions. |
| Build / Run / Test | 3 | 9 /15 | `README.md` documents `python -m unittest discover tests`. The project is stdlib-only, so nothing to install. 7 tests pass on the baseline. | Only the test command is documented. No lint, no single verification command, no Python version stated. `README.md` uses `list[float]` syntax, so Python 3.9+ is implied but not written down. |
| Architecture Boundaries | 1 | 2 /10 | One module with three pure functions. The layout is visible only from the folder names. | No `ARCHITECTURE.md`. Nothing says the module must stay pure, stdlib-only or free of I/O, or where to add new code. |
| Requirements & Traceability | 2 | 4 /10 | `SPEC.md` has REQ-001 to REQ-003 with IDs. | No acceptance criteria, no `REQUIREMENTS.md`, tests are not linked to REQ IDs. REQ-003 is still labelled "Pending / Issue #1" although `apply_discount` is implemented and tested. |
| Automation & Guardrails | 0 | 0 /10 | `.gitignore` only ignores `__pycache__/`, `*.pyc`, `.pytest_cache/`. No script, hook or CI exists. | Every rule is either absent or would be text only. |
| Testability & Evidence | 3 | 9 /15 | 7 unit tests cover valid and invalid inputs for all three functions. | No Definition of Done, no mapping from tests to requirements, no defined place or format for evidence. |
| Safety & Permissions | 0 | 0 /10 | `.gitignore` does not exclude `.env` or key files. Nothing is said about secrets, protected files or destructive actions. | No explicit limits of any kind. |

TOTAL BEFORE: 30 / 100

Top 3 friction points:

1. No agent instruction file and no source-of-truth order. The agent has to decide by itself whether `README.md` or `SPEC.md` rules, and `SPEC.md` is stale (REQ-003 "Pending").
2. No single verification command and no lint. The agent can run the tests but nothing tells it what "done" means.
3. No architecture boundaries, protected paths or stop conditions. Nothing prevents the agent from editing the specification, weakening tests or adding dependencies.
