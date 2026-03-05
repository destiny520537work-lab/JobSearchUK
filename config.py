"""
Configuration for LinkedIn Job Scraper
"""

# Search keywords for job titles
SEARCH_KEYWORDS = [
    "Junior Data Analyst",
    "Data Analyst",
    "Product Analyst",
    "Statistical Programmer",
    "Business Intelligence Analyst",
    "NLP Data Analyst",
    "Data Science Graduate Scheme",
    "AI Product Manager",
    "Prompt Engineer",
    "Social Data Analyst",
    "Business Analyst",
    "Credit Risk Analyst Junior",
    "Quantitative Research Assistant",
    "Learning Analytics Specialist",
]

# Title keywords to exclude
EXCLUDE_TITLE_KEYWORDS = [
    "senior",
    "lead",
    "principal",
    "director",
    "head of",
    "manager",  # Will be handled with special logic for "product" or "AI"
]

# Visa-related keywords to exclude
EXCLUDE_VISA_KEYWORDS = [
    "permanent right to work",
    "settled status",
    "indefinite leave",
    "right to work permanently",
    "uk work permit holders only",
]

# LinkedIn API endpoints
BASE_SEARCH_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
BASE_DETAIL_URL = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting"

# Search parameters
LOCATION = "United Kingdom"
GEO_ID = "101165590"
TIME_FILTER = "r86400"  # Past 24 hours
EXPERIENCE_LEVEL = "1,2"  # Internship, Entry level

# Pagination
PAGE_SIZE = 25
MAX_APPLICANTS = 100

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 60  # seconds

# Request delay (anti-ban)
MIN_DELAY = 1.5
MAX_DELAY = 3.0

# Column definitions for Excel output
EXCEL_COLUMNS = [
    "更新时间",
    "公司名称",
    "项目类型",
    "闭岗时间",
    "项目时间",
    "岗位类型",
    "岗位名称",
    "工作地区",
    "学历要求",
    "毕业时间",
    "link",
]

# Column widths
COLUMN_WIDTHS = {
    "A": 14,   # 更新时间
    "B": 20,   # 公司名称
    "C": 16,   # 项目类型
    "D": 12,   # 闭岗时间
    "E": 14,   # 项目时间
    "F": 10,   # 岗位类型
    "G": 55,   # 岗位名称
    "H": 18,   # 工作地区
    "I": 16,   # 学历要求
    "J": 14,   # 毕业时间
    "K": 80,   # link
}

# Color scheme (BGR format for openpyxl)
HEADER_COLOR = "FF8CDDFA"  # Light blue
LINK_COLOR = "FF175CEB"    # LinkedIn blue
