# 多 Agent 协作式竞品分析系统

字节 AI 全栈挑战赛参赛项目（2026.05.20 - 2026.06.10）

## 项目定位

输入一个产品、公司或行业关键词，系统自动从公开渠道采集信息，整理成结构化数据，输出竞品分析报告。
核心不是单个聊天机器人，而是把"调研小组"的工作流拆成多个 Agent，模拟真实调研团队。

---

## 开发执行原则（AI 写代码前必读）

1. **Demo 链路优先**：所有改动必须服务于 Demo 主路径（输入 → 澄清 → 6 Agent → 报告 PDF），不偏离不发散
2. **不引入 V2 依赖**：禁止在 V1 阶段引入 Redis、ChromaDB、MinIO、Celery，本地文件 + PostgreSQL 足够
3. **sources 强制贯穿**：任何 Agent 的输出必须带 `sources` 字段，未带源的结论不允许出现在最终报告
4. **先 mock 后真实**：每个 Agent 先用 mock 数据跑通流程，再接真实 API。优先保证端到端链路打通
5. **小步快跑**：每个 PR/commit 只改一个 Agent 或一个组件，每天能跑通一次完整 Demo
6. **失败优雅降级**：任何外部依赖（搜索、抓取、LLM）失败都不能阻塞整体流程，标记缺失继续往下走
7. **三个验收 case 必须始终能跑**：Notion AI / Cursor / Linear，每次合并前都要回归

---

## Non-Goals（V1 明确不做）

- ❌ 用户账号系统、登录注册、权限管理
- ❌ 企业知识库接入
- ❌ 长周期竞品监控、定时任务
- ❌ 高并发任务队列（用 FastAPI BackgroundTasks 即可）
- ❌ 多租户、SaaS 化
- ❌ 复杂的报告模板编辑器
- ❌ 国际化、多语言
- ❌ 移动端适配（桌面 Web 优先）

---

## 团队分工（待填）

| 角色 | 负责模块 | 成员 |
|------|---------|------|
| 后端 / Agent 编排 | LangGraph 工作流、Agent 实现、API | TBD |
| 前端 | Next.js 页面、Agent 可视化、报告渲染 | TBD |
| 算法 / Prompt | Agent prompt 设计、报告质量调优 | TBD |
| 数据 / 工具 | 信息源接入、抓取兜底、Demo 数据准备 | TBD |

> 独立参赛则按时间分配：5月20-27 后端骨架 → 5月28-6月3 前端 + Agent 调优 → 6月4-10 Demo 打磨

---

## 6 核心 Agent + 2 辅助节点

### 核心 Agent（6 个）

| Agent | 职责 | 模型 | 单次成本 | 超时 |
|-------|------|------|--------|------|
| 任务规划 planner | 理解用户需求，拆解任务、生成歧义点供澄清 | Sonnet 4.6 | ~$0.01 | 20s |
| 信息采集 collector | 从公开网页、官网、新闻、应用商店采集资料 | 无 LLM（Tavily + BS4）| $0 | 90s |
| 信息抽取 extractor | 非结构化文本 → 结构化字段（功能/价格/目标用户/融资/口碑）| **Haiku 4.5** | ~$0.01（并发 25）| 60s |
| 竞品对比 comparator | 横向对比，生成功能矩阵、价格矩阵、定位象限 | Sonnet 4.6 | ~$0.005 | 45s |
| 洞察分析 analyzer | SWOT、商业模式、护城河、趋势判断 | Sonnet 4.6 | ~$0.005 | 45s |
| 报告生成 reporter | 汇总 Markdown / PDF 报告 | Sonnet 4.6 | ~$0.01 | 60s |

### 辅助节点（2 个，v1-optimization-plan 决策）

| 节点 | 触发位置 | 作用 | 模型 |
|------|---------|------|------|
| clarifier | planner 之后**一次** | LangGraph `interrupt` → 前端多选卡片，对齐竞品范围/视角/地域 | Sonnet 4.6（~$0.005）|
| gap_filler | reporter 子循环 ≤1 次 | 检测到无 source 的结论时，定向补抓 + 重写段落 | Sonnet 4.6 |

### 执行顺序

