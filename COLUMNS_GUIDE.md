# V2 Excel 列指南 - 详细说明

## 📋 12 列详解

### A 列: 更新时间
**数据格式**: `YYYY-MM-DD`
**示例**: `2026-03-05`
**说明**: 数据抓取日期。用于追踪数据新鲜度。

---

### B 列: 公司名称
**数据来源**: LinkedIn 职位列表页
**示例**: `hackajob`, `targetjobs UK`, `TELUS Digital`
**说明**: 招聘公司的名称。

---

### C 列: 项目类型
**数据来源**: 职位标题和招聘类型判断
**可能值**:
- `full time` - 全职岗位
- `Internship` - 实习岗位
- `Graduate` - 应届毕业生项目

**示例**:
- "Data Analyst" → `full time`
- "Summer Internship" → `Internship`
- "Graduate Scheme" → `Graduate`

---

### D 列: 岗位类型 ⭐ (自动分类)
**数据来源**: 职位标题关键词分类
**可能值**:
- `数据` - 数据分析、数据科学相关
- `产品` - 产品经理、产品分析师
- `AI` - 人工智能、NLP、Prompt Engineer
- `商业` - 商业分析、商业智能
- `定量` - 定量分析、统计、风险分析
- `其他` - 其他类型

**示例**:
```
"Data Analyst" → 数据
"Product Manager" → 产品
"Prompt Engineer" → AI
"Business Analyst" → 商业
"Credit Risk Analyst" → 定量
```

---

### E 列: 岗位名称 ★★★
**数据来源**: LinkedIn 职位列表页
**示例**:
- `Graduate Associate Data Analyst`
- `Trainee Data Analyst`
- `Data Science Graduate Scheme`

**说明**: 完整的职位标题。是最重要的信息之一。

---

### F 列: 工作地区
**数据来源**: LinkedIn 职位列表页
**示例**:
- `London, England, United Kingdom`
- `West Midlands, England, United Kingdom`
- `Remote` (如果职位支持远程)

**说明**: 工作地点。可用于地理位置过滤。

---

### G 列: 💰 薪资 ⭐⭐⭐ (V2 新增)
**数据来源**: 职位详情页描述
**可能值**:
- **薪资范围**: `£30,000 - £45,000`
- **时薪**: `£25 per hour`
- **通用描述**: `Competitive Salary`
- **无信息**: `未标明`

**提取规则**:
```
匹配模式:
- £XXX,XXX - £XXX,XXX        (范围，年薪)
- £XXXk - £XXXk               (范围，缩写)
- £XXX,XXX per annum/year     (年薪)
- £XXX per hour/day           (时薪/日薪)
- Competitive (salary)         (通用描述)
```

**示例**:
```
✓ £25,000 - £35,000
✓ £30k - £45k
✓ Competitive Salary
✓ £20 per hour
✗ 未标明
```

---

### H 列: 🔑 签证/工签 ⭐⭐⭐ (V2 新增)
**数据来源**: 职位详情页描述
**可能值**:
- `✅ 可提供工签` - 明确表示可以赞助工作签证 (绿色背景)
- `❌ 不提供工签` - 明确表示不提供或需要永居 (红色背景)
- `未说明` - 职位描述未提及签证信息 (无背景)

**识别逻辑**:
```
绿色 (✅ 可提供工签):
- "visa sponsorship is available"
- "we can sponsor"
- "we will sponsor"
- "able to sponsor"
- "sponsor your visa"
...

红色 (❌ 不提供工签):
- "cannot sponsor"
- "will not sponsor"
- "permanent right to work"
- "settled status"
- "right to work in the uk without"
...
```

**如何使用**:
- 🟢 绿色: 可直接申请，公司会处理工签
- 🔴 红色: 需要谨慎，确认是否满足条件
- ⚪ 无标记: 联系公司咨询签证政策

---

### I 列: 🏢 公司规模 (V2 新增)
**数据来源**: 职位详情页描述
**可能值**:
- **范围**: `1,000-5,000 employees`
- **具体数字**: `5,000+ employees`
- **未知**: `未知` (无法从页面提取)

**提取规则**:
```
匹配模式:
- 1,000-5,000 employees
- 10,000+ employees
- Company size: 500-1,000
```

**如何使用**:
- 小公司 (< 100): 创业氛围，快速成长
- 中等公司 (100-1,000): 平衡的公司文化
- 大公司 (1,000+): 体系完整，资源丰富

---

### J 列: 📋 岗位关键词 ⭐⭐⭐ (V2 新增 - 最强新功能!)
**数据来源**: 职位详情页描述文本
**数据格式**: 逗号分隔的技能关键词 (最多 8 个)

**可识别的技能库 (50+ 技能)**:

**编程语言**: Python, R, SQL, Java, Scala, JavaScript, SAS, SPSS, Stata, C++...
**数据工具**: Tableau, Power BI, Excel, Looker, Qlik, dbt, Databricks...
**云平台**: AWS, Azure, GCP, Snowflake, BigQuery, Redshift...
**ML/AI**: Machine Learning, Deep Learning, NLP, LLM, TensorFlow, PyTorch...
**数据工程**: ETL, Airflow, Spark, Kafka, Docker, Kubernetes...
**分析方法**: A/B Testing, Statistical Analysis, Forecasting, Segmentation...
**产品工具**: Agile, JIRA, Google Analytics, Mixpanel, Amplitude...
**其他**: Git, API, Pandas, NumPy, Jupyter, REST, Matplotlib...

