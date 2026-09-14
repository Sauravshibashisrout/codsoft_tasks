"""
test_intents.py
----------------
Unit tests for individual intent patterns and handlers.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from chatbot.intents import INTENTS


def _find(name):
    for n, pattern, response in INTENTS:
        if n == name:
            return pattern, response
    raise ValueError(f"Intent {name} not found")


def test_greeting_matches_common_words():
    pattern, _ = _find("greeting")
    for word in ["hi", "hello", "hey there", "yo"]:
        assert pattern.search(word), f"'{word}' should match greeting"


def test_greeting_does_not_match_substring_inside_other_words():
    pattern, _ = _find("greeting")
    # "history" contains "hi" but word-boundaries (\b) should stop it matching
    assert pattern.search("history of india") is None
    # sanity check: the pattern does match a real standalone "hi"
    assert pattern.search("hi") is not None


def test_tell_name_extracts_name():
    pattern, handler = _find("tell_name")
    match = pattern.search("my name is saurav")
    assert match is not None
    ctx = {}
    result = handler(match, ctx)
    assert "Saurav" in result
    assert ctx["user_name"] == "Saurav"


def test_recall_name_with_no_prior_context():
    pattern, handler = _find("recall_name")
    match = pattern.search("what's my name")
    assert match is not None
    result = handler(match, {})
    assert "haven't told me" in result.lower()


def test_recall_name_with_context():
    pattern, handler = _find("recall_name")
    match = pattern.search("what's my name")
    result = handler(match, {"user_name": "Saurav"})
    assert "Saurav" in result


def test_goodbye_matches():
    pattern, _ = _find("goodbye")
    for word in ["bye", "goodbye", "exit", "quit"]:
        assert pattern.search(word)


def test_ask_time_matches():
    pattern, handler = _find("ask_time")
    match = pattern.search("what time is it")
    assert match is not None
    result = handler(match, {})
    assert ":" in result  # HH:MM:SS format
