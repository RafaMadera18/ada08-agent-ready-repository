# Specification

Verifiable behavior for each requirement in `REQUIREMENTS.md`. Acceptance criteria are named AC-<requirement number>-<n>. Each one maps to an automated test.

Adding acceptance criteria for an existing REQ is allowed. Adding or editing a REQ needs human approval.

## REQ-001: Subtotal Calculation

Function: `calculate_subtotal(prices: list[float]) -> float`

| ID | Criterion | Test |
|---|---|---|
| AC-001-1 | Returns the sum of the prices rounded to 2 decimals. `[10.5, 20.0, 5.25]` returns `35.75`. | `test_calculate_subtotal_valid` |
| AC-001-2 | An empty list returns `0.0`. | `test_calculate_subtotal_valid` |
| AC-001-3 | Any negative price raises `ValueError`. | `test_calculate_subtotal_negative` |

## REQ-002: Tax Application

Function: `apply_tax(amount: float, tax_rate: float) -> float`

| ID | Criterion | Test |
|---|---|---|
| AC-002-1 | Returns `amount * (1 + tax_rate)` rounded to 2 decimals. `apply_tax(100.0, 0.16)` returns `116.0`. | `test_apply_tax_valid` |
| AC-002-2 | A negative amount raises `ValueError`. | `test_apply_tax_negative_amount` |
| AC-002-3 | A negative tax rate raises `ValueError`. | `test_apply_tax_negative_rate` |

## REQ-003: Percentage Discount

Function: `apply_discount(subtotal: float, discount_percent: float) -> float`

| ID | Criterion | Test |
|---|---|---|
| AC-003-1 | Returns `subtotal * (1 - discount_percent / 100)` rounded to 2 decimals. `(100.0, 10.0)` returns `90.0`, `(100.0, 0.0)` returns `100.0`, `(100.0, 100.0)` returns `0.0`. | `test_apply_discount_valid` |
| AC-003-2 | A discount below 0 or above 100 raises `ValueError`. | `test_apply_discount_invalid` |
| AC-003-3 | A negative subtotal raises `ValueError`. | `test_apply_discount_invalid` |
| AC-003-4 | When a discount and a tax rate are both applied, the discount is applied first and the tax is calculated on the discounted amount (from "before tax calculation" in REQ-003). | not covered by a test |

## Conventions that apply to every criterion

- Invalid input raises `ValueError`.
- Returned amounts are rounded to 2 decimals.
- See `ARCHITECTURE.md` for module boundaries.
