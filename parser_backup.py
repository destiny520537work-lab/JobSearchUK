"""
HTML parsing logic for LinkedIn job listings
"""

import re
from bs4 import BeautifulSoup
from config import EXCLUDE_TITLE_KEYWORDS, EXCLUDE_VISA_KEYWORDS, MAX_APPLICANTS


def parse_job_cards(html_content):
    """
    Parse job listing cards from HTML

    Args:
        html_content: HTML response from LinkedIn jobs API

    Returns:
        List of dictionaries containing job information
    """
    soup = BeautifulSoup(html_content, "html.parser")
    jobs = []

    # Find all job cards (try multiple selectors)
    job_cards = soup.find_all("li")

    for card in job_cards:
        try:
            # Extract job ID from data-entity-urn
            job_id_raw = card.get("data-entity-urn", "")
            if not job_id_raw:
                continue

            job_id = job_id_raw.split(":")[-1]

            # Extract title
            title_elem = card.find("h3", class_="base-search-card__title")
            if not title_elem:
                title_elem = card.find("span", class_="sr-only")
            title = title_elem.get_text(strip=True) if title_elem else ""

            if not title:
                continue

            # Extract company
            company_elem = card.find("h4", class_="base-search-card__subtitle")
            company = company_elem.get_text(strip=True) if company_elem else ""

            # Extract location
            location_elem = card.find("span", class_="job-search-card__location")
            location = location_elem.get_text(strip=True) if location_elem else ""

            # Extract link
            link_elem = card.find("a", class_="base-card__full-link")
            link = link_elem.get("href", "") if link_elem else ""

            # Extract posted date
            time_elem = card.find("time", class_="job-search-card__listdate")
            posted_date = time_elem.get("datetime") if time_elem else None

            if job_id and title and company and location and link:
                jobs.append({
                    "job_id": job_id,
                    "title": title,
                    "company": company,
                    "location": location,
                    "link": link,
                    "posted_date": posted_date,
                })
        except Exception as e:
            # Skip malformed cards
            continue

    return jobs


def parse_job_detail(html_content):
    """
    Parse job detail page

    Args:
        html_content: HTML response from job detail page

    Returns:
        Dictionary with job details: description, applicants, seniority, employment_type
    """
    soup = BeautifulSoup(html_content, "html.parser")

    details = {
        "description": "",
        "applicant_count": None,
        "seniority": "",
        "employment_type": "",
        "job_function": "",
        "industries": "",
    }

    # Extract full description
    desc_elem = soup.find("div", class_="description__text")
    if desc_elem:
        details["description"] = desc_elem.get_text(strip=True)

    # Extract applicant count (multiple possible locations)
    applicant_count = None

    # Method 1: figcaption
    figcaption = soup.find("figcaption", class_="num-applicants__caption")
    if figcaption:
        text = figcaption.get_text()
        match = re.search(r"(\d+)", text)
        if match:
            applicant_count = int(match.group(1))

    # Method 2: span with applicants text
    if not applicant_count:
        text_content = soup.get_text()
        match = re.search(r"(\d+)\s*(?:applicants?|已申请)", text_content)
        if match:
            applicant_count = int(match.group(1))

    details["applicant_count"] = applicant_count

    # Extract job criteria
    criteria_items = soup.find_all("li", class_="description__job-criteria-item")

    if len(criteria_items) > 0:
        # Seniority level
        details["seniority"] = criteria_items[0].get_text(strip=True)

    if len(criteria_items) > 1:
        # Employment type
        details["employment_type"] = criteria_items[1].get_text(strip=True)

    if len(criteria_items) > 2:
        # Job function
        details["job_function"] = criteria_items[2].get_text(strip=True)

    if len(criteria_items) > 3:
        # Industries
        details["industries"] = criteria_items[3].get_text(strip=True)

    return details


def filter_by_title(title):
    """
    Filter job by title - exclude unwanted titles

    Args:
        title: Job title

    Returns:
        Boolean - True if job should be kept, False if excluded
    """
    title_lower = title.lower()

    for keyword in EXCLUDE_TITLE_KEYWORDS:
        if keyword in title_lower:
            # Special logic: keep if it's "AI Product Manager" or "Product Manager"
            if keyword == "manager":
                if any(p in title_lower for p in ["product", "ai"]):
                    return True
            # For other exclusion keywords, always exclude
            return False

    return True


def filter_by_visa(description):
    """
    Filter job by visa requirements

    Args:
        description: Job description text

    Returns:
        Boolean - True if job should be kept, False if excluded
    """
    desc_lower = description.lower()

    for keyword in EXCLUDE_VISA_KEYWORDS:
        if keyword in desc_lower:
            return False

    return True


def filter_by_applicants(applicant_count):
    """
    Filter job by applicant count

    Args:
        applicant_count: Number of applicants (or None if unknown)

    Returns:
        Boolean - True if job should be kept, False if excluded
    """
    if applicant_count is None:
        # Keep jobs with unknown applicant count
        return True

    return applicant_count <= MAX_APPLICANTS


def classify_job_type(title):
    """
    Classify job type based on title

    Args:
        title: Job title

    Returns:
        Job type string (数据, 产品, 商业, AI, 定量, 其他)
    """
    title_lower = title.lower()

    if any(k in title_lower for k in ["data analyst", "data science", "analytics"]):
        return "数据"
    elif any(k in title_lower for k in ["product analyst", "product manager"]):
        return "产品"
    elif any(k in title_lower for k in ["business analyst", "business intelligence", "bi"]):
        return "商业"
    elif any(k in title_lower for k in ["nlp", "ai ", "prompt engineer", "machine learning"]):
        return "AI"
    elif any(k in title_lower for k in ["quantitative", "statistical", "credit risk"]):
        return "定量"
    else:
        return "其他"


def classify_project_type(title, employment_type=""):
    """
    Classify project type

    Args:
        title: Job title
        employment_type: Employment type from LinkedIn

    Returns:
        Project type string (Internship, Graduate, full time)
    """
    title_lower = title.lower()

    if "intern" in title_lower:
        return "Internship"
    elif "graduate" in title_lower or "grad scheme" in title_lower:
        return "Graduate"
    elif "graduate" in employment_type.lower():
        return "Graduate"
    else:
        return "full time"


def extract_education_requirement(description):
    """
    Extract education requirement from job description

    Args:
        description: Job description text

    Returns:
        Education requirement or "官网无说明"
    """
    if not description:
        return "官网无说明"

    # Common education level keywords
    education_keywords = {
        "bachelor's degree": "Bachelor's Degree",
        "bachelor degree": "Bachelor's Degree",
        "bachelor": "Bachelor's Degree",
        "master's degree": "Master's Degree",
        "master degree": "Master's Degree",
        "phd": "PhD",
        "diploma": "Diploma",
        "higher national diploma": "HND",
        "hnd": "HND",
        "a level": "A Level",
        "gcse": "GCSE",
        "degree": "Degree",
    }

    desc_lower = description.lower()

    # Priority order: most specific first
    for keyword, label in education_keywords.items():
        if keyword in desc_lower:
            return label

    return "官网无说明"