```
START → planner → clarifier ──interrupt(前端多选)──┐
                              ↓
                          collector ←──(质量门, ≤1 次重试)
                              ↓
                          extractor ←──(质量门, ≤1 次重试)
                              ↓
                      ┌───────┴───────┐  (并行)
                  comparator       analyzer
                      └───────┬───────┘
                              ↓
                          reporter ←──(缺 source → gap_filler, ≤1 次)
                              ↓
                             END
```

### 三个质量门 + 硬超时

- **collector_gate**：采集文档 < 3 篇且未重试过 → 换 query 重跑 collector
- **extractor_gate**：结构化字段缺失率 > 50% 且未重试过 → 回 collector 定向补抓
- **reporter_gate**：报告含无引用结论 → 进 gap_filler 一次

**端到端预算**：单次任务 ≤ **$0.05**、happy path ≤ **90 秒**；硬超时 **8 分钟**，超限用已采集数据降级出简化报告。

### Agent 统一输出 Schema

所有 Agent 必须返回如下结构（字段名严格统一）：

```json
{
  "agent": "collector",
  "status": "done",
  "data": {},
  "sources": [
    {
      "url": "https://...",
      "title": "页面标题",
      "snippet": "原文片段，用于引用展示",
      "retrieved_at": "2026-05-20T10:30:00Z"
    }
  ],
  "errors": [],
  "started_at": "2026-05-20T10:29:00Z",
  "finished_at": "2026-05-20T10:30:00Z"
}
```

- `status`: `pending | running | done | failed | skipped`
- `data`: Agent 特定的结构化输出，schema 见各 Agent 实现
- `sources`: 引用必须全链路透传，最终在报告中悬浮显示
- `errors`: 非致命错误列表，不阻塞流程

---

## 技术栈（MVP 精简版）

### 前端
- **框架**：Next.js 14（App Router）+ TypeScript
- **UI**：Tailwind CSS + shadcn/ui
- **实时通信**：WebSocket（Agent 执行进度推送）
- **图表**：Recharts（功能矩阵、价格对比可视化）
- **报告渲染**：react-markdown + 自定义引用组件

### 后端
- **框架**：Python FastAPI
- **Agent 编排**：LangGraph（有状态多步骤工作流）
- **LLM**：Anthropic Claude API（模型分层见上方 Agent 表）
  - 主力：`claude-sonnet-4-6`（planner / clarifier / comparator / analyzer / reporter / gap_filler）
  - 抽取类：`claude-haiku-4-5`（extractor，单页一次 Haiku，`asyncio.gather` 并发）
  - **Prompt Caching**：planner / reporter 固定框架部分用 `cache_control`
- **搜索**：Tavily API（主）+ Serper API（兜底）+ BeautifulSoup 网页解析
- **PDF 生成**：WeasyPrint（Markdown → HTML → PDF）

### 存储（MVP 极简）
- **PostgreSQL**：任务、竞品、结构化分析结果、信息源引用
- **本地文件系统**：报告 PDF、采集快照（路径 `./data/reports/`、`./data/snapshots/`）

> V2 才引入：Redis 任务队列 + ChromaDB 向量检索 + MinIO 对象存储

---

## API 设计

### REST 接口

| Method | Path | 说明 |
|--------|------|------|
| `POST` | `/api/tasks` | 创建分析任务，body: `{product: string, options?: {}}`，返回 `{task_id}` |
| `GET` | `/api/tasks/{task_id}` | 查询任务状态与各 Agent 进度 |
| `GET` | `/api/tasks` | 列出最近任务（分页） |
| `GET` | `/api/reports/{task_id}` | 获取报告 JSON（含 Markdown + 引用） |
| `GET` | `/api/reports/{task_id}/pdf` | 下载 PDF |
| `GET` | `/api/reports/{task_id}/markdown` | 下载 Markdown 源文件 |

### WebSocket

| Path | 说明 |
|------|------|
| `WS /ws/tasks/{task_id}` | 订阅指定任务的 Agent 执行进度，推送 Agent 统一输出 Schema |

**WS 事件类型**：
- `agent_status`：Agent 状态变更（推送统一 Schema）
- `interrupt`：clarifier 触发，payload 含多选项，前端弹卡片
- `resume`：前端 → 后端，提交澄清答案，graph 用 `Command(resume=...)` 继续
- `done` / `failed`：任务终态

