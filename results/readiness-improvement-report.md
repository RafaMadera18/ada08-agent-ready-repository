# Readiness Improvement Report

## Summary

| | BEFORE | AFTER |
|---|---:|---:|
| Readiness score | 30 / 100 | 86 / 100 |
| Delta | | +56 |
| Task result (CR-001) | PASS | PASS |
| Clarification questions | 0 | 0 |
| Implicit knowledge items the agent had to infer | 8 | 0 left undocumented (5 also checked by scripts) |

Targets from the exercise: AFTER >= 80 and delta >= +15. Both are met. Details are in `REPOSITORY_READINESS_AUDIT.md`, `results/before-agent-run.md` and `results/after-agent-run.md`.

Honest reading: both runs passed, so the improvements did not change the outcome. They changed how much the agent had to infer, the definition of done it used, and the quality of the evidence it left. See Threats to Validity before drawing stronger conclusions.

## Changes Made

### Improvement I-01

Category: Context
Problem: No agent instruction file. Source-of-truth order, commands, change rules and Definition of Done were absent (IK-01, IK-02, IK-05, IK-06, IK-07).
Change: Added `AGENTS.md` (Read First, Sources of Truth, Standard Commands, Change Rules, Stop Conditions, Definition of Done). It points to the other documents and does not copy their content.
Evidence: `scripts/check_repo_contract.py` fails if a section or the verify command is missing. In the AFTER run the agent read `AGENTS.md` and then the documents it lists, ran `scripts/verify_repo.sh` and reported against the Definition of Done.

### Improvement I-02

Category: Context
Problem: Agent-specific tools need an entry file they actually load. Duplicating rules there would create a second source of truth.
Change: Added `CLAUDE.md` as a thin adapter: follow `AGENTS.md`, make a plan, identify tests. No requirements copied.
Evidence: The AFTER agent read it. It is a dozen lines and holds no rule that is not in `AGENTS.md`.

### Improvement I-03

Category: Navigation
Problem: The agent had to find where code and tests belong by listing the tree (IK-04).
Change: Added `docs/REPO_MAP.md` with entry points, tests, scripts and CI, a change guide and a do-not-edit list.
Evidence: The contract check fails if a path named in `AGENTS.md` or `docs/REPO_MAP.md` does not exist (shown by guardrail demo case 6).

### Improvement I-04

Category: Context (traceability)
Problem: `SPEC.md` mixed requirements with behavior, had no acceptance criteria, and still labelled REQ-003 as pending (IK-02, IK-03, IK-08).
Change: Added `REQUIREMENTS.md` (REQ statements moved verbatim, REQ-003 marked implemented), rewrote `SPEC.md` around acceptance criteria AC-xxx-y mapped to test names, and added `ARCHITECTURE.md` (boundaries, conventions) and `TASKS.md`. No new requirement was invented; criteria describe what the code and the original REQ text already said.
Evidence: The contract check fails if a REQ is defined in one file and missing in the other. In the AFTER run the agent added acceptance criteria for the new function using the existing REQ IDs and did not touch `REQUIREMENTS.md`.

### Improvement I-05

Category: Executable Knowledge
Problem: No single command defined "validated" (IK-01, IK-06).
Change: Added `scripts/verify_repo.sh`: tests, syntax lint, repository contract, protected paths. Standard library only, so no install step.
Evidence: The AFTER agent ran it and reported `VERIFY_REPO: PASS`; the reviewer re-ran it with the same result.

### Improvement I-06

Category: Guardrail
Problem: Nothing stopped an agent from editing requirements, the CI definition or committing secrets (IK-05).
Change: Added `scripts/check_protected_paths.py` (modifying `REQUIREMENTS.md`, `generated/` or `.github/workflows/` fails; staged or unignored `.env`, key files fail), plus `.gitignore` entries for secrets and a `.gitattributes` that fixes line endings, so shell scripts do not break with CRLF (IK-07).
Evidence: `results/evidence/guardrail-demo.txt` runs 8 cases on the improved branch. The 4 violations exit with code 1. The clean tree, a gitignored `.env`, the human-approved override and the restored tree pass.

### Improvement I-07

Category: Guardrail + Test
Problem: Rules about files, links and secrets existed only as intentions.
Change: Added `scripts/check_repo_contract.py` (required files, `AGENTS.md` sections, REQ consistency, documented paths exist, versioned secrets and secret patterns) and `tests/test_repo_contract.py` (13 tests for both checks).
Evidence: 13 tests pass; guardrail demo cases 4, 5 and 6 show the contract check failing on a force-added `.env`, a token-like string and a ghost path.

