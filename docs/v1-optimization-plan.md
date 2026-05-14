# V1 最终优化方案

> 整合多轮讨论的最终决策：**DAG 骨架 + 关键澄清 + 有界返工 + 上下文工程**

---

## 一、整体架构

```
                    ┌─ interrupt (前端多选) ─┐
START → planner → clarifier ────────────────┘
                    ↓
                 collector ←──(质量门, ≤1 次重试)
                    ↓
                 extractor ←──(质量门, ≤1 次重试)
                    ↓
            ┌───────┴───────┐         (并行)
        comparator       analyzer
            └───────┬───────┘
                    ↓
                 reporter ←──(缺 source 子循环, ≤1 次)
                    ↓
                   END
```

**三个关键设计**：
1. planner 后一次澄清（借鉴 Claude Code 的 AskUserQuestion）
2. collector / extractor 一次有界返工
3. reporter 一次补 source 子循环

---

## 二、为什么选 LangGraph DAG（不选纯 ReAct Agent）

| 维度 | DAG（本项目） | ReAct / Claude Code 风格 |
|------|------------|----------------------|
| 控制流 | 代码定义 | LLM 自主决定 |
| 可视化 | 容易（图就是 UI） | 难（每次走法不同） |
| 可控性 | 高 | 低 |
| 报告质量上限 | 中 | 高 |
| 3 周可交付 | ✅ | ❌ |
| 答辩效果 | ✅ Timeline 动画 | ❌ 黑盒 spinner |

**结论**：垂直竞品分析场景下，结构本来就固定（plan→collect→extract→compare→analyze→report），DAG 在工程可控性、可视化、答辩效果上全面优于 ReAct。

---

## 三、State 设计（瘦身版）

```python
class AnalysisState(TypedDict, total=False):
    # 输入
    product: str
    clarifications: dict[str, Any]        # 用户澄清结果

    # 中间产物（轻量结构化）
    competitors: list[str]
    plan_draft: dict                       # planner 输出的计划 + 歧义点
    raw_doc_refs: list[str]                # ← 路径，不是内容！
    structured: list[Competitor]           # 抽取后的精简 JSON
    comparison: dict
    insights: dict
    report_md: str

    # 全链路累加
    sources: Annotated[list[Source], add]  # snippet 限制 200 字
    events: Annotated[list[AgentEvent], add]

    # 控制流
    collector_retries: int
    extractor_retries: int
    quality_flags: list[str]
```

**铁律**：>1K 的原始内容一律落 `./data/snapshots/{task_id}/`，State 只存路径。

---

## 四、模型分层（成本核心）

| Agent | 模型 | 单次成本 | 说明 |
|-------|------|--------|-----|
| planner | Sonnet 4.6 | ~$0.01 | 判断力 + Prompt Cache |
| clarifier | Sonnet 4.6 | ~$0.005 | 决定是否反问 |
| collector | 无 LLM | $0 | Tavily + BeautifulSoup |
| **extractor** | **Haiku 4.5** | **~$0.01** | **25 次并发，成本敏感点** |
| comparator | Sonnet 4.6 | ~$0.005 | 输入已瘦身到 ~3K |
| analyzer | Sonnet 4.6 | ~$0.005 | 输入 ~5K |
| reporter | Sonnet 4.6 | ~$0.01 | 输入 ~15K |

**目标**：单次任务 ≤ $0.05，端到端 ≤ 90 秒。

---

## 五、上下文工程铁则

1. **State 分层**：raw 落盘、结构化进 State、sources 只存元信息
2. **按需读取**：每个 Agent 函数显式声明读哪些字段，不接受整 State
3. **extractor 分批并发**：单页一次 Haiku 调用，`asyncio.gather` 并行
4. **Prompt Caching**：planner / reporter 固定框架部分用 `cache_control`
5. **sources snippet 限长 200 字**：足够引用展示，不塞全文

**对比效果**（朴素 vs 优化）：
- 朴素 State 透传：单次 ~$0.5+，延迟 30s+
- 优化后：单次 ~$0.05，延迟 5-10s
- **节省 10 倍**

---

## 六、人机协同：clarifier 节点

**只在 planner 之后做一次**。

**协议**：
- `WS event: interrupt` → 前端弹多选卡片
- `WS event: resume` → 用户提交答案，graph 用 `Command(resume=...)` 继续
- 30 秒超时 → 默认选项继续（Demo 兜底）

**典型澄清问题**（planner 自动生成）：
- 竞品范围：垂直 AI 笔记 / 泛文档协作 / AI 办公套件
- 分析视角：产品选型 / 投资分析 / 竞争策略
- 地域：海外 / 国内 / 全球

---

## 七、有界返工：质量门

```python
def collector_gate(state):
    if len(state.get("raw_doc_refs", [])) < 3 and state.get("collector_retries", 0) < 1:
        return "collector"      # 换 query 再来一次
    return "extractor"

def extractor_gate(state):
    if missing_rate(state["structured"]) > 0.5 and state.get("extractor_retries", 0) < 1:
        return "collector"      # 让 collector 定向补抓
    return ["comparator", "analyzer"]

def reporter_gate(state):
    if has_unreferenced_claim(state["report_md"]) and not state.get("gap_filled"):
        return "gap_filler"
    return END
```

**整体硬超时 8 分钟**，超过直接降级出报告。

---

## 八、实施清单（按优先级）

| 优先级 | 任务 | 工期 |
|-------|-----|-----|
| P0 | 重构 state.py（raw_doc_refs 替换 raw_docs）| 0.5h |
| P0 | 6 个 Agent 节点接真实 LLM + Tavily | 3 天 |
| P0 | FastAPI + WebSocket（含 interrupt/resume 协议）| 1 天 |
| P0 | clarifier 节点 + LangGraph `interrupt` | 0.5 天 |
| P1 | 三个质量门 + retry 计数 | 0.5 天 |
| P1 | extractor Haiku + 并发分批 | 0.5 天 |
| P1 | Prompt Cache 接入 | 0.5 天 |
| P2 | reporter 的 gap_filler 子循环 | 1 天 |
| P2 | WeasyPrint PDF 导出 | 0.5 天 |
| P3 | 前端 AgentTimeline + 澄清卡片 | 3 天（并行） |

**P0 + P1 ≈ 7 人天，覆盖核心 Demo**。
