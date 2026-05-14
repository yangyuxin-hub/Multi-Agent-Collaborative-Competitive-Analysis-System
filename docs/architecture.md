# 系统架构图

> 与 [v1-optimization-plan.md](./v1-optimization-plan.md) 保持同步。HTML 版 `architecture.html` 需在本文件改动后重新渲染。

## 1. 整体分层架构

```mermaid
graph TB
    subgraph User["👤 用户层"]
        U[用户输入产品名]
    end

    subgraph Frontend["🎨 前端层 Next.js 14"]
        TI[TaskInput 输入框]
        AT[AgentTimeline 进度可视化]
        RV[ReportViewer 报告展示]
        CT[ComparisonTable 对比表格]
    end

    subgraph API["🔌 API 层 FastAPI"]
        REST[REST API<br/>任务/报告/PDF]
        WS[WebSocket<br/>实时进度推送]
    end

    subgraph Orchestration["🧠 编排层 LangGraph"]
        GRAPH[工作流引擎<br/>状态机 + 并行调度]
    end

    subgraph Agents["🤖 Agent 层（6 核心 + 2 辅助）"]
        A1[任务规划 planner]
        AC[澄清 clarifier<br/>⚡ interrupt]
        A2[信息采集 collector]
        A3[信息抽取 extractor<br/>Haiku 并发]
        A4[竞品对比 comparator]
        A5[洞察分析 analyzer]
        A6[报告生成 reporter]
        AG[缺源补抓 gap_filler<br/>↻ 子循环]
    end

    subgraph Tools["🛠️ 工具层"]
        T1[Tavily 搜索]
        T2[Serper 兜底]
        T3[BeautifulSoup 解析]
        T4[Claude API]
        T5[WeasyPrint PDF]
    end

    subgraph Storage["💾 存储层"]
        DB[(PostgreSQL<br/>任务/竞品/引用)]
        FS[本地文件系统<br/>PDF/快照]
    end

    U --> TI
    TI --> REST
    REST --> GRAPH
    GRAPH --> A1
    GRAPH --> AC
    GRAPH --> A2
    GRAPH --> A3
    GRAPH --> A4
    GRAPH --> A5
    GRAPH --> A6
    GRAPH --> AG
    A1 --> T4
    AC --> T4
    A2 --> T1
    A2 --> T2
    A2 --> T3
    A3 --> T4
    A4 --> T4
    A5 --> T4
    A6 --> T4
    AG --> T4
    A6 --> T5
    GRAPH --> DB
    A6 --> FS
    GRAPH --> WS
    WS --> AT
    REST --> RV
    REST --> CT

    style User fill:#e1f5ff
    style Frontend fill:#fff3e0
    style API fill:#f3e5f5
    style Orchestration fill:#e8f5e9
    style Agents fill:#fff9c4
    style Tools fill:#fce4ec
    style Storage fill:#f5f5f5
```

---

## 2. Agent 工作流（DAG + 质量门 + 子循环）

```mermaid
flowchart TB
    START([用户输入<br/>产品名]) --> P[任务规划 planner<br/>Sonnet · 20s]
    P --> CL{澄清 clarifier<br/>⚡ interrupt}
    CL -.30s 超时默认.-> C
    CL -- 前端多选 resume --> C[信息采集 collector<br/>无 LLM · 90s]

    C --> G1{collector_gate<br/>文档数 ≥ 3?}
    G1 -- 否 ≤1 次 --> C
    G1 -- 是 --> E[信息抽取 extractor<br/>Haiku 并发 · 60s]

    E --> G2{extractor_gate<br/>缺失率 ≤ 50%?}
    G2 -- 否 ≤1 次 --> C
    G2 -- 是 --> COMP[竞品对比 comparator<br/>Sonnet · 45s]
    G2 -- 是 --> ANA[洞察分析 analyzer<br/>Sonnet · 45s]

    COMP --> R[报告生成 reporter<br/>Sonnet · 60s]
    ANA --> R

    R --> G3{reporter_gate<br/>结论都有 source?}
    G3 -- 否 ≤1 次 --> GF[gap_filler<br/>定向补抓 + 重写]
    GF --> R
    G3 -- 是 --> ENDX([Markdown + PDF<br/>含引用])

    style START fill:#4caf50,color:#fff
    style ENDX fill:#2196f3,color:#fff
    style CL fill:#ffccbc
    style GF fill:#ffccbc
    style G1 fill:#fff59d
    style G2 fill:#fff59d
    style G3 fill:#fff59d
    style P fill:#fff9c4
    style C fill:#fff9c4
    style E fill:#fff9c4
    style COMP fill:#fff9c4
    style ANA fill:#fff9c4
    style R fill:#fff9c4
```

> **预算**：happy path ≤ 90s / ≤ $0.05，硬超时 8 min（超时用已采集数据降级出简化报告）

---

## 3. 数据流与引用追踪

