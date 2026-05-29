def classify_job_type(title: str) -> str:
    t = title.lower()
    # Cloud & DevOps (before software to separate cloud from general SWE)
    if any(k in t for k in [
        "devops", "cloud engineer", "cloud architect", "cloud support",
        "platform engineer", "site reliability", "sre", "infrastructure engineer",
        "devsecops", "cloud native",
    ]):
        return "云运维"
    # Cybersecurity
    if any(k in t for k in [
        "security engineer", "security analyst", "cyber", "information security",
        "penetration", "soc analyst", "vulnerability",
    ]):
        return "安全"
    # ML / AI (before data science to catch "ml" overlap)
    if any(k in t for k in [
        "machine learning", "ml engineer", "ai engineer", "nlp engineer",
        "computer vision", "deep learning", "prompt engineer", "llm engineer",
        "artificial intelligence", "reinforcement learning",
    ]):
        return "AI"
    # Data Science
    if any(k in t for k in [
        "data scientist", "data science", "research scientist", "applied scientist",
    ]):
        return "数据科学"
    # Data Engineering
    if any(k in t for k in [
        "data engineer", "analytics engineer", "etl engineer",
        "data platform", "data infrastructure", "data pipeline",
    ]):
        return "数据工程"
    # Data Analytics
    if any(k in t for k in [
        "data analyst", "business intelligence", " bi ", "bi analyst",
        "analytics", "reporting analyst", "insight analyst", "product analyst",
    ]):
        return "数据分析"
    # Software Engineering
    if any(k in t for k in [
        "software engineer", "software developer", "backend", "frontend",
        "full stack", "fullstack", "web developer", "mobile developer",
        "ios", "android", "developer", "programmer", "engineer",
    ]):
        return "软件"
    # Product
    if any(k in t for k in ["product manager", "product owner"]):
        return "产品"
    # Business Analysis
    if any(k in t for k in [
        "business analyst", "technology analyst", "it analyst",
        "systems analyst", "management consultant",
    ]):
        return "商业"
    # Quantitative / Finance
    if any(k in t for k in [
        "quantitative", "quant ", "credit risk", "risk analyst",
        "actuar", "financial engineer",
    ]):
        return "定量"
    return "其他"


def classify_project_type(title: str, employment_type: str = "") -> str:
    t = title.lower()
    if "intern" in t:
        return "Internship"
    if "graduate" in t or "grad scheme" in t:
        return "Graduate"
    if "graduate" in employment_type.lower():
        return "Graduate"
    return "full time"