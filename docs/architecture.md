# 系统架构图

> 主 Agent + Tools + Subagent 架构。详细说明见 [CLAUDE.md](../CLAUDE.md)。

## 整体分层

```mermaid
flowchart TB
    subgraph FE["前端 Next.js"]
        UI[TaskInput]
        Stream[EventStream<br/>思考链+tool卡片+subagent卡片]
        Budget[BudgetMeter]
        Report[ReportViewer<br/>引用悬浮]
    end

    subgraph BE["后端 FastAPI"]
        Agent[Lead Analyst<br/>Claude Agent SDK]
        Sub[Researcher×5 并发]
        Tools[Tools: search/fetch/extract<br/>ask_user/write_section/budget]
        Core[sources_pool / event_bus<br/>budget_tracker]
    end

    Claude[Anthropic Claude<br/>Sonnet 4.6 + Haiku 4.5]
    Tavily[Tavily / Serper]
    PG[(PostgreSQL)]

    UI --> Agent
    Agent -->|spawn| Sub
    Agent --> Tools
    Sub --> Tools
    Tools --> Claude
    Tools --> Tavily
    Agent --> Core
    Sub --> Core
    Core --> PG
    Core <-->|WS 事件流| Stream
    Core --> Budget
    Core --> Report
```

## 主 Agent 执行流

```mermaid
flowchart TD
    Start([输入产品名]) --> Plan[Lead Analyst 规划]
    Plan --> Ask[ask_user 澄清]
    Ask -->|interrupt/resume| Search[web_search 找竞品]
    Search --> Spawn[并发派 5× Researcher]
    Spawn --> R1[Researcher A]
    Spawn --> R2[Researcher B]
    Spawn --> R3[Researcher C]
    Spawn --> R4[Researcher D]
    Spawn --> R5[Researcher E]
    R1 & R2 & R3 & R4 & R5 --> Sync[主 agent 收 5 张卡片]
    Sync --> Gap{字段缺失?}
    Gap -->|是| Refill[再派子 agent 补抓]
    Refill --> Sync
    Gap -->|否| Synth[综合: 矩阵/SWOT/象限]
    Synth --> Write[write_section × N<br/>强校验 source_ids]
    Write --> End([END])
```

重试由主 agent 看 tool error 自主决策，无质量门。

## 引用追踪三道防线

```mermaid
flowchart LR
    subgraph A["① Tool 入口"]
        S[web_search]
        F[fetch_page]
    end
    P[(sources_pool)]
    subgraph B["② Write 校验"]
        W[write_section<br/>schema 强校验<br/>source_ids ∈ pool]
    end
    subgraph C["③ 前端校验"]
        R[渲染时回查 pool<br/>池外 id ⚠️]
    end
    S -->|分配 id| P
    F -->|分配 id| P
    W --> P
    R --> P
```

主 agent 写报告**只有 write_section 一条路径**。

## WS 事件流

```mermaid
flowchart LR
    Lead[Lead Analyst]
    Sub[Researcher Subagent]
    Bus[event_bus<br/>seq 编号 + 入库]
    WS[WebSocket]
    FE[前端 reducer]

    Lead --> Bus
    Sub --> Bus
    Bus --> WS
    WS <-->|reconnect last_seq| FE
```

事件类型：`text_delta` / `tool_use` / `tool_result` / `task_spawn` / `task_result` / `interrupt` / `resume` / `budget_update` / `done` / `failed`

## 部署

```mermaid
flowchart LR
    User[用户] <--> Vercel[Vercel<br/>Next.js]
    Vercel <-->|HTTPS+WSS| Render[Render<br/>FastAPI]
    Render --> Neon[(Neon PG)]
    Render --> Anth[Anthropic API]
    Render --> Tav[Tavily API]
```

免费档够用，Demo 离线事件流回放兜底。
