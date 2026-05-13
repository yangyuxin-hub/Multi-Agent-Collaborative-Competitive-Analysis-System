# 多 Agent 协作式竞品分析系统

> 字节 AI 全栈挑战赛参赛项目（2026.05.20 - 2026.06.10）

输入一个产品、公司或行业关键词，系统自动从公开渠道采集信息，整理成结构化数据，输出竞品分析报告。

## 技术栈

- **前端**：Next.js 14 + TypeScript + Tailwind CSS + shadcn/ui
- **后端**：FastAPI + LangGraph + Claude API
- **存储**：PostgreSQL + 本地文件

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
