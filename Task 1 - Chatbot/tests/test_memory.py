"""
test_memory.py
---------------
Tests for the MongoDB-backed Memory class. Uses mongomock so tests
never require a real MongoDB server or touch production data.
"""

import sys
import os
import pytest
import mongomock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from chatbot.memory import Memory


@pytest.fixture
def memory():
    fake_client = mongomock.MongoClient()
    return Memory(client=fake_client, db_name="test_chatbot")


def test_add_and_get_history(memory):
    memory.add_message("session1", "user", "hi")
    memory.add_message("session1", "assistant", "hello!")
    history = memory.get_history("session1")

    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "hi"
    assert history[1]["role"] == "assistant"


def test_history_is_isolated_per_session(memory):
    memory.add_message("session1", "user", "hi from session 1")
    memory.add_message("session2", "user", "hi from session 2")

    h1 = memory.get_history("session1")
    h2 = memory.get_history("session2")

    assert len(h1) == 1
    assert len(h2) == 1
    assert h1[0]["content"] != h2[0]["content"]


def test_clear_history(memory):
    memory.add_message("session1", "user", "hi")
    memory.clear_history("session1")
    assert memory.get_history("session1") == []


def test_context_save_and_load(memory):
    memory.save_context("session1", {"user_name": "Saurav"})
    ctx = memory.get_context("session1")
    assert ctx["user_name"] == "Saurav"


def test_context_update_overwrites(memory):
    memory.save_context("session1", {"user_name": "Saurav"})
    memory.save_context("session1", {"user_name": "Alex"})
    ctx = memory.get_context("session1")
    assert ctx["user_name"] == "Alex"


def test_context_missing_session_returns_empty(memory):
    ctx = memory.get_context("nonexistent")
    assert ctx == {}
