# Project Atlas

Project Atlas 是一个本地优先的 AI 项目知识地图系统，旨在帮助用户长期理解和管理自己的软件项目资产。

当前仓库包含工程基础设施、核心领域契约、本地项目发现、结构分析、稳定身份与指纹、历史与时间线、跨项目关系图，以及显式路径的 SQLite 本地知识存储。尚不包含知识查询引擎、Git 分析、内容语义分析、AI、API 或界面。

## 项目目标

长期规划中的核心能力包括项目发现、项目理解、项目历史重建和项目关系分析。所有能力都必须以明确的 Task 为单位逐步实现，并优先保护本地数据与用户控制权。

## 目录结构

```text
project-atlas/
├── config/              # 配置约定与示例（当前无业务配置）
├── docs/                # 架构、开发与决策文档
├── src/project_atlas/   # Python 领域模型、发现、结构分析与指纹能力
├── tests/               # 自动化测试
├── AGENTS.md            # 协作与 Task 执行规则
├── EXECUTION_PLAN.md    # 长期阶段与 Task 执行计划
├── PROJECT_STATUS.md    # 当前状态和最近验证结果
├── ROADMAP.md           # 阶段路线图
└── pyproject.toml       # 项目及工具配置
```

## 运行环境

- Python 3.11 或更高版本
- Git
- 无第三方运行时依赖

建议使用隔离环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --editable .
```

## 运行测试

无需安装项目也可以执行基础测试：

```bash
python3 -m unittest discover -s tests -v
```

## 本地知识存储

存储路径必须由调用者显式指定，默认拒绝覆盖已有记录：

```python
from datetime import datetime, timezone

from project_atlas.domain import KnowledgeRecord, KnowledgeRecordType
from project_atlas.knowledge import LocalKnowledgeStore

record = KnowledgeRecord.from_payload(
    id="project-1",
    record_type=KnowledgeRecordType.PROJECT,
    project_id="project-1",
    recorded_at=datetime.now(timezone.utc),
    payload={"name": "Project Atlas"},
)

with LocalKnowledgeStore("./data/project-atlas.db") as store:
    store.save(record)
```

数据库只保存在指定的本地文件中。当前版本不提供加密、自动同步或后台采集。

## 开发约定

开始工作前请阅读 [AGENTS.md](AGENTS.md)、[EXECUTION_PLAN.md](EXECUTION_PLAN.md) 与 [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)。项目状态以 [PROJECT_STATUS.md](PROJECT_STATUS.md) 为准，执行阶段以 [EXECUTION_PLAN.md](EXECUTION_PLAN.md) 为准，方向摘要以 [ROADMAP.md](ROADMAP.md) 为准。
