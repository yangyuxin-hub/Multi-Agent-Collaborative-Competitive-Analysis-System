# Claude Code 观察实验 · Cursor 竞品分析

> 用 Claude Code 跑一次 Cursor 竞品分析，**完整记录执行过程 + 错误与调整**，作为本项目主 agent 设计的活体参考样本。

> 本文档同时是**可复用模板** — 跑完 Cursor case 后，可以用同样结构跑 Notion AI / Linear，并最终抽象为 skill。

---

## 一、为什么做这个实验

| 价值 | 说明 |
|------|------|
| 范式同源 | Claude Code 是本项目主 Agent 范式的原型，行为即活的规范文档 |
| Prompt 对照 | 推断 CC 的隐式 prompt，对照 `lead_system.md v0` 找缺漏 |
| Fixture baseline | 输出可作为 `data/fixtures/cursor/` 的 baseline 报告 |
| 验证引用三道防线必要性 | 观察 CC 是否会编造 URL，证明强约束的工程价值 |
| 答辩素材 | "我们对照了 GPT-Researcher（通用 deep research）+ Claude Code（主 agent）两种范式" |

---

## 二、实验设置

### 输入 prompt（喂给 Claude Code）

```
帮我做 Cursor 的竞品分析，要求：

1. 找 4 个直接竞品（AI 编程助手类，建议候选：GitHub Copilot、Windsurf、Cline、Continue）
2. 输出结构化报告，必须包含：
   - 执行摘要
   - 竞品概览表
   - 功能矩阵（横向对比 ✅/⚠️/❌）
   - 定价矩阵（免费版 / 个人 / 团队 / 企业）
   - 用户痛点对比（好评 + 差评）
   - SWOT 分析（针对 Cursor）
   - 战略建议（3-5 条可执行）
3. 每条事实陈述必须带来源 URL，URL 必须是你真实访问过的页面
4. 报告中文，结构化（表格 + 列表）
5. 控制成本和时间，不要无限补搜
6. 中途如果有不确定的（比如视角、地域），用 AskUserQuestion 问我

请开始。
```

### 启动前准备
- [ ] 关闭其他干扰窗口，确保能完整记录
- [ ] 准备好本文档边跑边填
- [ ] 记下开始时间戳

### 观察项 checklist
- [ ] 它先做什么、后做什么（tool call 序列）
- [ ] 多少次 WebSearch、各搜什么 query
- [ ] 多少次 WebFetch、抓哪些 URL、优先级
- [ ] 是否派 Task subagent、什么时机、传什么参数
- [ ] 是否调用 AskUserQuestion、问什么、给什么选项
- [ ] 遇到抓不到的页面怎么处理（重试 / 换路 / 跳过）
- [ ] 报告输出时引用形式（`[1]` / inline URL / 文末列表）
- [ ] 总耗时 + 大致 token / cost 量

---

## 三、实时执行记录（边跑边填）

### 元数据
- 开始时间：`____-__-__ __:__`
- 结束时间：
- CC 版本：
- 模型：

### Tool Call 序列

按顺序记录每个工具调用（不需要完整 input/output，记关键字段即可）：

```
# 编号 | 工具 | 关键输入 | 关键输出 / 观察
01     | AskUserQuestion | 问"视角/地域" | 用户答 "PM/全球"
02     | WebSearch | "Cursor AI editor alternatives 2025" | 返回 10 条
03     | WebFetch | https://cursor.com/pricing | 价格 ...
04     | Task | research_competitor / GitHub Copilot | 子 agent 跑了 X 步...
...
```

### 思考链关键节点

记录 CC 的**关键决策时刻**（不要逐字抄，抓决策点）：

```
- 进入工具循环前: "我需要先确认范围..."（→ 触发 AskUserQuestion）
- 拿到澄清后: "我会先找候选，再逐个研究"（→ 决定流程）
- WebSearch 后: "找到 5 个候选，选其中 4 个最相关"（→ 体现收敛）
- ...
```

---

## 四、错误与调整日志（最重要！）

> 这是本文档的**核心价值** — 记录所有"它做错了什么 + 我（或它自己）怎么调整的"，未来直接避坑。

| # | 时间 | 错误现象 | 根因猜测 | CC 如何应对 / 我的干预 | 启示 / 后续避坑 |
|---|------|---------|---------|---------------------|---------------|
| 1 | 例：WebFetch G2 返回 403 | 反爬 | CC 改用 Tavily 兜底搜结果，跳过 G2 | 我们的 `fetch_page` 失败应返结构化 error 让主 agent 自决 |
| 2 | 例：第 5 次还在搜补充信息 | 收敛纪律弱 | 模型自己没意识 | 必须在 `lead_system.md` 里写硬上限触发条件 |
| 3 |   |   |   |   |   |

