"""
POST /api/match — upload CV (PDF/DOCX), get TF-IDF match scores for all active jobs.
"""

import io
import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import Job, get_session

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/match", tags=["match"])


def _extract_pdf_text(data: bytes) -> str:
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(data))
        return " ".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        logger.error("PDF parse error: %s", e)
        return ""


def _extract_docx_text(data: bytes) -> str:
    try:
        import docx
        doc = docx.Document(io.BytesIO(data))
        return " ".join(p.text for p in doc.paragraphs)
    except Exception as e:
        logger.error("DOCX parse error: %s", e)
        return ""


def _tfidf_scores(cv_text: str, descriptions: list[str]) -> list[float]:
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        docs = [cv_text] + descriptions
        vectorizer = TfidfVectorizer(stop_words="english", max_features=500)
        tfidf = vectorizer.fit_transform(docs)
        scores = cosine_similarity(tfidf[0:1], tfidf[1:])[0]
        return [round(float(s) * 100, 1) for s in scores]
    except Exception as e:
        logger.error("TF-IDF error: %s", e)
        return [0.0] * len(descriptions)


@router.post("")
async def match_cv(
    file: UploadFile = File(...),
    days: int = 7,
    db: AsyncSession = Depends(get_session),
):
    content_type = file.content_type or ""
    filename = file.filename or ""

    data = await file.read()

    if "pdf" in content_type or filename.lower().endswith(".pdf"):
        cv_text = _extract_pdf_text(data)
    elif "word" in content_type or filename.lower().endswith(".docx"):
        cv_text = _extract_docx_text(data)
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload PDF or DOCX."
        )

    if not cv_text.strip():
        raise HTTPException(status_code=422, detail="Could not extract text from CV.")

    cutoff = datetime.utcnow() - timedelta(days=days)
    stmt = (
        select(Job.job_id, Job.description)
        .where(and_(Job.is_active == True, Job.scraped_at >= cutoff))
    )
    result = await db.execute(stmt)
    rows = result.all()

    if not rows:
        return {"scores": {}}

    job_ids = [r[0] for r in rows]
    descriptions = [r[1] or "" for r in rows]

    scores = _tfidf_scores(cv_text, descriptions)

    return {
        "scores": {job_id: score for job_id, score in zip(job_ids, scores)}
    }
