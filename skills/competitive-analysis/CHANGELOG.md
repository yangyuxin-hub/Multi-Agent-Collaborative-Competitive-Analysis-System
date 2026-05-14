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

## v0.1 · 计划 5/17

**触发**：Cursor case 跑完，按 `docs/cc-observation-cursor.md` 记录完毕

**预期修订**：
- [ ] 引用真实性结果回写
- [ ] 实际工具调用次数与预设上限对比
- [ ] 收敛纪律是否需要更具体的触发条件
- [ ] 报告结构是否需要调整（比如目标产品 SWOT 还是放最前面）

---

## v0.2 · 计划 5/18

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