### Improvement I-08

Category: CI Check
Problem: Validation depended on whoever ran the agent.
Change: Added `.github/workflows/verify.yml`. It runs `bash scripts/verify_repo.sh` and nothing else. On pull requests it compares against the base branch for the protected-path check.
Evidence: After the audit and the AFTER run, the repository was pushed to GitHub and the workflow ran successfully on `main`, `ada08/after` and `ada08/improve` (Actions runs 40979418667, 40979418907 and 40979420758 in `RafaMadera18/ada08-agent-ready-repository`). The scores in the audit were not changed after this, because they were assigned before the first remote run.

### Improvement I-09

Category: Human Gate
Problem: No point where the agent must stop and ask.
Change: Stop Conditions in `AGENTS.md` (conflicting requirements, destructive action, architecture boundary, protected path, unavailable tool) and an explicit override variable, `HUMAN_APPROVED_PROTECTED_CHANGE=1`, that only a human may set. Requirement edits need human approval; adding acceptance criteria for an existing requirement does not.
Evidence: Guardrail demo case 2 shows the failure message that points to the stop conditions; case 7 shows the override path.

One correction made during the work: the first version of the rule said "never create `.env` files", but the check could not see a gitignored local `.env`, which is the desired behavior. The rule now says never commit or force-add them, and demo case 4 checks that.

## Impact Analysis

For the agent: context to understand (`AGENTS.md`, `REQUIREMENTS.md`, `SPEC.md`), discoverability to find things (`docs/REPO_MAP.md`), architecture to limit changes (`ARCHITECTURE.md`), tools to execute (`scripts/verify_repo.sh`), tests and CI to check (27 tests, workflow), guardrails to prevent (two scripts), and evidence to decide (Definition of Done and report format).

For a new human teammate: the same documents answer "where do I start, how do I run it, what may I not touch, when am I done" without asking anyone. The verify command and the CI workflow are the same thing for them as for the agent.

## Threats to Validity

- One run per condition. Language-model runs vary; the same prompt could produce a different path on another run.
- The agent in both runs was a subagent of the same orchestrating session, with a fresh context but not an interactive human-in-the-loop session. A subagent cannot receive answers, so "0 clarification questions" partly reflects that.
- The exact model version of the subagents was not reported back. Both runs used the same `sonnet` alias in the same session.
- The location line in the prompt was needed to point each agent to its working copy (`run-a` / `run-b`). The text is otherwise identical, and a fixed report format was added to both runs.
- The repository is tiny and the task is clearly stated, so a ceiling effect is likely: BEFORE already passed.
- The task, the improvements and the scoring were produced by the same party. Improvements were chosen after seeing the BEFORE run, and some of them (AC-003-4, the discount-before-tax ordering) were written knowing the task. They come from the original REQ-003 text, but a reader should treat that as a bias risk.
- `CLAUDE.md` is loaded by the tool used here. With another coding agent the adapter might not be read, and the effect of `AGENTS.md` could differ.
- Effort numbers (turns, seconds, tokens) were higher in AFTER. They are single observations, not a result.
- The rubric scores are self-assigned. Each one points to observable evidence, but they are not an independent assessment.

## Remaining Gaps

- The workflow only ran for push events. The pull-request path, which compares against the base branch for the protected-path check, has not been exercised.
- "Lint" is a syntax check. No real linter is configured, to avoid adding a dependency without justification.
- Purity of `src/calculator.py` and the AC-to-test mapping are documented but not checked automatically.
- No agent-side hook or permission settings; protected paths are checked after the fact, not before the edit.
- The rules do not say whether `TASKS.md` and `docs/REPO_MAP.md` should be updated by feature work. The AFTER agent did so; that was reasonable, but it is an ambiguity.
- The secret scan only knows a few token formats.

## Reflexión individual (borrador)

Borrador escrito por la IA a partir de la evidencia de este repositorio. Debe ser revisado y reescrito por la persona que entrega el ADA con su propio criterio.

