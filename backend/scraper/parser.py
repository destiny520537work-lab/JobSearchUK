"""
HTML parsing logic for LinkedIn job listings.
Migrated from _archive/parser.py — returns structured dicts instead of Excel rows.
"""

import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from bs4 import BeautifulSoup


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