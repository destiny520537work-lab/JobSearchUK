"""
HTML parsing logic for LinkedIn job listings.
Migrated from _archive/parser.py — returns structured dicts instead of Excel rows.
"""

import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from bs4 import BeautifulSoup
from config import (
    EXCLUDE_TITLE_KEYWORDS,
    MAX_APPLICANTS,
    SALARY_PATTERNS,
    SKILL_KEYWORDS,
)


def parse_job_cards(html_content: str) -> list[dict]:
    """Parse job listing cards. Returns list of basic job dicts."""
    soup = BeautifulSoup(html_content, "html.parser")
    jobs = []

    for card in soup.find_all("div", class_="base-search-card"):
        try:
            job_id_raw = card.get("data-entity-urn", "")
            if not job_id_raw:
                continue
            job_id = job_id_raw.split(":")[-1]

            title_elem = card.find("h3", class_="base-search-card__title")
            title = title_elem.get_text(strip=True) if title_elem else ""
            if not title:
                continue

            company_elem = card.find("h4", class_="base-search-card__subtitle")
            company = ""
            if company_elem:
                link_elem = company_elem.find("a")
                company = link_elem.get_text(strip=True) if link_elem else ""

            location_elem = card.find("span", class_="job-search-card__location")
            location = location_elem.get_text(strip=True) if location_elem else ""

            link_elem = card.find("a", class_="base-card__full-link")
            link = link_elem.get("href", "") if link_elem else ""

            time_elem = card.find("time")
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
        except Exception:
            continue

    return jobs


def parse_job_detail(html_content: str) -> dict:
    """Parse job detail page. Returns dict with description, applicants, etc."""
    soup = BeautifulSoup(html_content, "html.parser")

    details = {
        "description": "",
        "applicant_count": None,
        "seniority": "",
        "employment_type": "",
        "job_function": "",
        "industries": "",
    }

    desc_elem = soup.find("div", class_="description__text")
    if desc_elem:
        details["description"] = desc_elem.get_text(strip=True)

    # Applicant count — try figcaption first, then full-text regex
    figcaption = soup.find("figcaption", class_="num-applicants__caption")
    if figcaption:
        m = re.search(r"(\d+)", figcaption.get_text())
        if m:
            details["applicant_count"] = int(m.group(1))

    if not details["applicant_count"]:
        m = re.search(r"(\d+)\s*(?:applicants?|已申请)", soup.get_text())
        if m:
            details["applicant_count"] = int(m.group(1))

    # Job criteria items (seniority, type, function, industries)
    criteria = soup.find_all("li", class_="description__job-criteria-item")
    labels = ["seniority", "employment_type", "job_function", "industries"]
    for i, label in enumerate(labels):
        if i < len(criteria):
            details[label] = criteria[i].get_text(strip=True)

    return details


def filter_by_title(title: str) -> bool:
    """Return True to keep, False to exclude."""
    title_lower = title.lower()
    for kw in EXCLUDE_TITLE_KEYWORDS:
        if kw in title_lower:
            if kw == "manager" and any(p in title_lower for p in ["product", "ai"]):
                return True
            return False
    return True


def filter_by_applicants(applicant_count) -> bool:
    if applicant_count is None:
        return True
    return applicant_count <= MAX_APPLICANTS


def classify_job_type(title: str) -> str:
    t = title.lower()
    # Software Engineering (check before data to avoid misclassifying "data engineer")
    if any(k in t for k in [
        "software engineer", "software developer", "backend", "frontend",
        "full stack", "fullstack", "platform engineer", "devops", "cloud engineer",
        "site reliability", "sre", "infrastructure engineer",
    ]):
        return "软件"
    if any(k in t for k in [
        "data engineer", "data analyst", "data science", "analytics engineer",
        "analytics", "business intelligence", " bi ",
    ]):
        return "数据"
    if any(k in t for k in [
        "machine learning", "ml engineer", "ai engineer", "nlp", "ai ",
        "computer vision", "deep learning", "prompt engineer", "llm",
    ]):
        return "AI"
    if any(k in t for k in ["product analyst", "product manager"]):
        return "产品"
    if any(k in t for k in ["business analyst", "technology analyst"]):
        return "商业"
    if any(k in t for k in ["quantitative", "statistical", "credit risk"]):
        return "定量"
    return "其他"


def classify_project_type(title: str, employment_type: str = "") -> str:
    t = title.lower()
    if "intern" in t:
        return "Internship"
    if "graduate" in t or "grad scheme" in t:
        return "Graduate"
    if "graduate" in employment_type.lower():
        return "Graduate"
    return "full time"


def extract_salary(description: str) -> str:
    if not description:
        return "Not disclosed"
    for pattern in SALARY_PATTERNS:
        m = re.search(pattern, description, re.IGNORECASE)
        if m:
            return m.group(0).strip()
    return "Not disclosed"


def extract_company_size(description: str) -> str:
    if not description:
        return "Unknown"
    patterns = [
        r"([\d,]+-[\d,]+)\s*employees",
        r"([\d,]+)\+?\s*employees",
        r"Company size[:\s]*([\d,]+-[\d,]+)",
    ]
    for pattern in patterns:
        m = re.search(pattern, description, re.IGNORECASE)
        if m:
            return m.group(0).strip()
    return "Unknown"


def extract_skill_keywords(description: str) -> str:
    if not description:
        return ""
    found = []
    text_lower = description.lower()
    for skill in SKILL_KEYWORDS:
        if len(skill) <= 2:
            if re.search(r"\b" + re.escape(skill) + r"\b", description):
                found.append(skill)
        else:
            if skill.lower() in text_lower:
                found.append(skill)
    seen = set()
    unique = []
    for s in found:
        if s.lower() not in seen:
            seen.add(s.lower())
            unique.append(s)
    return ", ".join(unique[:8])


def extract_education(description: str) -> str:
    if not description:
        return "Not specified"
    d = description.lower()
    if "phd" in d or "doctorate" in d:
        return "PhD"
    if "master" in d:
        return "Master's Degree"
    if "bachelor" in d or "degree" in d:
        return "Bachelor's Degree"
    if "diploma" in d or "hnd" in d:
        return "Diploma/HND"
    return "Not specified"