1. **¿Cuál fue el principal obstáculo para el agente en la ejecución BEFORE?** No hubo un bloqueo: el agente terminó con PASS. La fricción fue que tuvo que decidir solo qué documento mandaba (`SPEC.md` decía que REQ-003 estaba pendiente, pero el código ya lo cumplía) y qué significaba "terminado".
2. **¿Qué información tuvo que inferir que un desarrollador experimentado ya conocía?** Las convenciones (`ValueError`, redondeo a 2 decimales, funciones puras), dónde van el código y los tests, qué archivos no debía tocar y que el estado real de REQ-003 era "implementado". Están en `results/implicit-knowledge.md` (8 elementos).
3. **¿Qué mejora produjo el mayor impacto y por qué?** No se puede aislar: todas las mejoras se aplicaron juntas y hay una sola corrida por condición. Lo observable es que el agente AFTER siguió la cadena `AGENTS.md` -> `REPO_MAP` -> `verify_repo.sh`, así que sospecho que `AGENTS.md` más el comando único de verificación fueron las más influyentes, pero es una hipótesis.
4. **¿Qué información pertenece en `AGENTS.md` y cuál NO debería vivir ahí?** Pertenecen el orden de lectura, las fuentes de verdad, los comandos, las reglas de cambio, las condiciones de parada y la Definition of Done. No deben vivir ahí los requisitos, el detalle de la arquitectura ni los criterios de aceptación: solo se enlazan.
5. **¿Qué regla convertiste en software en lugar de dejarla como instrucción?** Las rutas protegidas y los archivos prohibidos (`check_protected_paths.py`), la existencia de documentos y enlaces, la consistencia REQ entre `REQUIREMENTS.md` y `SPEC.md`, y la búsqueda de secretos (`check_repo_contract.py`). Quedan solo como texto las convenciones de código.
6. **¿Qué diferencia observaste entre "más contexto" y "mejor contexto"?** El AFTER leyó 18 archivos contra 6 del BEFORE, así que hubo más contexto, pero el valor vino de que cada archivo tenía un papel único y estaba enlazado desde la entrada, y de que un script lo verifica. Los documentos nuevos son cortos y no se repiten entre sí.
7. **¿Qué riesgo aparece cuando `CLAUDE.md`/`GEMINI.md`/copilot instructions duplican información del proyecto?** Se crea una segunda fuente de verdad que se desactualiza y que puede contradecir a la primera. Por eso `CLAUDE.md` solo dice "sigue `AGENTS.md`".
8. **¿Qué checks comparten ahora el agente, el desarrollador humano y CI?** Los cuatro pasos de `scripts/verify_repo.sh`: tests, chequeo de sintaxis, contrato del repositorio y rutas protegidas. El workflow de GitHub Actions ejecuta ese mismo script y ya corrió con éxito en GitHub para eventos push; falta probar la ruta de pull request.
9. **¿Qué parte del proceso sigue requiriendo decisión humana?** Cambiar o agregar requisitos, tocar rutas protegidas o el CI, cambiar la arquitectura (agregar I/O, dependencias, paquetes), acciones destructivas, y decidir si las reglas ambiguas (por ejemplo, actualizar `TASKS.md`) son aceptables.
10. **¿Qué evidencia demuestra que el AFTER es realmente mejor?** El agente AFTER validó con cinco tipos de verificación (cuatro en un solo comando) contra dos del BEFORE, dejó `SPEC.md`, `TASKS.md` y `REPO_MAP` consistentes con el cambio, y usó el mismo script que usará CI. Los guardrails se demostraron con 8 casos. Es evidencia de menor incertidumbre y mejor trazabilidad, no de mayor éxito: ambos fueron PASS.
11. **¿Qué mejora para el agente también beneficia a un desarrollador que entra por primera vez?** `REPO_MAP`, `AGENTS.md` (comandos y reglas) y `verify_repo.sh`: responden dónde empezar, cómo probar y qué no tocar sin preguntar a nadie.
12. **¿Qué variable no controlada podría afectar la comparación BEFORE/AFTER?** La variabilidad propia del modelo (una sola corrida por condición), que ambos agentes fueran subagentes y no una sesión interactiva, que el modelo exacto no se confirmó, y que yo diseñé tarea, mejoras y puntaje.
13. **¿Qué elementos de este ADA conservarás para tu proyecto final?** La estructura `AGENTS.md` + adaptadores, `REPO_MAP`, un único `verify_repo.sh` compartido con CI, al menos un guardrail ejecutable con pruebas negativas, y el protocolo de baseline congelado con un clon aislado para cada corrida.
