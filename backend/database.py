"""
SQLAlchemy async database models and connection setup.
Uses SQLite for local dev, PostgreSQL for production (set DATABASE_URL env var).
"""

import os
from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Date, DateTime,
    Index, select, func
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./gradjobs.db")
# Railway provides postgresql:// but asyncpg requires postgresql+asyncpg://
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(20), unique=True, nullable=False, index=True)
    title = Column(Text, nullable=False)
    company = Column(Text, nullable=False)
    location = Column(Text)
    salary = Column(Text, default="Not disclosed")
    visa_status = Column(Text, default="Not specified")
    company_size = Column(Text, default="Unknown")
    skills = Column(Text)                     # comma-separated
    education = Column(Text, default="Not specified")
    project_type = Column(Text)               # full time / Internship / Graduate
    job_type = Column(Text)                   # 数据 / 产品 / AI / 商业 / 定量 / 其他
    link = Column(Text, nullable=False)
    description = Column(Text)               # full text for CV matching
    applicant_count = Column(Integer)
    posted_date = Column(Date)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    source_keyword = Column(Text)            # which search keyword found this job

    __table_args__ = (
        Index("idx_jobs_visa", "visa_status"),
        Index("idx_jobs_location", "location"),
        Index("idx_jobs_posted", "posted_date"),
        Index("idx_jobs_active", "is_active"),
        Index("idx_jobs_job_type", "job_type"),
    )


class SponsorCompany(Base):
    __tablename__ = "sponsor_list"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(Text, nullable=False, index=True)
    town_city = Column(Text)
    route = Column(Text)
    rating = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow)


async def init_db():
    """Create all tables if they don't exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """Dependency: yield a DB session."""
    async with AsyncSessionLocal() as session:
        yield session
