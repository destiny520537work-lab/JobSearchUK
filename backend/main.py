"""
GradJobsUK — FastAPI entry point.
Starts APScheduler cron (every 6 hours) and mounts all routers.
"""

import asyncio
import logging
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routers import jobs, stats, filters, export, match
from scraper.sponsor_list import load_sponsor_set
from scraper.worker import run_scrape_job

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GradJobsUK API",
    description="UK graduate jobs for international students — cached LinkedIn data",
    version="4.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://job-search-uk.vercel.app",
        "http://localhost:5173",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(jobs.router)
app.include_router(stats.router)
app.include_router(filters.router)
app.include_router(export.router)
app.include_router(match.router)

scheduler = AsyncIOScheduler()


@app.on_event("startup")
async def startup():
    # 1. Create DB tables
    await init_db()
    logger.info("Database initialised.")

    # 2. Load GOV.UK sponsor list
    load_sponsor_set()

    # 3. Start cron scheduler (every 6 hours)
    scheduler.add_job(
        run_scrape_job,
        trigger="interval",
        hours=6,
        id="main_scrape",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started (every 6 hours).")

    # 4. Optionally trigger an immediate scrape on first startup
    if os.getenv("SCRAPE_ON_STARTUP", "false").lower() == "true":
        logger.info("SCRAPE_ON_STARTUP=true — triggering immediate scrape.")
        asyncio.create_task(run_scrape_job())


@app.on_event("shutdown")
async def shutdown():
    scheduler.shutdown(wait=False)


# Admin endpoint: manually trigger scrape (for development / testing)
@app.post("/api/admin/scrape", tags=["admin"])
async def trigger_scrape():
    asyncio.create_task(run_scrape_job())
    return {"message": "Scrape job started in background."}


@app.get("/api/health", tags=["health"])
async def health():
    return {"status": "ok"}
