# unfold

[中文](README.md)

**Let AI think deeply, write straightforward code, and explain how it works.**

AI-generated code can implement a feature while leaving its developer surrounded by abstractions and terminology they cannot comfortably change. unfold provides working instructions for AI (Skills) to help ordinary developers understand implementations, judge results, and continue maintaining their projects.

**Limit unnecessary complexity, not the ability to solve complex problems.**

**Business correctness with evidence → ease of understanding and maintenance → a small implementation.** Fewer lines may be a result; they are not the acceptance criterion.

## Two Skills

| Skill | Use | Delivery focus |
| --- | --- | --- |
| [unfold-dev](skills/unfold-dev/SKILL.md) | Add features, fix bugs, and refactor | Concrete expectations, necessary tradeoffs, verification evidence, and the next change location |
| [unfold-review](skills/unfold-review/SKILL.md) | Review existing code or a change when requested | Location, impact, evidence, and the smallest appropriate fix; no edits by default |

The Chinese Skills are the only authoritative rule sources. The English translations for [everyday coding](docs/en/unfold-dev.md) and [review](docs/en/unfold-review.md) are for reading only. AI responds in Chinese by default and follows explicit requests for another language.

## Install and use

1. Download this repository and create an `.agents/skills/` folder in your target project.
2. Manually copy the `skills/unfold-dev/` and `skills/unfold-review/` folders into it. If either destination already exists, back it up and check local edits before replacing it; do not overwrite it directly.
3. Copy this repository's root [LICENSE](LICENSE) into each installed Skill folder.
4. Start a new Codex session in the target project, check the available Skills, or request one explicitly:

```text
$unfold-dev Fix the inconsistent sales summary and export results. Explain how to verify the result and where to change the rules next time.
$unfold-review Review this change for missing business requirements, permission boundaries, and future maintenance. Report only; do not edit.
```

Codex can match Skills automatically based on the task and descriptions, but selection is not guaranteed every time. Non-coding tasks such as conversation and translation are outside their scope. Being listed does not prove use; check whether the corresponding `SKILL.md` was read. See the [official Codex instructions](https://learn.chatgpt.com/docs/build-skills) for loading behavior. Using the Skills does not require Python or this repository's checks.

**Update:** Compare the new version with the installed copies, back up the old folders, preserve required local edits when replacing them, and start a new session. Make lasting rule changes in this repository's Chinese Skills to avoid maintaining multiple authoritative copies.

**Disable:** Move both installed folders out of `.agents/skills/` to a backup location where Skills are not loaded, then start a new session to confirm. Old sessions may already have loaded the rules. Handle same-name installations in user-level directories or plugins separately. For an independent trial, also disable conflicting rules and start a new session.

## Understand, judge, and make the next change

After a trial, check whether the delivery helps you answer: Why was it changed this way? How can I verify it? Where should I make the next change?

The [refund-rule handoff example](examples/sales-handoff.en.md) shows this in practice: the summary and CSV share `summarize_sales`, so the refund calculation changes in one place. The handoff identifies the rule, checks, and next change location. It contains two runnable implementations for a simulated business exercise.

## Maintenance and verification

To change coding or review behavior, start with the two Chinese Skills above, update their versions, and synchronize the English translations. To change business samples, start with the requirements and checks in the [three acceptance exercises](evals/README.en.md), then adjust the implementation. Do not add duplicate rules or an installer.

Run these checks from the repository root with Python 3.10 or later. They use only the standard library:

```powershell
python -X utf8 evals/check_repo.py
python -X utf8 evals/check.py --selftest
python -X utf8 examples/sales/net/test_sales.py
python -X utf8 evals/check.py --case sales-handoff --workspace examples/sales/separate
```

GitHub automation runs the same four checks without calling models. After changing rules, also check explanations and handoff in a real task; passing tests does not establish better understanding. Before committing, check staged contents and the public author identity. Exclude private conversations, credentials, and local production files.

The first version targets Codex. Native automatic selection, explicit invocation, model behavior after disabling, and independent human maintenance remain unverified, as do other platforms. Use the [trigger and removal checklist](evals/trigger-prompts.md#english) to record actual trials.

Released under the [MIT license](LICENSE). Thanks to [Ponytail](https://github.com/DietrichGebert/ponytail) for inspiring small implementations. unfold's core rules were written independently around business acceptance and maintenance handoff.

Try it, and leave a Star if you find it useful ⭐
