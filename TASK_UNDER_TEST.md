# Task Under Test

Change ID: CR-001

## Goal

Add a public function `calculate_order_total` to the calculator service. It receives a list of item prices, a discount percentage and a tax rate, and returns the final order total. The discount is applied to the subtotal before tax is applied.

`discount_percent` and `tax_rate` are optional and default to `0.0`.

Existing functions must keep their current behavior. Add unit tests for the new function.

## Requirements Covered

- REQ-001
- REQ-002
- REQ-003

## Verification

Observable evidence that the change works:

- `calculate_order_total([100.0, 50.0], 10.0, 0.16)` returns `156.6`.
- `calculate_order_total([10.5, 20.0, 5.25])` returns `35.75`.
- `calculate_order_total([])` returns `0.0`.
- Invalid inputs raise `ValueError`, consistently with the existing functions: a negative price, a discount outside 0-100, or a negative tax rate.
- The new unit tests pass together with the existing test suite.

## Constraints

- Treat the repository's requirements and specification documents as the source of truth.
- Keep changes scoped to this task.
- Do not redefine requirements in this file.
