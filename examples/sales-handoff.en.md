# From a refund fix to the next requirement: a maintenance handoff example

[中文](sales-handoff.md) · [Back to project](../README.en.md)

This is a **simulated business teaching example**. Two runnable implementations show how to centralize refund rules, verify both entry points, and explain where to make the next change. Amounts use integer cents.

## First change: deduct refunds at both entry points

In the original code, direct summaries and CSV exports shared `summarize_sales`, but it summed only original amounts. Both outputs were therefore too high. The task required paid orders to contribute their original amount minus refunds, with cancelled orders excluded. Invalid inputs could not silently become zero or a partial total.

```text
Before: direct summary / CSV export -> summarize_sales -> sum original amounts only -> 15000
After:  direct summary / CSV export -> summarize_sales -> validate input and deduct refunds -> 13000
```

Fix the rule in the same calculation function and add a directly runnable check file, without new classes or dependencies. See the [net-amount code](sales/net/app.py) and [check file](sales/net/test_sales.py).

The delivery note can identify `summarize_sales` as the place to change future sales rules and `test_sales.py` as the corresponding check. That sentence gives the next maintainer a concrete starting point.

## Second change: use the handoff to separate original amounts and refunds

The next maintainer starts with the code, checks, and delivery note. The new requirement changes the return value and export format: the summary must return two amount fields, and CSV must contain two columns with those names. Existing input checks must remain intact.

```text
Before: summarize_sales -> net amount 13000 -> one sales_cents column
After:  summarize_sales -> original amount 15000, refunds 2000 -> two CSV columns
```

Start this change at `summarize_sales` and update the summary, CSV, and corresponding checks together. See the [separate-column code](sales/separate/app.py) and [checks](sales/separate/test_sales.py).

Check both implementations from the repository root:

```powershell
python -B -X utf8 examples/sales/net/test_sales.py
python -B -X utf8 examples/sales/separate/test_sales.py
python -B -X utf8 evals/check.py --case sales --workspace examples/sales/net
python -B -X utf8 evals/check.py --case sales-handoff --workspace examples/sales/separate
```

## What this demonstrates

This example demonstrates a shared rule location, runnable checks, and an explicit next-change location. It is teaching material you can run yourself, not a report measuring collaboration outcomes. Independent maintenance by humans has not been evaluated.

To change this exercise's business rules later, update the [task requirements](../evals/cases/sales/task.en.md) and [independent acceptance checks](../evals/check.py) first. Then adjust the implementation and run the corresponding checks.
