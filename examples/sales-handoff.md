# 从退款修复到下一次需求：维护交接示例

[English](sales-handoff.en.md) · [返回项目](../README.md)

这是**模拟业务教学案例**。两份可运行实现展示如何集中退款规则、验证两个入口，以及交代下一次修改的位置。金额使用整数分。

## 第一次：两个入口都要扣除退款

原代码中，直接汇总和 CSV 导出共用 `summarize_sales`，但它只累加原金额。因此两处结果都偏大。任务规定已支付订单按原金额减退款计算，取消订单不计入；非法输入不能悄悄变为零或部分合计。

```text
修改前：直接汇总 / CSV 导出 -> summarize_sales -> 只加原金额 -> 15000
修改后：直接汇总 / CSV 导出 -> summarize_sales -> 检查输入并扣退款 -> 13000
```

在同一个计算函数修复规则，并新增一个可以直接运行的检查文件，无需新类或依赖。查看[净额代码](sales/net/app.py)与[检查文件](sales/net/test_sales.py)。

交付说明可以明确指出：以后调整销售规则改 `summarize_sales`，对应检查在 `test_sales.py`。这句话给下一位维护者提供了具体入口。

## 第二次：按交接说明将原金额与退款分列

下一位维护者从代码、检查和交付说明开始。新需求改变返回值和导出格式：汇总返回两个金额字段，CSV 输出同名两列；原有输入检查保持不变。

```text
修改前：summarize_sales -> 净额 13000 -> sales_cents 一列
修改后：summarize_sales -> 原金额 15000、退款 2000 -> 两列 CSV
```

这次修改从 `summarize_sales` 进入，同时调整汇总、CSV 和对应检查。见[分列代码](sales/separate/app.py)和[分列检查](sales/separate/test_sales.py)。

从仓库根目录检查两份实现：

```powershell
python -B -X utf8 examples/sales/net/test_sales.py
python -B -X utf8 examples/sales/separate/test_sales.py
python -B -X utf8 evals/check.py --case sales --workspace examples/sales/net
python -B -X utf8 evals/check.py --case sales-handoff --workspace examples/sales/separate
```

## 能说明什么

这个案例展示了“共同规则位置 + 可运行检查 + 下一次修改入口”的具体写法。它是可自行运行的教学示例，不作为协作效果的测评报告。真人独立维护效果尚未评估。

以后修改这个练习的业务口径，应先改[任务要求](../evals/cases/sales/task.md)和[独立验收](../evals/check.py)，再调整实现并运行对应检查。
