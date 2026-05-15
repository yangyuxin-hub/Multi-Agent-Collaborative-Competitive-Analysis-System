# Example: Cursor 竞品分析

> 用 skill v0.2 跑出来的首个完整案例。
> 实体报告见：[data/fixtures/cursor/claude_code_baseline.md](../../../data/fixtures/cursor/claude_code_baseline.md)

## 输入

```
做 Cursor 的竞品分析
```

## 澄清回答

| 维度 | 回答 |
|------|------|
| 视角 | 创业者 / 战略 |
| 地域 | 全球 |
| 数量 | 自定义文本："包含 trae 以及主流顶尖的 ai 编程工具" |

## 选定竞品（5 个）

| 竞品 | 选取理由 |
|------|---------|
| GitHub Copilot | 现任老大 / 商业 SaaS |
| Windsurf | 同形态 agentic IDE 直接对手 |
| Trae | 用户指定 + 中国市场代表 |
| Claude Code | Anthropic 终端 agent 新范式 |
| Cline | 开源代表 / 透明计费模式 |

## 执行统计

| 指标 | 实际 | 预设上限 | 状态 |
|------|------|---------|------|
| 总工具调用 | 21 次 | 30 次 | ✅ |
| AskUserQuestion | 1 次 | — | ✅ |
| WebFetch | 13 次 | — | ✅ |
| WebSearch | 7 次 | — | ✅ |
| 单竞品 fetch 上限突破 | 否 | ≤ 5 | ✅ |
| 补搜次数 | 3 次（round 4 三个差评搜索）| ≤ 3 | ✅ 卡在上限 |
| 报告 7 段全齐 | ✅ | 必含 | ✅ |
| 每竞品 ≥ 2 来源 | ✅（最少 2，最多 4）| 验收 #3 | ✅ |
| 至少 1 个官方来源 | ✅ | 验收 #3 | ✅ |
| 定价来自官网 | ✅（Trae 除外，标 "来源 vibecoding.app"）| 验收 #4 | ⚠️ Trae 走第三方 |
| 差评非空 | ✅ | 验收 #5 | ✅ |
| 中文 + 英文专名 | ✅ | 验收 #6 | ✅ |
| 默认值声明 | 不适用（用户全部主动回答）| 验收 #7 | — |
| SWOT 每项 ≥ 2 | ✅（S/W/O/T 各 4-5 条）| 验收 #8 | ✅ |
| 战略建议 3-5 条 | ✅（5 条）| 验收 #9 | ✅ |

## 遇到的问题与调整

| # | 问题 | 调整 | 启示 |
|---|------|------|------|
| 1 | Trae 官网内容极简（"Collaborate with Intelligence" 几个字）| 改用 WebSearch 查第三方 review | skill 应建议**先 WebSearch 探查官网内容质量，再决定是否 fetch** |
| 2 | claude.com 域名 / codeium.com 都被 301 重定向 | 二次 fetch 跟随 redirect | skill 应建议**fetch 失败时优先看是否是 redirect 而非反爬** |
| 3 | Reddit 全站被拦截（"Claude Code is unable to fetch from www.reddit.com"）| 改用 WebSearch + 各 review 站 | skill 应**显式声明 Reddit 不可直接 fetch，差评走 review 聚合站**（G2 / Capterra / dev.to / The Register）|
| 4 | 用户用自由文本回答竞品数量 | LLM 自行解析为"5 个含 Trae" | skill 应**预留自由文本兜底逻辑**，不要假设用户只选预设选项 |
| 5 | Windsurf 官网内容被截断 | 改 WebSearch 查公司 + 估值新闻 | 同 #1，**fetch 优先用 search 校验信息密度** |

## 报告中可疑事实（需人工校验）

> 跑完后建议抽查这几条事实是否真实：

| 报告陈述 | 引用 | 待验证点 |
|---------|------|---------|
| "Cursor 实际月费 $40-50（120% 溢价）" | eesel.ai review | 数字来源是否可靠 |
| "Ryz Labs 测试 Copilot 大代码库准确率仅 50%" | 转引自 NxCode | 原始报告链接缺失 |
| "Cline 61.8k GitHub stars" | cline.bot | 是 51k 还是 61.8k 待确认 |
| "NVIDIA 4 万工程师 / Fortune 500 50%+" | cursor.com | 官网主张但无第三方核实 |
| "OpenAI $3B 收购 Windsurf 失败，Google 出 $2.4B 抽走核心团队" | Bloomberg / Fortune | 时间线 / 金额需对照原文 |

## 对 SKILL.md v0.2 的修订建议（→ v0.3，已应用 2026-05-14）

1. **Tool 使用顺序**：现在 playbook 是 search → fetch → extract，应改为 **"先 search 评估官网信息密度"，再决定 fetch 几页**（避免 Trae / Windsurf 这种 fetch 拿到空内容的浪费）✅
2. **Reddit 不可用**：在 disciplines.md 错误纪律里加一条"Reddit 在 CC 中不可 fetch，差评走 review 聚合站" ✅
3. **Redirect 处理**：错误纪律加一条"fetch 返回 redirect 时跟随新 URL，不算失败" ✅
4. **自由文本兜底**：playbook 第 2 步澄清里加一行"若用户用自由文本回答数量，LLM 自行解析为合理整数；若解析失败，用默认 5" ✅
5. **官方来源优先级**：实际情况是**定价页 > 官网 > 评测站**（Trae 官网空但评测站有完整定价表）✅
6. **共性洞察段**：本 case 自发产出了"共性洞察：所有商业产品都遭遇用量计费危机"这种横向观察，这是高质量报告的标志，**应在 output-spec.md 提示主 agent 主动寻找跨竞品共性** ✅
7. **新增自动验收**：补 `scripts/validate_report.py` 检查 7 段结构、可视化模块、共性洞察、HTML 段落编号 ✅

## 启示总结

- ✅ Skill v0.2 已能产出**结构化、可决策、引用密集**的合格报告
- ✅ 五大纪律基本被遵守（流程 / 预算 / 引用 / 错误 / 收敛）
- ⚠️ 引用真实性需人工抽查（LLM 可能在引用具体数字时打折扣）
- ⚠️ 补搜额度用满（3/3），说明初次 fetch 阶段对"哪些信息要先抓"判断不够准
- 🎯 v0.3 已补 fetch 策略 / 错误处理 / 事实风险 / HTML 契约 / 自动验收

## 时间线

- 2026-05-14 19:00 启动
- 2026-05-14 19:15 5 轮工具调用完成
- 2026-05-14 19:20 报告写完
- 总耗时约 20 分钟（含 AskUserQuestion 用户思考时间）

实际推理 token 用量估算（仅供参考）：
- Sonnet 4.6 / Opus 4.7 类: 输入 ~80k token（含历史）/ 输出 ~6k token
- 工程项目预算 $0.05 中**主 agent 部分需要继续控制**（本次因为是 CC 而非工程 agent，预算控制较宽松）
