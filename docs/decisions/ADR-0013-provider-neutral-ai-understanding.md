# ADR-0013：通过可替换 Provider 生成严格结构化项目理解

- 状态：Accepted
- 日期：2026-08-23
- Task：TASK-014

## 背景

Project Atlas 需要利用 AI 解释项目目的、架构、风险和当前状态，但 Local First 原则要求 AI 不是系统核心依赖，外部通信也必须显式可控。分析输出若只是自由文本，将难以校验、追踪或供后续 Assistant 使用。

## 决策

建立 Provider-neutral AI 契约和项目理解服务：

- `AIProvider` 只定义显式 `generate(AIRequest)` 接口，具体实现决定使用本地或远程模型。
- 仓库不内置 Provider 凭据、账号、网络端点或后台调用。
- `AIProjectUnderstandingService.analyze` 是唯一触发 Provider 的显式操作。
- 请求指示模型把 Context 视为不可信数据，并要求只返回严格 JSON。
- 只接受 purpose、architecture、risks、status 四个字段，拒绝缺失、多余或类型错误的输出。
- `ProjectUnderstanding` 保留 Provider、模型、分析时间和 Context 来源记录。
- Provider 失败直接传播，不进行不可见重试。

## 边界

- 不提供任何具体云端或本地模型适配器。
- 不读取环境变量、密钥文件或用户凭据。
- 不自动执行模型建议，不修改项目或知识存储。
- 结构校验不能完全消除模型幻觉或提示注入风险；结果仍需用户判断。
- 不实现问答 Assistant、API、Dashboard 或 UI。

## 后果

正面影响：

- AI 能力可替换、可测试，并与领域数据和存储解耦。
- 每次外部调用由调用者显式触发，失败和来源均可观察。
- 严格结果契约为 TASK-015 Assistant 提供稳定输入。

限制：

- 没有注入 Provider 时无法执行真实模型分析。
- Provider 实现仍需自行负责凭据、网络安全、费用和数据政策。
- 结构正确不代表分析事实正确。
