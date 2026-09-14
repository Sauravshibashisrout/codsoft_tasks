"""
safety.py
---------
Lightweight guardrails applied before a message reaches the intent
engine / LLM, and before a response is sent back to the user.

This is intentionally simple (keyword/pattern based) — it's meant to
demonstrate the *pattern* of a safety layer in a chatbot pipeline,
not to be a production moderation system.
"""

import re

# Very small illustrative blocklist. Extend as needed.
BLOCKED_PATTERNS = [
    re.compile(r"\bhow to make a bomb\b", re.IGNORECASE),
    re.compile(r"\bkill myself\b|\bsuicide\b", re.IGNORECASE),
    re.compile(r"\bhack (into|a) .* account\b", re.IGNORECASE),
]

MAX_INPUT_LENGTH = 1000

SAFE_REFUSAL = (
    "I can't help with that. If you're in distress, please reach out to a "
    "local helpline or someone you trust."
)


def check_input(text: str) -> tuple[bool, str | None]:
    """
    Returns (is_safe, refusal_message_or_None).
    """
    if not text or not text.strip():
        return False, "Please type something."

    if len(text) > MAX_INPUT_LENGTH:
        return False, f"Message too long (max {MAX_INPUT_LENGTH} characters)."

    for pattern in BLOCKED_PATTERNS:
        if pattern.search(text):
            return False, SAFE_REFUSAL

    return True, None


def sanitize_output(text: str) -> str:
    """Strip anything that shouldn't leak to the user (e.g. stray whitespace)."""
    return text.strip()
