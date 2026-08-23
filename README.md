# Project Atlas

Project Atlas 是一个本地优先的 AI 项目知识地图系统，旨在帮助用户长期理解和管理自己的软件项目资产。

当前仓库已完成 Execution Plan 1.5：除工程基础、项目理解、历史、知识、界面和多语言能力外，还可通过本机服务选择项目目录、识别其中的软件项目并定时检查结构变化。仓库仍不内置具体模型适配器、Git commit 分析、公网服务或外部 API。

## 项目目标

长期规划中的核心能力包括项目发现、项目理解、项目历史重建和项目关系分析。所有能力都必须以明确的 Task 为单位逐步实现，并优先保护本地数据与用户控制权。

## 目录结构

```text
project-atlas/
├── config/              # 配置约定与示例（当前无业务配置）
├── dashboard/           # 独立构建的本地 Dashboard
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
- Node.js 22.13 或更高版本（仅 Dashboard 开发与构建）
- Git
- Python Core 无第三方运行时依赖

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

## 本地 Dashboard 与项目目录

首次使用先安装 Dashboard 依赖：

```bash
npm --prefix dashboard install
```

之后在仓库根目录运行：

```bash
./scripts/start-local.sh
```

打开 `http://localhost:3000/`。在“项目目录”中点击“选择目录”，即可通过操作系统选择器指定扫描范围。系统会立即识别其中的软件项目；用户还可以手动检查，或明确开启 15、30、60 分钟的自动检查。

Dashboard 的项目目录功能只连接 `127.0.0.1` 上的 Project Atlas 本机服务。目录路径、项目基本资料、结构指纹和检查结果只保存在本机；关闭本机服务后自动检查停止。移除目录不会删除用户文件。详细说明见 [docs/LOCAL_WORKSPACES.md](docs/LOCAL_WORKSPACES.md)。

生产构建可在 `dashboard/` 运行 `npm run build`。移动浏览器可使用窄屏导航并将页面添加到主屏幕；项目不会自动建立公网入口或云同步。

界面支持中文、英语、俄语和韩语。用户未选择时自动跟随系统语言，不受支持的系统语言回退英语；显式选择只保存在当前浏览器，选择“跟随系统”即可清除偏好。

产品文案先用专业、清晰的中文确定含义，避免难懂术语和过度口语化，再翻译其他语言。具体规范见 [docs/PRODUCT_LANGUAGE.md](docs/PRODUCT_LANGUAGE.md)。

Dashboard 必须区分发布记录、项目组成和本机检查结果，不展示没有数据支持的运行结论。具体原则见 [docs/DASHBOARD_DESIGN.md](docs/DASHBOARD_DESIGN.md)。

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

本地查询支持 Project、类型、时间范围和数量限制，也支持不调用 AI 的关键词匹配：

```python
from project_atlas.knowledge import KnowledgeQueryEngine

with LocalKnowledgeStore("./data/project-atlas.db") as store:
    result = KnowledgeQueryEngine(store).search("Project Atlas")
```

关键词查询要求所有词项都出现在记录元数据或 JSON 数据中，不代表语义理解。

`AIContextBuilder` 可将调用者选定的知识记录整理为本地上下文。它会按敏感字段名递归脱敏并执行字符上限，但不会调用任何 AI 服务。

`AIProjectUnderstandingService` 只在调用者显式执行时调用所注入的 `AIProvider`。仓库不内置模型账号、密钥、端点或自动重试；Provider 实现由部署方选择。

`AIProjectAssistant` 使用同一可替换 Provider 回答单个项目问题。它不会保存会话、执行建议或修改项目。

`CommandCenter` 为宿主应用提供统一的进程内命令入口。命令必须显式注册；声明为变更型的命令必须在请求中明确确认，否则不会调用 Handler。仓库不内置 Shell 或远程执行命令。

`MultiProjectIntelligenceService` 可将调用者明确提供的多个项目、对应理解结果与关系图聚合为组合概览。它确定性计算共同风险、关系数量和孤立项目，不重新扫描、不调用 AI，也不保存结果。

`AutonomousProjectAgent` 由宿主显式触发，将已提供的变化与组合风险转换为提醒和建议。观察周期可追踪且强制零执行动作；当前没有后台调度、自动修改或通知发送。

## 开发约定

开始工作前请阅读 [AGENTS.md](AGENTS.md)、[EXECUTION_PLAN.md](EXECUTION_PLAN.md) 与 [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)。项目状态以 [PROJECT_STATUS.md](PROJECT_STATUS.md) 为准，执行阶段以 [EXECUTION_PLAN.md](EXECUTION_PLAN.md) 为准，方向摘要以 [ROADMAP.md](ROADMAP.md) 为准。
