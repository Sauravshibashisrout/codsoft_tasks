"""
tools.py
--------
Small standalone "tools" the chatbot can invoke — kept separate from
intents.py so intent handlers stay thin and tools stay unit-testable
in isolation.
"""

from datetime import datetime


def get_current_time() -> str:
    return datetime.now().strftime("%H:%M:%S")


def get_current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def word_count(text: str) -> int:
    return len(text.split())


def echo(text: str) -> str:
    return text
