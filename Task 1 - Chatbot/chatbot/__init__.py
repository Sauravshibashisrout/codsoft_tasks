"""
chatbot package
----------------
Rule-based chatbot with optional LLM fallback and persistent memory.
"""

from .engine import ChatbotEngine
from .memory import Memory
from .llm import LLMFallback

__all__ = ["ChatbotEngine", "Memory", "LLMFallback"]
__version__ = "1.0.0"
