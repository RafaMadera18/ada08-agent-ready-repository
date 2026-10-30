# Architecture

## Components

| Component | Responsibility | Depends on |
|---|---|---|
| `src/calculator.py` | Business rules: subtotal, discount, tax. Pure functions. | Python standard library only |
| `tests/` | Automated tests with `unittest`. | `src/` |
| `scripts/` | Deterministic repository checks used by humans, agents and CI. | Python standard library, `git` |
| `docs/` | Navigation and operational context. | none |

Dependency direction: `tests` -> `src`. `src` imports nothing from `tests`, `scripts` or `docs`.

## Boundaries

- `src/calculator.py` is a pure module: no I/O, no global state, no third-party imports.
- Public functions take numbers and return numbers rounded to 2 decimals.
- Invalid input raises `ValueError` with a descriptive message. Never return `None` or a sentinel value.
- New business functions go in `src/calculator.py` and are tested in `tests/test_calculator.py`.

## Where NOT to change without human approval

- Adding I/O, a network call, persistence, a CLI or an API. That changes the architecture.
- Splitting `src/calculator.py` into packages.
- Adding third-party dependencies.
- Anything listed as protected in `AGENTS.md`.

## Verification

`./scripts/verify_repo.sh` is the single verification contract. Humans, agents and CI all run it.
