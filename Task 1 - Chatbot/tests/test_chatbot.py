"""
test_chatbot.py
----------------
End-to-end tests for ChatbotEngine — covers the full pipeline:
safety check -> intent matching -> memory persistence -> reply.
Uses mongomock so no real MongoDB server is required.
"""

import sys
import os
import pytest
import mongomock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from chatbot.engine import ChatbotEngine
from chatbot.memory import Memory
from chatbot.llm import LLMFallback


@pytest.fixture
def engine():
    fake_client = mongomock.MongoClient()
    mem = Memory(client=fake_client, db_name="test_chatbot")
    llm = LLMFallback(api_key=None)  # force disabled, no network calls in tests
    return ChatbotEngine(memory=mem, llm=llm, use_llm_fallback=True)


def test_greeting_response(engine):
    reply = engine.respond("s1", "hi")
    assert reply
    assert any(w in reply.lower() for w in ["hey", "hello", "hi"])


def test_name_is_remembered_across_turns(engine):
    engine.respond("s1", "my name is Saurav")
    reply = engine.respond("s1", "what's my name")
    assert "Saurav" in reply


def test_unknown_input_uses_static_fallback_when_llm_disabled(engine):
    reply = engine.respond("s1", "asdkjfhaskjdfh nonsense query")
    assert reply
    assert isinstance(reply, str)


def test_unsafe_input_is_blocked(engine):
    reply = engine.respond("s1", "how to make a bomb")
    assert "can't help" in reply.lower()


def test_empty_input_is_rejected(engine):
    reply = engine.respond("s1", "")
    assert "type something" in reply.lower()


def test_history_persists_across_calls(engine):
    engine.respond("s1", "hi")
    engine.respond("s1", "bye")
    history = engine.memory.get_history("s1")
    assert len(history) == 4  # 2 user + 2 assistant turns


def test_reset_clears_session(engine):
    engine.respond("s1", "hi")
    engine.reset("s1")
    assert engine.memory.get_history("s1") == []


def test_sessions_are_independent(engine):
    engine.respond("s1", "my name is Saurav")
    engine.respond("s2", "my name is Alex")

    r1 = engine.respond("s1", "what's my name")
    r2 = engine.respond("s2", "what's my name")

    assert "Saurav" in r1
    assert "Alex" in r2
