# 项目文档索引

> 字节 AI 全栈挑战赛 · 多 Agent 协作式竞品分析系统
> 三周冲刺（2026-05-20 → 2026-06-10），文档按"工程 → 设计 → 业务 → 答辩"四层组织。

---

## 一、按角色阅读

### 🆕 新队友 / 第一次看
1. [`../CLAUDE.md`](../CLAUDE.md) — 工程总规范（**先读这个**，10 分钟扫完）
2. [`v1-optimization-plan.md`](./v1-optimization-plan.md) — DAG + 质量门最新决策
3. [`architecture.md`](./architecture.md) — 6 张 Mermaid 视图（整体/工作流/时序/Schema/创新点/State/部署）

### 👨‍💻 后端 / Agent 编排
1. [`../CLAUDE.md`](../CLAUDE.md) §"6 核心 Agent + 2 辅助节点"、§"Agent 统一输出 Schema"、§"API 设计"
2. [`v1-optimization-plan.md`](./v1-optimization-plan.md) §"State 设计"、§"模型分层"、§"质量门"
3. [`architecture.md`](./architecture.md) §2 工作流、§3 时序、§6 State

### 🎨 前端
1. [`../CLAUDE.md`](../CLAUDE.md) §"WebSocket 事件类型"、§"Demo 设计"
2. [`architecture.md`](./architecture.md) §1 整体分层、§3 时序（含 interrupt/resume）
3. [`v1-optimization-plan.md`](./v1-optimization-plan.md) §"clarifier 节点协议"

### 🧠 算法 / Prompt
1. [`competitor-analysis-knowledge.md`](./competitor-analysis-knowledge.md) — 抽什么字段、做什么矩阵的业务依据
2. [`v1-optimization-plan.md`](./v1-optimization-plan.md) §"上下文工程铁则"
3. [`research-questions.md`](./research-questions.md) §二 信息采集与抽取

### 🎤 答辩 / PPT 制作
1. [`differentiation-and-related-work.md`](./differentiation-and-related-work.md) — 差异化定位 + 对照 GPT-Researcher 等开源项目
2. [`../CLAUDE.md`](../CLAUDE.md) §"项目创新点（答辩用）"、§"Demo 设计"
3. [`architecture.md`](./architecture.md) §5 创新点 mindmap

---

## 二、文档清单

| 文档 | 角色 | 状态 | 维护频率 |
|------|------|------|----------|
| [`../CLAUDE.md`](../CLAUDE.md) | 工程总规范（栈/Schema/API/分工/时间节点）| ✅ 现行 | 重要决策变化时同步 |
| [`v1-optimization-plan.md`](./v1-optimization-plan.md) | V1 最终设计（DAG/澄清/质量门/上下文）| ✅ 最新决策 | 锁定，仅 bug 修订 |
| [`differentiation-and-related-work.md`](./differentiation-and-related-work.md) | 答辩素材（对照商业品 + 开源项目）| ✅ | 调研到新项目时补充 |
| [`competitor-analysis-knowledge.md`](./competitor-analysis-knowledge.md) | 业务领域知识（字段/矩阵/视角）| ✅ | 抽取逻辑微调时同步 |
| [`research-questions.md`](./research-questions.md) | 25 个研究问题清单 | 🟡 进行中 | 每个问题答完打勾 |
| [`architecture.md`](./architecture.md) | 7 张 Mermaid 系统视图 | ✅ 同步 v1-plan | 架构变化时同步 |
| [`architecture.html`](./architecture.html) | 架构图浏览器渲染版 | ⚠️ 需重渲染 | architecture.md 改后重生成 |

---

## 三、关键决策快速索引

| 想知道… | 看哪一节 |
|---------|---------|
| 为什么选 LangGraph DAG 而不是 ReAct? | [`v1-optimization-plan.md`](./v1-optimization-plan.md) §二 |
| 跟 GPT-Researcher 的差异是什么? | [`differentiation-and-related-work.md`](./differentiation-and-related-work.md) §二 |
| State 里到底放什么？raw 文档怎么处理? | [`v1-optimization-plan.md`](./v1-optimization-plan.md) §三 + [`architecture.md`](./architecture.md) §6 |
| 哪个 Agent 用 Sonnet 哪个用 Haiku? | [`../CLAUDE.md`](../CLAUDE.md) §"6 核心 Agent + 2 辅助节点" |
| clarifier 怎么和前端通信? | [`../CLAUDE.md`](../CLAUDE.md) §"WebSocket 事件类型" + [`v1-optimization-plan.md`](./v1-optimization-plan.md) §六 |
| 报告里"每条结论可溯源"怎么实现? | [`v1-optimization-plan.md`](./v1-optimization-plan.md) §七 reporter_gate + gap_filler |
| 单次任务成本/延迟目标是多少? | [`../CLAUDE.md`](../CLAUDE.md) §"执行顺序"末段 + [`v1-optimization-plan.md`](./v1-optimization-plan.md) §四 |
| 不同读者关心的报告字段差异? | [`competitor-analysis-knowledge.md`](./competitor-analysis-knowledge.md) §一、§四 |
| Demo 当天网络断了怎么办? | [`../CLAUDE.md`](../CLAUDE.md) §"失败兜底方案" |

---

## 四、维护约定

1. **CLAUDE.md 与 v1-optimization-plan.md 是双锚点**：架构/流程/预算决策的事实来源
2. **architecture.md 跟随 v1-plan**：改 v1-plan 必须同步架构图，并重渲染 `.html`
3. **research-questions.md 的状态字段**：`待研究 / 进行中 / 已结论 / 跳过`，问完更新
4. **新增文档时必须更新本 INDEX.md**：保持单一入口
