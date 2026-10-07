# unfold: Review on request

Reading translation only; do not load this document as a separate Skill.
Chinese source: [unfold-review](../../skills/unfold-review/SKILL.md). Source version: **0.1.0**.
The Chinese source is authoritative. Keep this translation aligned when changing it.

**Name:** `unfold-review`

**Description:** When the user requests a review of code, a change, or a diff, check business completeness, boundaries and permissions, unnecessary complexity, and maintenance handoff. Report findings without modifying code by default. Do not trigger for everyday implementation or non-coding tasks.

**License:** MIT

Find concrete problems affecting business correctness and future maintenance; do not invent findings to fill a quota. Use Chinese by default, following the user when they explicitly request another language. Explain technical terms in plain language when they first appear.

## Establish evidence and scope first

- Read the user's requirements, project instructions, changes under review, and relevant callers. Confirm the version and scope being reviewed; do not infer the whole business behavior from a few lines in a diff.
- Look for business requirements in existing code and documentation. Distinguish confirmed requirements, reasonable assumptions, and missing information. Ask only when essential scope or business decisions cannot otherwise be determined.
- By default, do not edit the reviewed code, apply fixes automatically, or run commands that rewrite source files or snapshots. Verification may use temporary directories or external checks to keep generated files out of the reviewed directory. When the user explicitly requests fixes, perform them within the authorized scope.

## Check in this order

1. **Business completeness:** Were requirements missed or misunderstood? Do multiple entry points follow the same rule? Does the implementation work only for the normal example?
2. **Boundaries and failures:** Are relevant null values, boundary inputs, permissions, and failure cases handled correctly? Could access exceed the user's permissions, or could data leak or be lost? Check actual risks related to this change, without expanding into an unrelated security checklist.
3. **Structure and duplication:** Does added structure solve a current problem? Does it reimplement existing capabilities, copy the same business rule, or unnecessarily broaden the change? Do not label necessary shared functions, permission checks, or tests as excessive complexity just because they add lines.
4. **Maintenance and verification:** Can a reader locate the rules, call relationships, and future change points? Is there evidence for the checks claimed in the handoff? Label missing handoff information as maintenance advice, not as a proven business defect.

## Report with evidence

- Put confirmed problems with the greatest impact first. For each finding, include **location (file and accurate line number), trigger and actual impact, business or code evidence, and the smallest appropriate fix**.
- List judgments that cannot be reproduced or lack evidence separately as “Needs confirmation,” stating what evidence is missing. Do not present speculation as a confirmed defect.
- State clearly when no problems have been confirmed, and explain the coverage and unverified areas. Do not claim to have proven the code free of all problems.
- Describe the checks actually executed and their results; say directly if tests were not run. Avoid relying on subjective scores or generic best-practice advice.
- Prefer fixes at existing rule locations and point to the corresponding verification entry points. Recommend new structure only when the existing structure cannot solve the problem, and explain why a simpler approach is insufficient.

This Skill does not automatically expand into a whole-repository audit or create a persistent review mode.
