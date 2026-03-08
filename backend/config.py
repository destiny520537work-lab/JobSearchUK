"""
GradJobsUK Backend Configuration
"""

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
MAX_PAGES = 4
MAX_APPLICANTS = 100

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

# Search keywords (14 presets)
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
