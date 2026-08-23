# ADR-0019：受控的 Autonomous Project Agent

- 状态：Accepted
- 日期：2026-08-23
- 关联任务：TASK-020

## 背景

Project Atlas 的最终阶段需要主动发现变化、提醒风险并提供建议。但完全无人值守的执行会与 Local First、Human Controlled 和可恢复原则冲突，也会在缺少授权、调度和安全策略时扩大风险。

## 决定

实现 `AutonomousProjectAgent` 的显式观察周期。宿主必须主动调用 `observe`，并提供已经确认的 `ProjectChange` 与 `MultiProjectIntelligence`。Agent 确定性生成变化、共同风险和孤立项目 Signal，以及只读建议。

每个观察周期、Signal、输入引用和时间都可序列化。领域契约强制 `actions_executed == 0`。Agent 不包含调度器、文件扫描、Provider 调用、Command 执行、写入、通知发送或网络访问。

## 后果

- 系统获得可测试、可追踪的主动观察核心，同时保持用户控制。
- 删除变化升级为 WARNING；共同风险和孤立项目产生明确提示。
- “自主”限定为自动解释已提供事实，不代表无人监督地改变外部状态。
- 未来若加入后台调度、通知或自动修复，必须分别获得授权并建立新的安全 ADR。
