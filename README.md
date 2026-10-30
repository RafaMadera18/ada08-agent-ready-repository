# Calculator Service

A lightweight Python service to calculate order subtotals, discounts, and taxes.

## Structure
- `src/calculator.py`: Core calculation functions.
- `tests/test_calculator.py`: Unit test suite.
- `SPEC.md`: Acceptance criteria for each requirement.
- `REQUIREMENTS.md`: Requirements.

## Running Tests
```bash
python -m unittest discover tests
```

## Verifying a Change
```bash
./scripts/verify_repo.sh
```
This is the same command CI runs. See `AGENTS.md` for the full contract for coding agents and `docs/REPO_MAP.md` for a map of the repository.
