"""
GOV.UK Licensed Sponsor Register loader.

Download the CSV from:
https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers

Place the CSV file at: backend/data/sponsor_register.csv
Columns expected: Organisation Name, Town/City, County, Type & Rating, Route

Only A-rated Skilled Worker route entries are loaded.
"""

import csv
import os
import logging

logger = logging.getLogger(__name__)

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
_CSV_PATH = os.path.join(_DATA_DIR, "sponsor_register.csv")

# Global cache — loaded once at startup
_sponsor_set: set = set()


def load_sponsor_set() -> set:
    """
    Load sponsor names from CSV into a lowercase set.
    Returns empty set if CSV not found (visa layer 2 will be skipped gracefully).
    """
    global _sponsor_set

    if _sponsor_set:
        return _sponsor_set

    if not os.path.exists(_CSV_PATH):
        logger.warning(
            "Sponsor register CSV not found at %s. "
            "Layer 2 visa check disabled. "
            "Download from: https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers",
            _CSV_PATH,
        )
        return set()

    loaded = set()
    try:
        with open(_CSV_PATH, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("Organisation Name", "").strip().lower()
                route = row.get("Route", "").strip()
                rating = row.get("Type & Rating", "").strip()

                # Only keep A-rated Skilled Worker entries
                # Rating format: "Worker (A rating)", "Worker (A (Premium))", "Worker (A (SME+))"
                is_a_rated = "Worker (A" in rating  # covers A rating, A (Premium), A (SME+)
                if name and "Skilled Worker" in route and is_a_rated:
                    loaded.add(name)

        logger.info("Loaded %d sponsor companies from GOV.UK register.", len(loaded))
        _sponsor_set = loaded
    except Exception as e:
        logger.error("Failed to load sponsor register: %s", e)

    return _sponsor_set


def get_sponsor_set() -> set:
    """Return the cached sponsor set (call load_sponsor_set() first)."""
    return _sponsor_set
