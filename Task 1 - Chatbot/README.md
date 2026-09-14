# AI Chatbot

A modular chatbot built for the **CodSoft AI Internship — Task 1 (Chatbot with Rule-Based Responses)**.

It uses regex-based intent matching as its core engine, backed by persistent **MongoDB** memory, a lightweight safety filter, and an optional **Groq LLM fallback** (free, no credit card) for messages that don't match any rule.

## Project Structure

```
ai-chatbot/
├── app.py                 # Streamlit entry point
├── chatbot/
│   ├── __init__.py
│   ├── engine.py          # Orchestrates safety → intent match → LLM fallback → memory
│   ├── intents.py         # Regex rules and response handlers
│   ├── memory.py          # MongoDB conversation + context storage
│   ├── llm.py             # Optional Groq API fallback
│   ├── tools.py           # Small reusable utility functions
│   ├── safety.py          # Input/output guardrails
│   └── utils.py           # Shared helpers
├── tests/                 # pytest suite (mongomock — no live DB needed)
│   ├── test_intents.py
│   ├── test_memory.py
│   └── test_chatbot.py
├── .env.example
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone <your-repo-url>
cd ai-chatbot
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Database

You need a MongoDB instance. Two easy options:

1. **Local MongoDB** — install via [MongoDB Community Server](https://www.mongodb.com/try/download/community), run `mongod` in the background. Default connection works with no config.
2. **MongoDB Atlas (free tier, no local install)** — create a free cluster at [mongodb.com/atlas](https://www.mongodb.com/atlas), grab the connection string, and put it in `.env`.

```bash
cp .env.example .env
# edit .env:
#   MONGODB_URI=mongodb://localhost:27017          (local)
#   MONGODB_URI=mongodb+srv://user:pass@...        (Atlas)
```

### LLM Fallback (optional)

Get a free API key (no credit card) at [console.groq.com/keys](https://console.groq.com/keys) and add it to `.env`:

```
GROQ_API_KEY=gsk_...
```

The bot works fully in rule-based mode without it.

## Run

```bash
streamlit run app.py
```

## Run Tests

Tests use `mongomock` (in-memory fake MongoDB) — **no real database or API keys needed**:

```bash
pytest tests/ -v
```

## Example Conversation

```
You: hi
Bot: Hey there! 👋

You: my name is Saurav
Bot: Nice to meet you, Saurav!

You: what's my name
Bot: You told me your name is Saurav!

You: what time is it
Bot: The current time is 14:22:05.

You: bye
Bot: Goodbye! Have a great day!
```

## How It Works

1. **Safety** — `safety.py` checks every message first. Empty input, oversized input, and blocked patterns are refused immediately and logged to memory.
2. **Intent matching** — `intents.py` runs a list of compiled regex patterns against the normalised text. First match wins. Responses are either a random pick from a list or a handler function for dynamic replies (time, date, name recall). Handlers receive a per-session `ctx` dict so the bot can remember facts like the user's name.
3. **LLM fallback** — if no rule matches and `GROQ_API_KEY` is set, the message plus recent history is sent to Groq (Llama 3). Otherwise a static fallback reply is used.
4. **Memory** — every turn is saved to MongoDB (`memory.py`): one document per message in `messages`, one context document per session in `session_context`. Conversations persist across restarts, keyed by session ID.

## Notes

Built for the CodSoft AI internship Task 1 (rule-based chatbot with if-else/pattern matching). This project fulfils that requirement with a regex intent engine and additionally demonstrates how such a system extends into a full pipeline — persistent database, safety layer, and optional LLM fallback — as used in real chatbot applications.
