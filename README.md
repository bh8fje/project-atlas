# Project Atlas

Project Atlas 是一个本地优先的 AI 项目知识地图系统，旨在帮助用户长期理解和管理自己的软件项目资产。

当前仓库包含工程基础设施、核心领域契约、本地项目发现、受限的项目结构分析、稳定的本地项目身份和元数据指纹、历史契约，以及基于显式结构输入的变化检测。尚不包含时间线、Git 分析、内容语义分析、AI、数据库、API 或界面。

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

## 开发约定

开始工作前请阅读 [AGENTS.md](AGENTS.md)、[EXECUTION_PLAN.md](EXECUTION_PLAN.md) 与 [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)。项目状态以 [PROJECT_STATUS.md](PROJECT_STATUS.md) 为准，执行阶段以 [EXECUTION_PLAN.md](EXECUTION_PLAN.md) 为准，方向摘要以 [ROADMAP.md](ROADMAP.md) 为准。
