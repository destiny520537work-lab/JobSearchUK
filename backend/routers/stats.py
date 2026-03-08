"""
GET /api/stats — aggregated statistics for the dashboard cards and charts.
"""

import re
from collections import Counter
from datetime import datetime, timedelta, date as date_type
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import Job, get_session

router = APIRouter(prefix="/api/stats", tags=["stats"])


def _parse_salary_number(salary_text: str) -> Optional[int]:
    """Extract the midpoint salary as an integer from a salary string."""
    if not salary_text or salary_text in ("Not disclosed", "未标明"):
        return None
    # e.g. £30,000 - £45,000 → average 37500
    numbers = re.findall(r"(\d[\d,]*)", salary_text.replace(",", ""))
    nums = []
    for n in numbers:
        try:
            val = int(n)
            # Convert k notation: 30k → 30000
            if val < 1000 and "k" in salary_text.lower():
                val *= 1000
            if 5000 < val < 500000:
                nums.append(val)
        except ValueError:
            pass
    if nums:
        return sum(nums) // len(nums)
    return None


def _salary_band(salary_num: int) -> str:
    if salary_num < 20000:
        return "< £20k"
    if salary_num < 30000:
        return "£20k–30k"
    if salary_num < 40000:
        return "£30k–40k"
    if salary_num < 55000:
        return "£40k–55k"
    return "£55k+"


@router.get("")
async def get_stats(
    days: int = Query(default=7, ge=1, le=365),
    db: AsyncSession = Depends(get_session),
):
    cutoff_dt = datetime.utcnow() - timedelta(days=days)
    cutoff_date = cutoff_dt.date()
    stmt = select(Job).where(
        and_(
            Job.is_active == True,
            or_(
                Job.posted_date >= cutoff_date,
                and_(Job.posted_date == None, Job.scraped_at >= cutoff_dt),
            ),
        )
    )
    result = await db.execute(stmt)
    jobs = result.scalars().all()

    total = len(jobs)
    if total == 0:
        return {
            "total_jobs": 0,
            "sponsor_rate": 0,
            "avg_salary": None,
            "salary_disclosed_rate": 0,
            "by_location": [],
            "by_visa": [],
            "by_salary_band": [],
            "by_job_type": [],
            "last_updated": datetime.utcnow().isoformat(),
        }

    # Sponsor rate: ✅ confirmed + 🟡 licensed company (can sponsor even if role unspecified)
    sponsor_count = sum(1 for j in jobs if j.visa_status and ("✅" in j.visa_status or "🟡" in j.visa_status))
    sponsor_rate = round(sponsor_count / total, 4)

    # Salary stats
    salary_nums = [_parse_salary_number(j.salary) for j in jobs]
    salary_nums = [s for s in salary_nums if s]
    avg_salary = int(sum(salary_nums) / len(salary_nums)) if salary_nums else None
    salary_disclosed_rate = round(len(salary_nums) / total, 4)

    # By location (top 10)
    location_counter = Counter(j.location for j in jobs if j.location)
    by_location = [
        {"location": loc, "count": cnt}
        for loc, cnt in location_counter.most_common(10)
    ]

    # By visa status
    visa_counter = Counter(j.visa_status for j in jobs if j.visa_status)
    by_visa = [{"status": s, "count": c} for s, c in visa_counter.most_common()]

    # By salary band
    band_counter = Counter()
    for j in jobs:
        n = _parse_salary_number(j.salary)
        if n:
            band_counter[_salary_band(n)] += 1
    by_salary_band = [{"band": b, "count": c} for b, c in band_counter.most_common()]

    # By job type
    jt_counter = Counter(j.job_type for j in jobs if j.job_type)
    by_job_type = [{"type": t, "count": c} for t, c in jt_counter.most_common()]

    # Last updated
    last_scrape = max((j.scraped_at for j in jobs if j.scraped_at), default=None)

    return {
        "total_jobs": total,
        "sponsor_rate": sponsor_rate,
        "avg_salary": avg_salary,
        "salary_disclosed_rate": salary_disclosed_rate,
        "by_location": by_location,
        "by_visa": by_visa,
        "by_salary_band": by_salary_band,
        "by_job_type": by_job_type,
        "last_updated": last_scrape.isoformat() if last_scrape else None,
    }
