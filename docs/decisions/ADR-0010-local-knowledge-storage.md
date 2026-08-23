# ADR-0010：使用 SQLite 保存版本化本地知识记录

- 状态：Accepted
- 日期：2026-08-23
- Task：TASK-011

## 背景

关系图和项目历史当前只存在于内存，无法跨运行保留。Project Atlas 的 Local First 原则要求数据默认留在用户设备，同时存储需要事务保证、明确冲突行为和可演进的版本边界。此阶段尚不实现知识查询引擎。

## 决策

建立 `KnowledgeRecord` 与 `LocalKnowledgeStore`：

- `KnowledgeRecord` 使用类型、记录 ID、可选 Project ID、记录时间和规范 JSON 数据组成稳定信封。
- 记录类型覆盖 Project、Structure、Snapshot、Change、Event、Timeline 和 Relationship Graph。
- 使用 Python 标准库 SQLite，在调用者显式指定的本地文件中事务化保存记录。
- 使用“记录类型 + 记录 ID”作为复合主键。
- 默认拒绝覆盖已有记录；只有调用者传入 `replace=True` 才允许替换。
- 数据库保存 Schema Version，并拒绝静默打开不支持的版本。
- 提供按精确记录类型和 Project ID 的基础列表过滤，为 TASK-012 提供最小存储接口。

## 边界

- 不自动选择或扫描用户目录；数据库路径必须显式提供。
- 不自动保存现有领域对象；调用者负责创建记录信封。
- 不提供全文、自然语言或图查询。
- 不提供删除、云同步、远程访问或后台写入。
- 当前数据未加密；文件系统权限和备份由部署环境负责。
- 不调用 Git、AI、API、Dashboard 或 UI。

## 后果

正面影响：

- 本地知识可跨进程保留，并具有事务与唯一性保证。
- 无新增第三方运行时依赖，也无外部网络通信。
- 明确覆盖和 Schema Version 降低不可追踪修改风险。

限制：

- 通用 JSON 信封牺牲部分数据库列级类型约束。
- 未来 Schema 升级需要显式迁移机制。
- 当前没有加密、删除、压缩或保留策略。