**未填项**（实验时遇到再追加）

---

## 五、引用真实性抽查（关键对照）

跑完后，**逐条抽查报告中的事实陈述**：

| 报告中的陈述 | 引用的 URL | 实际访问该 URL | 原文是否支持 | 结论 |
|-------------|-----------|--------------|------------|------|
| 例："GitHub Copilot 企业版 $19/用户/月" | github.com/.../pricing | ✅ 能打开 | ✅ 原文确有此价格 | 引用真实 |
| 例："Windsurf 支持自托管" | windsurf.com | ✅ | ❌ 原文未提及自托管 | **引用幻觉** |

**结果统计**：
- 总事实陈述数：____
- 引用真实数：____
- 引用幻觉数：____
- 幻觉率：____%

> 幻觉率 > 5% → 直接证明你做"引用三道防线"的工程价值。这是答辩级洞察。

---

## 六、对照 `lead_system.md v0` 找缺漏

跑完后，把 CC 的行为与你写的 v0 prompt 逐条对照：

| `lead_system.md v0` 中的纪律 | CC 实际是否遵守 | 缺漏 / 改进点 |
|---------------------------|---------------|-------------|
| 第一步必须 `ask_user` |   |   |
| 5 张卡片回齐立即写报告 |   |   |
| 预算 < 30% 立即出报告 |   |   |
| 禁止凭空构造 URL |   |   |
| `write_section` 每段一次调用 |   |   |
| tool 报错换路而非重试 |   |   |
| 工具调用上限 |   |   |

> 把"CC 没遵守的"作为**你的差异化卖点**：CC 是通用 agent，我们是为竞品分析做了 N 条强约束。

---

## 七、量化对照（更新到差异化文档）

| 维度 | Claude Code | 本项目目标 |
|------|------------|---------|
| 工具调用次数 | __ 次 | ≤ 30 次 |
| WebSearch 次数 | __ 次 | ≤ 8 次（主 1-2 + 5 个 Researcher 各 3）|
| WebFetch 次数 | __ 次 | ≤ 25 次（5 Researcher × 5 页）|
| 子 agent 数量 | __ 个 | 5 个固定 |
| 引用真实率 | __% | 100%（schema 兜底）|
| 总耗时 | __ 秒 | ≤ 90s |
| 总 cost | $__ | ≤ $0.05 |
| 报告字数 | __ 字 | 结构化优先，不追求长 |

---

## 八、产出归档

实验完成后，把以下文件归档到 `data/fixtures/cursor/`：

- [ ] `claude_code_baseline.md` — CC 输出的完整报告
- [ ] `claude_code_trace.md` — 本文档填写完整的副本
- [ ] `claude_code_sources.json` — 它引用的所有 URL（含真实性标注）

---

## 九、提炼到项目（实验后必做）

跑完且分析完，**必须**回写以下文件：

- [ ] `backend/app/agent/prompts/lead_system.md` — 根据"缺漏对照"补充 v0.1
- [ ] `backend/app/agent/prompts/researcher_system.md` — 同上
- [ ] `docs/differentiation-and-related-work.md` — 加入 vs Claude Code 的量化对照
- [ ] `docs/tasks.md` — 阶段 0 这条打勾，更新进度速览

---

## 十、未来 skill 化的接口设计（草稿）

如果这套方法验证有效，可以抽象为一个 skill：`/observe-cc-on-task`

```
输入：
- target_task: 任务描述（如 "做 Notion AI 竞品分析"）
- focus_observations: 重点观察项（默认全部）
- baseline_dir: 产出归档目录（默认 data/fixtures/{slug}/）

工作流：
1. 准备 prompt 模板（基于本文档第二节）
2. 用户在外部 Claude Code 中执行
3. 用户把过程录入本文档结构
4. skill 自动生成对照报告 + 提炼建议
5. 自动 PR 到 prompts/ + differentiation 文档

适用场景：
- 跑多个 case 时复用观察结构
- 新成员入门时学习项目设计的"为什么"
- 评估其他 agent 框架（如 OpenAI Swarm）时同样适用
```

---

## 备注

- 本文档**第一次填**：Cursor case，5/15 ~ 5/17 之间完成
- **第二次跑**：Notion AI case，5/18，复用本结构，对照两个 case 的共性差异
- **第三次跑**：Linear case，仅在前两次跑通后才考虑
- 每跑完一次都更新 `lead_system.md` 一个小版本
