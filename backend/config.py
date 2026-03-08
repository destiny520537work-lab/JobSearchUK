"""
GradJobsUK Backend Configuration
"""

# LinkedIn API endpoints
BASE_SEARCH_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
BASE_DETAIL_URL = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting"

# Search parameters
LOCATION = "United Kingdom"
GEO_ID = "101165590"
TIME_FILTER = "r604800"  # Past 7 days
EXPERIENCE_LEVEL = "1,2"  # Internship, Entry level

# Pagination
PAGE_SIZE = 25
MAX_PAGES = 6       # 6 pages × 25 = 150 results per keyword
MAX_APPLICANTS = 150

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 60  # seconds

# Request delay (anti-ban): random between MIN and MAX
MIN_DELAY = 0.8
MAX_DELAY = 2.0

# Cron interval
SCRAPE_INTERVAL_HOURS = 6

# Data retention
RETENTION_DAYS = 30

# Search keywords — CS & Data focus for international graduate students
SEARCH_KEYWORDS = [
    # ── Software Engineering ──────────────────────────────────────
    "Graduate Software Engineer",
    "Junior Software Engineer",
    "Software Developer Graduate",
    "Backend Developer Graduate",
    "Full Stack Developer Graduate",
    "Frontend Developer Graduate",
    "Graduate Developer",

    # ── Data & Analytics ─────────────────────────────────────────
    "Data Analyst Graduate",
    "Junior Data Analyst",
    "Data Analyst",
    "Business Intelligence Analyst",
    "Analytics Engineer",
    "Data Science Graduate Scheme",
    "Junior Data Scientist",
    "Product Analyst",

    # ── Machine Learning & AI ────────────────────────────────────
    "Machine Learning Engineer Graduate",
    "Junior Machine Learning Engineer",
    "AI Engineer Graduate",
    "NLP Engineer Graduate",
    "Computer Vision Engineer Graduate",

    # ── Data Engineering & Cloud ─────────────────────────────────
    "Data Engineer Graduate",
    "Junior Data Engineer",
    "Cloud Engineer Graduate",
    "DevOps Engineer Graduate",
    "Platform Engineer Graduate",

    # ── Quant & Business ─────────────────────────────────────────
    "Quantitative Analyst Graduate",
    "Business Analyst Graduate",
    "Credit Risk Analyst Graduate",
    "Technology Graduate Scheme",
    "Technology Analyst Graduate",
]

# Title keywords to exclude (with special logic for manager)
EXCLUDE_TITLE_KEYWORDS = [
    "senior",
    "lead",
    "principal",
    "director",
    "head of",
    "manager",
]

# Salary extraction patterns
SALARY_PATTERNS = [
    r'£[\d,]+\s*[-–to]+\s*£[\d,]+',
    r'£\d+k?\s*[-–to]+\s*£?\d+k',
    r'£[\d,]+\s*(?:per annum|per year|p\.?a\.?|annually)',
    r'£[\d,.]+\s*(?:per hour|per day|hourly|daily)',
    r'[Cc]ompetitive\s*(?:salary)?',
]

# Skill keywords (50+)
SKILL_KEYWORDS = {
    "Python", "R", "SQL", "Java", "Scala", "JavaScript", "SAS", "SPSS", "Stata",
    "C++", "Go", "Rust", "Ruby", "PHP",
    "Tableau", "Power BI", "Excel", "Looker", "Qlik", "Databricks", "dbt",
    "Google Sheets", "MATLAB",
    "AWS", "Azure", "GCP", "Snowflake", "BigQuery", "Redshift", "Athena",
    "Machine Learning", "Deep Learning", "NLP", "LLM", "GPT", "TensorFlow",
    "PyTorch", "Scikit-learn", "GenAI", "RAG", "Transformers",
    "ETL", "Airflow", "Spark", "Hadoop", "Kafka", "Docker", "Kubernetes",
    "Fivetran",
    "A/B Testing", "Statistical Analysis", "Regression", "Causal Inference",
    "Forecasting", "Time Series", "Segmentation", "Experimentation",
    "Agile", "Scrum", "JIRA", "Stakeholder Management", "Product Analytics",
    "Google Analytics", "Mixpanel", "Amplitude", "Segment",
    "Git", "API", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly",
    "LaTeX", "Jupyter", "REST", "GraphQL",
}
