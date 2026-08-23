# ADR-0014：建立显式单轮、只读的 AI Project Assistant

- 状态：Accepted
- 日期：2026-08-23
- Task：TASK-015

## 背景

用户需要询问“项目现在怎么样”和“下一步应该做什么”。Assistant 应复用受控 Context 与结构化 Project Understanding，同时保持 Human Controlled：回答和建议不能被解释为已执行操作，也不能在后台积累或发送更多数据。

## 决策

建立 `ProjectAssistantAnswer` 与 `AIProjectAssistant`：

- 每次 `ask` 是调用者显式触发的单轮 Provider 请求。
- Context 与 Understanding 必须属于同一 Project，否则在调用 Provider 前拒绝。
- 请求把项目数据标记为不可信，并明确建议仅是建议、不得声称已执行操作。
- Provider 只允许返回 answer、recommendations 和 cautions 三个严格 JSON 字段。
- Answer 保留问题、Project、Provider、模型、回答时间和合并后的来源记录。
- Provider 失败直接传播，不隐藏重试。

## 边界

- 不保存对话历史或用户问题。
- 不自动查询、构建 Context 或刷新 Understanding。
- 不执行命令、修改项目、写入知识存储或发送通知。
- 不提供具体模型适配器、API、Dashboard 或 UI。
- AI 回答可能不准确，用户必须审查建议。

## 后果

正面影响：

- 用户问答建立在受控、可溯源的数据链路上。
- 单轮只读边界避免 Assistant 演变为未授权 Agent。
- 严格结果可以被后续界面安全呈现。

限制：

- 当前没有多轮上下文、会话记忆或工具调用。
- 调用者必须预先准备 Context 和 Understanding。
- 没有具体 Provider 时无法生成真实回答。
