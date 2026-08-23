# 架构基线

## 当前边界

TASK-002 与 TASK-003 在 `src/project_atlas/domain/` 建立纯内存领域契约。Domain 层定义 Project、Task、Repository、Artifact、Snapshot、Relationship、生命周期状态、基础校验和序列化，不执行 I/O，也不依赖基础设施。

TASK-004 在 `src/project_atlas/discovery/` 建立有显式边界的本地项目发现层。该层可以识别候选项目根目录并创建 `Project`，但不分析项目内容。

TASK-005 在 `src/project_atlas/analysis/` 建立受限的项目结构分析层。该层只读取目录条目和文件元数据，输出 `ProjectStructure`，不读取文件内容或 Git 历史。

TASK-006 在 `src/project_atlas/fingerprint/` 建立稳定本地项目身份和版本化元数据指纹。身份由规范化项目路径确定；指纹只使用结构元数据，不读取文件内容。

TASK-007 在 Domain 层建立 `ProjectSnapshot`、`ProjectChange` 和 `ProjectHistoryEvent`。这些对象只表达历史事实与引用，不负责生成、比较、排序或保存历史。

TASK-008 在 `src/project_atlas/history/` 建立纯内存变化检测层。该层比较调用者提供的两个 `ProjectStructure`，以相对路径和资产元数据生成有序 `ProjectChange`，不自行扫描或保存结果。

TASK-009 在 Domain 与 History 层建立 `ProjectTimeline` 和 `ProjectTimelineBuilder`。构建器校验项目归属及历史引用，并按时间与 Event ID 生成确定性事件顺序。

TASK-010 在 Domain 与 `src/project_atlas/knowledge/` 建立显式项目关系和确定性内存图。项目图与项目内部的资产关系保持独立，不自动推断边。

TASK-011 在 Domain 与 Knowledge 层建立版本化 `KnowledgeRecord` 和事务化 SQLite 本地存储。存储路径与覆盖行为必须显式，记录内容使用规范 JSON 信封。

TASK-012 在 Domain 与 Knowledge 层建立结构化查询、只读查询结果和本地关键词匹配。文本查询是确定性词项匹配，不是 AI 语义理解。

TASK-013 在 Domain 与 `src/project_atlas/intelligence/` 建立有来源、字段脱敏和字符上限的 `AIContext`。构建过程完全本地，不调用模型。

TASK-014 建立 `AIProvider` 可替换接口和 `AIProjectUnderstandingService`。服务只在显式调用时向注入的 Provider 发送已准备 Context，并把严格 JSON 转换为可溯源的 `ProjectUnderstanding`。

TASK-015 建立单轮、只读 `AIProjectAssistant` 和结构化 `ProjectAssistantAnswer`。Assistant 复用同 Project 的 Context 与 Understanding，不保存会话或执行建议。

TASK-016 在 `dashboard/` 建立独立的 Sites/Vinext 本地界面。Dashboard 只投影已发布的项目状态、历史和关系基线，不读取远端数据、不写入 Core，也不配置云资源。

TASK-017 在同一界面层增加标准 Web App Manifest、移动 Viewport、安全区域和触控导航。它不建立公网连接、后台同步或原生应用。

TASK-018 在 `src/project_atlas/application/` 建立进程内 `CommandCenter`。命令必须显式注册，副作用必须声明，变更命令必须由请求明确确认；服务不包含 Shell 或远程执行器。

TASK-019 在 Intelligence 层建立确定性多项目聚合。它只组合调用者提供的 Project、Understanding 和关系图，生成共同风险、孤立项目与项目摘要，不发起新的发现或 AI 调用。

TASK-020 在 Intelligence 层建立显式触发的 `AutonomousProjectAgent` 观察周期。Agent 将已提供的变化与组合风险转换为 Signal 和建议，领域契约强制零执行动作。

TASK-021 在 Dashboard 客户端层建立类型化中文、英语、俄语、韩语翻译字典。未设置偏好时跟随系统语言；显式偏好只保存在浏览器本地，不进入 Core 或远端服务。

TASK-022 规定 Dashboard 等用户界面以清晰中文为文案源，其他语言按中文含义翻译；工程术语保留在开发与架构文档中。

TASK-023 将该标准进一步收敛为专业、清晰且不过度口语化，并将 Dashboard 建设阶段建模为本地静态的可展开详情；决策见 `docs/decisions/ADR-0022-browsable-development-phases.md`。

TASK-024 规定 Dashboard 的静态数字必须标记为发布记录，项目组成示意必须与真实的多项目关系分开；决策见 `docs/decisions/ADR-0023-dashboard-information-semantics.md`。

TASK-025 在 `src/project_atlas/application/workspaces.py` 与 `src/project_atlas/local_service.py` 建立本机项目目录管理。用户通过操作系统选择器批准目录，本机服务复用既有发现、结构分析和指纹能力，并把轻量检查状态保存在本机 JSON 文件中。Dashboard 只通过固定回环地址读取这部分本机检查结果；决策见 `docs/decisions/ADR-0024-local-workspace-monitoring.md`。

