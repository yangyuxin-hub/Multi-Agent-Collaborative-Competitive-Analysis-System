# Playbook · 5 步工作流详解

> SKILL.md 的工作流展开版。CC 在执行调研时按需读取本文件。

## 1. 规划（内部 think，≤ 30 秒）

- 判断产品所属赛道（如 "AI IDE" / "项目管理 SaaS" / "文档协作"）
- 用先验知识列 5-8 个候选竞品
- **不要立刻搜**，先内部成型再去验证

## 2. 澄清（默认 + 自动兜底）

用 `AskUserQuestion` **一次性**提问：

| 问题 | 选项 | 默认 |
|------|------|------|
| 报告视角？ | PM / 创业者 / 投资人 / 销售 / 求职研究 | PM |
| 地域焦点？ | 全球 / 国内 / 海外 / 自定义 | 全球 |
| 竞品数量？ | 3 / 5 / 7 | 5 |

**兜底**：
- 30 秒未回 → 用默认值继续
- 用户回"直接开始"→ 用默认值继续
- 任何使用默认值的情况，**报告开头必须显式声明**：
  > "本报告按 PM 视角 / 全球市场 / 5 个竞品的默认假设产出。"

**不要为细节追问**。澄清只对齐范围。

## 3. 找候选 + 补全（1-2 次 WebSearch）

- 推荐 query：`"X alternatives"` / `"X competitors {year}"` / `"top {category} tools"`
- 把搜索结果与第 1 步先验候选名单**去重合并**
- 选定 N 个最直接的竞品（按澄清的数量）
- **找到就停**，不要继续探索性搜索

## 4. 单竞品调研

**每个竞品独立调研**。推荐用 `Task` 子 agent 隔离上下文（避免原始网页噪声污染主线程），不用子 agent 也可以顺序处理但要分块清晰。

### 单竞品流程

1. **WebSearch** 1-3 次找关键 URL（官网 / pricing / 评测 / Reddit）
2. **WebFetch** 选最重要的 3-5 个 URL（按优先级）
3. **抽取字段** 填 [competitor-card.json](../schemas/competitor-card.json)

### 信息源优先级

```
官网首页 / pricing 页    ← P0，必抓
评测站（G2/Capterra/PH） ← P0
Reddit / HackerNews     ← P1，挖差评
官方博客 / 招聘页        ← P1，找增长信号
新闻 / TechCrunch       ← P2
```

### 单竞品工具硬上限

- WebSearch ≤ 3 次
- WebFetch ≤ 5 次

超限立即停止该竞品调研，已抽到的字段照常返回，未抽到的标 `null` + 加入 `gaps`。

### 字段优先级（预算紧时按此砍）

- **P0**（必抓）：`name` / `website` / `one_liner` / `core_features` / `pricing_tiers`
- **P1**（应抓）：`feature_flags` / `target_audience` / `positive_reviews` / `negative_reviews`
- **P2**（有则抓）：`founded` / `team_size` / `funding` / `notable_customers` / `growth_signals`

## 5. 综合 + 写报告

**进入综合阶段后**：
- ✅ 允许为已选竞品**补搜关键缺失字段**（pricing / official features / negative reviews），**补搜总次数 ≤ 3**
- ❌ 禁止扩展新竞品
- ❌ 禁止再做探索性 search

**写报告时**：
- 按 [output-spec.md](./output-spec.md) 7 段结构产出
- 每段独立写完再写下一段，**不要交叉跳跃**
- 事实陈述必带 inline URL；分析判断必须基于前文引用的事实
- 表格优先于段落，段落优先于自由叙述

## 满足任一条件 → 立即停止调研、开始写报告

- N 个竞品全部完成（即使部分字段缺失）
- 总工具调用次数 ≥ 30
- 已用时间 ≥ 总预算的 70%

**不要陷入"再补一点会更好"**。结构化产出 > 信息完美。