**clarifier 兜底**：前端 30 秒未提交 → 用默认选项自动 resume，保证 Demo 不卡。

---

## 项目结构

```
ai-product/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI 路由（任务、报告、WebSocket）
│   │   ├── agents/
│   │   │   ├── base.py           # Agent 基类，统一 Schema
│   │   │   ├── planner.py
│   │   │   ├── clarifier.py      # 澄清节点（interrupt）
│   │   │   ├── collector.py
│   │   │   ├── extractor.py
│   │   │   ├── comparator.py
│   │   │   ├── analyzer.py
│   │   │   ├── reporter.py
│   │   │   └── gap_filler.py     # reporter 子循环
│   │   ├── graph/            # LangGraph 工作流编排 + 质量门
│   │   ├── tools/            # 搜索、抓取、引用追踪
│   │   ├── models/           # Pydantic + SQLAlchemy
│   │   ├── mocks/            # mock 数据，先 mock 后真实
│   │   └── core/             # 配置、DB、LLM client
│   ├── tests/
│   ├── data/                 # 本地文件存储
│   │   ├── reports/
│   │   ├── snapshots/
│   │   └── fixtures/         # 三个验收 case 缓存
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AgentTimeline/    # Agent 流程动画
│   │   │   ├── ReportViewer/     # 报告 + 引用悬浮
│   │   │   ├── ComparisonTable/  # 对比表格
│   │   │   └── TaskInput/
│   │   └── app/
│   └── package.json
├── docker-compose.yml        # PostgreSQL only
└── CLAUDE.md
```

---

## 本地启动 / 验证命令

### 首次安装
```bash
# 后端
cd backend
uv sync

# 前端
cd frontend
pnpm install

# 数据库
docker-compose up -d postgres
```

### 日常开发
```bash
# 后端开发服务器
cd backend && uv run fastapi dev app/main.py

# 前端开发服务器
cd frontend && pnpm dev
```

### 代码质量
```bash
# Python
cd backend && uv run ruff check . && uv run ruff format .

# TypeScript
cd frontend && pnpm lint && pnpm type-check
```

### 验收用例回归
```bash
# 跑通三个 case，所有 Agent 必须返回 done
cd backend && uv run pytest tests/e2e/ -v
```

---

## 验收用例（V1 必须始终能跑）

| Case | 产品 | 行业 | 预期竞品（至少识别 4 个） | 预期报告维度 |
|------|------|------|------------------------|------------|
| 1 | Notion AI | 文档协作 + AI 办公 | Coda AI, ClickUp AI, Confluence AI, Microsoft Copilot | 功能矩阵、定价、用户痛点 |
| 2 | Cursor | AI IDE / 编程助手 | GitHub Copilot, Windsurf, Cline, Continue | 模型支持、定价、IDE 集成 |
| 3 | Linear | 项目管理 / issue tracking | Jira, Asana, Height, Shortcut | 协作功能、定价、目标团队规模 |

每个 case 在 `backend/data/fixtures/{case_name}/` 下保存：
- `task.json`：任务输入
- `expected.json`：预期产出关键字段
- `snapshots/`：采集到的网页快照（兜底用）

---

## MVP 范围（V1，比赛截止前必交付）

**输入**：产品名称（如"Notion AI"）

**输出**：
- 自动识别 5 个竞品
- 抓取公开网页内容
- 竞品对比表（功能、定价、目标用户）
- Markdown 报告 + PDF 导出
- **6 Agent + 澄清节点的执行流程实时可视化**（核心 Demo 卖点）
- **planner 后一次多选澄清**（人机协同，避免跑偏）
- **报告每条结论绑定来源链接**（核心创新点）

---

## V2 规划（比赛后/加分项）

- 报告模板选择（简洁版 / 深度版 / PPT 版）
- 用户自定义分析维度
- 定时监控竞品动态
- 企业知识库接入
- Redis 任务队列 + ChromaDB 向量检索（支持大规模并发与语义搜索）
- MinIO 对象存储

---

## 项目创新点（答辩用，对齐评分维度）

