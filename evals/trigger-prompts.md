# Skill 触发与停用验收清单

[English below](#english) · [验收说明](README.md)

每行用全新会话。编码和审查工作区仅放对应题目的代码、需求及已安装的两个 Skill；非编程场景只安装 Skill。记录实际读取的 `SKILL.md` 路径、输出和文件变化。描述匹配只是选择条件，不是触发保证。

| 场景 | 输入示例 | 预期 |
| --- | --- | --- |
| 中文自动匹配 | 请完成 task.md 的需求。 | 编码任务选择 unfold-dev，完成业务验收 |
| 英文自动匹配 | Implement the requirements in task.md. Please respond in English. | 编码任务选择 unfold-dev，英文交付 |
| 手动调用 | $unfold-dev 请按 task.md 完成修改。 | 读取日常 Skill 并完成验收 |
| 中文审查 | 请按 task.md 审查实现，先报告，不修改。 | 选择 unfold-review，不修改受检文件 |
| 英文审查 | Review this implementation against task.md. Report in English without editing. | 选择 unfold-review，不修改受检文件 |
| 中文非编程 | 将“今天阳光很好，适合散步。”译为英文，只输出译文。 | 不读取两个编程 Skill |
| 英文非编程 | Translate “The meeting starts at nine.” into Chinese. Return only the translation. | 不读取两个编程 Skill |
| 停用 | 移出两个 Skill 并新开会话后重复上述输入。 | Skill 不再出现在可用目录中或被读取 |

以上原生行为检查尚未完成验证。目录检查和规则正文对照不能代替原生触发验收；没有实际执行的场景不能标记为通过。

## English

Use a fresh session for each row. Provide only the exercise code, task, and installed Skills for coding/review cases; provide only Skills for non-coding cases. Record actual Skill reads, output, and file changes. Expected selection is not a guarantee:

- Chinese/English implementation requests should select `unfold-dev`; an explicit `$unfold-dev` request should load it.
- Chinese/English review requests should select `unfold-review` and leave inspected files unchanged.
- Both translation requests above should use neither programming Skill.
- After moving both Skills out and starting a fresh session, they should disappear from discovery and no longer be read.

Native behavioral checks above remain unverified. Directory checks and rule-text comparisons do not establish native trigger behavior; scenarios that have not actually been run must not be marked as passed.
