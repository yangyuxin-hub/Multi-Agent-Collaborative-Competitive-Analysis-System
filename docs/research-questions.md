# 项目研究问题清单

本项目实施前/中需要回答的核心问题。按 **8 类 32 个问题**组织，每个问题包含背景、建议解法与状态。

> 对齐文档：[CLAUDE.md](../CLAUDE.md)、[v1-optimization-plan.md](./v1-optimization-plan.md)、[architecture.md](./architecture.md)

---

## 一、Agent 编排与协作

### Q1. LangGraph 用什么图结构编排 6 Agent + 2 辅助节点？
- **背景**：StateGraph 还是 MessageGraph？state 在 Agent 间怎么流转？
- **建议解法**：`StateGraph + TypedDict`，所有 Agent 读写同一个 `AnalysisState`
- **状态**：待研究
- **优先级**：🔴 P0

### Q2. comparator 与 analyzer 并行怎么实现？
- **背景**：CLAUDE.md 图里两者并行，LangGraph 怎么写 fan-out / fan-in？
- **建议解法**：从 extractor 加两条 `add_edge` 平行边，下游用合并节点等待两个 key 都 ready
- **状态**：待研究
- **优先级**：🔴 P0

### Q3. clarifier 的 interrupt / resume 怎么落地？
- **背景**：planner 后弹多选卡片，前端提交后续跑，30s 兜底自动 resume
- **建议解法**：LangGraph `interrupt()` + WebSocket 推 `interrupt` 事件，前端 `Command(resume=...)`；超时由后端定时器触发默认值 resume
- **状态**：待研究
- **优先级**：🔴 P0

### Q4. 三个质量门（collector/extractor/reporter）的判定阈值与重试边怎么画？
- **背景**：collector < 3 篇、extractor 缺失率 > 50%、reporter 含无源结论
- **建议解法**：每个 gate 一个 `conditional_edge`，state 里加 `retry_count`，硬上限 1 次防死循环
- **状态**：待研究
- **优先级**：🔴 P0

### Q5. gap_filler 子循环怎么收敛？
- **背景**：reporter 发现无源结论 → gap_filler 定向补抓 → 重写段落，但不能无限循环
- **建议解法**：限定 1 次；二次仍无源则强制删除该结论或标"信息不足"
- **状态**：待研究
- **优先级**：🔴 P0

### Q6. Agent 失败后流程怎么走？
- **背景**：信息采集失败，后续 Agent 跳过还是降级？
- **建议解法**：`conditional_edge` 走降级路径，state 标 `data_gaps[]`，reporter 在报告里显式声明缺失
- **状态**：待研究
- **优先级**：🔴 P0

---

## 二、上下文工程（多 Agent 系统的核心难点）

### Q7. AnalysisState TypedDict 怎么设计？
- **背景**：6 Agent 共享 state，但各自只关心局部；字段太多 LLM 会被噪声干扰
- **建议解法**：分层设计 — `task` / `clarification` / `raw_docs` / `extracted` / `comparison` / `analysis` / `report` / `sources_pool` / `gates`，Agent 只读必要字段
- **状态**：待研究
- **优先级**：🔴 P0

### Q8. 各 Agent 之间传什么、不传什么？
- **背景**：collector 抓到的原始 HTML 不应进 comparator 的 prompt，否则 token 爆炸
- **建议解法**：原文存 `raw_docs[]`（按 source_id 索引），下游 Agent 只读 extractor 产出的结构化字段；引用时按 id 回查
- **状态**：待研究
- **优先级**：🔴 P0

### Q9. Prompt Caching 缓存哪些前缀？
- **背景**：planner / reporter / comparator 的系统 prompt 长且固定，重复调用浪费
- **建议解法**：Anthropic `cache_control` 标记系统 prompt + few-shot 例子 + 报告模板骨架；目标缓存命中率 > 70%
- **状态**：待研究
- **优先级**：🟡 P1

### Q10. 长上下文怎么裁剪？
- **背景**：collector 抓 20 篇网页全塞进 extractor 会超 200k token
- **建议解法**：extractor 按页粒度调用（单页一次 Haiku），不做跨页拼接；comparator/analyzer 只看 extractor 摘要
- **状态**：待研究
- **优先级**：🔴 P0