| 评分维度 | 创新点 | 落地实现 |
|---------|--------|---------|
| 技术创新 | **多 Agent DAG 编排** | LangGraph 显式图 + 三个质量门 + 子循环，相比 ReAct 黑盒可视化、可控、可降级 |
| 人机协同 | **planner 后意图澄清** | 借鉴 Claude Code `AskUserQuestion`，interrupt/resume 多选卡片，避免"两万字报告跑偏" |
| 完成度 | **端到端自动化** | 一句话输入 → 完整 PDF 报告输出，目标 90s / $0.05 |
| 可信度 | **可追溯信息来源** | 每条结论悬浮显示原始链接 + reporter 缺源子循环，解决 LLM 幻觉 |
| 商业价值 | **决策导向分析框架** | 内置 SWOT、功能矩阵、定价矩阵，非纯信息汇总 |
| 体验 | **Agent 过程可视化** | Timeline 动画展示 6 Agent + 澄清/重试边，不是黑盒 spinner |

---

## 失败兜底方案

| 风险 | 兜底 |
|------|------|
| Tavily API 限额 | 切换 Serper / DuckDuckGo，准备 3 个验收 case 的预跑缓存 |
| Claude API 限流 | 降级到 haiku-4-5，必要时切 GPT-4o-mini |
| 网页反爬 / 抓取失败 | 重试 2 次后跳过，继续后续 Agent，标记数据缺失 |
| Demo 当天网络问题 | 本地预录三个完整 case 缓存，现场可离线回放 |
| LangGraph 工作流卡死 | 整体任务 8 分钟硬超时，已采集数据降级生成简化报告 |

---

## 环境变量

```env
# LLM
ANTHROPIC_API_KEY=

# 搜索
TAVILY_API_KEY=
SERPER_API_KEY=        # 兜底

# 数据库
DATABASE_URL=postgresql://localhost:5432/competitor_analysis

# 后端
SECRET_KEY=

# 数据目录（默认 ./data）
DATA_DIR=./data
```

---

## 开发规范

- Agent 每步执行完毕后向 WebSocket 广播状态：`pending → running → done / failed`
- LLM 调用用 tenacity 重试，最多 3 次，指数退避
- 每个 Agent 输出严格遵循统一 Schema，未带 `sources` 的结论不允许进入报告
- Python：ruff 格式化，类型注解必填
- TypeScript：strict 模式
- 提交前必须跑通三个验收 case（`pytest tests/e2e/`）

---

## 关键时间节点

| 日期 | 目标 | 验收标准 |
|------|------|---------|
| 5月20日 | 项目启动 | FastAPI + PostgreSQL + WebSocket 骨架 + Next.js 空壳，三个 case fixture 就位 |
| 5月23日 | 数据链路打通 | planner + clarifier(interrupt) + collector + extractor 跑通，输出结构化 JSON（带 sources） |
| 5月27日 | 6 Agent + 辅助节点全通 | 端到端能生成粗糙 Markdown 报告，三个 case 都能跑完，质量门 + gap_filler 生效 |
| 5月31日 | 前端可视化完成 | Agent Timeline 动画 + 澄清卡片 + 报告渲染 + 引用悬浮 |
| 6月3日 | 报告质量达标 | prompt 调优完毕，三个测试 case 报告质量可用 |
| 6月5日 | PDF + Demo 数据 | PDF 导出能用，三个预跑 case 缓存就绪 |
| 6月7日 | 功能冻结 | 只修 bug，专注答辩 PPT + 演示视频 |
| 6月10日 | 提交截止 | 代码 + 文档 + 视频 + 部署链接 |

---

## Demo 设计（答辩用）

**主演示脚本**：输入"帮我分析 Notion AI 的竞品"
1. planner 激活，**弹出澄清卡片**：竞品范围 / 分析视角 / 地域，用户多选确认
2. 实时展示 collector → extractor → comparator‖analyzer → reporter 依次激活、执行、完成
3. 中途点击采集卡片，展示原始信息源（链接 + 摘要）
4. 展示竞品对比表（功能矩阵、定价矩阵），可交互筛选
5. 展示最终报告，**结论上悬浮显示来源引用**
6. 一键导出 PDF

**追问演示**：切换"Cursor 的竞品" / "Linear 的竞品"，展示系统通用性

**降级预案**：网络故障时切本地缓存 case，体验完全一致
