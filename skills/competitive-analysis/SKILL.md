---
name: competitive-analysis
description: 给定产品名，自主完成竞品调研并产出结构化报告（功能矩阵 + 定价矩阵 + SWOT + 战略建议），每条结论强制带引用来源。当用户说"做 X 的竞品分析"、"分析 X 的竞品"、"X 有哪些对手"等场景时触发。
version: v0
---

# Competitive Analysis Skill

> 主 Agent 范式的竞品分析方法论。
> **双重身份**：① Claude Code 中可直接调用的 skill ② 本项目 agent 设计的活的规范文档。
> 迭代历史见 [CHANGELOG.md](./CHANGELOG.md)。

---

## 何时触发

- "做 X 的竞品分析" / "分析 X 的竞品"
- "X 有哪些对手 / 替代品"
- "X 在 {赛道} 里的定位"
- "对比 X 和 {竞品1, 竞品2}"（已知部分竞品）

**不触发**：单产品功能介绍、用户调研、产品规划（不是竞品分析）

---

## 工作流（5 步）

### 1. 规划（内部 think，≤ 30 秒）
- 判断产品所属赛道
- 列出 5-8 个候选竞品（用先验知识 + 准备搜证实）

### 2. 澄清（强制，**仅一次**）

用 `AskUserQuestion`（或同等机制）问三件事：

| 问题 | 选项 | 默认 |
|------|------|------|
| 报告视角？ | PM / 创业者 / 投资人 / 销售 / 求职研究 | PM |
| 地域焦点？ | 全球 / 国内 / 海外 / 自定义 | 全球 |
| 竞品数量？ | 3 / 5 / 7 | 5 |

**禁止跳过澄清直接搜**。

### 3. 找候选 + 派调研

- WebSearch 1-2 次（"X alternatives" / "X competitors {year}"）找补 + 验证候选名单
- 选定 N 个竞品后，**并发**对每个竞品做调研（Task 子 agent 或顺序处理均可，但要保持隔离）

### 4. 单竞品调研（每个竞品独立）

参考 [`schemas/competitor-card.json`](./schemas/competitor-card.json) 收集这些字段：

- **身份**：name / company / website / one_liner / founded / headquarters / team_size
- **产品**：core_features / feature_flags / platforms / integrations
- **商业**：pricing_tiers / business_model / target_audience / funding / notable_customers
- **口碑**：positive_reviews / negative_reviews / growth_signals

**信息源优先级**：官网 > 评测站（G2/Capterra） > Reddit / HN > 新闻
**单竞品工具上限**：WebSearch ≤ 3、WebFetch ≤ 5

### 5. 综合 + 写报告（按以下结构）

1. **执行摘要** — 3-5 句话总结竞品格局
2. **竞品概览表** — 产品 / 公司 / 定位 / 目标用户
3. **功能矩阵** — ✅ 完整 / ⚠️ 部分 / ❌ 不支持
4. **定价矩阵** — 免费版 / 个人 / 团队 / 企业
5. **用户痛点对比表** — 好评 + 差评
6. **SWOT** — 仅针对**目标产品**（不是所有竞品）
7. **战略建议** — 3-5 条可执行建议

---

## 五大纪律（违反即任务失败）

### 1. 流程纪律
- 第一步必须澄清，**不许跳过**
- 找到 N 个竞品后立即开始调研，**不要继续探索**
- 综合阶段**不再补搜**（除非某竞品的关键字段全缺）

### 2. 预算纪律
- 默认预算：$0.05 / 90 秒（参考值，CC 中实际看模型）
- 总工具调用数硬上限：30 次
- 时间过半时必须开始综合，**不要陷入完美主义**

### 3. 引用纪律 ⭐
- **所有事实陈述必须有真实访问过的 URL 作为依据**
- 不要凭空构造 URL / 编造引用
- 报告中每个结论后标注来源（如 `[github.com/features/copilot]` 或注脚）
- 若某结论无来源支撑，**删除或改为"信息不足，建议进一步调研"**

### 4. 错误纪律
- WebFetch 失败 → 换 URL 而非重试同一个
- 同竞品同字段连续 2 次抓不到 → 标 `null` 跳过
- 整个竞品调研失败 → 在报告中显式声明"X 信息不足"

### 5. 收敛纪律
- 满足任一条件**立即停止调研、开始写报告**：
  - N 个竞品全部完成（部分字段缺失也算）
  - 已用工具调用 ≥ 30
  - 已用时 ≥ 总预算的 70%
- **不要因为"再补一点会更好"而继续**

---

## 输出语言

- 报告全部中文
- 表格字段值保留英文专有名词（产品名 / 公司名）
- 引用 URL 直接 inline（不混淆 source_id 体系）

---

## 严禁事项

- ❌ 跳过澄清直接调研
- ❌ 凭空构造 URL / 编造融资金额 / 编造价格
- ❌ 写自由叙述长文而非结构化矩阵
- ❌ 用模糊词替代具体数据（"很多用户认为..."）
- ❌ 给目标产品做 SWOT 时只写优点

---

## 与本项目 agent 的差异

| 维度 | 本 Skill（人调 CC） | Agent 系统（代码调 SDK） |
|------|------------------|--------------------------|
| 引用约束 | 软（prompt 引导）| 硬（tool schema 强校验）|
| Subagent | Task 通用 | research_competitor 专用 |
| 澄清 | AskUserQuestion | ask_user tool + WS interrupt |
| 预算 | 模糊感知 | check_budget tool 实时 |
| 可视化 | CC 自带 | 自建事件流 |
| 重复使用 | CC 中即调即用 | 部署后 Web 访问 |

Skill 是**方法论的口语化表达**，Agent 是**方法论的工程化封装**。

---

## 案例库（实验产出）

跑通的 case 归档在 [`examples/`](./examples/)，每个 case 包含：
- 完整报告
- 执行过程笔记（tool 序列 + 错误日志）
- 引用真实性审计

| Case | 状态 | 关键发现 |
|------|------|---------|
| Cursor | 待跑（5/15-5/17）| — |
| Notion AI | 待跑（5/18）| — |
| Linear | 待跑（5/19）| — |

---

## 调用方式

在 Claude Code 中：

```
请用 competitive-analysis skill 帮我做 {产品名} 的竞品分析。
```

或直接：

```
做 {产品名} 的竞品分析
```

CC 应自动触发本 skill。
