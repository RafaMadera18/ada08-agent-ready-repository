# AFTER Agent Run

## Run Context

Agent: Claude Code subagent (`general-purpose`), fresh context, launched from the same Claude Code session as the BEFORE run. It received the same official prompt, the same report format and a location line that differs only in the directory name. No hints were added.
Model: requested with the `sonnet` alias, same as BEFORE (parent session: Claude Sonnet 5.5, `claude-sonnet-5-5`). The subagent did not report its own model ID, so the exact version is not independently confirmed.
Tools: default subagent toolset, same as BEFORE.
Permissions: session defaults, same as BEFORE.
Baseline commit/tag: `ada08-baseline` (commit `53d91b6`) plus readiness improvements only (branch `ada08/improve`, commit `82a149d`).
Working copy: isolated repository created with `git init` + `git fetch` of `ada08/improve` only, so the BEFORE implementation, the BEFORE results and the audit were not reachable from it.
Run effort (informational only): 7 tool-use turns, about 44 seconds, about 76k tokens.
Captured output: branch `ada08/after` (commit `7d71647`), patch in `results/evidence/after-implementation.patch`.

## Clarification Questions

None. The agent stated that the repository documents were enough and that no stop condition from `AGENTS.md` applied.

## Repository Exploration

Files read (reported by the agent): `TASK_UNDER_TEST.md`, `AGENTS.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `README.md`, `REQUIREMENTS.md`, `SPEC.md`, `TASKS.md`, `.gitignore`, `.gitattributes`, `docs/REPO_MAP.md`, `src/calculator.py`, `tests/test_calculator.py`, `tests/test_repo_contract.py`, `scripts/verify_repo.sh`, `scripts/check_protected_paths.py`, `scripts/check_repo_contract.py`, `.github/workflows/verify.yml`. It also listed the tree and ran `git log` and `git status`.

## Incorrect Assumptions

None reported, and none found when reviewing the diff. The agent noted that the function composes the existing functions, so the discounted subtotal is rounded to 2 decimals before tax is applied, as the existing functions do.

## Failed / Unknown Commands

None failed. A git warning about CRLF/LF line endings appeared, which is harmless.

## Out-of-Scope Changes

None. Verified with `git diff --stat ada08/improve`: `src/calculator.py` (+13), `tests/test_calculator.py` (+35/-1), `SPEC.md` (+15/-1), `TASKS.md` (1 line), `docs/REPO_MAP.md` (1 line). `REQUIREMENTS.md`, `.github/workflows/` and `scripts/` were not touched.

The three documentation files were updated to keep the docs consistent with the change: new acceptance criteria for an existing requirement (allowed by `AGENTS.md`), the function list in the repository map, and the status of CR-001. In BEFORE the agent changed no documentation, and `SPEC.md` stayed stale.

## Validation Evidence

Reported by the agent and re-run independently by the reviewer:

- `python -c "from src.calculator import calculate_order_total as c; print(c([100.0,50.0],10.0,0.16), c([10.5,20.0,5.25]), c([]))"` printed `156.6 35.75 0.0`.
- `bash scripts/verify_repo.sh` ended with `VERIFY_REPO: PASS`: 27 tests OK, syntax lint, `REPO_CONTRACT: PASS`, `PROTECTED_PATHS: PASS` (reviewer re-run: same result).
- `python -m unittest discover tests -v`: 27 tests OK.
- `git status --short` listed only the five files above.

## Final Result

PASS

## Comparison with BEFORE

| Indicator | BEFORE | AFTER |
|---|---|---|
| Clarification questions | 0 | 0 |
| Failed / unknown commands | 0 | 0 |
| Incorrect assumptions | 0 | 0 |
| Out-of-scope files modified | 0 | 0 |
| Validations executed correctly | 2 kinds (unit tests, one-line smoke check) | 5 kinds (unit tests, syntax lint, repository contract, protected paths, smoke check), 4 of them through one shared command |
| Final result | PASS | PASS |
| Qualitative observation | The agent had to infer conventions, resolve a stale `SPEC.md` by itself, and invent its own definition of done. It left docs unchanged. | The agent read the instruction chain in the order given, used the official verify command, followed the stated conventions, and kept the docs consistent with the change. |
| Discoverability | Found the relevant files by listing the tree and reading 6 files. The test command came from `README.md`, the rest was inferred. | Found everything through `AGENTS.md` -> `docs/REPO_MAP.md`. It read 18 files, all of them named in those entry documents. |
| Implicit Knowledge | 8 items in `results/implicit-knowledge.md` that the agent had to infer. | The 8 items are written in `AGENTS.md`, `ARCHITECTURE.md`, `SPEC.md`, `docs/REPO_MAP.md` and `.gitattributes`, and 5 of them are checked by scripts. |
| CI / shared checks | None. | The same `scripts/verify_repo.sh` is run by the agent locally and by `.github/workflows/verify.yml` (workflow not yet executed on GitHub). |

## Reviewer Notes

- Both runs passed. The repository is small and the task is clear, so the outcome could not differ much. The measurable difference is in uncertainty and evidence, as the exercise intends, not in success.
- The AFTER run used more tool turns, time and tokens (7 vs 5, 44 s vs 27 s, 76k vs 62k). Reading the instruction files costs effort. The exercise asks for less uncertainty and better evidence, not for speed, and the sample is a single run per condition, so none of these effort numbers should be treated as a result.
- The AFTER agent reported "8 new tests". The suite grew from 20 to 27, so it added 7. The test names it listed also total 7. This is a small error in the agent's own report, caught by the reviewer's count.
- The AFTER agent updated `TASKS.md` and `docs/REPO_MAP.md`, which `AGENTS.md` neither requires nor forbids. This is an ambiguity in the rules, not a violation. It is listed as a remaining gap in the improvement report.
