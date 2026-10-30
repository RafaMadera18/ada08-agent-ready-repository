# Repository Map

Answers "where is what I need?". Rules live in `AGENTS.md`.

## Entry Points

- `src/calculator.py` - the whole service: `calculate_subtotal`, `apply_discount`, `apply_tax`, `calculate_order_total`. There is no executable entry point; callers import these functions.

## Tests

- `tests/test_calculator.py` - tests for `src/calculator.py`.
- `tests/test_repo_contract.py` - tests for the repository checks in `scripts/`.

## Requirements and Docs

- `REQUIREMENTS.md` - requirements (REQ-xxx).
- `SPEC.md` - acceptance criteria (AC-xxx-y) and the test that covers each one.
- `ARCHITECTURE.md` - boundaries and conventions.
- `TASKS.md` - work items.
- `TASK_UNDER_TEST.md` - the change request currently being measured.

## Scripts and CI

- `scripts/verify_repo.sh` - single verification command.
- `scripts/check_repo_contract.py` - required files, traceability, doc paths, secret patterns.
- `scripts/check_protected_paths.py` - blocks edits to protected paths and forbidden files.
- `.github/workflows/verify.yml` - CI; runs `scripts/verify_repo.sh`.

## Change Guide

If adding or changing calculation behavior:

1. Check `REQUIREMENTS.md` and `SPEC.md` for the REQ and AC that apply.
2. Change `src/calculator.py`. Keep it pure and stdlib-only.
3. Add or update tests in `tests/test_calculator.py`.
4. Add acceptance criteria to `SPEC.md` if the behavior is new (for an existing REQ only).
5. Run `./scripts/verify_repo.sh`.

## Do Not Edit Directly

- `REQUIREMENTS.md` (human approval)
- `generated/` (if it ever exists)
- `.github/workflows/` (human approval)
- `.env`, key files, credentials
- `results/` (evidence, written by the ADA-08 process, not by feature work)
