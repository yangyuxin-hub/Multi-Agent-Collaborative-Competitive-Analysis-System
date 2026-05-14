# Integration with Agent System · 与本项目主 Agent 的对接

> 仅项目开发者参考。CC 执行 skill 时不需要读本文件。

## 双轨身份

本 skill 同时是：
- **人调 Claude Code 的可执行 skill**（即时使用）
- **本项目 Lead Analyst agent 的行为基线**（agent 设计的活规范）

跑完三个 case 稳定到 v1.0 后，作为 `backend/app/agent/prompts/lead_system.md` 的**蓝本**。

## 两套实现差异

| 维度 | 本 Skill（人调 CC） | Agent 系统（代码调 SDK） |
|------|------------------|------------------------|
| 引用约束 | 软（prompt 引导）| 硬（`write_section` tool schema 强校验 `source_ids ∈ pool`）|
| Subagent | `Task` 通用类型 | `research_competitor` 专用类型，schema 固定 |
| 澄清机制 | `AskUserQuestion`（CC 内置）| `ask_user` tool + WS interrupt/resume |
| 预算感知 | 模糊（system prompt 提醒）| `check_budget` tool 实时返回 + 拦截器自动 interrupt |
| 进度可视化 | CC 自带 thinking + tool 卡片 | 自建 WS 事件流（嵌套 subagent 卡片 + 预算条）|
| 触发方式 | CC 中说"做 X 竞品分析" | `POST /api/tasks` |

**核心理念**：
- Skill = 方法论的口语化表达，靠模型自律
- Agent = 方法论的工程化封装，靠 tool schema 强约束

## 字段映射

| Skill 概念 | Agent 系统对应 |
|----------|---------------|
| `competitor-card.json` schema | Researcher subagent 返回卡片 |
| Source `used_for` 字段 | `sources_pool` 中的 `source_id` |
| 报告 7 段结构 | `write_section` 调用 7 次 |
| 默认值兜底（30s 超时）| `ask_user` tool 的 default 参数 |
| 工具调用 ≤ 30 次 | `check_budget` 软上限 + token 拦截器硬上限 |

## 同步约定

1. Skill 每次升版 (v0.x → v0.x+1)，必须更新 [CHANGELOG.md](../CHANGELOG.md)
2. 当 Agent 系统编码（5/20 之后）发现 skill 中某条约束**无法用 tool schema 落地**时，回到 skill 调整措辞
3. 当 Agent 系统跑 e2e 测试报告质量下降时，对照 skill 最新版找 prompt 缺漏

## 文件位置约定

| 用途 | 位置 |
|------|------|
| 项目内分发 / git 版本控制 | `skills/competitive-analysis/`（当前位置）|
| 用户本地启用（CC 调用）| `~/.claude/skills/competitive-analysis/` 或 `.claude/skills/competitive-analysis/`（symlink 到当前位置）|
| 编码到 agent system prompt | `backend/app/agent/prompts/lead_system.md`（v1.0 之后同步）|

## 启用方式（对用户）

把项目内的 skill symlink 到 CC 的 skill 目录：

```bash
# macOS / Linux
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/competitive-analysis" ~/.claude/skills/

# Windows PowerShell（管理员）
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\competitive-analysis" -Target "$PWD\skills\competitive-analysis"
```

之后在 CC 中说"做 Cursor 的竞品分析"应能自动触发。
