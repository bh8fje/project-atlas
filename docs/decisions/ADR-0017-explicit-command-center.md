# ADR-0017：显式且可审计的 Command Center

- 状态：Accepted
- 日期：2026-08-23
- 关联任务：TASK-018

## 背景

Project Atlas 的能力分布在发现、历史、知识和智能模块中。未来界面需要统一调用入口，但直接执行任意函数、Shell 命令或隐式自动化会破坏 Human Controlled 原则。

## 决定

建立进程内 `CommandCenter` 应用服务。只有调用者显式注册的命令和 Handler 可以执行；命令定义声明 `READ_ONLY` 或 `MUTATING` 副作用等级。所有请求与结果使用可序列化、带时间和请求 ID 的领域契约。

任何 `MUTATING` 命令必须在请求中明确确认，否则返回可审计的 `REJECTED` 结果且不调用 Handler。未知命令和 Handler 异常保持透明，不做隐藏重试。

## 后果

- 界面和未来入口可以共享稳定的命令契约。
- 默认没有预注册命令，也没有 Shell、网络、文件写入或远程 API 能力。
- 确认标志是应用层安全边界之一，不替代未来的授权、身份或策略系统。
- 多项目推理属于 TASK-019，不在 Command Center 内实现。
