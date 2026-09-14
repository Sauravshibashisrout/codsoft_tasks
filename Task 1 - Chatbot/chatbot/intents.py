"""
intents.py
----------
Defines all rule-based intents as (name, pattern, responses/handler) tuples.
Keeping intents in their own module makes it easy to add/remove rules
without touching the matching engine in engine.py.
"""

import re
from datetime import datetime


def _handle_name(match, ctx):
    name = match.group(1).capitalize()
    ctx["user_name"] = name
    return f"Nice to meet you, {name}!"


def _handle_time(match, ctx):
    return f"The current time is {datetime.now().strftime('%H:%M:%S')}."


def _handle_date(match, ctx):
    return f"Today's date is {datetime.now().strftime('%Y-%m-%d')}."


def _handle_recall_name(match, ctx):
    name = ctx.get("user_name")
    if name:
        return f"You told me your name is {name}!"
    return "You haven't told me your name yet — what is it?"


# Each intent: (intent_name, compiled_pattern, response)
# response is either a list[str] (random choice) or a callable(match, ctx) -> str
INTENTS = [
    ("greeting",
     re.compile(r"\b(hi|hello|hey|yo|sup)\b"),
     ["Hey there! 👋", "Hello! How can I help you today?", "Hi! What's up?"]),

    ("tell_name",
     re.compile(r"\bmy name is (\w+)"),
     _handle_name),

    ("recall_name",
     re.compile(r"\bwhat.?s my name\b|\bdo you remember my name\b"),
     _handle_recall_name),

    ("ask_bot_name",
     re.compile(r"\bwhat.*your name\b|\bwho are you\b"),
     ["I'm Botty, your friendly rule-based chatbot."]),

    ("ask_wellbeing",
     re.compile(r"\bhow are you\b"),
     ["I'm just code, but I'm running smoothly! How about you?",
      "Doing great, thanks for asking!"]),

    ("ask_time",
     re.compile(r"\b(what.*time|current time)\b"),
     _handle_time),

    ("ask_date",
     re.compile(r"\b(date|today.?s date)\b"),
     _handle_date),

    ("thanks",
     re.compile(r"\bthank(s| you)\b"),
     ["You're welcome!", "No problem at all!", "Anytime!"]),

    ("help",
     re.compile(r"\bhelp\b"),
     ["I can chat about greetings, tell you the time/date, remember your name, "
      "or just have small talk. Try 'hi', 'what time is it', or 'my name is Alex'."]),

    ("weather",
     re.compile(r"\bweather\b"),
     ["I can't check live weather right now, but I hope it's sunny where you are!"]),

    ("goodbye",
     re.compile(r"\b(bye|exit|quit|goodbye)\b"),
     ["Goodbye! Have a great day!", "See you later!", "Bye! 👋"]),
]
