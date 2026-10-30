# AI Usage Log

Tools: Claude Code (Claude Sonnet 5.5) as the orchestrating assistant, and two fresh Claude Code subagents (`general-purpose`, `sonnet` alias) used only as the BEFORE and AFTER coding agents.

How to read the "Human decision" lines: the student gave two instructions, "utiliza el ada 06" (use ADA-06 as the base repository) and "realiza toda la tarea con ese" (carry out the whole task with it). Everything else was decided by the assistant. A line-by-line human review of the deliverable has not happened at the time of writing. Each entry lists what the student should check.

## Entry 1 - Choosing the repository and freezing the baseline (2026-10-29)

AI contribution: Found two ADA-06 folders. `ada06-github-mcp` contains only documents; `ada06-sample-repo` has code, tests and a spec. Proposed and used `ada06-sample-repo`. Copied it with its history, removed the `origin` remote so nothing can be pushed to the original, and created the tag `ada08-baseline`. Later moved the tag to the commit that adds `TASK_UNDER_TEST.md`, because the task must be identical in BEFORE and AFTER.
Human decision: Student chose ADA-06 and delegated the rest. Not reviewed: which of the two folders to use, and moving the tag.
To verify: `git log --oneline --decorate` shows the tag on `53d91b6`; the original `ada06-sample-repo` is unchanged.

## Entry 2 - Initial audit (BEFORE)

AI contribution: Read the baseline files, ran the 7 tests, and scored the 8 dimensions: 30/100. Rejected a more generous score for Build / Run / Test because only the test command was documented; kept 3. Committed the audit before launching any agent, and created the agent's working copy from the baseline tag only, so the audit was not reachable from it.
Human decision: None yet beyond delegation.
To verify: the scores in `REPOSITORY_READINESS_AUDIT.md` against the evidence column; that the audit commit `c587533` precedes the BEFORE run.

## Entry 3 - Task design (CR-001)

AI contribution: Proposed `calculate_order_total(prices, discount_percent=0.0, tax_rate=0.0)`. Rejected "implement the discount" as the task because `apply_discount` already exists (a stale `SPEC.md` said otherwise). Checked the expected value 156.6 by running the existing functions before writing it into the task. The task cites REQ-001..003 and does not restate them.
Human decision: Delegated.
To verify: that this task is a fair test (small, non-trivial, verifiable) and that the stated expected values are correct.

## Entry 4 - Design of AGENTS.md and the other documents

AI contribution: Wrote `AGENTS.md` short, with links and no copied requirements. Accepted a thin `CLAUDE.md` adapter because Claude Code loads that file. Rejected putting `TASK_UNDER_TEST.md` in the Read First list, because it is an experiment artifact and not a project document. Rejected a third-party linter (not installed, would add a dependency); used `python -m compileall` as a syntax check and said so. Allowed agents to add acceptance criteria but not requirements, so traceability can grow without letting the agent redefine what the product must do.
Human decision: Delegated.
To verify: that the rules in `AGENTS.md` match what the student wants agents to be allowed to do, especially editing `SPEC.md`.

## Entry 5 - Turning rules into software (guardrail)

AI contribution: Converted "do not change requirements or CI" and "do not commit secrets" into `scripts/check_protected_paths.py` and `scripts/check_repo_contract.py`, with 13 tests, and ran 8 negative cases. The demo exposed a mismatch: a gitignored `.env` was not detected, although the rule text said "never create `.env`". The assistant changed the rule text, not the script, because a gitignored local `.env` is the desired state and the real risk is committing it; case 4 now covers `git add -f`.
Human decision: Delegated.
To verify: `results/evidence/guardrail-demo.txt`; whether the student agrees with the choice of protected paths.

## Entry 6 - BEFORE and AFTER executions

AI contribution: Ran each agent as a fresh subagent in its own isolated repository (`ada08-runs/run-a` and `run-b`) holding only the history the run was allowed to see. Reviewed both outputs independently: re-ran tests and `verify_repo.sh`, checked diffs and the protected files. Both passed. The assistant caught one inaccuracy in the AFTER agent's own report (it said 8 new tests; the suite grew from 20 to 27, so 7) and recorded it instead of repeating the claim.
What changed in agent behavior: BEFORE read 6 files and chose its own validation. AFTER followed the instruction chain, ran the shared verify command, and kept `SPEC.md`, `TASKS.md` and `docs/REPO_MAP.md` consistent. AFTER used more turns and tokens.
Human decision: None.
To verify: the two result files and the two patches in `results/evidence/`.

## Entry 7 - Discoverability and implicit knowledge

AI contribution: Listed 8 items the BEFORE agent had to infer or could not know (`results/implicit-knowledge.md`) and gave each a place where it should become explicit. Kept the rule from the exercise: where a rule can be checked deterministically it became a script; conventions that cannot are documented only.
Human decision: None.
To verify: that each IK item maps to an improvement in the report.

## Entry 8 - Shared checks and CI

AI contribution: Made `scripts/verify_repo.sh` the only definition of "verified" and made the GitHub Actions workflow call it, with no duplicated logic. The working copy had no remote, so the workflow could not run at first. After the student agreed, the assistant created the public repository `RafaMadera18/ada08-agent-ready-repository`, pushed `main` (the final branch), `ada08/before`, `ada08/after`, `ada08/improve` and the tag, and the workflow passed on all three branches that contain it.
Human decision: The student approved publishing and chose a public repository with the evidence branches included.
To verify: the three passing runs in the Actions tab; open a pull request to exercise the base-branch comparison, which has not run yet.

## Entry 9 - Final evaluation and remaining human work

AI contribution: Scored AFTER at 86/100 (+56), with a caveat that the improvements and the score come from the same author, and listed what still needs a human: no real linter, no automatic AC-to-test check, no agent hooks, an unclear rule about updating `TASKS.md` and `docs/REPO_MAP.md`, the untested pull-request path of the workflow, and the single run per condition. The reflection answers in the improvement report are a draft for the student to rewrite.
Human decision: Pending.
To verify: whether to accept 86/100 or lower some rows; and replace the draft reflection with the student's own.
