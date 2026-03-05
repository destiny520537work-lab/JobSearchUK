# 🚀 Quick Start Guide

## Installation & Running (一键启动)

### macOS / Linux

```bash
chmod +x install_and_run.sh
./install_and_run.sh
```

### Windows

Double-click `install_and_run.bat` or run:

```cmd
install_and_run.bat
```

---

## Manual Installation (手动安装)

If the above doesn't work, follow these steps:

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Scraper

```bash
python scraper.py
```

---

## Advanced Usage (高级用法)

### Custom Output Filename

```bash
python scraper.py --output my_results.xlsx
```

### Search Specific Keywords Only

```bash
python scraper.py --keywords "Data Analyst" "Product Analyst"
```

### Combined Options

```bash
python scraper.py --output my_results.xlsx --keywords "Data Analyst" "AI Product Manager"
```

---

## Configuration Customization (自定义配置)

Edit `config.py` to customize:

1. **SEARCH_KEYWORDS** - Job titles to search for
2. **EXCLUDE_TITLE_KEYWORDS** - Keywords in titles to exclude
3. **EXCLUDE_VISA_KEYWORDS** - Visa requirement keywords to exclude
4. **MAX_APPLICANTS** - Maximum applicant count filter
5. **MIN_DELAY / MAX_DELAY** - Request delay range (for anti-ban protection)

### Example: Change Search Keywords

```python
# In config.py, modify SEARCH_KEYWORDS:
SEARCH_KEYWORDS = [
    "Data Analyst",
    "Product Manager",
    "Business Analyst",
]
```

### Example: Increase Anti-Ban Delays

```python
# In config.py, adjust delays:
MIN_DELAY = 2.0    # Minimum 2 seconds between requests
MAX_DELAY = 5.0    # Maximum 5 seconds between requests
```

---

## Understanding the Output

The output Excel file contains these columns:

| Column | Description | Source |
|--------|-------------|--------|
| 更新时间 | Scrape date | Generated |
| 公司名称 | Company name | LinkedIn list page |
| 项目类型 | Project type (full time/internship/graduate) | Analyzed from title |
| 闭岗时间 | Closing date | / (LinkedIn doesn't provide) |
| 项目时间 | Duration | / (LinkedIn doesn't provide) |
| 岗位类型 | Job category (数据/产品/AI/商业/定量/其他) | Auto-classified |
| 岗位名称 | Job title | LinkedIn list page |
| 工作地区 | Location | LinkedIn list page |
| 学历要求 | Education requirement | Extracted from job description |
| 毕业时间 | Graduation date | / (Not available) |
| link | LinkedIn job URL | Clickable hyperlink |

---

## Troubleshooting (故障排除)

### Problem: "ModuleNotFoundError: No module named 'fake_useragent'"

**Solution:**
```bash
pip install fake-useragent
```

### Problem: "No results found"

**Solutions:**
- Check internet connection
- Verify keywords in config.py are correct
- LinkedIn may have updated HTML structure
- Try running at a different time

### Problem: Getting 429 (Rate Limited) errors

**Solutions:**
- Increase delays in config.py:
  ```python
  MIN_DELAY = 3.0
  MAX_DELAY = 6.0
  ```
- Wait a few hours before running again
- Use fewer keywords

### Problem: "Permission denied" on install_and_run.sh

**Solution:**
```bash
chmod +x install_and_run.sh
./install_and_run.sh
```

---

## Performance Tips (性能优化)

1. **Search fewer keywords** - Reduces total execution time
   ```bash
   python scraper.py --keywords "Data Analyst"
   ```

2. **Run during off-peak hours** - Fewer rate limit issues
   - Best time: Early morning or late evening (UK time)

3. **Increase delays gradually** - If getting rate limited:
   ```python
   MIN_DELAY = 2.0
   MAX_DELAY = 4.0
   ```

4. **Run once per day** - The default `f_TPR=r86400` only fetches jobs from the past 24 hours

---

## Example Workflow (工作流示例)

### Daily Job Search Routine

```bash
# Every morning at 9 AM:
python scraper.py --output "jobs_$(date +%Y-%m-%d).xlsx"

# This creates: jobs_2024-03-05.xlsx, jobs_2024-03-06.xlsx, etc.
```

### Search for Specific Roles

```bash
# Only data roles:
python scraper.py --keywords "Data Analyst" "Data Science Graduate Scheme"

# Only product roles:
python scraper.py --keywords "Product Analyst" "AI Product Manager"

# Only AI roles:
python scraper.py --keywords "Prompt Engineer" "NLP Data Analyst"
```

---

## Need More Help?

- Read the full **README.md** for detailed documentation
- Check **config.py** for all available configuration options
- Review **parser.py** for filtering logic details
- Look at **scraper.py** for implementation details

---

## Happy Job Hunting! 🎯

Good luck with your job search! This tool will help you find the latest opportunities in the UK job market.
