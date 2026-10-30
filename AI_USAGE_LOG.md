# AI Usage Log

I used Claude Code (Claude Sonnet 5.5) for this ADA. I gave it the course PDF and two instructions, "utiliza el ada 06" and "realiza toda la tarea con ese", and it did the audit, the improvements and the runs. Two fresh Claude Code subagents (`general-purpose`, `sonnet` alias) played the BEFORE and AFTER coding agents and did nothing else. I approved publishing the result to GitHub.

## Entry 1: Choosing the repository and freezing the baseline (2026-10-29)

I had two ADA-06 folders. `ada06-github-mcp` has only documents; `ada06-sample-repo` has code, tests and a spec, so Claude used that one. It copied the repo with its history, removed the `origin` remote so nothing could be pushed to the original, and tagged `ada08-baseline`. It later moved the tag to the commit that adds `TASK_UNDER_TEST.md`, because BEFORE and AFTER need the same task.

My decision: I picked ADA-06 and left the rest to Claude.

## Entry 2: Initial audit (BEFORE)

Claude read the baseline files, ran the 7 tests and scored the 8 dimensions: 30/100. It considered a higher score for Build / Run / Test and kept 3, because only the test command was documented. It committed the audit before launching any agent and built the agent's working copy from the baseline tag alone, so the agent could not see the audit.

My decision: none beyond the delegation.

## Entry 3: Task design (CR-001)

Claude proposed `calculate_order_total(prices, discount_percent=0.0, tax_rate=0.0)`. It rejected "implement the discount" because `apply_discount` already existed, even though a stale `SPEC.md` called it pending. It ran the existing functions to confirm the expected value of 156.6 before writing it into the task. The task cites REQ-001 to REQ-003 without restating them.

My decision: I left the task choice to Claude.

## Entry 4: Design of AGENTS.md and the other documents

Claude kept `AGENTS.md` short and linked to other files instead of copying them. It added a thin `CLAUDE.md` adapter because Claude Code loads that file. It left `TASK_UNDER_TEST.md` out of the Read First list, since it belongs to the experiment and not to the project. It did not add a third-party linter (none was installed and it would be a new dependency), so lint is `python -m compileall`, and the docs say so. Agents may add acceptance criteria but not requirements, which lets traceability grow without letting an agent redefine the product.

My decision: I left the design to Claude.

## Entry 5: Turning rules into software

Claude turned "don't change requirements or CI" and "don't commit secrets" into `scripts/check_protected_paths.py` and `scripts/check_repo_contract.py`, wrote 13 tests for them and ran 8 negative cases. The first run exposed a mismatch: a gitignored `.env` went undetected although the rule said "never create `.env`". Claude changed the rule instead of the script. A gitignored local `.env` is the right state, and the real risk is committing it, which case 4 now covers with `git add -f`.

My decision: I left the choice of rules to Claude.

## Entry 6: BEFORE and AFTER executions

Each agent ran in its own repository (`ada08-runs/run-a` and `run-b`) containing only the history that run was allowed to see. Claude checked both outputs itself: it re-ran the tests and `verify_repo.sh`, read the diffs and checked the protected files. Both passed. It caught one error in the AFTER agent's report, which claimed 8 new tests when the suite went from 20 to 27, so 7. The log records the corrected number.

BEFORE read 6 files and chose its own validation. AFTER followed the instruction chain, ran the shared verify command and left `SPEC.md`, `TASKS.md` and `docs/REPO_MAP.md` consistent with the change. It also used more turns and tokens.

My decision: none.

## Entry 7: Discoverability and implicit knowledge

Claude listed 8 things the BEFORE agent had to infer or could not know (`results/implicit-knowledge.md`) and picked a place for each to become explicit. Whatever a script could check became a script. Conventions a script cannot check stayed as documentation.

My decision: none.

## Entry 8: Shared checks and CI

`scripts/verify_repo.sh` is the only definition of "verified", and the GitHub Actions workflow calls it with no logic of its own. The working copy had no remote, so the workflow could not run at first. After I agreed, Claude created the public repository `RafaMadera18/ada08-agent-ready-repository` and pushed `main` (the final branch), `ada08/before`, `ada08/after`, `ada08/improve` and the tag. The workflow passed on every branch that contains it.

My decision: I approved publishing, chose a public repository and asked for the evidence branches to be included.

## Entry 9: Final evaluation and remaining human work

Claude scored AFTER at 86/100 (+56). The improvements and the score came from the same author, and the report says so. Still open: no real linter, no automatic check that each acceptance criterion has a test, no agent hooks, no rule on whether feature work should update `TASKS.md` and `docs/REPO_MAP.md`, a workflow whose pull-request path is untested, and one run per condition. Claude also wrote a first draft of the reflection answers in the improvement report, and I asked it to rewrite that draft and this log in plainer language.

My decision: I asked for the rewrite.
