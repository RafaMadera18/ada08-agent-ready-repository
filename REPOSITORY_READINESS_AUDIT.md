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

## AFTER

Same rubric, dimensions and weights. State audited: branch `ada08/improve` (commit `82a149d`), which is the baseline plus readiness improvements only. The AFTER agent output is on `ada08/after`.

| Dimension | Score 0-5 | Weighted | Evidence | Improvement |
|---|---:|---:|---|---|
| Entry Point & Navigation | 5 | 15 /15 | `AGENTS.md` "Read First" and "Repository Map"; `docs/REPO_MAP.md` with entry points, tests, change guide and do-not-edit list; `README.md` links to both. `check_repo_contract.py` fails if a path in those docs does not exist. The AFTER agent found every file it needed with 0 questions. | I-01, I-03 |
| Agent Instructions | 5 | 15 /15 | `AGENTS.md` has Sources of Truth, Standard Commands, Change Rules, Stop Conditions and Definition of Done. The contract check fails if a section is missing. `CLAUDE.md` is an adapter with no duplicated rules. The AFTER agent followed the Read First order, ran the verify command and stayed within the change rules. | I-01, I-02 |
| Build / Run / Test | 4 | 12 /15 | `./scripts/verify_repo.sh` runs tests, syntax lint, repository contract and protected paths. Python version and no-install are stated. The same script runs in `.github/workflows/verify.yml`. | I-05, I-08 |
| Architecture Boundaries | 4 | 8 /10 | `ARCHITECTURE.md` lists components, dependency direction, purity and error conventions, and what needs human approval. | I-04 |
| Requirements & Traceability | 4 | 8 /10 | `REQUIREMENTS.md` (REQ) -> `SPEC.md` (AC) -> test names. REQ-003 status fixed. The contract check keeps REQ IDs consistent between both files. | I-04 |
| Automation & Guardrails | 4 | 8 /10 | Two deterministic guardrails plus 13 tests for them. `results/evidence/guardrail-demo.txt` shows 8 cases: 4 violations blocked, 4 allowed cases (clean tree, gitignored `.env`, human-approved override, restored tree) passed as designed. | I-06, I-07 |
| Testability & Evidence | 4 | 12 /15 | 27 tests, a Definition of Done, a required report format and acceptance criteria mapped to tests. | I-04, I-05 |
| Safety & Permissions | 4 | 8 /10 | Protected paths, forbidden files, secret-pattern scan, `.gitignore` for secrets, stop conditions, explicit human override variable. | I-06, I-07, I-09 |

TOTAL AFTER: 86 / 100

DELTA: AFTER - BEFORE = 86 - 30 = +56 points

Why not 5 in the remaining dimensions:

- Build / Run / Test: the GitHub Actions workflow has not run on GitHub yet because this repository has no remote. Lint is a syntax check only, there is no real linter.
- Architecture Boundaries: purity of `src/calculator.py` is documented but not checked by a script.
- Requirements & Traceability: the AC-to-test table is maintained by hand and is not verified automatically.
- Automation & Guardrails: no agent-side hook is configured, and CI has not been run remotely.
- Testability & Evidence: no coverage measurement, and the evidence report is written by the person running the process.
- Safety & Permissions: the secret scan only knows a handful of patterns, and no agent permission settings are provided.

Caveat: the same people who made the improvements scored the rubric. The scores rely on the observable evidence listed in each row, but they are not an independent assessment.
