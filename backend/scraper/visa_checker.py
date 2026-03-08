"""
Three-layer visa sponsorship verification.

Layer 1: Sentence-level regex (positive/negative signals)
Layer 2: GOV.UK official sponsor list fuzzy match
Layer 3: Combined verdict
"""

import re


# ─── Layer 1: sentence-level regex ───────────────────────────────────────────

NEG_PATTERNS = [
    r"(?:do(?:es)?n['\u2019]?t|cannot|can\s?not|will\s?not|won['\u2019]?t|unable to|not able to)\s+(?:\w+\s+)*?sponsor",
    r"no\s+(?:visa\s+)?sponsorship",
    r"without\s+(?:requiring\s+)?(?:visa\s+)?sponsorship",
    r"must\s+(?:already\s+)?have\s+(?:the\s+)?(?:full\s+)?right\s+to\s+work",
    r"right\s+to\s+work\s+in\s+the\s+uk\s+(?:without|independently)",
    r"permanent\s+right\s+to\s+work",
    r"(?:pre-?)?settled\s+status",
    r"indefinite\s+leave",
    r"not\s+offer(?:ing)?\s+(?:visa\s+)?sponsorship",
    r"sponsorship\s+is\s+not\s+available",
    r"this\s+role\s+does\s+not\s+(?:offer|provide)",
]

POS_PATTERNS = [
    r"(?:visa\s+)?sponsorship\s+(?:is\s+)?available",
    r"(?:we|the company)\s+(?:can|will|do)\s+sponsor",
    r"able\s+to\s+sponsor",
    r"offer(?:s|ing)?\s+(?:visa\s+)?sponsorship",
    r"skilled\s+worker\s+visa\s+(?:sponsorship\s+)?(?:is\s+)?available",
    r"willing\s+to\s+sponsor",
    r"we\s+sponsor\s+(?:visa|work\s+permit)",
]

NEG_WORDS = {"not ", "no ", "don't", "doesn't", "won't", "cannot", "can't", "unable"}


def classify_visa_from_text(desc_text: str) -> str:
    """
    Returns: 'sponsor' | 'no_sponsor' | 'unknown'
    """
    if not desc_text:
        return "unknown"

    text = desc_text.lower()
    sentences = re.split(r"[.!?\n]", text)
    positive_signals = []
    negative_signals = []

    for s in sentences:
        s = s.strip()
        if not s:
            continue

        # Negative check first
        for p in NEG_PATTERNS:
            if re.search(p, s):
                negative_signals.append(s)
                break

        # Positive check — only if no negation word in sentence
        if not any(w in s for w in NEG_WORDS):
            for p in POS_PATTERNS:
                if re.search(p, s):
                    positive_signals.append(s)
                    break

    if negative_signals:
        return "no_sponsor"
    if positive_signals:
        return "sponsor"
    return "unknown"


# ─── Layer 2: GOV.UK sponsor list fuzzy match ─────────────────────────────────

def check_sponsor_list(company_name: str, sponsor_set: set) -> bool:
    """
    Returns True if company is in the GOV.UK licensed sponsor list.
    Uses exact match first, then thefuzz token_set_ratio >= 85.
    """
    if not company_name or not sponsor_set:
        return False

    name = company_name.strip().lower()
    if name in sponsor_set:
        return True

    try:
        from thefuzz import fuzz
        for sponsor in sponsor_set:
            if fuzz.token_set_ratio(name, sponsor) >= 85:
                return True
    except ImportError:
        pass

    return False


# ─── Layer 3: combined verdict ────────────────────────────────────────────────

_VERDICT_MAP = {
    ("sponsor", True):    "✅ Visa sponsorship available",
    ("sponsor", False):   "⚠️ Claims sponsor but not on gov list",
    ("no_sponsor", True): "❌ Not for this role (company is licensed)",
    ("no_sponsor", False): "❌ No sponsorship",
    ("unknown", True):    "🟡 Company is licensed (role unspecified)",
    ("unknown", False):   "Not specified",
}


def final_visa_verdict(text_result: str, on_list: bool) -> str:
    return _VERDICT_MAP.get((text_result, on_list), "Not specified")
