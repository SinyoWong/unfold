# Business acceptance and handoff exercises

[中文](README.md) · [Project](../README.en.md)

These are **simulated business exercises using the Python standard library**, not production case studies. Python 3.10+ is required; no packages are needed. The external checker validates business behavior and does not automatically score understandability.

These are the first version's core business checks and handoff exercises. Using the Skills does not require running them; check the relevant samples when changing them. For understanding and collaboration, report what was unclear, which decisions lacked evidence, and whether you could locate the next change in a real task. No rating form is required first.

## Check the exercises

Run from the repository root:

```powershell
python -X utf8 evals/check.py --selftest
```

Expect `PASS selftest: 8 fixture outcomes verified`: three incomplete starters fail, three references pass, and two intentionally faulty review samples fail. `PASS ... expected failure detected` means the checker caught the specified defect, not that the faulty application passed acceptance. Runner checks also verify that missing exercises fail and different workspaces can import same-name sibling modules without sharing cached modules.

| Case | Coding task | Reference | Faulty review sample |
| --- | --- | --- | --- |
| `status` | [Status label](cases/status/task.en.md) | Change only the `pending` label | None |
| `sales` | [Sales after refunds](cases/sales/task.en.md) | Summary and CSV share the refund rule | Correct summary; CSV ignores refunds |
| `permissions` | [Department detail](cases/permissions/task.en.md) | List and detail share permissions | Correct list; detail bypasses permissions |

Each `starter/app.py` is the initial code. `reference/app.py` is evaluator-only; `review-bad/app.py` contains the known defect. References demonstrate a plain implementation; candidates need not match them line by line.

## Coding exercise

1. Create a fresh temporary workspace containing only the selected `starter/app.py` and `task.md` (or `task.en.md`). Do not copy references, review samples, this checker, or the whole unfold repository into the executing agent's workspace.
2. Copy the Skills using the [installation instructions](../README.en.md#install-and-use), then send the original task in a new session. Preserve the request, process, and delivery. Do not change requirements to accommodate results.
3. After execution, run acceptance externally. For example:

```powershell
python -X utf8 evals/check.py --case sales --workspace C:\Temp\unfold-sales
```

4. Save the exit code and complete output: `0` means success; `1` means acceptance failure or runtime error. Preserve candidate-authored checks too, but do not substitute them for external acceptance.

`--case` accepts `status`, `sales`, `permissions`, or `sales-handoff`. `--workspace` points to the directory containing `app.py`, which may import sibling helper modules. Each command and every selftest sample runs in a separate process to avoid cached modules leaking across workspaces. The checker executes candidate code; use it only with your own exercise workspaces. It is not a security sandbox for hostile code.

Coverage includes unchanged labels; refunds with empty input, full refunds, cancelled orders, missing fields, invalid types, negative or excessive refunds, large integers, and multiple seeded datasets; permissions across roles, missing departments, cross-department filters, details, missing records, and unchanged inputs. Inspect code and delivery notes manually to assess centralized rules and accurate explanations.

## Review and handoff

- Review separate workspaces containing correct and faulty `sales` and `permissions` versions. Supply requirements and request review only. Save and compare SHA-256 content fingerprints for all reviewed files before and after to verify no modification.
- Faulty samples must produce findings tied to the real omission and impact. Correct versions should not trigger false business defects. Findings need location, impact, evidence, and minimal remedy; uncertain issues must be labeled for confirmation.
- Handoff uses the **actual coding run's output and delivery note** in a new independent session, with [Separate amounts and refunds](cases/sales/handoff-task.en.md). Do not present a reference solution as a prior agent's output.
- Run `--case sales-handoff` afterwards. Record whether the agent located the rule before editing, clarification count, actual changes, and acceptance results. Report missing delivery notes, lack of session independence, and failures honestly.
- This version provides an agent handoff exercise method; independent code changes by humans and long-term maintenance are **not yet evaluated**.

## Records and feedback

For an ordinary trial, keep the task, actual changes, delivery note, check output, and anything confusing. Include the date, model, client, and rule version when sharing; mark unavailable information as unknown. Store actual runs in the local ignored `results/` directory and teaching material in `../examples/`. Never present examples or reference answers as measured runs, and do not submit private conversations or credentials.

Verify business requirements and key boundaries first, then assess whether you can understand, judge, and continue the work. Passing tests does not establish more accurate understanding, and shorter code cannot offset business failure. For native usage, follow the [trigger and removal checklist](trigger-prompts.md#english), recording actual Skill reads and behavior. Unrun scenarios remain unverified.
