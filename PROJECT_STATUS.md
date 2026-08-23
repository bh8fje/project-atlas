# Project Atlas 项目状态

## 当前阶段

Phase 3 - Knowledge Map（IN PROGRESS）。

TASK-010 COMPLETED。

当前版本：`v0.10.0`。

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
- 尚无知识持久化、Git 分析、内容语义分析、AI、API 或界面功能。

## 工程基线

- 状态：已建立目录、配置、文档与开发规范基线
- 运行环境：Python 3.11+，无第三方运行时依赖
- 测试框架：Python `unittest`
- 最近验证：2026-08-23，`python3 -m unittest discover -s tests -v`，74 项测试通过
- 版本控制：Git 已纳入 TASK-001 完成流程
- 远端镜像：GitHub `bh8fje/project-atlas` 与群晖 `project-atlas.git`
- 发布规则：所有发布提交必须双推送并分别验证
- 版本规则：每个里程碑使用带备注的 Git 标签，规范见 `docs/VERSIONING.md`
- 执行计划：`EXECUTION_PLAN.md` Version 1.0，状态 ACTIVE

## 下一步

- 开始 TASK-011 Knowledge Storage。
- 不提前实现 TASK-012 Knowledge Query Engine。
