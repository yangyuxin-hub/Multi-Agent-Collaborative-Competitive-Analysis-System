# HTML Report Template

> HTML 报告的视觉规范与必备图表。基于 Cursor case baseline 抽象。
> 实例参考：[data/fixtures/cursor/claude_code_baseline.html](../../../data/fixtures/cursor/claude_code_baseline.html)

## 设计原则

1. **自包含单文件**：仅外链 Mermaid CDN，浏览器直接 `file://` 打开
2. **打印友好**：A4 / Letter 打印后仍可读
3. **响应式**：手机也能看（关键给评委 / leader 分享场景）
4. **轻量**：单文件 < 50KB，无构建工具

## 必备视觉元素

### 1. 头部 Banner

渐变色 banner（primary → dark），含：
- 报告标题
- 元信息：视角 / 市场 / 时间
- 标签（如 "5 个竞品" / "21 个工具调用" / "由 skill v0.2 产出"）

### 2. 摘要 Callout

```html
<div class="summary-callout">
  <p>...核心洞察 1...</p>
  <p>...核心洞察 2...</p>
  <p>...风险与机会...</p>
</div>
```
样式：渐变浅蓝背景 + 左侧 4px 强调边。

### 3. SWOT 2×2 网格

```html
<div class="swot-grid">
  <div class="swot s"><h4>🟢 Strengths 优势</h4><ul>...</ul></div>
  <div class="swot w"><h4>🔴 Weaknesses 劣势</h4><ul>...</ul></div>
  <div class="swot o"><h4>🔵 Opportunities 机会</h4><ul>...</ul></div>
  <div class="swot t"><h4>🟡 Threats 威胁</h4><ul>...</ul></div>
</div>
```
颜色映射：S=绿 / W=红 / O=蓝 / T=黄。

### 4. 定位象限图（Mermaid quadrantChart）

象限图是报告 7 段内的可视化模块，通常放在"竞品概览"之后或"战略建议"之前，但**不要新增第 8 个主段落**。

```html
<div class="mermaid">
quadrantChart
    title 价格 vs Agentic 自主程度
    x-axis "低价/免费" --> "高价"
    y-axis "弱 Agentic" --> "强 Agentic"
    quadrant-1 "高价高 Agentic"
    quadrant-2 "低价强 Agentic"
    quadrant-3 "低价弱 Agentic"
    quadrant-4 "高价弱 Agentic"
    Cursor: [0.55, 0.75]
    "GitHub Copilot": [0.3, 0.55]
    Windsurf: [0.6, 0.88]
</div>
```

**两个轴的选择需要根据产品类型调整**：
- AI 编程工具：价格 × Agentic 程度
- 文档协作：价格 × 协作深度
- 项目管理：定制化 × 团队规模
- 通用兜底：价格 × 核心能力强度

### 5. 定价条形对比（HTML/CSS）

```html
<div class="price-bar-chart">
  <div class="price-row">
    <span class="label">Copilot Pro</span>
    <div class="bar-container"><div class="bar" style="width:25%">市场最低</div></div>
    <span class="value">$10</span>
  </div>
  <!-- 重复每个竞品... -->
</div>
```

按价格从低到高排序，**目标产品的"广告价 vs 实际价"对比放在最显眼位置**。

### 6. 战略建议卡片

```html
<div class="strategy-card">
  <h4>建议 1：定价大改革</h4>
  <p class="why"><strong>为什么</strong>：...</p>
  <p class="how"><strong>怎么做</strong>：...</p>
</div>
```
每条建议独立一张卡，左侧 4px primary 强调边，背景浅灰。

## 标准化样式 CSS 变量

```css
:root {
  --primary: #0969da;       /* 主蓝 */
  --success: #1a7f37;       /* 绿 (Strengths / 完整支持) */
  --warning: #bf8700;       /* 黄 (Threats / 部分支持) */
  --danger: #d1242f;        /* 红 (Weaknesses / 不支持) */
  --bg: #ffffff;
  --bg-soft: #f6f8fa;
  --border: #d0d7de;
  --text: #1f2328;
  --text-soft: #656d76;
}
```

## 表格规范

- 功能矩阵：用 `✅` / `⚠️` / `❌` / `—` / `❓`，配套色类 `.check-full` / `.check-partial` / `.check-none` / `.check-unknown`
- 表格底部加图例
- 宽表必须包在 `.table-wrap` 内：

```html
<div class="table-wrap">
  <table>...</table>
</div>
```

```css
.table-wrap { width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; }
.table-wrap table { min-width: 720px; }
@media (max-width: 768px) {
  body { padding: 16px 12px; overflow-x: hidden; }
  section { padding: 20px 16px; overflow-x: hidden; }
  .mermaid { overflow-x: auto; padding: 12px; }
  .mermaid svg { max-width: 100%; height: auto; }
}
```

## Mermaid 初始化

```html
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({
    startOnLoad: true,
    theme: 'default',
    quadrantChart: { chartWidth: 800, chartHeight: 500 },
    securityLevel: 'loose'
  });
</script>
```

## 文件命名约定

| 文件 | 位置 |
|------|------|
| `report.md` | 报告 markdown 源文件 |
| `report.html` | 渲染版（同目录）|
| `data/fixtures/{slug}/` | 项目工程归档（同时有 md 和 html）|
| `skills/competitive-analysis/examples/{slug}.md` | skill 案例笔记（只引用，不重复内容）|

## 实操：从 md 转 html 的步骤

1. **写完 md** — 用 7 段标准结构
2. **抽取要素** — 找出 SWOT 四象限点 / 定价数字 / 战略建议
3. **应用模板** — 复制本目录 baseline.html 改内容
4. **填入 Mermaid quadrantChart** — 6 个竞品的坐标（自评，0-1 区间）
5. **填入定价条形** — 按价格升序，宽度 = 价格/最大价格 * 100%
6. **打开浏览器验收** — 确认 Mermaid 渲染正常 + 移动端 `document.documentElement.scrollWidth <= window.innerWidth + 1`，宽表只在 `.table-wrap` 内横向滚动

## 禁止事项

- ❌ 用复杂前端框架（React / Vue / Svelte 等）
- ❌ 外链多个 CDN（仅 Mermaid 一个）
- ❌ 内嵌大量 SVG / 图片资源（让单文件膨胀）
- ❌ 用 inline `style="..."` 替代 class（破坏可维护）
- ❌ 表格用 `<div>` 模拟（必须用 `<table>`，便于复制到 Notion / Word）
