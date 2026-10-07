# unfold

[English](README.en.md)

**让 AI 深入思考，把代码写得朴素，把逻辑讲得明白。**

AI 写出的代码，有时功能实现了，层层抽象和满屏术语却让人看不懂、改不动。unfold 是给 AI 使用的工作规范（Skill），帮助普通开发者看懂实现、判断结果、继续维护自己的项目。

**限制不必要的复杂度，不限制解决复杂问题的能力。**

**业务正确且可验证 → 容易理解和维护 → 实现精简。** 代码更少只是可能的结果，不是验收标准。

## 两个 Skill

| Skill | 用途 | 交付重点 |
| --- | --- | --- |
| [unfold-dev](skills/unfold-dev/SKILL.md) | 新增功能、修复问题、重构 | 具体预期、必要取舍、验证证据、下次修改入口 |
| [unfold-review](skills/unfold-review/SKILL.md) | 用户要求检查已有代码或某次修改 | 位置、影响、依据、最小修复建议；默认不修改 |

中文 Skill 是唯一规则来源；[日常协作英文译文](docs/en/unfold-dev.md)和[审查英文译文](docs/en/unfold-review.md)只供阅读。AI 默认中文回复，用户明确要求其他语言时跟随用户。

## 安装与使用

1. 下载本仓库，在目标项目中创建 `.agents/skills/` 文件夹。
2. 手动将 `skills/unfold-dev/` 和 `skills/unfold-review/` 两个文件夹复制进去；目标已有同名目录时，先备份并核对本地修改，不直接覆盖。
3. 将本仓库根目录的 [LICENSE](LICENSE) 分别复制到这两个已安装的 Skill 文件夹。
4. 在目标项目中新开 Codex 会话，检查可用 Skill，或明确调用：

```text
$unfold-dev 修复销售汇总与导出结果不一致的问题，说明如何验证，以及以后从哪里修改规则。
$unfold-review 审查这次修改，检查业务遗漏、权限边界和后续维护；只报告，不修改。
```

Codex 可以根据任务和描述自动匹配 Skill，但不保证每次触发；闲聊、翻译等非编程任务不适用。列表中可见不等于实际使用，应检查是否读取了对应 `SKILL.md`。加载方式参考 [Codex 官方说明](https://learn.chatgpt.com/docs/build-skills)。使用 Skill 不需要运行 Python 或安装本仓库的检查工具。

**更新：**比较新版与已安装副本，备份旧目录，保留需要的本地修改后替换，再开启新会话。长期规则修改回到本仓库中文 Skill，避免维护多套来源。

**停用：**将两个已安装目录移出 `.agents/skills/`，放到不会加载 Skill 的备份位置，再开启新会话确认。旧会话可能已经加载规则；用户级目录或插件中的同名安装需要分别处理。需要独立试用时，也应停用冲突规则并开启新会话。

## 看懂、判断、接着改

试用后，看交付是否帮助你回答：为什么这样改？怎样确认正确？下次应该改哪里？

[退款规则交接案例](examples/sales-handoff.md)展示了具体写法：汇总和 CSV 共用 `summarize_sales`，退款计算在同一处修改；交付说明指出规则位置、检查文件和下次修改入口。案例包含两份可运行代码，是模拟业务教学材料。

## 维护与验证

修改协作或审查行为，从上面的两个中文 Skill 开始，更新版本并同步英文译文。修改业务样本，从[三个验收题](evals/README.md)的要求和检查方法开始，再调整实现；不新增规则副本或安装器。

在仓库根目录运行以下检查，需要 Python 3.10 或更高版本，只使用标准库：

```powershell
python -X utf8 evals/check_repo.py
python -X utf8 evals/check.py --selftest
python -X utf8 examples/sales/net/test_sales.py
python -X utf8 evals/check.py --case sales-handoff --workspace examples/sales/separate
```

GitHub 自动检查使用同样四项，不调用模型。修改规则后还应在实际任务中检查解释和交接；测试通过不能证明用户更容易理解。提交前核对暂存内容和公开作者信息，不包含私人会话、凭据或本地制作文件。

首版面向 Codex。原生自动匹配、手动调用、停用后的模型行为，以及真人独立维护效果仍未验证；其他平台也未验证。[触发与停用清单](evals/trigger-prompts.md)可用于记录实际试用。

采用 [MIT 许可](LICENSE)。感谢 [Ponytail](https://github.com/DietrichGebert/ponytail) 对精简实现的启发；unfold 的核心规则围绕业务验收与维护交接独立编写。

欢迎体验，觉得有用的话，点个 Star ⭐
