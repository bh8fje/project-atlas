# Project Atlas 项目状态

## 当前阶段

Phase 8 - Local Operations（COMPLETED）。

TASK-025 COMPLETED。

当前版本：`v0.25.0`。

## 当前能力

- 已定义 `Project` 与 `Task` 核心领域模型。
- 已定义 `ProjectStatus` 与 `TaskStatus` 生命周期状态。
- 已提供基础校验、Task 状态迁移及 JSON 兼容的字典序列化。
- 已定义 `ProjectArtifact`、`Repository`、`RepositorySnapshot` 与 `AssetRelationship` 项目资产模型。
- 已定义 `ArtifactType` 与 `RelationshipType` 资产分类和关系类型。
- 已提供显式扫描根目录、最大深度、排除目录和符号链接边界的本地项目发现引擎。
- 已支持通过基础项目标记识别候选项目并创建 `Project` 实例。
- 已支持对项目目录、文件、文档、源码和配置进行有边界的结构分类。
- 已提供 `ProjectStructure`、包含关系、技术标签与资产类型计数。
- 已提供基于规范化本地路径的稳定 Project ID。
- 已提供 `sha256-metadata-v1` 项目结构指纹、校验、序列化与状态匹配。
- 已提供 `ProjectSnapshot`、`ProjectChange` 与 `ProjectHistoryEvent` 不可变历史领域契约。
- 已定义 `ChangeType` 与 `HistoryEventType`，并支持校验和 JSON 兼容序列化。
- 已提供基于相对路径和资产元数据的确定性变化检测，支持新增、删除和修改。
- 已支持初始结构检测、稳定 Change ID 与显式 Snapshot 引用。
- 已提供 `ProjectTimeline` 与 `ProjectTimelineBuilder`，支持历史引用完整性校验和确定性排序。
- 已提供 `ProjectRelationship`、`ProjectRelationshipGraph` 与显式图构建器。
- 已支持项目图入边、出边、引用完整性、确定性排序和序列化。
- 已提供版本化 `KnowledgeRecord` 与显式路径的事务化 SQLite 本地存储。
- 已支持跨进程读取、精确类型/Project 过滤、冲突保护与显式替换。
- 已提供 `KnowledgeQuery`、`KnowledgeQueryResult` 与只读 `KnowledgeQueryEngine`。
- 已支持类型、Project、时间范围、限制条件和本地全部词项匹配。
- 已提供 `AIContext` 与本地 `AIContextBuilder`，支持来源追踪、确定性排序和字符上限。
- 已对常见密码、令牌、密钥和授权字段进行递归脱敏。
- 已定义 `AIProvider`、`AIRequest`、`AIProviderResponse` 和结构化 `ProjectUnderstanding`。
- 已提供显式项目理解服务、严格 JSON 校验、Provider/模型归属和失败透明传播。
- 已提供单轮只读 `AIProjectAssistant` 与可溯源 `ProjectAssistantAnswer`。
- 已支持严格回答/建议/注意事项结构、Project 一致性校验和失败透明传播。
- 已提供独立构建的 Sites/Vinext 本地 Dashboard；发布记录、历史和组成基线保持只读。
- Dashboard 未配置云资源，不调用远端服务，不写入 Core。
- 已提供移动安全区域、触控导航、Viewport 与可安装 Web App Manifest。
- 移动访问不建立公网入口、账号、后台同步或远程数据通道。
- 已提供显式注册的进程内 `CommandCenter`、副作用声明、变更确认与可审计结果。
- Command Center 未预置 Handler，不执行 Shell、网络请求或隐式自动化。
- 已提供确定性 `MultiProjectIntelligenceService`，聚合项目摘要、共同风险、关系数量和孤立项目。
- 多项目聚合不重新发现项目、不调用 AI、不写入存储，也不推断关系。
- 已提供显式触发的 `AutonomousProjectAgent`，将已有变化和组合风险转换为可追踪 Signal 与建议。
- Agent 观察周期强制零执行动作，不包含后台调度、自动修改、通知发送或网络调用。
- Execution Plan 1.0 的 TASK-001 至 TASK-020 已全部完成。
- Dashboard 已支持中文、英语、俄语和韩语，未选择偏好时跟随系统语言，不受支持时回退英语。
- 用户显式语言偏好仅保存在当前浏览器，可随时恢复“跟随系统”。
- 面向用户的内容已改为清晰中文优先，英语、俄语和韩语均按中文含义翻译。
- Dashboard 不再使用“供应商无关的分析契约”等内部工程表述介绍功能。
- 产品文案标准已调整为专业、清晰和准确，同时避免难懂术语与过度口语化。
- Dashboard 建设进度的九个阶段均可展开，查看阶段说明与已实现功能。
- Dashboard 已将原“项目关系”示意改为“项目组成”，明确标注代码仓库、核心功能和本地资料的连接含义。
- Dashboard 明确标注当前数字为发布记录，已移除无数据支持的“100%”健康分数和实时稳定表述。
- Dashboard 设计边界已记录在 `docs/DASHBOARD_DESIGN.md`。
- 已提供操作系统目录选择器，由用户明确批准需要管理的本地扫描目录。
- 已提供本机项目目录登记、首次项目识别、手动检查和明确开关的定时检查。
- 定时检查复用现有项目发现、结构分析和结构指纹能力，只比较结构元数据，不读取文件内容或 Git 历史。
- Dashboard “项目目录”模块显示最近检查时间、已识别项目和新增、变化、移除摘要，并每 10 秒读取一次本机最新结果。
- 本机服务只监听回环地址，仅接受明确的本地 Dashboard 来源；路径与检查记录不传输到外部网络。
- 关闭本机服务后自动检查停止；移除目录只删除登记与检查记录，不删除或修改用户项目文件。
- 尚无具体模型适配器、Git commit 分析、公网服务、常驻系统服务或外部 API。

## 工程基线

- 状态：已建立目录、配置、文档与开发规范基线
- 运行环境：Python 3.11+；Dashboard 构建需要 Node.js 22.13+
- 测试框架：Python `unittest`
- 最近验证：2026-08-23，`python3 -m unittest discover -s tests -v`，168 项测试通过；`dashboard/` 生产构建通过；Dashboard 与本机服务预览均返回 HTTP 200
- 版本控制：Git 已纳入 TASK-001 完成流程
- 远端镜像：GitHub `bh8fje/project-atlas` 与群晖 `project-atlas.git`
- 发布规则：所有发布提交必须双推送并分别验证
- 版本规则：每个里程碑使用带备注的 Git 标签，规范见 `docs/VERSIONING.md`
- 执行计划：`EXECUTION_PLAN.md` Version 1.5，状态 COMPLETED

## 下一步

- Execution Plan 1.5 已完成。
- 等待新的明确 Task；面向用户的新文案继续遵循中文优先、专业清晰且不过度口语化的规范。
