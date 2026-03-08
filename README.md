# GradJobsUK

> Forked and redesigned from [JobSearchUK](https://github.com/destiny520537work-lab/JobSearchUK) (personal CLI tool) into a full-stack web platform.

A web platform for international students searching for graduate jobs in the UK, featuring automatic visa sponsorship detection and LinkedIn data cached every 6 hours.

---

## Architecture

```
Cron Worker (every 6h)
  └─ LinkedIn Guest API → PostgreSQL
         ↓
    FastAPI backend (pure DB queries)
         ↓
    React frontend (Vercel)
```

Users see only cached data — no real-time LinkedIn requests, so no ban risk.

---
## User Flow

```
sequenceDiagram
    participant Cron as Cron Worker (6h)
    participant Scraper as Scraper.py
    participant VC as Visa Verification (3-Layer)
    participant DB as PostgreSQL (Supabase)
    actor User
    participant FE as React Frontend (Vercel)
    participant BE as FastAPI Backend (Railway/Render)

    Note over Cron, DB: Data Sourcing Phase (Every 6 Hours)
    Cron->>Scraper: Trigger periodic scrape
    Scraper->>Scraper: Fetch LinkedIn Guest API
    Scraper->>VC: Run 3-Layer Verification
    Note right of VC: 1. Regex 2. Sponsor Register 3. Verdict
    VC-->>Scraper: ✅/⚠️/🟡/❌/Not specified
    Scraper->>DB: Upsert job data (Cached)

    Note over User, BE: User Interaction Phase
    User->>FE: Access Dashboard
    FE->>BE: GET /api/jobs (Filter/Sort/Page)
    BE->>DB: Pure DB Query (No real-time API)
    DB-->>BE: Cached Job Data
    BE-->>FE: JSON Results

    User->>FE: Upload CV for matching
    FE->>BE: POST /api/match (TF-IDF Match)
    BE-->>FE: Match Scores & Recommendations

    User->>FE: Export Data
    FE->>BE: GET /api/export
    BE-->>FE: XLSX File
```

---
## Quick Start (Local Development)

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # uses SQLite by default

# Start the API server
uvicorn main:app --reload --port 8000

# Trigger an immediate scrape (in another terminal)
curl -X POST http://localhost:8000/api/admin/scrape
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

### With Docker Compose

```bash
docker-compose up
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
```

---

## Visa Sponsorship — 3-Layer Verification

1. **Sentence-level regex** — positive/negative signals in job descriptions
2. **GOV.UK Sponsor Register** — fuzzy match against official licensed sponsors list
3. **Combined verdict** — 5 possible outcomes (✅ ⚠️ 🟡 ❌ Not specified)

To enable Layer 2, download the CSV from [GOV.UK](https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers) and place it at `backend/data/sponsor_register.csv`.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/jobs` | Jobs with filtering, pagination, sorting |
| GET | `/api/stats` | Dashboard statistics |
| GET | `/api/filters` | Available filter values |
| GET | `/api/export` | Export filtered jobs as XLSX |
| POST | `/api/match` | Upload CV to get TF-IDF match scores |
| POST | `/api/admin/scrape` | Manually trigger a scrape |

---

## Deployment

| Service | Platform | Notes |
|---------|----------|-------|
| Frontend | Vercel | Free tier |
| Backend | Railway / Render | Set `DATABASE_URL` env var |
| Database | Supabase PostgreSQL | Free tier 500MB |

---

## Project Structure

```
├── _archive/           # Original CLI tool (preserved at git tag v2-cli-original)
├── backend/
│   ├── main.py         # FastAPI entry + APScheduler
│   ├── database.py     # SQLAlchemy async models
│   ├── config.py       # Constants and keywords
│   ├── scraper/
│   │   ├── worker.py        # Cron job main logic
│   │   ├── parser.py        # HTML parsing
│   │   ├── visa_checker.py  # 3-layer visa verification
│   │   └── sponsor_list.py  # GOV.UK CSV loader
│   ├── routers/        # API route handlers (jobs/stats/filters/export/match)
│   ├── data/           # Place sponsor_register.csv here
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/  # Header, SearchBar, DateTabs, SortTabs,
│   │   │                # FilterSidebar, StatsCards, ChartsPanel,
│   │   │                # JobTable, CVUpload
│   │   ├── hooks/       # useJobs, useStats
│   │   └── i18n/        # en, zh, fr, es, nl
│   └── package.json
└── docker-compose.yml
```

---

## Original CLI Tool

The original command-line scraper is preserved in `_archive/`. You can still run it independently:

```bash
cd _archive
pip install -r requirements.txt
python scraper.py
```

The original version is also tagged in git: `v2-cli-original`
