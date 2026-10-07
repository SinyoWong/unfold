# Handoff: separate amounts and refunds (simulated business exercise)

Using the completed sales fix and the previous developer's delivery note, report original amounts and refunds separately. The independent session must not see the reference implementation first.

- `summarize_sales(orders)` now returns a dictionary with exactly two keys: `amount_cents` totals original paid amounts; `refund_cents` totals cumulative refunds on paid orders.
- `export_sales_csv(orders)` now returns header `amount_cents,refund_cents` followed by one totals row, in that order.
- The two sample orders `10000/2000` and `5000/0` return `{"amount_cents": 15000, "refund_cents": 2000}`. Empty input returns two zeros.
- Cancelled orders contribute to neither column. Preserve all original input validation, reject invalid orders from both entry points, and do not mutate inputs.
- Before editing, identify the edit location found in the previous delivery note. Afterwards, explain actual changes and validation results.

The evaluator records whether the edit location was found, clarification count, and business checks. This is an agent handoff exercise, not a substitute for testing with a human.
