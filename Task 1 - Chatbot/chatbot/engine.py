"""
engine.py
---------
The core orchestrator. Given a user message + session id, it:
  1. Runs the safety check on the input.
  2. Tries to match a rule-based intent (intents.py).
  3. Falls back to an LLM (llm.py) if no rule matches and one is configured,
     otherwise returns a static fallback response.
  4. Persists the turn to memory (memory.py).
  5. Sanitizes and returns the output.
"""

import random

from .intents import INTENTS
from .memory import Memory
from .safety import check_input, sanitize_output
from .llm import LLMFallback
from .utils import normalize

FALLBACK_RESPONSES = [
    "I'm not sure I understand. Could you rephrase that?",
    "Hmm, I don't have an answer for that yet.",
    "Interesting! Tell me more, or try asking something else.",
]


class ChatbotEngine:
    def __init__(self, memory: Memory = None, llm: LLMFallback = None, use_llm_fallback: bool = False):
        self.memory = memory or Memory()
        self.llm = llm or LLMFallback()
        self.use_llm_fallback = use_llm_fallback

    def respond(self, session_id: str, user_message: str) -> str:
        # 1. Safety check on input
        is_safe, refusal = check_input(user_message)
        if not is_safe:
            self.memory.add_message(session_id, "user", user_message, intent="blocked")
            self.memory.add_message(session_id, "assistant", refusal, intent="safety_refusal")
            return refusal

        # 2. Load session context (e.g. remembered user name)
        ctx = self.memory.get_context(session_id)

        # 3. Try rule-based intents
        text = normalize(user_message)
        matched_intent, reply = self._match_intent(text, ctx)

        # 4. LLM fallback if nothing matched
        if reply is None:
            if self.use_llm_fallback and self.llm.enabled:
                history = self.memory.get_history(session_id)
                reply = self.llm.get_response(user_message, history)
                matched_intent = "llm_fallback"
            else:
                reply = random.choice(FALLBACK_RESPONSES)
                matched_intent = "fallback"

        reply = sanitize_output(reply)

        # 5. Persist context + history
        self.memory.save_context(session_id, ctx)
        self.memory.add_message(session_id, "user", user_message, intent=matched_intent)
        self.memory.add_message(session_id, "assistant", reply, intent=matched_intent)

        return reply

    def _match_intent(self, text: str, ctx: dict):
        for name, pattern, response in INTENTS:
            match = pattern.search(text)
            if match:
                if callable(response):
                    return name, response(match, ctx)
                return name, random.choice(response)
        return None, None

    def reset(self, session_id: str):
        self.memory.clear_history(session_id)
