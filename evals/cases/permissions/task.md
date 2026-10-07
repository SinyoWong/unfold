# 为部门资料增加详情入口（模拟业务练习）

现有 `list_documents` 已按部门和角色限制可见资料。现在增加 `get_document`，要求列表和详情使用同一条权限规则，不让新入口绕过限制。

## 输入与接口

- `list_documents(documents, actor, department=None) -> list`：按原顺序返回可见资料，可选部门筛选只能缩小范围。
- 新增 `get_document(documents, actor, document_id) -> dict | None`：返回指定可见资料；资料不存在或无权访问都返回 `None`，避免泄露是否存在。
- `documents` 为格式正确的字典列表，每条包含唯一字符串 `id`、非空字符串 `department` 和字符串 `title`。此题不处理数据库或不合法存储数据。
- `actor` 是服务器已验证身份得到的字典，含 `role` 和可选 `department`，**不能直接使用客户端提供的角色或部门冒充身份**。此题不实现登录；真实接入需要从已验证身份取得 `actor`。
- `role=admin` 可读全部部门；`role=member` 只可读自身部门；其他角色或缺失角色全部拒绝。成员部门为 `None`、空字符串或缺失时全部拒绝。
- `department` 筛选及 `document_id` 来自用户请求，均为字符串（筛选也可以是 `None`）。未知部门和空字符串筛选返回空列表，不能扩大权限。
- 空资料列表安全返回空列表或 `None`。不得修改资料或身份字典。

此练习只使用 Python 标准库，不引入框架或新依赖。
