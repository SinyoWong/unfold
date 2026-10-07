# 状态文案（模拟业务练习）

用户需求：订单列表的“Pending”改成“待处理”。只调整这个展示文案，内部状态仍为 `pending`。

`app.py` 的入口为 `display_status(status) -> str`，输入是字符串。`paid` 仍展示 `Paid`，`cancelled` 仍展示 `Cancelled`，未知状态和空字符串原样返回。不增加依赖，不改变调用接口。

保留命令行入口：`python app.py pending` 应输出一行“待处理”；其他状态同样按上述规则输出。传入参数仍使用内部状态字符串，不把内部 `pending` 改成中文。
