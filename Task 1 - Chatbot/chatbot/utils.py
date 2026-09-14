"""
utils.py
--------
Small shared helpers used across the chatbot package.
"""

import uuid


def normalize(text: str) -> str:
    """Lowercase + strip whitespace — the standard form we match rules against."""
    return text.lower().strip()


def new_session_id() -> str:
    return str(uuid.uuid4())
