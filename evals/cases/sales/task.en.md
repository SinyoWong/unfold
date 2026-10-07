# Sales after refunds (simulated business exercise)

Request: both sales summary and CSV export must calculate paid amounts minus cumulative refunds; cancelled orders contribute nothing. Current results contain only original amounts. Fix both entry points and keep their business rules consistent.

## Inputs and interfaces

- `app.py` exports `summarize_sales(orders) -> int` and `export_sales_csv(orders) -> str`.
- `orders` is a list of dictionaries, each containing `status`, `amount_cents`, and `refund_cents`. Iterators, databases, HTTP, and file I/O are outside this exercise.
- `status` is `paid` or `cancelled`. Money is integer cents, excluding booleans, decimals, and strings. Require `0 <= refund_cents <= amount_cents`.
- Missing fields, invalid status, or invalid money must raise `ValueError` from both entry points, without a partial total. Validate cancelled orders too.
- CSV contains exactly two rows: header `sales_cents`, then an integer total. Use standard CSV; either newline style is acceptable.
- Empty input totals `0`; fully refunded paid orders contribute `0`. Do not mutate input.

Example: paid `10000`, refunded `2000`, plus paid `5000`, refunded `0`, totals `13000` cents. Any valid cancelled order leaves the total unchanged.

Use only the Python standard library; add no framework or dependency.
