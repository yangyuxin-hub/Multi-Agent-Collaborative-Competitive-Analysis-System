# Spec & Tasks Checklist

> 按 CLAUDE.md 时间节点对齐，每阶段含 **Spec（做什么 + 验收）** 与 **Tasks（勾选项）**。
> 优先级：🔴 P0 必做 / 🟡 P1 应做 / 🟢 P2 可延后。
> 状态：`- [ ]` 未开始 / `- [x]` 完成 / `- [~]` 进行中 / `- [-]` 跳过。

---

## 📍 当前进度速览（每次工作前/后更新）

- **今天日期**：2026-05-14
- **当前阶段**：阶段 0 — 开工前准备（5/19 前完成）
- **下一步要做**：
  1. 注册 Anthropic / Tavily / Serper key + 写 `.env.example`
  2. 跑 Notion AI 竞品分析（skill v0.3 实战，复用 Cursor case 改进路径）
  3. 注册部署平台账号（Vercel / Render / Neon）
- **最近完成**：Cursor 竞品分析 baseline + skill v0.2 实战验证（21 个工具调用，发现 6 处改进点）
- **最近一次卡点**：（无）
- **风险触发**：（无）

> 切换上下文 / 新会话开始时，先看这里 + 阶段 0 / 当前阶段勾选状态即可恢复进度。

---

## 阶段 0 ｜ 5/19（开工前一天）准备

**Spec**：把 prompt / fixture / 风险评估准备好，5/20 当天能直接开工。

- [x] 🔴 写 `prompts/lead_system.md` 草稿 v0（5 大纪律：流程/预算/引用/错误/收敛）
- [x] 🔴 写 `prompts/researcher_system.md` 草稿 v0（含工具上限 + 返回 schema 示例）
- [ ] 🔴 注册 Anthropic / Tavily / Serper API key，写入 `.env.example`
- [x] 🔴 **用 Claude Code 跑一次 Cursor 竞品分析**（已完成 2026-05-14）
  - [x] 输出归档到 `data/fixtures/cursor/claude_code_baseline.md`
  - [x] 案例笔记 `skills/competitive-analysis/examples/cursor.md`（含执行统计 + 6 处问题与启示）
  - [x] CHANGELOG 加入 v0.3 待办（6 处改进点）
  - [ ] **待人工**：引用真实性抽查 5 条事实
  - [ ] **待人工**：把 v0.3 改进点应用到 SKILL.md / reference/
- [ ] 🟡 clone GPT-Researcher 跑一次 Notion AI 调研，截图存档（另一种范式对照组）
- [ ] 🟡 选定部署平台：前端 Vercel + 后端 Render + Neon PG，账号注册
- [ ] 🟢 与队友（如有）对一次 prompt 草稿

---

## 阶段 1 ｜ 5/20 ｜ Agent SDK 三件事验证

**Spec**：当天必须验证 Claude Agent SDK 能否支撑核心架构。**任何一项不通就退回 Anthropic SDK 手撸**。

**验收**：跑通一个最小 demo，输出包含 ① 主 agent 用 1 个 mock tool ② spawn 1 个 mock subagent ③ tool 内部 raise interrupt 暂停 ④ WS 推 SDK 事件 ⑤ resume 后继续。

- [ ] 🔴 安装 Agent SDK + 跑官方 hello-world
- [ ] 🔴 验证 `tool_use` loop 能跑（最简 echo tool）
- [ ] 🔴 验证 spawn subagent 能 await 结果
- [ ] 🔴 验证 tool 内部异步 await（interrupt 兜底方案：raise 特殊异常 → FastAPI 捕获 → WS → resume → replay）
- [ ] 🔴 验证 SDK 事件流能完整取到（text_delta / tool_use / task_spawn / task_result）
- [ ] 🔴 验证 prompt caching 生效：检查 `usage.cache_read_input_tokens > 0`
- [ ] 🔴 把上面 5 项写成 `tests/integration/test_sdk_smoke.py`，每天回归
- [ ] 🟡 项目脚手架：FastAPI + WS + PG + Next.js 空壳跑通

---

## 阶段 2 ｜ 5/21-5/23 ｜ 后端骨架 + Tools

**Spec**：6 个 tools 全实现（先 mock 数据），主 agent 用 mock tools 跑通端到端"输入 → 澄清 → 调研 → 写报告" mock 流程。

**验收**：`POST /api/tasks` 触发主 agent，事件流通过 WS 推出，最终落 `report.md`（内容是 mock，但流程完整）。

### Tools 实现

