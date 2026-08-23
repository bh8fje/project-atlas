# Project Atlas 项目状态

## 当前阶段

Phase 0 - Foundation。

TASK-002 COMPLETED。

当前版本：`v0.2.0`。

## 当前能力

- 已定义 `Project` 与 `Task` 核心领域模型。
- 已定义 `ProjectStatus` 与 `TaskStatus` 生命周期状态。
- 已提供基础校验、Task 状态迁移及 JSON 兼容的字典序列化。
- 尚无项目发现、扫描、Git 分析、AI、持久化、API 或界面功能。

## 工程基线

- 状态：已建立目录、配置、文档与开发规范基线
- 运行环境：Python 3.11+，无第三方运行时依赖
- 测试框架：Python `unittest`
- 最近验证：2026-08-23，`python3 -m unittest discover -s tests -v`，12 项测试通过
- 版本控制：Git 已纳入 TASK-001 完成流程
- 远端镜像：GitHub `bh8fje/project-atlas` 与群晖 `project-atlas.git`
- 发布规则：所有发布提交必须双推送并分别验证
- 版本规则：每个里程碑使用带备注的 Git 标签，规范见 `docs/VERSIONING.md`

## 下一步

- 等待用户明确启动后续 Task；不自动开始 TASK-003。