v0.25.1 保留结构分析的 10,000 项保护上限，并在工作区协调层将超过上限的单个项目记录为受限。受限项目不生成完整结构指纹，但不会阻断同一目录中其他项目的识别。

仓库目前没有具体模型适配器、Git commit 分析、公网服务、后台 Agent 调度、自动修改或外部 API。本机目录服务不监听局域网或公网，也不是常驻系统服务。

## 设计约束

- 本地优先是系统级约束，不是单个功能选项。
- 领域逻辑应与存储、模型供应商和界面解耦。
- 外部通信必须是显式、可观察且可关闭的。
- 用户项目内容不得被测试夹具或日志意外提交。
- 重要架构选择应通过独立文档记录背景、决定和后果。

## 分层边界

- `src/project_atlas/domain/`：稳定的领域语言与不变量，不访问外部系统。
- `src/project_atlas/discovery/`：受 `DiscoveryScope` 约束的只读文件系统发现，不分析项目内部结构。
- `src/project_atlas/analysis/`：受深度和资产数量约束的结构与技术标记分析，不读取文件内容。
- `src/project_atlas/fingerprint/`：生成稳定本地身份和版本化元数据摘要，不保存历史或判断变化类型。
- `src/project_atlas/history/`：比较显式提供的结构并生成变化事实，不采集、持久化或展示历史。
- `src/project_atlas/knowledge/`：构建显式项目关系图，并在调用者指定的 SQLite 文件中保存版本化知识记录；不自动采集或推断关系。
- `src/project_atlas/intelligence/`：准备受控 AI 上下文，通过注入 Provider 执行结构化分析，并确定性聚合多项目事实与观察 Signal；不内置凭据、端点、调度或动作执行。
- `dashboard/`：本地界面与独立前端构建；静态发布记录保持只读，项目目录模块只连接固定的本机回环服务，不访问外部服务。
- `src/project_atlas/application/`：协调显式用户命令与副作用边界；项目目录登记与指纹状态使用明确的本机 JSON 文件，不隐式注册远端执行器。
- `src/project_atlas/local_service.py`：本机目录选择和定时检查入口，只监听回环地址，只接受明确的本地 Dashboard 来源。
- 未来基础设施或应用层只能依赖 Domain 层；Domain 层不得反向依赖它们。
- 只有获得具体 Task 授权后，才可增加发现、持久化、分析或界面模块。

领域模型决策见 [ADR-0001](decisions/ADR-0001-domain-model.md)。
资产抽象决策见 [ADR-0002](decisions/ADR-0002-repository-asset-model.md)。
本地发现边界见 [ADR-0003](decisions/ADR-0003-local-project-discovery.md)。
结构分析边界见 [ADR-0004](decisions/ADR-0004-project-structure-analysis.md)。
项目指纹决策见 [ADR-0005](decisions/ADR-0005-project-fingerprint.md)。
项目历史模型见 [ADR-0006](decisions/ADR-0006-project-history-model.md)。
结构变化检测见 [ADR-0007](decisions/ADR-0007-structure-change-detection.md)。
项目时间线见 [ADR-0008](decisions/ADR-0008-project-timeline.md)。
项目关系图见 [ADR-0009](decisions/ADR-0009-project-relationship-graph.md)。
本地知识存储见 [ADR-0010](decisions/ADR-0010-local-knowledge-storage.md)。
本地知识查询见 [ADR-0011](decisions/ADR-0011-local-knowledge-query.md)。
受控 AI 上下文见 [ADR-0012](decisions/ADR-0012-bounded-ai-context.md)。
Provider-neutral 项目理解见 [ADR-0013](decisions/ADR-0013-provider-neutral-ai-understanding.md)。
只读 AI Project Assistant 见 [ADR-0014](decisions/ADR-0014-read-only-ai-project-assistant.md)。
本地只读 Dashboard 见 [ADR-0015](decisions/ADR-0015-local-dashboard.md)。
移动端本地 Web 访问见 [ADR-0016](decisions/ADR-0016-mobile-local-web-access.md)。
显式 Command Center 见 [ADR-0017](decisions/ADR-0017-explicit-command-center.md)。
确定性多项目智能见 [ADR-0018](decisions/ADR-0018-deterministic-multi-project-intelligence.md)。
受控 Autonomous Project Agent 见 [ADR-0019](decisions/ADR-0019-controlled-autonomous-agent.md)。
本机语言偏好见 [ADR-0020](decisions/ADR-0020-local-language-preferences.md)。
中文优先产品文案见 [ADR-0021](decisions/ADR-0021-chinese-first-product-language.md)。
专业产品文案与阶段详情见 [ADR-0022](decisions/ADR-0022-browsable-development-phases.md)。
Dashboard 信息含义见 [ADR-0023](decisions/ADR-0023-dashboard-information-semantics.md)。
本机项目目录管理见 [ADR-0024](decisions/ADR-0024-local-workspace-monitoring.md)。