### Q11. sources_pool 跨 Agent 共享怎么组织？
- **背景**：所有 Agent 都要引用 source，但 source 在不同阶段产生
- **建议解法**：state 里 `sources_pool: dict[source_id, Source]` 全局唯一，collector 写入后只读；Agent 输出 sources 时只填 id 列表
- **状态**：待研究
- **优先级**：🔴 P0

---

## 三、信息采集与抽取

### Q12. 怎么自动识别一个产品的 5 个竞品？
- **背景**：用 LLM 直接问还是搜 "alternatives to X"？
- **建议解法**：双路召回 — LLM 知识（planner 阶段）+ Tavily 搜 "X alternatives / competitors"，去重合并；clarifier 给用户确认
- **状态**：待研究
- **优先级**：🔴 P0

### Q13. 网页内容抓取的优先级与去噪？
- **背景**：官网、ProductHunt、G2、Reddit、HackerNews 权重？
- **建议解法**：优先级 = 官网 > 评测站(G2/Capterra) > Reddit > 新闻；BS4 + readability 抽正文
- **状态**：待研究
- **优先级**：🔴 P0

### Q14. extractor 用 Haiku 并发 25 路怎么控流？
- **背景**：单页一次 Haiku，5 个竞品 × 5 页 = 25 个并发请求，可能限流
- **建议解法**：`asyncio.Semaphore(10)` 限并发 + tenacity 指数退避；失败的页加入 `data_gaps[]`
- **状态**：待研究
- **优先级**：🔴 P0

### Q15. 抽取置信度与多源投票？
- **背景**：价格信息可能藏在表格、博客、FAQ 里，不同源给不同结果
- **建议解法**：每个字段带 `confidence` 与 `source_ids[]`，多源同值置信度提高；冲突时取最高优先级源
- **状态**：待研究
- **优先级**：🟡 P1

### Q16. 信息时效性怎么保证？
- **背景**：价格 2023 年的过时了
- **建议解法**：source 带 `retrieved_at` + LLM 评估"信息新鲜度"，>1 年标黄
- **状态**：待研究
- **优先级**：🟡 P1

### Q17. 反爬怎么办？
- **背景**：Cloudflare、JS 渲染
- **建议解法**：第一版用 Tavily `include_raw_content`，自抓只做兜底；失败标记继续
- **状态**：待研究
- **优先级**：🟡 P1

---

## 四、Prompt 工程

### Q18. 每个 Agent 的 prompt 怎么组织？
- **背景**：系统 prompt、用户 prompt、few-shot？
- **建议解法**：每 Agent 一个 `prompts/{agent}.md`，分 system / user / few-shot 三段，便于迭代与缓存
- **状态**：待研究
- **优先级**：🟡 P1

### Q19. planner 怎么生成澄清选项？
- **背景**：clarifier 要展示"竞品范围 / 分析视角 / 地域"多选项
- **建议解法**：planner 输出 schema 强制带 `clarification_questions[]`，每题 2-4 选项 + 推荐项
- **状态**：待研究
- **优先级**：🔴 P0

### Q20. 怎么让 LLM 严格输出指定 JSON Schema？
- **背景**：Claude tool use 还是 prefill？
- **建议解法**：Claude `tool_use` 模式，schema 即工具定义；Pydantic 二次校验
- **状态**：待研究
- **优先级**：🟡 P1

### Q21. 怎么让结论强制带引用？
- **背景**：LLM 容易"忘记"引用
- **建议解法**：prompt 规定"每个事实陈述必须以 [src_id] 结尾"，后处理正则校验，无引用的句子触发 reporter_gate
- **状态**：待研究
- **优先级**：🔴 P0

---

## 五、引用追踪机制

### Q22. source_id 怎么从采集贯穿到报告？
- **背景**：多 Agent 处理后，如何溯源某条结论的原始 URL？
- **建议解法**：collector 入库即分配全局 `source_id`（如 `src_001`），下游所有输出只引用 id；reporter 渲染时回查 sources_pool
- **状态**：待研究
- **优先级**：🔴 P0