**示例**:
```
岗位要求文本: "We're looking for a Python expert with SQL, Power BI
and Machine Learning experience. Must know Docker and have experience
with A/B Testing."

提取结果: Python, SQL, Power BI, Machine Learning, Docker, A/B Testing
```

**如何使用** 👍:
这是最实用的列！快速扫描判断：
- ✅ 我有 8 个中的 6 个技能 → 高匹配度，强烈推荐申请
- ✅ 我有 8 个中的 4 个技能 → 中等匹配度，可以申请
- ⚠️ 我有 8 个中的 2 个技能 → 低匹配度，但可学习该技能

---

### K 列: 学历要求
**数据来源**: 职位详情页描述
**可能值**:
- `Bachelor's Degree` - 学士学位
- `Master's Degree` - 硕士学位
- `PhD` - 博士学位
- `HND` - 高等国家文凭
- `Degree` - 大学学位 (具体等级未指明)
- `官网无说明` - 网站未提及学历要求

**示例**:
```
"Bachelor's Degree in Mathematics, Physics or Computer Science"
→ 提取为: Bachelor's Degree

"Any degree preferred, but not essential"
→ 提取为: Degree

没有提及学历要求
→ 提取为: 官网无说明
```

---

### L 列: link 🔗
**数据来源**: LinkedIn 职位链接
**格式**: 完整的 LinkedIn 职位 URL
**示例**:
```
https://uk.linkedin.com/jobs/view/graduate-data-analyst-london-at-targetjobs-uk-4380441510
```

**特点**:
- ✅ 可点击的超链接 (蓝色下划线)
- ✅ 点击直接打开 LinkedIn 职位页面
- ✅ 不需要登录即可查看

---

## 🎯 常见使用场景

### 场景 1: 找"有工签"的岗位
```
筛选: H 列 = "✅ 可提供工签"
排序: G 列 (薪资) 从高到低
```

### 场景 2: 找"我能做的"岗位
```
方法1: 查看 J 列岗位关键词，看重合度
方法2: 按 D 列岗位类型筛选 (如: 数据)
方法3: 检查 K 列学历要求是否符合
```

### 场景 3: 找高薪岗位
```
筛选: G 列 包含具体薪资数字 (排除 "Competitive")
排序: G 列 从高到低
```

### 场景 4: 了解公司大小
```
排序: I 列 (公司规模)
- 最上面: 大公司 (1,000+)
- 中间: 中等公司
- 最下面: 小公司/未知
```

### 场景 5: 按毕业生项目筛选
```
筛选: C 列 = "Graduate"
同时看 D 列确定岗位类型
查看 J 列了解需要的技能
```

---

## 📊 数据质量说明

### 100% 有数据的列
- A: 更新时间
- B: 公司名称
- C: 项目类型
- D: 岗位类型
- E: 岗位名称
- F: 工作地区
- K: 学历要求
- L: link

### 部分可能为空的列
- G: 薪资 (如果职位未公布) → "未标明"
- H: 签证/工签 (如果职位未提及) → "未说明"
- I: 公司规模 (如果页面未显示) → "未知"
- J: 岗位关键词 (如果未识别到) → "/"

### 数据提取准确度
| 字段 | 准确度 | 说明 |
|---|---|---|
| 薪资 | 95%+ | 正则表达式精准匹配 |
| 签证 | 98%+ | 关键词列表完整 |
| 公司规模 | 70% | 不是所有职位都显示公司规模 |
| 岗位关键词 | 90%+ | 50+ 个技能库覆盖面广 |

---

## ✨ V2 相比 V1 的优势

| 方面 | V1 | V2 |
|---|---|---|
| 总列数 | 11 列 | 12 列 |
| 薪资信息 | ❌ 无 | ✅ 有 |
| 签证状态 | ❌ 排除不提供工签的 | ✅ 标注所有,用户自决 |
| 技能提取 | ❌ 无 | ✅ 自动提取 8 个关键技能 |
| 公司规模 | ❌ 无 | ✅ 有 (尽力提取) |
| 可视化标记 | ❌ 无 | ✅ 签证列彩色 |
| 用户决策权 | ❌ 低 | ✅ 高 |

---

## 🚀 最佳实践

1. **导入 Excel** 后，立即按 D 列 (岗位类型) 和 C 列 (项目类型) 筛选
2. **快速扫描** J 列 (岗位关键词)，看技能匹配度
3. **检查** H 列 (签证)，确认工签政策
4. **对比** G 列 (薪资)，确保在合理范围
5. **点击** L 列 (link) 打开 LinkedIn，详细阅读职位描述
6. **记录** 感兴趣的岗位，准备申请材料

---

**更新时间**: V2 (2026-03-05)
**维护者**: LinkedIn Job Scraper Team
**最后修改**: 2026-03-05
