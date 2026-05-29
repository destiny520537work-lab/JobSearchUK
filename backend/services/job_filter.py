from config import (
    EXCLUDE_TITLE_KEYWORDS,
    MAX_APPLICANTS,
    )


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