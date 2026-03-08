"""
Configuration Examples
Uncomment and use these examples to customize your scraper behavior
"""

# ============================================================================
# EXAMPLE 1: Search only Data-related roles
# ============================================================================
EXAMPLE_1_KEYWORDS = [
    "Data Analyst",
    "Data Science Graduate Scheme",
    "Statistical Programmer",
    "Business Intelligence Analyst",
]


# ============================================================================
# EXAMPLE 2: Search only Product/AI roles
# ============================================================================
EXAMPLE_2_KEYWORDS = [
    "Product Analyst",
    "AI Product Manager",
    "Prompt Engineer",
    "NLP Data Analyst",
]


# ============================================================================
# EXAMPLE 3: Search only Entry-Level and Internship roles
# ============================================================================
EXAMPLE_3_KEYWORDS = [
    "Junior Data Analyst",
    "Data Science Graduate Scheme",
    "Quantitative Research Assistant",
    "Learning Analytics Specialist",
]


# ============================================================================
# EXAMPLE 4: Exclude more keywords (stricter filtering)
# ============================================================================
STRICT_EXCLUSION_KEYWORDS = [
    "senior",
    "lead",
    "principal",
    "director",
    "head of",
    "manager",
    "chief",
    "vice president",
    "executive",
    "experienced",
]


# ============================================================================
# EXAMPLE 5: Extend visa keywords (catch more sponsorship requirements)
# ============================================================================
EXTENDED_VISA_KEYWORDS = [
    "permanent right to work",
    "settled status",
    "indefinite leave",
    "right to work permanently",
    "uk work permit holders only",
    "visa sponsorship",
    "sponsorship required",
    "sponsored",
    "right to work",
    "must have right to work",
    "eligible to work",
    "british citizen",
]


# ============================================================================
# EXAMPLE 6: Lower applicant limit (less competition)
# ============================================================================
EXAMPLE_6_MAX_APPLICANTS = 50  # Only jobs with ≤ 50 applicants


# ============================================================================
# EXAMPLE 7: Longer delays (anti-ban protection)
# ============================================================================
EXAMPLE_7_DELAYS = {
    "MIN_DELAY": 3.0,   # Minimum 3 seconds between requests
    "MAX_DELAY": 6.0,   # Maximum 6 seconds between requests
}


# ============================================================================
# EXAMPLE 8: Alternative job type classification
# ============================================================================
def classify_job_type_extended(title):
    """Extended job type classification"""
    title_lower = title.lower()

    if any(k in title_lower for k in ["data analyst", "data science", "analytics", "analyst"]):
        return "数据分析"
    elif any(k in title_lower for k in ["product"]):
        return "产品"
    elif any(k in title_lower for k in ["business", "intelligence", "bi"]):
        return "商业分析"
    elif any(k in title_lower for k in ["nlp", "ai", "prompt", "machine learning", "deep learning"]):
        return "AI/ML"
    elif any(k in title_lower for k in ["quantitative", "statistical", "quant", "credit risk"]):
        return "定量分析"
    elif any(k in title_lower for k in ["engineer", "developer", "programmer"]):
        return "工程"
    elif any(k in title_lower for k in ["researcher"]):
        return "研究"
    else:
        return "其他"


# ============================================================================
# HOW TO USE THESE EXAMPLES
# ============================================================================
"""
1. To use EXAMPLE_1 (Data roles only):
   - Edit config.py
   - Replace SEARCH_KEYWORDS = [...]  with SEARCH_KEYWORDS = EXAMPLE_1_KEYWORDS

2. To use EXAMPLE_4 (stricter filtering):
   - Edit config.py
   - Replace EXCLUDE_TITLE_KEYWORDS with STRICT_EXCLUSION_KEYWORDS

3. To use EXAMPLE_7 (longer delays):
   - Edit config.py
   - Change MIN_DELAY = 3.0 and MAX_DELAY = 6.0

4. To use EXAMPLE_8 (extended classification):
   - Edit parser.py
   - Replace the classify_job_type function with classify_job_type_extended
"""


# ============================================================================
# QUICK PRESETS - Copy-paste configurations
# ============================================================================

# PRESET_DATA_ANALYST: Focus on all data analyst roles
PRESET_DATA_ANALYST = {
    "keywords": [
        "Data Analyst",
        "Product Analyst",
        "Statistical Programmer",
        "Business Intelligence Analyst",
        "Social Data Analyst",
    ],
    "max_applicants": 100,
    "min_delay": 1.5,
    "max_delay": 3.0,
}

# PRESET_ENTRY_LEVEL: Focus on entry-level and grad roles
PRESET_ENTRY_LEVEL = {
    "keywords": [
        "Junior Data Analyst",
        "Data Science Graduate Scheme",
        "Quantitative Research Assistant",
        "Learning Analytics Specialist",
        "Business Analyst",
    ],
    "max_applicants": 150,  # More lenient for entry-level
    "min_delay": 1.5,
    "max_delay": 3.0,
}

# PRESET_AI_TECH: Focus on AI and technical roles
PRESET_AI_TECH = {
    "keywords": [
        "AI Product Manager",
        "Prompt Engineer",
        "NLP Data Analyst",
        "Data Science Graduate Scheme",
        "Statistical Programmer",
    ],
    "max_applicants": 80,
    "min_delay": 1.5,
    "max_delay": 3.0,
}

# PRESET_COMPETITIVE: More aggressive (longer delays, fewer results)
PRESET_COMPETITIVE = {
    "keywords": [
        "Data Analyst",
        "Product Analyst",
        "Business Analyst",
    ],
    "max_applicants": 50,  # Only less competitive jobs
    "min_delay": 3.0,      # Longer delays
    "max_delay": 6.0,
}

# PRESET_FAST: Quick scan (all roles, high applicant limit)
PRESET_FAST = {
    "keywords": [  # All keywords
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
    ],
    "max_applicants": 200,  # Less filtering
    "min_delay": 1.0,       # Shorter delays
    "max_delay": 2.0,
}
