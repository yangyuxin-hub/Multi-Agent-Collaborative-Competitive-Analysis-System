# 差异化定位 & 相关产品/开源项目

> 答辩用素材：证明做的是真实需求 + 在已有方案中做出独特性。

---

## 一、商业产品对照组

| 产品 | 定位 | 价格 | 跟本项目差异 |
|------|-----|------|----------|
| **Crayon** | 企业级 CI 监控，大量竞品追踪 | ~$20-40K/年 | 持续监控为主；本项目做**一次性深度调研**，无登录、轻量 |
| **Klue** | 销售赋能（Battlecard）+ Agentic AI | ~$20-40K/年 | 输出销售话术卡片；本项目输出**结构化分析报告** |
| **Kompyte**（已被 Semrush 收购）| 中端，网站/数字追踪自动化 | $300+/年 | 偏 SEO 营销监控；本项目偏**多维度战略分析** |

**核心差异化**：
1. 它们都是 SaaS 订阅 + 长周期监控；本项目是**输入产品名一次性出报告**
2. 它们封闭黑盒；本项目**多 Agent 过程可视化 + 每条结论可溯源**
3. 它们万元美金起步；本项目**几乎零成本**

---

## 二、开源对标（必须深入研究）

### 🎯 GPT-Researcher — 最相关
- https://github.com/assafelovic/gpt-researcher
- **20K+ star**，开源 deep research agent 标杆
- 已用 **LangGraph + AG2 做多 Agent**，写带引用的长报告
- **要做**：clone 下来跑一次"Notion AI 竞品分析"，截图作为答辩对照

**它的本质：通用研究框架，不是竞品分析专用**
- 输入：任意主题（"AI 对金融业的影响"也行）
- 输出：2000+ 字带引用的叙述性长文
- 架构：planner + N 个 executor + publisher（3 类角色）

**本项目相对差异**：
| 维度 | GPT-Researcher | 本项目 |
|------|--------------|--------|
| 场景 | 任意主题研究 | 垂直竞品分析 |
| 输入 | 自然语言问题 | 产品/公司名 |
| 输出形态 | 叙述性长文 | **结构化对比矩阵 + SWOT + 报告** |
| Agent 设计 | 3 类角色 | 6 个职责显式分工 |
| 过程可视化 | 简单 UI | **Timeline 动画 + 实时澄清** |
| 人机协同 | 无 | **planner 后多选澄清** |
| 决策框架 | 无（纯信息汇总） | **内置功能矩阵/定价矩阵/SWOT** |

### 🎯 LangChain Open Deep Research — 架构参考
- https://github.com/langchain-ai/open_deep_research
- LangChain 官方实现，Deep Research Bench 排名 #6
- **必读**：State 设计、节点拆分、checkpointer 用法可直接借鉴

### 🎯 Local Deep Researcher — 反思循环范本
- https://github.com/langchain-ai/local-deep-researcher
- 实现"搜索→总结→反思缺口→再搜→出报告"循环
- **本项目 reporter gap_filler 子循环**直接参考

### 🎯 Deep Agents — 通用 Agent harness
- https://github.com/langchain-ai/deepagents
- MIT 许可，扩展性强

### 📚 Awesome-Deep-Research
- https://github.com/DavidZWZ/Awesome-Deep-Research
- 资源列表

---

## 三、Multi-Agent 框架对比（2026 市场）

| 框架 | 月搜索量 | 定位 | 选它吗 |
|------|---------|-----|------|
| **LangGraph** | 27,100（第一）| 显式图 + 状态 + checkpointer，**production 首选** | ✅ 已选 |
| **CrewAI** | 14,800 | 角色化 Agent 团队，**易学** | 备选 |
| **AutoGen** | — | 对话式多 Agent，研究/原型 | ❌ 微软已弱化 |
| **OpenAgents** | — | 唯一原生支持 MCP + A2A | ❌ 太新 |

**选 LangGraph 的理由**：图结构稳定 + 状态共享 + checkpointer + human-in-the-loop —— 全是本项目需要的。

---

## 四、答辩三句话定位

> 1. **架构**：垂直竞品分析场景下，LangGraph DAG 显式编排 6 个 Agent，相比 Deep Research 的黑盒循环，**过程可视化、可控、可降级**。
> 2. **人机协同**：planner 后借鉴 Claude Code 的 `AskUserQuestion` 机制做意图对齐，避免"两万字报告跑偏"。
> 3. **工程**：State 分层 + 模型分层 + Prompt Cache，单次成本 5 美分内、90 秒出报告，每条结论可追溯到原始链接。

---

## 五、应对评委可能的提问

### Q1: "GPT-Researcher 已经有了，你做的有啥用？"
> GPT-Researcher 是**通用研究助手**，输出叙述性长文。本项目做**垂直竞品分析**：
> ① **决策导向的结构化输出**（功能矩阵 / 定价矩阵 / SWOT，不是长文）
> ② **过程可视化的六 Agent DAG**（不是黑盒 ReAct loop）
> ③ **planner 后的意图澄清**（避免跑偏）
>
> 本质上是 **GPT-Researcher 的检索能力 + Klue 的决策框架 + Claude Code 的人机协同**三者的交集。

### Q2: "为什么不做成 Claude Code 那种动态 Agent？"
> Claude Code 是**通用工具调用 Agent**，控制流由 LLM 决定，灵活但**过程不可视化、不可预测**——这对编程助手是优点，对答辩 Demo 是缺点。本项目做**垂直 DAG + 关键节点人机协同**：流程固定保证可视化和可控性，在 planner 后借鉴 `AskUserQuestion` 机制做意图对齐——在灵活和可控之间取了适合竞品分析场景的平衡点。

### Q3: "上下文怎么控制？多 Agent 不会爆吗？"
> 我们用 **State 分层**：原始网页落 `./data/snapshots/`，State 只存路径；每个 Agent 只读自己需要的字段；extractor 用 Haiku 4.5 分批并发处理大体量；planner / reporter 用 Prompt Cache。优化后单次任务 ~$0.05、90 秒内出报告，比无脑透传方案省 10 倍。

---

## 六、答辩 PPT 关键页建议

**"赛道全景图"页**：
- 商业：Crayon / Klue / Kompyte（贵 + 黑盒 + 监控为主）
- 开源：GPT-Researcher / Open Deep Research（通用 + 长文 + 无对比矩阵）
- **我们**：垂直 + 可视化 + 结构化对比 + 可溯源 + 人机协同

**"输出对比"页**（视觉冲击力最强）：
- 左侧：GPT-Researcher 输出（一坨长文）
- 右侧：本项目输出（矩阵 + 可视化 + 引用悬浮）

---

## 七、风险提示

⚠️ **GPT-Researcher 很成熟，工程量必须聚焦在它没做的事上**：
- 不要重复造检索 + 长文生成轮子
- All-in 在**结构化矩阵 + 可视化 Timeline + 澄清节点** —— 这是差异化护城河

⚠️ **不要试图"全面碾压"开源项目**：
- 3 周时间不够
- 目标是**在"竞品分析"这个垂直点上做得更深**
