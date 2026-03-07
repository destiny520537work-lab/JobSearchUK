"""
GET /api/jobs — multi-filter + pagination + sorting.
Pure database queries, zero LinkedIn requests.
"""

from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_, or_, select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from database import Job, get_session

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


def _salary_sort_key(salary_text: str) -> int:
    """Extract first number from salary string for sorting."""
    import re
    if not salary_text:
        return 0
    m = re.search(r"(\d[\d,]*)", salary_text.replace(",", ""))
    if m:
        try:
            return int(m.group(1).replace(",", ""))
        except ValueError:
            pass
    return 0


@router.get("")
async def get_jobs(
    q: Optional[str] = None,
    visa: List[str] = Query(default=[]),
    location: List[str] = Query(default=[]),
    job_type: List[str] = Query(default=[]),
    skills: List[str] = Query(default=[]),
    min_salary: Optional[int] = None,
    days: int = Query(default=7, ge=1, le=365),
    sort: str = Query(default="newest", pattern="^(newest|salary|match)$"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    db: AsyncSession = Depends(get_session),
):
    cutoff = datetime.utcnow() - timedelta(days=days)

    conditions = [
        Job.is_active == True,
        Job.scraped_at >= cutoff,
    ]

    if q:
        search_term = f"%{q}%"
        conditions.append(
            or_(
                Job.title.ilike(search_term),
                Job.company.ilike(search_term),
                Job.location.ilike(search_term),
            )
        )

    if visa:
        visa_conditions = [Job.visa_status.ilike(f"%{v}%") for v in visa]
        conditions.append(or_(*visa_conditions))

    if location:
        loc_conditions = [Job.location.ilike(f"%{loc}%") for loc in location]
        conditions.append(or_(*loc_conditions))

    if job_type:
        jt_conditions = [Job.job_type == jt for jt in job_type]
        conditions.append(or_(*jt_conditions))

    if skills:
        skill_conditions = [Job.skills.ilike(f"%{sk}%") for sk in skills]
        conditions.append(or_(*skill_conditions))

    # Count total matching
    count_stmt = select(func.count()).select_from(Job).where(and_(*conditions))
    total = await db.scalar(count_stmt)

    # Fetch page
    stmt = select(Job).where(and_(*conditions))

    if sort == "newest":
        stmt = stmt.order_by(Job.posted_date.desc().nulls_last(), Job.scraped_at.desc())
    elif sort == "salary":
        # Sort in Python after fetching (salary is a text field)
        stmt = stmt.order_by(Job.scraped_at.desc())
    else:
        stmt = stmt.order_by(Job.scraped_at.desc())

    offset = (page - 1) * page_size
    stmt = stmt.offset(offset).limit(page_size)

    result = await db.execute(stmt)
    jobs = result.scalars().all()

    if sort == "salary":
        jobs = sorted(jobs, key=lambda j: _salary_sort_key(j.salary), reverse=True)

    items = [_job_to_dict(j) for j in jobs]

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size,
        "items": items,
    }


def _job_to_dict(job: Job) -> dict:
    return {
        "id": job.id,
        "job_id": job.job_id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "salary": job.salary,
        "visa_status": job.visa_status,
        "company_size": job.company_size,
        "skills": job.skills,
        "education": job.education,
        "project_type": job.project_type,
        "job_type": job.job_type,
        "link": job.link,
        "applicant_count": job.applicant_count,
        "posted_date": job.posted_date.isoformat() if job.posted_date else None,
        "scraped_at": job.scraped_at.isoformat() if job.scraped_at else None,
    }
