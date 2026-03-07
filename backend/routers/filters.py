"""
GET /api/filters — returns all available filter values from the current DB state.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from database import Job, get_session

router = APIRouter(prefix="/api/filters", tags=["filters"])


@router.get("")
async def get_filter_options(db: AsyncSession = Depends(get_session)):
    # Locations
    loc_result = await db.execute(
        select(distinct(Job.location)).where(Job.is_active == True, Job.location.isnot(None))
    )
    locations = sorted([r[0] for r in loc_result if r[0]])

    # Job types
    jt_result = await db.execute(
        select(distinct(Job.job_type)).where(Job.is_active == True, Job.job_type.isnot(None))
    )
    job_types = sorted([r[0] for r in jt_result if r[0]])

    # Project types
    pt_result = await db.execute(
        select(distinct(Job.project_type)).where(Job.is_active == True, Job.project_type.isnot(None))
    )
    project_types = sorted([r[0] for r in pt_result if r[0]])

    # Skills (extract from comma-separated skills column)
    sk_result = await db.execute(
        select(Job.skills).where(Job.is_active == True, Job.skills.isnot(None), Job.skills != "")
    )
    skill_set = set()
    for row in sk_result:
        if row[0]:
            for skill in row[0].split(","):
                s = skill.strip()
                if s:
                    skill_set.add(s)
    skills = sorted(skill_set)

    # Visa status options
    visa_result = await db.execute(
        select(distinct(Job.visa_status)).where(Job.is_active == True, Job.visa_status.isnot(None))
    )
    visa_statuses = [r[0] for r in visa_result if r[0]]

    return {
        "locations": locations,
        "job_types": job_types,
        "project_types": project_types,
        "skills": skills,
        "visa_statuses": visa_statuses,
    }
