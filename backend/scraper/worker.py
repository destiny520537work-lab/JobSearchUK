"""
Cron worker: scrape LinkedIn every 6 hours, write results to DB.
Single-threaded, conservative rate (2-5s delay between requests).
"""

import asyncio
import logging
import random
import time
from datetime import date, datetime, timedelta

import requests
from fake_useragent import UserAgent

from config import (
    BASE_DETAIL_URL,
    BASE_SEARCH_URL,
    EXPERIENCE_LEVEL,
    GEO_ID,
    LOCATION,
    MAX_DELAY,
    MAX_PAGES,
    MAX_RETRIES,
    MIN_DELAY,
    PAGE_SIZE,
    RETRY_DELAY,
    RETENTION_DAYS,
    SCRAPE_INTERVAL_HOURS,
    SEARCH_KEYWORDS,
    TIME_FILTER,
)
from database import AsyncSessionLocal, Job
from scraper.parser import (
    classify_job_type,
    classify_project_type,
    extract_company_size,
    extract_education,
    extract_salary,
    extract_skill_keywords,
    filter_by_applicants,
    filter_by_title,
    parse_job_cards,
    parse_job_detail,
)
from scraper.sponsor_list import get_sponsor_set
from scraper.visa_checker import check_sponsor_list, classify_visa_from_text, final_visa_verdict
from sqlalchemy import select, update

logger = logging.getLogger(__name__)
ua = UserAgent()


def _get_headers() -> dict:
    return {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Referer": "https://www.linkedin.com/jobs/search/",
    }


def _safe_get(url: str, params: dict = None) -> requests.Response | None:
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(url, params=params, headers=_get_headers(), timeout=15)
            if resp.status_code == 429:
                logger.warning("Rate limited (429). Waiting %ds before retry %d/%d",
                               RETRY_DELAY, attempt + 1, MAX_RETRIES)
                time.sleep(RETRY_DELAY)
                continue
            resp.raise_for_status()
            return resp
        except requests.RequestException as e:
            logger.error("Request failed: %s (attempt %d/%d)", e, attempt + 1, MAX_RETRIES)
            if attempt < MAX_RETRIES - 1:
                time.sleep(5 * (attempt + 1))
    return None


def _scrape_keyword(keyword: str) -> list[dict]:
    """Scrape one keyword across up to MAX_PAGES pages. Returns raw job list."""
    jobs = []
    seen_ids = set()

    for page in range(MAX_PAGES):
        params = {
            "keywords": keyword,
            "location": LOCATION,
            "geoId": GEO_ID,
            "f_TPR": TIME_FILTER,
            "f_E": EXPERIENCE_LEVEL,
            "start": page * PAGE_SIZE,
        }
        resp = _safe_get(BASE_SEARCH_URL, params=params)
        if not resp:
            break

        cards = parse_job_cards(resp.text)
        if not cards:
            break  # No more results

        new = [c for c in cards if c["job_id"] not in seen_ids and filter_by_title(c["title"])]
        seen_ids.update(c["job_id"] for c in new)
        jobs.extend(new)

        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        time.sleep(delay)

    return jobs


def _enrich_job(job: dict, sponsor_set: set) -> dict:
    """Fetch detail page, enrich job dict with visa/salary/skills/etc."""
    url = f"{BASE_DETAIL_URL}/{job['job_id']}"
    resp = _safe_get(url)
    if not resp:
        return job

    detail = parse_job_detail(resp.text)

    if not filter_by_applicants(detail.get("applicant_count")):
        return None  # Too many applicants — skip

    desc = detail.get("description", "")
    text_verdict = classify_visa_from_text(desc)
    on_list = check_sponsor_list(job["company"], sponsor_set)
    visa_status = final_visa_verdict(text_verdict, on_list)

    job.update({
        "description": desc,
        "applicant_count": detail.get("applicant_count"),
        "salary": extract_salary(desc),
        "visa_status": visa_status,
        "company_size": extract_company_size(desc),
        "skills": extract_skill_keywords(desc),
        "education": extract_education(desc),
        "project_type": classify_project_type(
            job["title"], detail.get("employment_type", "")
        ),
        "job_type": classify_job_type(job["title"]),
    })
    return job


async def _upsert_jobs(jobs: list[dict], keyword: str):
    """Insert or update jobs in DB."""
    async with AsyncSessionLocal() as session:
        for j in jobs:
            if not j:
                continue
            # Parse posted_date
            posted = None
            if j.get("posted_date"):
                try:
                    posted = date.fromisoformat(j["posted_date"][:10])
                except Exception:
                    pass

            existing = await session.scalar(
                select(Job).where(Job.job_id == j["job_id"])
            )
            if existing:
                # Update changeable fields
                existing.visa_status = j.get("visa_status", existing.visa_status)
                existing.salary = j.get("salary", existing.salary)
                existing.skills = j.get("skills", existing.skills)
                existing.applicant_count = j.get("applicant_count", existing.applicant_count)
                existing.scraped_at = datetime.utcnow()
                existing.is_active = True
            else:
                session.add(Job(
                    job_id=j["job_id"],
                    title=j["title"],
                    company=j["company"],
                    location=j["location"],
                    salary=j.get("salary", "Not disclosed"),
                    visa_status=j.get("visa_status", "Not specified"),
                    company_size=j.get("company_size", "Unknown"),
                    skills=j.get("skills", ""),
                    education=j.get("education", "Not specified"),
                    project_type=j.get("project_type", "full time"),
                    job_type=j.get("job_type", "其他"),
                    link=j["link"],
                    description=j.get("description", ""),
                    applicant_count=j.get("applicant_count"),
                    posted_date=posted,
                    source_keyword=keyword,
                ))
        await session.commit()


async def _deactivate_old_jobs():
    """Mark jobs older than RETENTION_DAYS as inactive."""
    cutoff = datetime.utcnow() - timedelta(days=RETENTION_DAYS)
    async with AsyncSessionLocal() as session:
        await session.execute(
            update(Job)
            .where(Job.scraped_at < cutoff)
            .values(is_active=False)
        )
        await session.commit()


async def run_scrape_job():
    """Main cron entry point: scrape all keywords and write to DB."""
    logger.info("=== Scrape job started at %s ===", datetime.utcnow().isoformat())
    sponsor_set = get_sponsor_set()
    total_saved = 0

    for keyword in SEARCH_KEYWORDS:
        logger.info("Scraping keyword: %s", keyword)
        try:
            raw_jobs = _scrape_keyword(keyword)
            logger.info("  Found %d candidate jobs", len(raw_jobs))

            enriched = []
            for job in raw_jobs:
                result = _enrich_job(job, sponsor_set)
                if result:
                    result["source_keyword"] = keyword
                    enriched.append(result)
                delay = random.uniform(MIN_DELAY, MAX_DELAY)
                time.sleep(delay)

            await _upsert_jobs(enriched, keyword)
            total_saved += len(enriched)
            logger.info("  Saved %d jobs for '%s'", len(enriched), keyword)
        except Exception as e:
            logger.error("Error scraping '%s': %s", keyword, e)

    await _deactivate_old_jobs()
    logger.info("=== Scrape job complete. Total saved: %d ===", total_saved)