- [ ] 🔴 `core/sources_pool.py`：内存 + PG JSONB，分配/查询 source_id
- [ ] 🔴 `core/budget_tracker.py`：token / cost / 时间累计，超 $0.04 触发软警告，超 $0.05 触发硬 interrupt
- [ ] 🔴 `core/event_bus.py`：SDK 事件 → WS，带 seq 编号 + PG 持久化
- [ ] 🔴 `tools/search.py`：web_search（先 mock 固定结果）
- [ ] 🔴 `tools/fetch.py`：fetch_page（先 mock）
- [ ] 🔴 `tools/extract.py`：extract_fields（先 mock 返回 Researcher schema）
- [ ] 🔴 `tools/ask_user.py`：interrupt 实现（asyncio.Event + 30s 兜底 default）
- [ ] 🔴 `tools/write_section.py`：**source_ids 强校验**（非空 + ∈ pool）
- [ ] 🔴 `tools/budget.py`：check_budget tool
- [ ] 🟡 所有 tool 用 Pydantic 校验输入输出
- [ ] 🟡 失败统一返结构化 error，不抛异常

### Agent 装配

- [ ] 🔴 `agent/lead.py`：装配 SDK + system prompt + 6 tools
- [ ] 🔴 `agent/researcher.py`：定义 subagent，工具子集（search/fetch/extract）
- [ ] 🔴 主 agent 端到端 mock 跑通（不调真实 API）
- [ ] 🟡 单元测试：每个 tool 独立可测

### API

- [ ] 🔴 `POST /api/tasks` 创建任务，返回 task_id，background 启动 agent
- [ ] 🔴 `WS /ws/tasks/{id}` 订阅事件流，含 reconnect last_seq 补推
- [ ] 🟡 `GET /api/tasks/{id}` 查任务状态 + 事件流回放
- [ ] 🟡 `GET /api/reports/{id}` / `/pdf`

---

## 阶段 3 ｜ 5/24-5/27 ｜ 接真实 API + 引用三道防线

**Spec**：所有 tool 接真实 API（Tavily / Haiku / Anthropic），三个 case 端到端跑通，**报告 100% 结论带 source，预算 ≤ $0.05**。

**验收**：`pytest tests/e2e/` 三个 case 全绿，断言：
- 主 agent 成功调用 `ask_user` 至少 1 次
- 5 个 Researcher subagent 全部 spawn
- 报告内所有 `[ref:src_xxx]` 均在 sources_pool 中
- 单任务总 cost ≤ $0.05、wall time ≤ 90s（happy path）

- [ ] 🔴 `web_search` 接 Tavily（兜底 Serper）
- [ ] 🔴 `fetch_page` 接 BS4 + readability，反爬失败返结构化 error
- [ ] 🔴 `extract_fields` 接 Haiku 4.5，schema 用 Pydantic
- [ ] 🔴 主 agent + Researcher 接真实 Sonnet 4.6
- [ ] 🔴 Prompt Caching 启用，验证命中率 > 50%（5/27 目标 70%）
- [ ] 🔴 引用三道防线**集成测试**：
  - [ ] 防线 ①：web_search/fetch_page 必返 source_id 且写入 pool
  - [ ] 防线 ②：write_section 注入伪造 source_id 必须报错
  - [ ] 防线 ③：前端渲染池外 id 显示 ⚠️
- [ ] 🔴 三个 fixture 落地：
  - [ ] `data/fixtures/notion_ai/{task,researcher_cards,sources_pool,report,events}.json/md/jsonl`
  - [ ] `data/fixtures/cursor/...`
  - [ ] `data/fixtures/linear/...`
- [ ] 🔴 e2e 测试三个 case 全绿
- [ ] 🟡 token / cost 监控面板（开发用）
- [ ] 🟡 主 agent 系统 prompt v1 调优（依据三个 case 跑偏情况）

---

## 阶段 4 ｜ 5/28-5/31 ｜ 前端事件流可视化

**Spec**：Claude Code 式事件流前端完成，Demo 视觉到位。

**验收**：浏览器输入产品名 → 看到主 agent 思考链 + tool 卡片 + 嵌套 5 个 Researcher 卡片 + 预算条实时更新 + 澄清 Modal + 报告悬浮引用 + 一键下载 PDF。

- [ ] 🔴 `EventStream/` 核心组件
  - [ ] `TextDelta.tsx` 思考链气泡
  - [ ] `ToolUseCard.tsx` 工具调用卡片（输入/输出折叠）
  - [ ] `SubagentCard.tsx` 嵌套 subagent 卡片，独立进度
  - [ ] `InterruptModal.tsx` 澄清多选弹窗（30s 倒计时）
  - [ ] reducer 状态机：处理乱序 / 嵌套深度 / 重连补推
- [ ] 🔴 `BudgetMeter/` 顶部预算条（$ + 时间 + token）
- [ ] 🔴 `ReportViewer/`
  - [ ] react-markdown 渲染
  - [ ] `[ref:src_xxx]` 解析为 Tooltip 组件
  - [ ] 池外 id 渲染为 ⚠️
- [ ] 🔴 `ComparisonTable/` 功能矩阵 + 定价矩阵
- [ ] 🟡 定位象限图（Recharts 散点图）
- [ ] 🟡 离线事件流回放模式（开发 + Demo 兜底）
- [ ] 🟡 WS 断线重连 + last_seq 补推前端实现
- [ ] 🟢 加载/失败状态/空状态打磨

