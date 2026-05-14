# 竞品分析领域知识（写报告必读）

> 决定 extractor 抽什么字段、comparator 做什么矩阵、analyzer 写什么洞察的**业务侧依据**。

---

## 一、不同读者关心的东西完全不同

planner 后的 clarifier 必须先问"**你是哪种视角看这份报告？**"——视角决定字段权重。

| 读者 | 用途 | 最关心 |
|------|-----|--------|
| **产品经理** | 决定下个季度做什么功能、怎么差异化 | 功能矩阵、用户痛点、迭代速度 |
| **创业者 / 战略** | 决定要不要进这个赛道、定位往哪打 | 市场格局、融资情况、护城河 |
| **投资人 / BD** | 决定要不要投、估值多少 | 商业模式、收入、增长曲线、团队 |
| **销售 / Marketing** | 销售对话怎么应对、Battlecard | 定价、目标客户、客户吐槽点 |
| **求职者 / 行业研究** | 判断行业趋势 | 全景图、领头羊、新兴玩家 |

---

## 二、信息金字塔（按重要性五层）

### 第 1 层 — 身份（必有，最基础）
- 产品名 + 公司名 + 官网
- 一句话定位
- 成立时间 / 团队规模 / 总部 / 公司类型
- **来源**：官网首页 + Crunchbase + Wikipedia

### 第 2 层 — 产品（核心 ⭐⭐⭐）
- 核心功能列表（3-5 个杀手锏）
- **功能矩阵**（横向对比谁有谁没） ← 矩阵 1
- 技术亮点 / 平台支持 / 集成生态 / 数据隐私合规

### 第 3 层 — 商业（决策核心 ⭐⭐⭐）
- **定价矩阵**（免费版 / Pro / 企业版） ← 矩阵 2
- 商业模式（订阅 / 按量 / 一次性 / Freemium）
- 目标客户 / 收入估算 / 用户规模 / 融资情况

### 第 4 层 — 口碑（差异化关键 ⭐⭐）
- 用户评价（**好评 + 差评**）
- 典型客户 logo / 增长信号 / 社区活跃度 / 渠道策略

> 差评里藏着机会，**必须抓**。

### 第 5 层 — 战略洞察（报告灵魂 ⭐⭐⭐）
分析框架（不是字段）：
- **SWOT**（优势/劣势/机会/威胁）
- **市场定位图**（横轴价格 / 纵轴功能复杂度）
- 差异化分析 / 护城河评估 / 趋势判断 / 给"自己产品"的建议

---

## 三、报告的三张必备表（PPT 里直接放）

### 表 1：功能矩阵

| 功能 | 竞品A | 竞品B | 竞品C |
|------|------|------|------|
| 功能 X | ✅ | ✅ | ⚠️ |
| 功能 Y | ✅ | ❌ | ✅ |

✅完整 / ⚠️部分 / ❌不支持

### 表 2：定价矩阵

| 竞品 | 免费版 | 个人付费 | 团队版 | 企业版 |
|------|-------|---------|--------|--------|

### 表 3：定位象限图（散点图）
- 横轴：价格
- 纵轴：功能复杂度
- 每个竞品打一个点

---

## 四、不同视角的字段权重表

| 字段类别 | PM | 创业者 | 投资人 | 销售 |
|---------|----|--------|--------|------|
| 核心功能 | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐ |
| 功能矩阵 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ |
| 定价 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| 商业模式 | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ |
| 融资情况 | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ | — |
| 用户评价 | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| SWOT | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ |
| 市场定位 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ |
| 差评/痛点 | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐ |
| 增长信号 | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ |

**默认视角 = PM**（最通用），其他视角通过 clarifier 切换权重。

---

## 五、extractor 的目标 Schema

```python
class Competitor(TypedDict):
    # 第 1 层 身份
    name: str
    company: str
    website: str
    one_liner: str
    founded: str | None
    headquarters: str | None
    team_size: str | None

    # 第 2 层 产品
    core_features: list[str]
    feature_flags: dict[str, Literal["full", "partial", "none"]]
    platforms: list[str]
    integrations: list[str]
    tech_stack: list[str] | None

    # 第 3 层 商业
    pricing_tiers: list[dict]    # [{name: "Pro", price: "$10/mo", limits: "..."}]
    business_model: str
    target_audience: list[str]
    funding: dict | None
    notable_customers: list[str] | None

    # 第 4 层 口碑
    positive_reviews: list[str]
    negative_reviews: list[str]
    growth_signals: list[str]

    sources: list[Source]
```

---

## 六、collector 的信息源 + Tavily Query 模板

| 数据 | 优先级 | 来源 |
|------|-------|-----|
| 一句话定位 / 核心功能 | P0 | 官网首页 + features 页 |
| 定价 | P0 | 官网 /pricing |
| 融资 | P0 | Crunchbase / 36氪 / TechCrunch |
| 用户评价 | P0 | G2 / Product Hunt / 知乎 / Reddit |
| 团队规模 | P1 | LinkedIn / Crunchbase |
| 集成生态 | P1 | 官网 integrations 页 |
| 增长信号 | P1 | 官网招聘页 / Twitter / Google Trends |
| 技术栈 | P2 | 官方博客 / 技术文档 |

**搜索关键词模板**：

```
"{product} pricing"
"{product} features review"
"{product} vs {competitor}"            ← 最强，直接拿对比文章
"{product} funding crunchbase"
"{product} reddit users complain"      ← 挖差评
"alternatives to {product}"             ← 反向找竞品
```

---

## 七、新手常踩的坑

| ❌ 做错 | ✅ 应该 |
|--------|--------|
| 堆字段不分轻重，50 个字段塞满 | 3-5 个核心维度 + 1 张大表，聚焦才有密度 |
| 只汇总不分析（"A 支持 X，B 也支持 X"）| 对比 + 判断（"只有 A 能跨库语义搜索——这是护城河"）|
| 只列优点 | **必含差评和痛点**，差评是机会 |
| 信息时间静止 | 带时间戳 + 趋势线 |

---

## 八、工程优先级

> **先把"功能矩阵 + 定价矩阵 + SWOT"这三块做扎实，再考虑其他**。
> 这三块占报告价值的 70%，且最容易做出可视化效果。
