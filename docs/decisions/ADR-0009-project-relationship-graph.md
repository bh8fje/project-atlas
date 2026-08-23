# ADR-0009：以显式有向边建立项目关系图

- 状态：Accepted
- 日期：2026-08-23
- Task：TASK-010

## 背景

Project Atlas 需要表达多个软件项目之间的依赖、派生和一般关联。现有 `AssetRelationship` 用于单个项目内部资产，不应混用为跨项目关系；同时当前没有足够证据自动推断项目关系，推断行为也会引入扫描或 AI 范围。

## 决策

建立 `ProjectRelationship`、`ProjectRelationshipGraph` 与 `ProjectRelationshipGraphBuilder`：

- 每个 Project 是图节点，使用稳定 Project ID 标识。
- `ProjectRelationship` 是显式声明的有向边，支持 `DEPENDS_ON`、`GENERATED_FROM`、`RELATED_TO` 和 `UNKNOWN`。
- 图拒绝自引用、重复节点、重复边及指向未知节点的边。
- 节点按 Project ID 排序，边按来源、目标和类型排序。
- 图提供入边和出边查询，并支持完整序列化。

## 边界

- 不扫描依赖文件，不自动发现或推断关系。
- 不合并 `AssetRelationship` 与 `ProjectRelationship`。
- 不提供持久化、图数据库、跨进程同步或查询语言。
- 不调用 Git、AI、API、Dashboard 或 UI。

## 后果

正面影响：

- 项目间关系获得与项目内资产关系分离的稳定契约。
- 图结构具有确定顺序、引用完整性和基础邻接能力。
- TASK-011 可选择存储表示，而无需改变图的领域语义。

限制：

- 所有关系必须由调用者显式提供。
- 当前不计算传递依赖、环路、最短路径或影响范围。
- 图只存在于内存中。
