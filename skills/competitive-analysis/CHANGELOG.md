# Competitive Analysis Skill · CHANGELOG

迭代历史。每跑完一个 case 必须更新这里。

---

## v0 · 2026-05-14（今日）

**状态**：初始版本，未经任何 case 验证

**来源**：合并精简自 `backend/app/agent/prompts/lead_system.md v0` + `researcher_system.md v0`

**核心约束**：
- 工作流 5 步（规划 / 澄清 / 找候选 / 单竞品调研 / 综合写报告）
- 五大纪律（流程 / 预算 / 引用 / 错误 / 收敛）
- 报告 7 段结构
- 单竞品工具上限 WebSearch ≤ 3 / WebFetch ≤ 5

**已知风险**（未验证）：
- "禁止凭空构造 URL" 仅 prompt 引导，CC 是否真遵守需 Cursor case 验证
- 收敛纪律的"已用时 ≥ 70%" 在 CC 中不一定可感知
- 报告输出格式（中英混排）可能不稳定

**下一步**：5/15-5/17 用 Cursor case 验证

---

## v0.1 · 2026-05-14（同日修订，未经 case 验证）

**状态**：根据约束合理性 review 收敛，可运行版本

**修改清单**：
1. **澄清从"强制"改为"默认 + 自动兜底"**：30s 超时或用户说"直接开始" → 用默认值继续 + 报告开头声明默认假设
2. **引用纪律分两类**：事实必须有源，分析判断可基于事实推导，避免 SWOT / 战略建议被卡死
3. **新增 Source 最小结构段**：用 `used_for` 字段标注每个 source 被哪些字段引用，对接 sources_pool
4. **综合阶段放宽**：禁止扩竞品，但允许补搜关键字段 ≤ 3 次
5. **新增"输出验收标准"段**：6 条硬指标，便于测试与 Demo 自检

**schema 升级**：
- `pricing_tiers.source_url` 必填，强制定价绑定来源
- `feature_flags` 加入 `unknown`（区分"明确不支持"与"信息缺失"）
- `sources.used_for` 必填，便于引用审计
- `sources` minItems 2（每竞品 ≥ 2 来源）
- `negative_reviews` 不可空（评价不足须显式声明）

**未变**：5 步工作流、五大纪律框架、报告 7 段结构

---

## v0.2 · 2026-05-14（按 obra/superpowers 规范重构）

**状态**：格式合规版，结构按 CC skill 事实标准对齐

**核心修改**：
1. **frontmatter 规范化**：
   - `description` 改为 `Use when...` 开头，**仅描述触发条件**（不再总结工作流），符合 obra 规范
   - 移除 `version` 字段（不在规范内；版本号由 CHANGELOG 维护）
2. **body 结构按 obra 模板**：Overview / When to Use / Workflow / Disciplines / Quick Reference / Common Mistakes / Acceptance / Reference / Examples
3. **拆分重型内容到 reference/**：
   - `reference/playbook.md` — 5 步工作流详细
   - `reference/disciplines.md` — 五大纪律完整版
   - `reference/output-spec.md` — 报告 7 段细节 + 验收 + Source 结构
   - `reference/integration.md` — 与本项目 agent 系统对接（开发者参考）
4. **SKILL.md 精简到 ~500 词**，触发时 CC 全文读完即可知道结构与约束；细节按需读 reference/
5. **新增 Common Mistakes 段**：6 条易错点 + 修正

**未变**：5 步工作流、五大纪律、报告 7 段、competitor-card.json schema

---

## v0.3 · 计划 5/17

**触发**：Cursor case 跑完，按 `docs/cc-observation-cursor.md` 记录完毕

**预期修订**：
- [ ] 引用真实性结果回写（量化幻觉率）
- [ ] 实际工具调用次数与预设上限对比
- [ ] 收敛纪律是否需要更具体的触发条件
- [ ] 报告结构是否需要调整
- [ ] description 触发覆盖度（CC 在用户没说完整关键词时是否触发）

---

## v0.3 · 计划 5/18

**触发**：Notion AI case 跑完

**预期修订**：
- [ ] 巩固两个 case 的共性约束
- [ ] 发现差异性（SaaS 文档 vs IDE 类产品报告维度差异）
- [ ] 是否需要按产品类型分支 schema

---

## v1.0 · 计划 5/19

**触发**：Linear case 跑完，三个 case 全部稳定

**交付**：
- [ ] Skill 定型
- [ ] 用作 `backend/app/agent/prompts/lead_system.md v1` 的参考蓝本
- [ ] 用作 `backend/app/agent/prompts/researcher_system.md v1` 的参考蓝本
- [ ] 编码完成后，skill 和 agent 双向校对一次

---

## 版本约定

- 每个 case 验证后必须更新版本（哪怕只改一条）
- 不向后兼容的重大改动 → 升 major（v0 → v1）
- 增加约束 / 调整 schema → 升 minor（v0.1 → v0.2）
- 措辞优化 / 案例补充 → patch（v0.1.0 → v0.1.1）
