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

# Column definitions for Excel output (V2)
EXCEL_COLUMNS = [
    "更新时间",      # A
    "公司名称",      # B
    "项目类型",      # C
    "岗位类型",      # D
    "岗位名称",      # E
    "工作地区",      # F
    "💰 薪资",       # G
    "🔑 签证/工签",  # H
    "🏢 公司规模",   # I
    "📋 岗位关键词", # J
    "学历要求",      # K
    "link",          # L
]

# Column widths (V2)
COLUMN_WIDTHS = {
    "A": 14,   # 更新时间
    "B": 20,   # 公司名称
    "C": 16,   # 项目类型
    "D": 10,   # 岗位类型
    "E": 50,   # 岗位名称
    "F": 18,   # 工作地区
    "G": 22,   # 薪资
    "H": 16,   # 签证/工签
    "I": 18,   # 公司规模
    "J": 45,   # 岗位关键词
    "K": 16,   # 学历要求
    "L": 70,   # link
}

# Color scheme (BGR format for openpyxl)
HEADER_COLOR = "FF8CDDFA"  # Light blue
LINK_COLOR = "FF175CEB"    # LinkedIn blue
VISA_YES_COLOR = "FFD5F5D5"  # Light green (可提供工签)
VISA_NO_COLOR = "FFFFD5D5"   # Light red (不提供工签)

# ============================================================================
# V2 NEW: Visa/Sponsorship Keywords
# ============================================================================
VISA_SPONSOR_POSITIVE = [
    "visa sponsorship is available",
    "visa sponsorship available",
    "we can sponsor",
    "we will sponsor",
    "able to sponsor",
    "offer sponsorship",
    "sponsor a work visa",
    "sponsor your visa",
    "skilled worker visa",
    "provide sponsorship",
    "sponsorship can be offered",
    "sponsor candidates",
    "visa support",
    "work visa support",
]

VISA_SPONSOR_NEGATIVE = [
    "cannot sponsor",
    "can not sponsor",
    "will not sponsor",
    "won't sponsor",
    "not able to sponsor",
    "no sponsorship",
    "unable to sponsor",
    "without requiring sponsorship",
    "without sponsorship",
    "must have the right to work",
    "right to work in the uk without",
    "permanent right to work",
    "settled status",
    "indefinite leave to remain",
    "pre-settled status",
    "not offer visa sponsorship",
    "do not sponsor",
    "doesn't sponsor",
    "does not sponsor",
]

# ============================================================================
# V2 NEW: Salary Extraction Patterns
# ============================================================================
SALARY_PATTERNS = [
    r'£[\d,]+\s*[-–to]+\s*£[\d,]+',           # £30,000 - £45,000
    r'£\d+k?\s*[-–to]+\s*£?\d+k',             # £30k - £45k
    r'£[\d,]+\s*(?:per annum|per year|p\.?a\.?|annually)',  # £30,000 per annum
    r'£[\d,.]+\s*(?:per hour|per day|hourly|daily)',        # £25 per hour
    r'[Cc]ompetitive\s*(?:salary)?',          # Competitive
]

# ============================================================================
# V2 NEW: Skill Keywords Library
# ============================================================================
SKILL_KEYWORDS = {
    # Programming Languages
    "Python", "R", "SQL", "Java", "Scala", "JavaScript", "SAS", "SPSS", "Stata",
    "C++", "Go", "Rust", "Ruby", "PHP",

    # Data Tools
    "Tableau", "Power BI", "Excel", "Looker", "Qlik", "Databricks", "dbt",
    "Google Sheets", "MATLAB",

    # Cloud Platforms
    "AWS", "Azure", "GCP", "Snowflake", "BigQuery", "Redshift", "Athena",

    # ML/AI
    "Machine Learning", "Deep Learning", "NLP", "LLM", "GPT", "TensorFlow",
    "PyTorch", "Scikit-learn", "GenAI", "RAG", "Transformers",

    # Data Engineering
    "ETL", "Airflow", "Spark", "Hadoop", "Kafka", "Docker", "Kubernetes",
    "dbt", "Fivetran",

    # Analytics & Statistical Methods
    "A/B Testing", "Statistical Analysis", "Regression", "Causal Inference",
    "Forecasting", "Time Series", "Segmentation", "Experimentation",

    # Product & Business
    "Agile", "Scrum", "JIRA", "Stakeholder Management", "Product Analytics",
    "Google Analytics", "Mixpanel", "Amplitude", "Segment",

    # Other Tools
    "Git", "API", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly",
    "LaTeX", "Jupyter", "REST", "GraphQL",
}
