# 架构基线

## 当前边界

TASK-002 与 TASK-003 在 `src/project_atlas/domain/` 建立纯内存领域契约。Domain 层定义 Project、Task、Repository、Artifact、Snapshot、Relationship、生命周期状态、基础校验和序列化，不执行 I/O，也不依赖基础设施。

TASK-004 在 `src/project_atlas/discovery/` 建立有显式边界的本地项目发现层。该层可以识别候选项目根目录并创建 `Project`，但不分析项目内容。

TASK-005 在 `src/project_atlas/analysis/` 建立受限的项目结构分析层。该层只读取目录条目和文件元数据，输出 `ProjectStructure`，不读取文件内容或 Git 历史。

仓库目前没有稳定项目指纹、变化检测、Git 分析、内容语义分析、AI 分析、Dashboard、数据库、API 或其他后续业务能力。

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
- 未来基础设施或应用层只能依赖 Domain 层；Domain 层不得反向依赖它们。
- 只有获得具体 Task 授权后，才可增加发现、持久化、分析或界面模块。

领域模型决策见 [ADR-0001](decisions/ADR-0001-domain-model.md)。
资产抽象决策见 [ADR-0002](decisions/ADR-0002-repository-asset-model.md)。
本地发现边界见 [ADR-0003](decisions/ADR-0003-local-project-discovery.md)。
结构分析边界见 [ADR-0004](decisions/ADR-0004-project-structure-analysis.md)。
