"""
app.py
------
Streamlit UI for the chatbot package.
Run: streamlit run app.py
"""

from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from chatbot import ChatbotEngine
from chatbot.utils import new_session_id

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 AI Chatbot")
st.caption("Rule-based intent matching · MongoDB memory · optional Groq LLM fallback")

# ---- init engine + session ----
if "engine" not in st.session_state:
    try:
        st.session_state.engine = ChatbotEngine(use_llm_fallback=True)
    except Exception as e:
        st.error(
            f"Couldn't connect to MongoDB ({e}). "
            "Make sure MongoDB is running and MONGODB_URI in .env is correct."
        )
        st.stop()

if "session_id" not in st.session_state:
    st.session_state.session_id = new_session_id()

engine = st.session_state.engine
session_id = st.session_state.session_id

# ---- load history from DB (source of truth, survives refresh) ----
history = engine.memory.get_history(session_id)

if not history:
    st.chat_message("assistant").markdown(
        "Hey! I'm Botty 🤖. Type something like 'hi', 'what time is it', "
        "'my name is Alex', or 'help'."
    )

for turn in history:
    with st.chat_message(turn["role"]):
        st.markdown(turn["content"])

# ---- chat input ----
user_input = st.chat_input("Type your message...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    reply = engine.respond(session_id, user_input)

    with st.chat_message("assistant"):
        st.markdown(reply)

# ---- sidebar ----
with st.sidebar:
    st.header("About")
    st.write(
        "This chatbot uses **regex-based intent matching** as its primary engine, "
        "backed by **MongoDB** for persistent memory. "
        "For anything it doesn't recognise, it optionally falls back to "
        "**Groq** (free, no credit card — set `GROQ_API_KEY` in `.env`)."
    )
    st.write("**Try:**")
    st.code("hi\nmy name is Saurav\nwhat's my name\nwhat time is it\nhelp\nbye")

    st.divider()
    st.caption(f"Session ID: `{session_id[:8]}...`")

    if st.button("🔄 Reset Conversation"):
        engine.reset(session_id)
        st.rerun()
