"""
llm.py
------
Optional LLM fallback using Groq's free API (no credit card required).
If GROQ_API_KEY is not set, the bot works fully in rule-based mode.
"""

import os

try:
    from groq import Groq
except ImportError:
    Groq = None


class LLMFallback:
    def __init__(self, api_key: str = None, model: str = "llama-3.1-8b-instant"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        self.enabled = bool(self.api_key and Groq is not None)
        self._client = Groq(api_key=self.api_key) if self.enabled else None

    def get_response(self, user_message: str, history: list[dict] = None) -> str:
        if not self.enabled:
            return "I don't have an LLM configured to answer that right now."

        messages = [
            {
                "role": "system",
                "content": (
                    "You are Botty, a friendly, concise chatbot. "
                    "Keep answers short and conversational."
                ),
            }
        ]
        for turn in (history or [])[-10:]:
            if turn["role"] in ("user", "assistant"):
                messages.append({"role": turn["role"], "content": turn["content"]})
        messages.append({"role": "user", "content": user_message})

        try:
            response = self._client.chat.completions.create(
                model=self.model,
                max_tokens=500,
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"(LLM error: {e})"