### Q23. 前端怎么实现"悬浮显示引用"？
- **背景**：报告里的 [1][2] 怎么和 source 卡片对应？
- **建议解法**：Markdown 渲染时把 `[ref:src_001]` 解析成 `<Tooltip>` 组件，悬浮显示 url + title + snippet
- **状态**：待研究
- **优先级**：🟡 P1

### Q24. 如何防止 LLM 编造 URL？
- **背景**：LLM 可能伪造引用
- **建议解法**：所有 source 必须来自 sources_pool，reporter 引用 id 不在池中即视为幻觉，触发 gap_filler 或删除
- **状态**：待研究
- **优先级**：🔴 P0

---

## 六、报告模板与生成

### Q25. 三种产品类型（SaaS / IDE / PM 工具）模板一样吗？
- **背景**：Notion AI / Cursor / Linear 关注维度差异大（如 Cursor 重模型支持，Linear 重协作）
- **建议解法**：统一框架（封面 / 摘要 / 竞品列表 / 功能矩阵 / 定价 / SWOT / 结论），按产品类型动态启用扩展段（如 IDE 类多一段"模型与插件生态"）
- **状态**：待研究
- **优先级**：🔴 P0

### Q26. 功能矩阵的列怎么自动生成？
- **背景**：列是预定义还是从 extractor 输出聚合？
- **建议解法**：extractor 抽取字段并集 → comparator 投票选 top-N 共性功能作为列；预留"自定义维度"扩展位
- **状态**：待研究
- **优先级**：🟡 P1

### Q27. SWOT / 定位象限怎么结构化？
- **背景**：analyzer 输出要能被前端可视化（非纯文本）
- **建议解法**：analyzer 输出 JSON `{swot: {s:[], w:[], o:[], t:[]}, quadrant: {x_axis, y_axis, products:[{name, x, y}]}}`，前端 Recharts 渲染
- **状态**：待研究
- **优先级**：🟡 P1

### Q28. 报告布局怎么排版才像专业咨询报告？
- **背景**：评委一眼判断专业度
- **建议解法**：参考艾瑞 / 易观 — 封面、目录、执行摘要、对比表、SWOT、结论；few-shot 喂真实报告片段
- **状态**：待研究
- **优先级**：🟡 P1

### Q29. WeasyPrint Markdown → PDF 的字体与样式？
- **背景**：中文字体经常掉字，表格分页错位
- **建议解法**：预装思源黑体 + 内置 CSS（table 防截断、code 块换行），提前用三个 case 实测
- **状态**：待研究
- **优先级**：🟢 P2

---

## 七、速度与成本

### Q30. $0.05 / 任务 预算怎么分摊到各 Agent？
- **背景**：CLAUDE.md 表格已给单次成本估算，需验证总和 ≤ $0.05
- **建议解法**：planner $0.01 + clarifier $0.005 + extractor $0.01 (Haiku ×25 并发) + comparator $0.005 + analyzer $0.005 + reporter $0.01 + gap_filler $0.005 = $0.05；实测后调整
- **状态**：待研究
- **优先级**：🔴 P0

### Q31. 90 秒 happy path 哪步是瓶颈？
- **背景**：collector 90s 超时已最长，能压缩吗？
- **建议解法**：collector 内部 Tavily + 抓取并发；extractor 并发 25；comparator‖analyzer 并行；目标 collector 60s / extractor 30s / 其他 ≤ 10s 各
- **状态**：待研究
- **优先级**：🔴 P0

### Q32. token 用量与缓存命中率怎么监控？
- **背景**：超预算需要快速定位是哪个 Agent
- **建议解法**：每次 LLM 调用记录 `(agent, input_tokens, output_tokens, cache_read, cache_write, cost)` 入 PG，前端开发面板展示
- **状态**：待研究
- **优先级**：🟡 P1

### Q33. 8 分钟硬超时的降级路径？
- **背景**：超时点可能发生在任何 Agent
- **建议解法**：state 全程持久化，超时后用已有 `extracted` / `comparison` 数据直接进 reporter 生成简化版报告，明确标"因超时降级"
- **状态**：待研究
- **优先级**：🟡 P1

---

## 八、UX / 工程 / Demo

### Q34. Agent 进度动画怎么设计才有冲击力？
- **背景**：单纯进度条无聊
- **建议解法**：每 Agent 一个角色卡片（头像 + 名字 + 当前在做的事），过渡动画用 framer-motion
- **状态**：待研究
- **优先级**：🟡 P1

