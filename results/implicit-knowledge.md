# Implicit Knowledge Found

Source: BEFORE run (`results/before-agent-run.md`) and the BEFORE audit.

## IK-01

What: The test command is `python -m unittest discover tests`, and it only works from the repository root.

How was it discovered: By reading `README.md`. It is the only place that states it.

Should this remain implicit? NO

Where should it become explicit? `AGENTS.md` (Standard Commands) and `scripts/verify_repo.sh`.

Remediation: AGENTS.md + single verification script.

## IK-02

What: `SPEC.md` is stale. REQ-003 is labelled "Pending / Issue #1" although `apply_discount` is implemented and tested.

How was it discovered: By comparing `SPEC.md` with `src/calculator.py` and `git log`. The agent resolved the conflict on its own.

Risk: An agent that trusts the document would reimplement `apply_discount`, or treat REQ-003 as open work and change behavior that is already correct.

Should this remain implicit? NO

Where should it become explicit? `REQUIREMENTS.md` (status per requirement), `SPEC.md` (acceptance criteria) and the source-of-truth order in `AGENTS.md`.

Remediation: Requirements and traceability cleanup + contract check that every REQ in `SPEC.md` exists in `REQUIREMENTS.md`.

## IK-03

What: Project conventions: invalid input raises `ValueError` with a descriptive message, money values are rounded to 2 decimals, public functions are pure and use only the standard library.

How was it discovered: By reading `src/calculator.py` and inferring the pattern from three functions. Not documented anywhere.

Risk: A different agent could return `None` or a custom exception, skip rounding, or add a dependency.

Should this remain implicit? NO

Where should it become explicit? `ARCHITECTURE.md` (boundaries and conventions) and `SPEC.md` (acceptance criteria).

Remediation: ARCHITECTURE.md + acceptance criteria.

## IK-04

What: Where new code and tests belong: functions in `src/calculator.py`, tests in `tests/test_calculator.py` using `unittest`.

How was it discovered: By listing the tree and reading the existing files.

Should this remain implicit? NO

Where should it become explicit? `docs/REPO_MAP.md` (Change Guide).

Remediation: REPO_MAP.md.

## IK-05

What: What the agent may and may not edit. The agent chose by itself to leave `SPEC.md` and `README.md` alone.

How was it discovered: Not documented. The agent used the constraint in `TASK_UNDER_TEST.md` ("do not redefine requirements") as the only guide.

Risk: The agent could modify requirements to make a test pass, weaken existing tests, add dependencies, or create `.env` files. Nothing detects it.

Should this remain implicit? NO

Where should it become explicit? `AGENTS.md` (Change Rules, Stop Conditions) and a deterministic protected-path check.

Remediation: AGENTS.md + `scripts/check_protected_paths.py`.

## IK-06

What: What "done" means. There is no lint, no single verification command, no Definition of Done and no rule about the final report.

How was it discovered: Not documented. The agent chose its own validation (unit tests plus a one-line smoke command).

Should this remain implicit? NO

Where should it become explicit? `AGENTS.md` (Definition of Done) and `scripts/verify_repo.sh`, executed by the same command in CI.

Remediation: verify_repo.sh + GitHub Actions workflow that calls it.

## IK-07

What: Environment facts: Python 3.9+ is required (`list[float]` annotations), the project has no dependencies, and Git on Windows rewrites line endings (the agent saw the "LF will be replaced by CRLF" warning).

How was it discovered: By inference and by a git warning. Not documented, and there is no `.gitattributes`.

Should this remain implicit? NO

Where should it become explicit? `AGENTS.md` (Standard Commands) and `.gitattributes`.

Remediation: AGENTS.md + `.gitattributes`. The line-ending rule also protects shell scripts from CRLF breakage.

## IK-08

What: The discount-before-tax ordering lives only in the prose of REQ-003.

How was it discovered: By reading `SPEC.md`. The task description repeated it, so the agent did not need to guess in this run.

Risk: For a task that did not restate the ordering, the agent would have to infer it.

Should this remain implicit? NO

Where should it become explicit? `SPEC.md` as a verifiable acceptance criterion that references REQ-003.

Remediation: acceptance criterion AC-003-4.
