# 开发指南

## 环境准备

需要 Python 3.11+ 与 Git。项目当前没有第三方运行时依赖。

可选的本地开发环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --editable .
```

## 测试

从仓库根目录运行：

```bash
python3 -m unittest discover -s tests -v
```

测试应保持确定性，不访问真实网络、用户项目或机器级秘密。每个业务 Task 应为新增行为提供对应测试。

## 提交前检查

1. 确认改动属于当前 Task。
2. 运行完整基础测试。
3. 更新受影响的文档和 `PROJECT_STATUS.md`。
4. 检查 Git diff 与未跟踪文件。
5. 使用简洁、聚焦的提交信息。
