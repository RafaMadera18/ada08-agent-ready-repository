# Requirements

Single source of truth for what the Calculator Service must do. Verifiable behavior for each requirement is in `SPEC.md`.

Changing or adding a requirement needs human approval.

## REQ-001: Subtotal Calculation

The service must sum a list of numerical item prices. If the list is empty, the subtotal is 0.0. Negative prices must raise a `ValueError`.

Status: Implemented (`calculate_subtotal`).

## REQ-002: Tax Application

The service must apply a tax percentage rate (e.g. 0.16 for 16%) to an amount. Negative amounts or tax rates must raise a `ValueError`.

Status: Implemented (`apply_tax`).

## REQ-003: Percentage Discount

The service must support applying a discount percentage (between 0% and 100%) to a subtotal before tax calculation.

Status: Implemented (`apply_discount`). It was tracked as GitHub Issue #1 and is no longer pending.
