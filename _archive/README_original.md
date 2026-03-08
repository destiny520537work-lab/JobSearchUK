# LinkedIn UK Job Scraper

A powerful Python tool to automatically scrape job listings from LinkedIn UK using the public Guest API (no login required).

## Features

- ✅ **No authentication required** - Uses LinkedIn's public Guest API
- ✅ **Targeted search** - 14 curated job titles for data/product/AI roles
- ✅ **Multi-level filtering** - Title, visa requirements, and applicant count filters
- ✅ **Comprehensive details** - Company, location, education requirements, applicant count
- ✅ **Auto-categorization** - Automatically classifies job types (数据/产品/AI/商业/定量/其他)
- ✅ **Anti-ban protection** - Random delays and user agent rotation
- ✅ **Progress tracking** - Real-time progress bars with tqdm
- ✅ **Excel export** - Professional formatted XLSX output with styling

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.py` to customize:

- **Search keywords** - Job titles to search for
- **Exclusion rules** - Title keywords to exclude (Senior, Lead, etc.)
- **Visa filters** - Keywords indicating visa sponsorship requirements
- **Search parameters** - Location, time range, experience level
- **Rate limiting** - Request delays and retry settings

## Usage

### Basic Usage

```bash
python scraper.py
```

This will:
1. Search all configured keywords
2. Filter results by title, visa requirements, and applicant count
3. Fetch detailed information for each job
4. Export results to `output/UK_jobs_YYYY-MM-DD.xlsx`

### Custom Output Filename

```bash
python scraper.py --output my_jobs.xlsx
```

### Search Specific Keywords

```bash
python scraper.py --keywords "Data Analyst" "Product Manager"
```

## Project Structure

```
linkedin-job-scraper/
├── scraper.py          # Main scraper program
├── config.py           # Configuration (keywords, filters, parameters)
├── parser.py           # HTML parsing and filtering logic
├── exporter.py         # Excel export functionality
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── output/             # Output directory (auto-created)
    └── UK_jobs_YYYY-MM-DD.xlsx  # Result file
```

## How It Works

### Phase 1: Search
- Searches each keyword using LinkedIn's Guest API
- Extracts job ID, title, company, location, and link
- Applies title-level filtering (excludes Senior, Lead, etc.)
- Paginates through all results

### Phase 2: Detail Processing
- Fetches detailed information for each job
- Extracts description, applicant count, and criteria
- Filters by visa requirements (permanent right to work, etc.)
- Filters by applicant count (≤ 100)
- Classifies job type and project type

### Phase 3: Export
- Deduplicates jobs by ID
- Exports to professional Excel file
- Applies formatting (headers, colors, hyperlinks)

## Filtering Rules

### Title Exclusions
Excludes jobs containing:
- Senior, Lead, Principal, Director, Head of, Manager (except "AI Product Manager" and "Product Manager")

### Visa Exclusions
Excludes jobs requiring:
- Permanent right to work
- Settled status
- Indefinite leave
- Right to work permanently
- UK work permit holders only

### Applicant Filtering
- Keeps only jobs with ≤ 100 applicants
- If applicant count is unknown, the job is kept

## Output Format

Excel file with columns:
- **更新时间** - Scrape date (YYYY-MM-DD)
- **公司名称** - Company name
- **项目类型** - Project type (full time / internship / graduate)
- **闭岗时间** - Closing date (LinkedIn doesn't provide this)
- **项目时间** - Project duration (LinkedIn doesn't provide this)
- **岗位类型** - Job classification (数据/产品/AI/商业/定量/其他)
- **岗位名称** - Job title
- **工作地区** - Location
- **学历要求** - Education requirement
- **毕业时间** - Graduation date (not available)
- **link** - LinkedIn job URL (clickable)

## Anti-Ban Protection

The scraper includes several anti-detection measures:
- Random User-Agent rotation
- Random delays between requests (1.5-3 seconds)
- Exponential backoff for rate limiting (429 errors)
- Maximum retry limit (3 attempts)

## Performance

Typical execution time: **5-15 minutes** depending on:
- Number of results
- Network speed
- Request delays
- Rate limiting

## Notes

1. **Rate Limiting** - If you encounter 429 errors, the tool automatically waits 60 seconds and retries up to 3 times
2. **Applicant Count** - Not all jobs may have applicant information available; missing values are marked as "未知"
3. **Deduplication** - Same job may appear in multiple keyword searches; automatically deduplicated by job_id
4. **Encoding** - All text is UTF-8 encoded
5. **Recommended Usage** - Run once per day with `f_TPR=r86400` to fetch only the past 24 hours of new jobs

## Troubleshooting

### No results found
- Check internet connection
- Verify keywords in config.py are correct
- LinkedIn may have changed their HTML structure - check browser console

### Rate limit errors persist
- Increase `RETRY_DELAY` in config.py
- Increase `MIN_DELAY` and `MAX_DELAY` values
- Run at different times

### Missing applicant information
- This is normal; some jobs don't display applicant counts
- The scraper keeps these jobs (marked as "未知")

## Legal Notice

This tool uses LinkedIn's public Guest API, which is accessible without authentication. Scraping should comply with:
- LinkedIn's Terms of Service
- Local data protection laws
- Responsible use guidelines

Use this tool for personal job search purposes only.

## License

This project is provided as-is for educational purposes.