### Q35. WebSocket 实时推送的频率和粒度？
- **背景**：每秒推还是状态变更才推？
- **建议解法**：状态变更 + 关键节点（如"找到第 3 个竞品"）；心跳 10s 一次防断
- **状态**：待研究
- **优先级**：🟡 P1

### Q36. PostgreSQL 表结构？
- **背景**：task / agent_run / source / report 关系
- **建议解法**：`task` 主表 → `agent_run` 关联 → `source` 关联 → `report` 关联 task；state 整体存 JSONB 字段方便恢复
- **状态**：待研究
- **优先级**：🟢 P2

### Q37. WebSocket 断线重连？
- **背景**：Demo 时网络抖动
- **建议解法**：前端 reconnect + 后端按 task_id 重发未确认事件（事件序号）
- **状态**：待研究
- **优先级**：🟢 P2

### Q38. 三个验收 case 的"理想报告" baseline 怎么写？
- **背景**：没有标准答案怎么判断报告质量？
- **建议解法**：人工写一份 baseline，存 `fixtures/{case}/expected.json`；LLM-as-judge 对比关键字段命中率
- **状态**：待研究
- **优先级**：🟢 P2

### Q39. 答辩 Demo 的"高光时刻"在哪？
- **背景**：评委注意力只有 3 分钟
- **建议解法**：开场放 5x 加速的 Agent 工作流动画 + 澄清卡片交互 + 引用悬浮三连击
- **状态**：待研究
- **优先级**：🟢 P2

### Q40. 部署到哪里供评委访问？
- **背景**：Vercel + Railway / Render，还是只交录屏？
- **建议解法**：Vercel(前端) + Render(后端) 免费档；准备本地预跑缓存 + 录屏兜底
- **状态**：待研究
- **优先级**：🟢 P2

---

## 优先级矩阵

| 优先级 | 问题 | 类别 | 何时研究 |
|--------|------|------|---------|
| 🔴 P0 | Q1-Q6 | LangGraph 编排 | 5/14-5/18 必须想清楚 |
| 🔴 P0 | Q7-Q8, Q10-Q11 | 上下文工程 | 5/14-5/18 与编排同步 |
| 🔴 P0 | Q12-Q14 | 采集抽取核心 | 5/15 前 POC Tavily + Haiku 并发 |
| 🔴 P0 | Q19, Q21 | Prompt 关键 | 5/22 第一个 Agent 开工 |
| 🔴 P0 | Q22, Q24 | 引用追踪 schema | 5/18 前设计完 |
| 🔴 P0 | Q25 | 报告模板骨架 | 5/20 前确定 |
| 🔴 P0 | Q30-Q31 | 预算与瓶颈 | 5/27 端到端跑通后实测 |
| 🟡 P1 | Q9, Q15-Q17 | 缓存与数据质量 | 5/22 起边做边解决 |
| 🟡 P1 | Q18, Q20 | Prompt 工程 | 5/22 起 |
| 🟡 P1 | Q23, Q26-Q28 | 报告与可视化 | 5/28 前端阶段 |
| 🟡 P1 | Q32-Q33 | 监控与降级 | 5/31 前完成 |
| 🟡 P1 | Q34-Q35 | UX | 5/28 前端阶段 |
| 🟢 P2 | Q29, Q36-Q40 | 工程与 Demo | 6/1 起边做边解决 |

---

## 本周（5/13-5/19）必须先动手的 5 个

1. **Q1-Q5**：跑通 LangGraph 多 Agent + interrupt/resume + 质量门最小 demo
2. **Q7-Q8**：在草稿纸上画完整 AnalysisState 字段表与读写矩阵
3. **Q12, Q14**：用 Tavily 搜 "Notion AI alternatives"，Haiku 并发抽取看返回质量
4. **Q22**：画 source_id 从采集到报告的完整传递路径
5. **Q25**：写出三个验收 case 的报告模板骨架，确认是否能用统一框架

---

## 状态更新约定

每个问题研究完成后，把"状态"字段更新为：
- `待研究` → `研究中` → `已确定方案` → `已实现`

并在问题下方追加 `### 结论` 小节，记录最终方案与关键链接。