---

## 阶段 5 ｜ 6/1-6/3 ｜ 报告质量调优

**Spec**：三个 case 报告质量稳定（同 case 多次跑差异可接受），符合"决策导向 + 结构化"标准。

**验收**：
- 每个 case 跑 5 次，关键字段（竞品名 / 定价 / 核心功能）一致率 ≥ 80%
- 人工评审：报告"专业感"评分 ≥ 4/5（参照艾瑞标准）
- SWOT / 矩阵 / 象限三件套齐全

- [ ] 🔴 主 agent prompt v2 调优：报告模板、SWOT 框架、引用规则
- [ ] 🔴 Researcher prompt v2 调优：返回 schema 完整度
- [ ] 🔴 few-shot 例子写入 prompt（Cursor 的标杆报告片段）
- [ ] 🔴 温度调低至 0.2，稳定性优先
- [ ] 🔴 后处理校验：Haiku 二次审查段落与 source_ids 语义是否匹配
- [ ] 🟡 三个 case baseline 报告人工写出，作为 LLM-as-judge 对比基准
- [ ] 🟡 报告质量 5 次重复 e2e 测试
- [ ] 🟢 加入"按视角切换字段权重"（PM/创业者/投资人/销售）

---

## 阶段 6 ｜ 6/4-6/5 ｜ PDF + Demo 数据

**Spec**：PDF 导出可用，三个 case 离线事件流缓存就位。

**验收**：
- 三个 case 都能导出 PDF，中文字体正确、表格不分页错位
- 离线模式：网络断开下能完整回放任一 case 的事件流和报告

- [ ] 🔴 WeasyPrint Markdown → HTML → PDF
- [ ] 🔴 思源黑体打包到 Docker / Render 部署
- [ ] 🔴 PDF 三个 case 实测，修复字体掉字 / 表格截断
- [ ] 🔴 `events.jsonl` 三个 case 录制 + 离线回放工具
- [ ] 🔴 部署到 Vercel + Render + Neon，演示链接可访问
- [ ] 🟡 演示模式开关：`?demo=cursor` 直接走离线回放
- [ ] 🟡 Render 免费档防 sleep（定时 ping）

---

## 阶段 7 ｜ 6/6-6/9 ｜ 功能冻结 + 答辩准备

**Spec**：代码冻结，只修 bug；输出答辩物料。

- [ ] 🔴 答辩 PPT
  - [ ] 赛道全景图（vs 商业 / vs 开源 / vs Claude Code）
  - [ ] 架构图（5 张 Mermaid 之精选）
  - [ ] 输出对比页（vs GPT-Researcher 视觉冲击）
  - [ ] 引用追踪三道防线讲解页
  - [ ] Demo 流程截图
- [ ] 🔴 录制演示视频 3-5 分钟（含离线兜底版本）
- [ ] 🔴 答辩 Q&A 演练（5 个高频提问对答）
- [ ] 🔴 离线兜底全链路测试：拔网线能演示
- [ ] 🟡 README 完善（含演示链接、架构图、技术亮点）
- [ ] 🟡 排查 PG / Render / Vercel 各环境配置

---

## 阶段 8 ｜ 6/10 ｜ 提交

- [ ] 🔴 代码仓库整理：清理临时文件、补 README 截图
- [ ] 🔴 演示视频上传
- [ ] 🔴 部署链接最终检查（演示前 1 小时手动跑一次）
- [ ] 🔴 文档检查：CLAUDE.md / architecture.md / differentiation 一致性
- [ ] 🔴 提交！

---

## 横切关注点（贯穿全程）

### 每日纪律
- [ ] 每天能跑通端到端（mock 也算）
- [ ] commit 前跑 `pytest tests/e2e/`
- [ ] commit message 描述清楚

### 风险预案触发
- [ ] 🚨 5/20 SDK 三件事任一不通 → 当天决定退回 Anthropic SDK 手撸
- [ ] 🚨 5/27 三个 case 报告质量极差 → 6/3 前必须修复或砍掉 1 个 case
- [ ] 🚨 6/3 前端事件流复杂度超预期 → 砍嵌套 subagent 卡片，简化为线性时间轴
- [ ] 🚨 6/5 部署失败 → 切本地演示 + 录屏兜底

### 上下文 / Prompt 工程专项
- [ ] 主 agent 单次任务历史 ≤ 40k token（含 cache 部分）
- [ ] Researcher 单次任务 ≤ 8k token
- [ ] Prompt Caching 命中率 ≥ 70%
- [ ] system prompt 完全静态（动态变量走 user message）
- [ ] prompts/ 目录 git 跟踪，e2e 锁定 prompt 版本

### 文档同步
- [ ] CLAUDE.md 时间节点更新（每周）
- [ ] architecture.md 架构调整时同步 + 重渲染 .html
- [ ] differentiation 调研到新对标项目时补充
