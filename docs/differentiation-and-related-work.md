# 差异化定位 & 相关产品

> 答辩素材。证明做的是真实需求 + 在已有方案中做出独特性。

## 一、商业产品对照

| 产品 | 定位 | 价格 | 差异 |
|------|------|------|------|
| Crayon | 企业 CI 监控，长周期追踪 | $20-40K/年 | 持续监控；本项目**一次性深度调研** |
| Klue | 销售赋能 Battlecard + Agentic AI | $20-40K/年 | 输出销售话术；本项目输出**结构化分析报告** |
| Kompyte | 网站/数字追踪自动化 | $300+/年 | SEO 监控为主；本项目偏**多维战略分析** |

**核心差异**：它们 SaaS 订阅 + 长周期监控 + 黑盒；本项目**一次输入即出报告 + 过程可视化 + 每条结论可溯源 + 几乎零成本**。

## 二、开源对标

### GPT-Researcher（最相关，必须深入研究）
- https://github.com/assafelovic/gpt-researcher · 20K+ star
- 通用研究 agent：任意主题 → 2000+ 字带引用长文
- 架构：planner + N executor + publisher

| 维度 | GPT-Researcher | 本项目 |
|------|--------------|--------|
| 场景 | 任意主题研究 | **垂直竞品分析** |
| 输出 | 叙述性长文 | **结构化矩阵 + SWOT** |
| 架构 | 预定义角色循环 | **Claude Code 风格 主 Agent + 专用 subagent** |
| 引用 | 文末列表 | **三道防线 + 悬浮溯源** |
| 人机协同 | 无 | **主 agent 自主调用澄清** |
| 可视化 | 简单 UI | **事件流 + 嵌套 subagent + 预算条** |

**5/20 必须 clone 跑一次 Notion AI 调研，截图对照**。

### 其他参考
- **LangChain Open Deep Research** — Deep Research Bench #6，state 设计可参考
- **Local Deep Researcher** — 搜索→反思→再搜循环，主 agent 缺字段补抓的思路源头
- **Claude Code** — 主 Agent + Tools + Task() subagent 范式的标杆，直接借用

## 三、为什么不直接用 Claude Code

| 维度 | Claude Code | 本项目 |
|------|-----------|--------|
| 任务范围 | 通用编程 | 垂直竞品分析 |
| 工具集 | bash/file/grep 等 | 专项化 6 个工具（含 search/extract/write_section）|
| Subagent | 通用 Task | 仅 1 类 research_competitor，schema 固定 |
| 输出 | 自由文本 | 强约束结构化报告 + 引用追踪 |
| 用户介入 | 命令行问答 | **主 agent 自主调用 ask_user 弹多选卡片** |
| 评估 | 不适用 | 三个验收 case + baseline 比对 |

**一句话**：Claude Code 是范式，本项目是这个范式在"竞品分析"任务上的产品化。

## 四、答辩三句话定位

1. **架构**：Claude Code 范式专项化 — Agent SDK 主循环 + 1 类专用 subagent，比预定义 DAG 灵活、比通用 agent 可控。
2. **工程**：引用追踪三道防线（tool 入口分配 source_id + write_section schema 校验 + 前端二次校验），从根本上消除 URL 幻觉。
3. **协同**：主 agent 自主判断何时调用 `ask_user` 澄清，不预定义节点；事件流可视化思考链 + 嵌套 subagent + 实时预算条。

## 五、应对评委可能的提问

**Q: "GPT-Researcher 已经有了，做这个有啥用？"**
> GPT-Researcher 是**通用研究助手**，输出叙述性长文。本项目做**垂直竞品分析**：① 决策导向的结构化输出（功能矩阵 / 定价矩阵 / SWOT）② Claude Code 式主 Agent + 专用 subagent，比预定义角色更灵活 ③ 引用追踪三道防线，从根本上消除 URL 幻觉。

**Q: "为什么不用 LangGraph DAG？流程更可控。"**
> DAG 把 agent 的决策路径硬编码，本质用工程兜底模型能力。Claude Code 已证明主 Agent 自主规划 + 工具调用 + 子 agent 并发的范式可工业化。我们的可控性不靠 DAG，而靠：tool schema 强约束 + 预算自感知 + 主 agent system prompt 引导 + 8 分钟硬超时降级。

**Q: "上下文怎么控制？多 agent 不会爆吗？"**
> 主 agent 只看 subagent 返回的结构化卡片，**不看原始网页**（噪声留在 subagent 独立 thread）。Prompt Caching 缓存 system prompt 大头（目标命中 > 70%）。单任务预算 ≤ $0.05，端到端 90s 内。

## 六、答辩 PPT 关键页

**"赛道全景"页**
- 商业：Crayon / Klue（贵 + 黑盒 + 监控为主）
- 开源：GPT-Researcher / Open Deep Research（通用 + 长文 + 无结构化对比）
- 范式：Claude Code（通用编程 agent）
- **我们**：Claude Code 范式 × 竞品分析垂直场景 × 引用追踪 × 事件流可视化

**"输出对比"页**（视觉冲击力最强）
- 左：GPT-Researcher 输出（一坨叙述长文）
- 右：本项目输出（功能矩阵 + 定位象限 + 悬浮引用）

## 七、风险提示

⚠️ GPT-Researcher 很成熟，工程量必须聚焦在它没做的事上：
- 不重复造检索 + 长文生成轮子
- All-in 在**结构化矩阵 + 事件流可视化 + 自主澄清 + 引用三道防线**

⚠️ 不试图全面碾压开源项目，3 周不够。目标是**在"竞品分析"垂直点上做得更深**。
