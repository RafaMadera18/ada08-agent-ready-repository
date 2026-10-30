# AGENTS.md

Operating contract for coding agents and humans working in this repository. Tool-specific files such as `CLAUDE.md` only point here.

## Read First

1. `REQUIREMENTS.md` - what the service must do (REQ-xxx).
2. `SPEC.md` - verifiable behavior and acceptance criteria (AC-xxx-y).
3. `ARCHITECTURE.md` - module boundaries and conventions.
4. `TASKS.md` - finished and planned work.
5. `docs/REPO_MAP.md` - where things live and what not to edit.

## Sources of Truth

- Requirements live only in `REQUIREMENTS.md`.
- Verifiable behavior and acceptance criteria live only in `SPEC.md`.
- Boundaries and conventions live only in `ARCHITECTURE.md`.
- `README.md` is an overview. If it disagrees with the files above, the files above win.
- Do not change requirements or the spec merely to make tests pass.

## Repository Map

- `src/` - implementation (`src/calculator.py`).
- `tests/` - automated tests (`unittest`).
- `docs/` - navigation (`docs/REPO_MAP.md`).
- `scripts/` - deterministic checks.
- `results/` - generated evidence, not source.

## Standard Commands

Run everything from the repository root. Python 3.9 or newer, standard library only.

- Install: nothing to install.
- Run: this is a library with no executable entry point. Import from `src.calculator`.
- Test: `python -m unittest discover tests`
- Lint: `python -m compileall -q src tests scripts` (syntax check; no linter is configured).
- Verify: `./scripts/verify_repo.sh`

`./scripts/verify_repo.sh` runs the test, lint, repository-contract and protected-path checks. On Windows use Git Bash. If bash is unavailable, run the same four steps by hand; the script lists them.

## Change Rules

- Keep changes scoped to the requested task.
- Follow the conventions in `ARCHITECTURE.md`: pure functions in `src/calculator.py`, `ValueError` for invalid input, money rounded to 2 decimals.
- Add tests for new behavior in `tests/test_calculator.py`, in the same `unittest` style. Do not weaken or delete existing tests.
- Do not add dependencies without justification.
- You may add acceptance criteria (AC-xxx-y) to `SPEC.md` for an existing REQ-xxx. Adding or editing a REQ-xxx needs human approval.
- Do not modify protected paths: `REQUIREMENTS.md`, `generated/`, `.github/workflows/`.
- Never create or commit `.env` files, keys or credentials.
- `scripts/check_protected_paths.py` enforces the two rules above. Only a human may set `HUMAN_APPROVED_PROTECTED_CHANGE=1`.

## Stop Conditions

Stop and ask for human input when:

- requirements or the spec conflict with each other or with the code,
- a destructive action is required,
- an architecture boundary in `ARCHITECTURE.md` must change,
- a protected path must change,
- a required tool or external system is unavailable.

## Definition of Done

- `./scripts/verify_repo.sh` ends with `VERIFY_REPO: PASS`.
- New behavior has unit tests and the existing tests still pass unchanged.
- Only files related to the task were modified.
- The final report lists the files modified, the commands executed with their result, the evidence that the requested behavior works, and any assumption made.
