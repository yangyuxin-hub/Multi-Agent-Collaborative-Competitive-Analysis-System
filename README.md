# 主 Agent 协作式竞品分析系统

> 字节 AI 全栈挑战赛参赛项目（2026.05.20 - 2026.06.10）

输入产品名，**首席分析师主 Agent** 自主规划，调用 tools 搜索/抓取/抽取，并发派**调研员 Subagent** 研究每个竞品，输出带引用追踪的结构化报告。

Claude Code 风格的 agentic 系统，专项化用于竞品分析。

## 技术栈

- **前端**：Next.js 14 + TypeScript + Tailwind CSS + shadcn/ui + Recharts
- **后端**：FastAPI + **Claude Agent SDK** + Anthropic Claude (Sonnet 4.6 / Haiku 4.5)
- **检索**：Tavily / Serper + BeautifulSoup
- **存储**：PostgreSQL + 本地文件
- **PDF**：WeasyPrint

## 核心特性

- 主 Agent + 6 个 tools + Researcher subagent 并发架构
- 引用追踪三道防线（tool 入口 / schema 校验 / 前端二次校验）
- 主 agent 自主调用 `ask_user` 澄清（WS interrupt/resume）
- Claude Code 式事件流可视化（思考链 + tool use + 嵌套 subagent + 实时预算）
- 单任务预算 ≤ $0.05、happy path ≤ 90s

## 快速开始

```bash
# 启动数据库
docker-compose up -d postgres

# 后端
cd backend && uv sync && uv run fastapi dev app/main.py

# 前端
cd frontend && pnpm install && pnpm dev
```

详细工程说明见 [CLAUDE.md](./CLAUDE.md)。

## 作者

小羊肖恩