```mermaid
sequenceDiagram
    autonumber
    participant U as 用户
    participant F as 前端
    participant API as FastAPI
    participant G as LangGraph
    participant A as Agent
    participant T as Tavily/Claude
    participant DB as PostgreSQL

    U->>F: 输入"Notion AI 的竞品"
    F->>API: POST /api/tasks
    API->>DB: 创建 task 记录
    API-->>F: 返回 task_id
    F->>API: WS /ws/tasks/{id} 订阅

    API->>G: 启动工作流
    G->>A: planner 执行
    A-->>G: 返回计划 + 歧义点
    G-->>API: agent_status (planner done)
    API-->>F: WS 推送

    Note over G,F: 澄清节点 interrupt
    G-->>API: interrupt (多选项)
    API-->>F: WS interrupt 事件
    F->>U: 弹出澄清卡片
    U->>F: 多选确认 / 30s 超时默认
    F->>API: WS resume (用户选择)
    API->>G: Command(resume=...)

    loop collector/extractor/comparator/analyzer/reporter
        G->>A: 执行 Agent
        A->>T: 调用工具 (搜索/LLM)
        T-->>A: 数据 + sources (snippet ≤200 字)
        A->>DB: 持久化输出 + sources
        A-->>G: 统一 Schema
        G-->>API: agent_status
        API-->>F: WS 推送进度
    end

    Note over G: reporter_gate 若缺 source → gap_filler 子循环 ≤1 次

    G->>API: 工作流完成
    API->>DB: 生成最终报告
    F->>API: GET /api/reports/{id}
    API-->>F: 报告 + 引用映射
    F-->>U: 渲染报告<br/>结论悬浮显示来源
```

---

## 4. Agent 统一输出 Schema

```mermaid
classDiagram
    class AgentOutput {
        +string agent
        +string status
        +object data
        +Source[] sources
        +Error[] errors
        +datetime started_at
        +datetime finished_at
    }

    class Source {
        +string url
        +string title
        +string snippet
        +datetime retrieved_at
    }

    class Error {
        +string code
        +string message
        +bool fatal
    }

    AgentOutput "1" --> "*" Source
    AgentOutput "1" --> "*" Error

    note for AgentOutput "所有 Agent 必须返回此结构\nsources 字段全链路透传到报告"
```

---

## 5. 创新点对照视图

```mermaid
mindmap
  root((竞品分析<br/>Agent系统))
    技术创新
      LangGraph DAG 显式编排
      6 Agent + 2 辅助节点
      并行 comparator/analyzer
      三个质量门 + 子循环
    人机协同
      planner 后 clarifier interrupt
      多选卡片对齐意图
      30s 超时默认兜底
    可信度
      sources 全链路透传
      snippet 限长 200 字
      gap_filler 缺源回填
      结论悬浮显示来源
    工程优化
      State 分层 raw 落盘
      模型分层 Sonnet/Haiku
      Prompt Caching
      单次 0.05 美元 90 秒
    商业价值
      SWOT 分析
      功能矩阵
      定价矩阵
      多视角字段权重
    体验
      Timeline 动画
      实时澄清交互
      引用悬浮
      PDF 一键导出
```

---

## 6. State 与上下文工程

```mermaid
graph LR
    subgraph State["AnalysisState（瘦身版，进 LangGraph）"]
        S1[product / clarifications]
        S2[plan_draft / competitors]
        S3[raw_doc_refs<br/>路径，不是内容]
        S4[structured 精简 JSON]
        S5[comparison / insights]
        S6[report_md]
        S7[sources<br/>snippet ≤ 200 字]
        S8[retries / quality_flags]
    end

    subgraph Disk["./data/snapshots/{task_id}/ (磁盘)"]
        D1[原始 HTML / Markdown]
        D2[抓取截图]
    end

    subgraph DB[("PostgreSQL")]
        T1[tasks 表]
        T2[sources 表]
        T3[reports 表]
    end

    S3 -. 引用路径 .-> D1
    S7 -. 落库 .-> T2
    S6 -. 落库 .-> T3
    S1 -. 落库 .-> T1

    style State fill:#e3f2fd
    style Disk fill:#f5f5f5
    style DB fill:#fff3e0
```

> **铁律**：>1K 的原始内容一律落盘，State 只存路径；每个 Agent 显式声明读哪些字段，不接受整 State。

---

## 7. 部署架构（简化版）

```mermaid
graph LR
    subgraph Local["本地开发 / Demo 环境"]
        FE[Next.js<br/>:3000]
        BE[FastAPI<br/>:8000]
        PG[(PostgreSQL<br/>Docker)]
        FS[./data/]
    end

    subgraph External["外部服务"]
        CLAUDE[Anthropic<br/>Claude API]
        TAVILY[Tavily 搜索]
        SERPER[Serper 兜底]
    end

    FE -.HTTP/WS.-> BE
    BE -.SQL.-> PG
    BE -.读写.-> FS
    BE -.HTTPS.-> CLAUDE
    BE -.HTTPS.-> TAVILY
    BE -.HTTPS.-> SERPER

    style Local fill:#e8f5e9
    style External fill:#fff3e0
```
