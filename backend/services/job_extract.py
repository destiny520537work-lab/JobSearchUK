import re

from config import (
    SALARY_PATTERNS,
    SKILL_KEYWORDS,
)
def extract_salary(description: str) -> str:
    if not description:
        return "Not disclosed"
    for pattern in SALARY_PATTERNS:
        m = re.search(pattern, description, re.IGNORECASE)
        if m:
            return m.group(0).strip()
    return "Not disclosed"


def extract_company_size(description: str) -> str:
    if not description:
        return "Unknown"
    patterns = [
        r"([\d,]+-[\d,]+)\s*employees",
        r"([\d,]+)\+?\s*employees",
        r"Company size[:\s]*([\d,]+-[\d,]+)",
    ]
    for pattern in patterns:
        m = re.search(pattern, description, re.IGNORECASE)
        if m:
            return m.group(0).strip()
    return "Unknown"


def extract_skill_keywords(description: str) -> str:
    if not description:
        return ""
    found = []
    text_lower = description.lower()
    for skill in SKILL_KEYWORDS:
        if len(skill) <= 2:
            if re.search(r"\b" + re.escape(skill) + r"\b", description):
                found.append(skill)
        else:
            if skill.lower() in text_lower:
                found.append(skill)
    seen = set()
    unique = []
    for s in found:
        if s.lower() not in seen:
            seen.add(s.lower())
            unique.append(s)
    return ", ".join(unique[:8])


def extract_education(description: str) -> str:
    if not description:
        return "Not specified"
    d = description.lower()
    if "phd" in d or "doctorate" in d:
        return "PhD"
    if "master" in d:
        return "Master's Degree"
    if "bachelor" in d or "degree" in d:
        return "Bachelor's Degree"
    if "diploma" in d or "hnd" in d:
        return "Diploma/HND"
    return "Not specified"
