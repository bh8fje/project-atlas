# ADR-0006：以不可变事实建立项目历史模型

- 状态：Accepted
- 日期：2026-08-23
- Task：TASK-007

## 背景

项目指纹只能表达一个时点的结构状态。要在后续重建项目演化，需要先区分“某时点的状态”“两个状态之间声明的变化”和“时间线上发生的事实”。如果直接把检测、存储或展示逻辑写入这些对象，领域契约会与基础设施绑定。

## 决策

建立三个不可变、可校验、可序列化的领域契约：

- `ProjectSnapshot`：组合 `ProjectFingerprint`，记录项目在一个时点的结构摘要。
- `ProjectChange`：描述两个 Snapshot 之间某条资产路径的声明变化，类型为 `ADDED`、`REMOVED`、`MODIFIED` 或 `UNKNOWN`。
- `ProjectHistoryEvent`：记录带时间的历史事实，可引用一个 Snapshot 和多个 Change。
- `HistoryEventType` 区分 Snapshot 捕获、变化记录与未知事件。
- 所有模型只保存值和引用，不访问文件系统或外部服务。

保留 TASK-003 的 `RepositorySnapshot` 作为仓库资产层的轻量摘要；`ProjectSnapshot` 是项目历史层契约，两者用途不同，不进行破坏性替换。

## 边界

- 不自动创建 Snapshot、Change 或 Event。
- 不比较指纹，不判断新增、删除或修改。
- 不建立时间线排序、聚合或查询能力。
- 不持久化，不调用 Git、AI、数据库、API 或 UI。

## 后果

正面影响：

- Snapshot、Change、Event 拥有清晰且稳定的职责。
- TASK-008 可实现检测逻辑而无需改变历史数据契约。
- TASK-009 可在不可变事件之上构建时间线。

限制：

- 当前只能由调用者显式构造历史对象。
- 引用完整性只在单个对象内部校验，跨对象一致性留给后续应用层。
- 模型尚未定义存储格式、保留策略或查询索引。
