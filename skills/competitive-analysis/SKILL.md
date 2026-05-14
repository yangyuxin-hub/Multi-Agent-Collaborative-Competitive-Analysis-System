---
name: competitive-analysis
description: Use when the user asks for competitive analysis of a specific product, company, or industry. Triggers include "做 X 的竞品分析", "分析 X 的竞品", "X 的对手 / 替代品", "X vs Y 对比", "X 有哪些竞争对手". Not for single-product feature reviews, user research, or product roadmap planning.
---

# Competitive Analysis

## Overview

给定一个产品名，调研其直接竞品并产出**结构化、可决策、关键事实必带引用**的对比报告。核心原则：**结构化 > 叙述长文，引用真实 > 看起来完整**。

## When to Use

**适用症状**
- 用户输入一个产品 / 公司 / 行业关键词，想知道"对手是谁、强弱在哪、怎么打"
- 需要功能矩阵 / 定价矩阵 / SWOT / 战略建议这类**决策导向**的输出
- 报告需要可溯源（每条事实能追到原始 URL）

**不适用**
- 单产品的功能介绍（用户没问对比）
- 用户调研 / 产品规划 / 用户访谈
- 实时监控竞品动态（这是周期任务，本 skill 是一次性深度调研）

## Workflow

5 步流程，详见 [reference/playbook.md](./reference/playbook.md)：

1. **规划** — 内部 think，列出 5-8 个候选竞品（≤ 30 秒）
2. **澄清** — `AskUserQuestion` 问视角 / 地域 / 数量（30s 超时用默认值 + 报告头声明）
3. **找候选** — `WebSearch` 1-2 次验证 + 补全候选名单
4. **单竞品调研** — 对每个竞品独立调研（建议 `Task` 子 agent 隔离上下文），收集 [competitor-card](./schemas/competitor-card.json) 字段
5. **综合 + 写报告** — 按 [reference/output-spec.md](./reference/output-spec.md) 7 段结构产出 **同时输出 `.md` 和 `.html`**（HTML 含 Mermaid 定位象限图 + SWOT 2×2 网格 + 定价条形对比，见 [reference/html-template.md](./reference/html-template.md)）

## Five Disciplines（违反即失败）

| # | 纪律 | 关键约束 |
|---|------|---------|
| 1 | 流程 | 第一步必澄清；找到候选立即调研，不再扩展 |
| 2 | 预算 | 工具调用 ≤ 30 次；时间过半必须开始综合 |
| 3 | 引用 | **事实必有 URL，分析判断基于事实**；禁构造 URL |
| 4 | 错误 | 失败换路而非重试同输入；连续 2 次失败标 `null` |
| 5 | 收敛 | 综合阶段禁扩竞品；补搜关键字段 ≤ 3 次 |

完整版见 [reference/disciplines.md](./reference/disciplines.md)。

## Quick Reference

**报告必含 7 段**

```
1. 执行摘要 → 2. 竞品概览表 → 3. 功能矩阵 → 4. 定价矩阵
→ 5. 用户痛点对比 → 6. 目标产品 SWOT → 7. 战略建议
```

**单竞品工具上限**：WebSearch ≤ 3 / WebFetch ≤ 5

**引用分层**

| 内容类型 | 引用要求 |
|---------|---------|
| 事实（定位 / 功能 / 价格 / 融资 / 客户 / 评价 / 团队） | 必须有真实访问过的 URL |
| 分析结论（SWOT / 差异化 / 战略建议 / 定位象限） | 不需逐句引用，但必须基于前文引用过的事实 |

**报告语言**：中文；产品 / 公司 / 套餐名保留英文。

## Common Mistakes

| ❌ 错误 | ✅ 正确 |
|--------|--------|
| 跳过澄清直接调研 | 必须先 `AskUserQuestion`，超时用默认值并在报告头声明 |
| 凭空构造 URL / 编造价格 / 编造融资 | 不确定就标 "信息不足"；价格信息必须来自官网 pricing 页或显式标 "未公开" |
| 输出自由叙述长文 | 强制 7 段表格化结构，叙述只在执行摘要和战略建议段 |
| 给目标产品 SWOT 只写优点 | S/W/O/T 必须各 ≥ 2 条；差评和威胁不可空 |
| 综合阶段反复补搜 | 补搜 ≤ 3 次，超过即用现有数据出报告 |
| 用 "many users believe" 类模糊词 | 必须 "Reddit 用户 X 评论..."（带 source）或不写 |

## Output Acceptance Criteria

详见 [reference/output-spec.md](./reference/output-spec.md#acceptance)。核心 6 条：

- ≥ 3 个竞品（默认 5）
- 7 段全齐
- 每竞品 ≥ 2 来源，其中 ≥ 1 官方
- 定价来自官网或标"未公开"
- 差评不可空，不足须显式声明
- 若用了澄清默认值，报告头必须声明

## Reference Files

- [reference/playbook.md](./reference/playbook.md) — 工作流详细步骤
- [reference/disciplines.md](./reference/disciplines.md) — 五大纪律完整版
- [reference/output-spec.md](./reference/output-spec.md) — 报告 7 段细节 + 验收 + **双格式产出（md + html）+ Source 结构**
- [reference/html-template.md](./reference/html-template.md) — HTML 报告模板（Mermaid 象限图 / SWOT 网格 / 定价条形 / 战略卡片）
- [reference/integration.md](./reference/integration.md) — 与本项目 agent 系统的对接（开发者参考）
- [schemas/competitor-card.json](./schemas/competitor-card.json) — 单竞品 JSON Schema
- [CHANGELOG.md](./CHANGELOG.md) — 版本迭代历史

## Examples

跑通的 case 归档在 `examples/`：

| Case | 状态 |
|------|------|
| Cursor | 待跑（5/15-5/17）|
| Notion AI | 待跑（5/18）|
| Linear | 待跑（5/19）|
