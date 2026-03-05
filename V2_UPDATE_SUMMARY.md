# LinkedIn Job Scraper V2 - Update Summary

## 📋 V2 迭代完成清单

### ✅ 第一步：删除无用列 (3 列)
- ~~闭岗时间~~ ✓
- ~~项目时间~~ ✓
- ~~毕业时间~~ ✓

### ✅ 第二步：新增关键列 (4 列)

| 列 | 名称 | 数据来源 | 功能 |
|---|---|---|---|
| G | 💰 薪资 | 详情页 | 提取薪资范围（如 £30,000-45,000 或 Competitive） |
| H | 🔑 签证/工签 | 详情页描述 | 分类为"可提供工签"、"不提供工签"或"未说明" |
| I | 🏢 公司规模 | 详情页描述 | 提取公司员工规模（如 1000-5000 employees） |
| J | 📋 岗位关键词 | 详情页描述 | 自动提取 5-8 个核心技能（Python、SQL、Tableau等） |

### ✅ 第三步：新增 Excel 列结构 (总 12 列)

```
A: 更新时间        → 抓取日期 (YYYY-MM-DD)
B: 公司名称        → 公司名
C: 项目类型        → full time / Internship / Graduate
D: 岗位类型        → 数据/产品/AI/商业/定量/其他
E: 岗位名称        → 完整职位名称
F: 工作地区        → 城市/地区
G: 💰 薪资        → 薪资范围或 "Competitive" / "未标明"
H: 🔑 签证/工签     → ✅ 可提供工签 / ❌ 不提供工签 / 未说明
I: 🏢 公司规模     → 员工数 / "未知"
J: 📋 岗位关键词    → 技能关键词列表 (Python, SQL, Tableau...)
K: 学历要求        → Bachelor's Degree / Master's Degree / 官网无说明
L: link           → LinkedIn 职位链接 (可点击)
```

### ✅ 第四步：实现新的数据提取函数

**config.py 新增：**
- `SALARY_PATTERNS` - 薪资提取正则表达式
- `VISA_SPONSOR_POSITIVE` - 明确提供工签的关键词列表
- `VISA_SPONSOR_NEGATIVE` - 不提供工签/需要永居的关键词列表
- `SKILL_KEYWORDS` - 技能词库 (50+ 个技能关键字)
- 颜色配置: `VISA_YES_COLOR` (绿色), `VISA_NO_COLOR` (红色)

**parser.py 新增：**
- `extract_salary()` - 从描述中提取薪资信息
- `classify_visa_status()` - 分类签证赞助状态
- `extract_company_size()` - 提取公司规模
- `extract_skill_keywords()` - 提取岗位关键技能

**scraper.py 修改：**
- 导入新的提取函数
- 修改 `process_job_details()` 调用新函数
- 所有提取的信息添加到 job 字典中

**exporter.py 修改：**
- 调整列定义和顺序
- 为签证列 (H) 添加条件格式颜色标记
  - ✅ 可提供工签 → 绿色背景
  - ❌ 不提供工签 → 红色背景
  - 未说明 → 无背景

### ✅ 第五步：修改筛选规则

**保留的筛选：**
- ✅ 排除标题含 Senior/Lead/Principal 等的岗位
- ✅ 保留 "AI Product Manager" / "Product Manager" 特殊逻辑
- ✅ 申请人数 ≤ 100
- ✅ 过去 24 小时发布
- ✅ UK 地区
- ✅ Entry level / Internship 经验等级

**修改的筛选：**
- ❌ 删除：排除需要永居的岗位
- ✅ 改为：保留所有岗位，在 H 列标记签证状态，让用户自己决定

### ✅ 第六步：签证列条件格式

颜色标记已实现：
- 🟢 绿色背景 (FFD5F5D5) - "✅ 可提供工签"
- 🔴 红色背景 (FFFFD5D5) - "❌ 不提供工签"
- ⚪ 无背景 - "未说明"

---

## 📊 测试结果

### 测试执行
- **关键词**: "Data Analyst"
- **生成时间**: 2026-03-05
- **总岗位数**: 48 个

### 数据示例

```
岗位名称: Graduate Data Analyst - London
公司: hackajob
地区: London, England, United Kingdom
项目类型: Graduate
岗位类型: 数据
薪资: Competitive Salary
签证: ✅ 可提供工签 (绿色标记)
公司规模: 未知
岗位关键词: Python, Power BI, Tableau, Scala, RAG, Git, SAS, SQL
学历要求: Degree
```

### 签证分布 (V2 新功能)
- ✅ 可提供工签: 2 个 (绿色)
- ❌ 不提供工签: 1 个 (红色)
- 未说明: 45 个 (无颜色)

---

## 🚀 使用方法

### 基础运行
```bash
python scraper.py
```
搜索所有 14 个预设关键词，导出到 `output/UK_jobs_YYYY-MM-DD.xlsx`

### 自定义关键词
```bash
python scraper.py --keywords "Data Analyst" "Product Analyst"
```

### 自定义输出文件名
```bash
python scraper.py --output my_results.xlsx
```

### 完整示例
```bash
python scraper.py --keywords "Data Analyst" "AI Product Manager" --output data_ai_jobs.xlsx
```

---

## 📈 性能提升

**新增数据点**：每个岗位现在包含 4 个额外的关键信息
- 薪资信息 → 快速筛选薪资范围
- 签证状态 → 一目了然是否可工签
- 公司规模 → 了解公司大小
- 岗位关键词 → 快速判断技能匹配度

**用户决策权**：不再自动排除任何岗位，让用户根据签证状态自己决定

---

## 🔧 文件变更总结

### 修改的文件
- ✅ `config.py` - 新增配置 (visa keywords, salary patterns, skills library)
- ✅ `parser.py` - 新增 4 个提取函数
- ✅ `exporter.py` - 更新列结构和颜色格式
- ✅ `scraper.py` - 集成新的提取函数

### 新增文件
- ✅ `V2_UPDATE_SUMMARY.md` - 本文档

### 备份文件
- ✅ `parser_backup.py` - V1 版本备份
- ✅ `parser_fixed.py` - 修复后的版本

---

## ✨ V2 核心特性

| 特性 | 说明 |
|---|---|
| 🎯 更精准的职位信息 | 薪资、签证、公司规模、技能关键词 |
| 🟢 可视化标记 | 签证列自动着色 (绿/红/无) |
| 🧠 智能技能提取 | 自动识别 50+ 个技能关键词 |
| 📊 用户主权 | 所有岗位保留，签证状态标注，用户自决 |
| ⚡ 高效匹配 | 快速扫描岗位关键词判断适配度 |

---

## 📝 后续建议

### 可选增强
1. 在签证列添加数据有效性下拉列表
2. 添加"关键词匹配度"列（匹配我的技能数）
3. 添加"薪资评分"列（按薪资排序）
4. 实现自动过滤功能（按薪资、签证等）
5. 添加 PDF 导出功能

### 定时任务建议
```bash
# 每天 9AM 运行
0 9 * * * cd /path/to/linkedin-job-scraper && python scraper.py
```

---

**Status**: ✅ V2 完全就绪
**测试时间**: 2026-03-05
**下一版本**: V3 (敬请期待)
