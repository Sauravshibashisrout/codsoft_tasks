"""
memory.py
---------
Persistent conversation memory backed by MongoDB.

Two collections:
  - messages          -> full turn-by-turn history, one document per message
  - session_context   -> one document per session_id, holding remembered
                         facts (e.g. the user's name)

Pass a `client` in for testing (e.g. mongomock.MongoClient()) to avoid
needing a real MongoDB server.
"""

import os
from datetime import datetime, timezone

from pymongo import MongoClient, ASCENDING

DEFAULT_MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DEFAULT_DB_NAME = os.getenv("MONGODB_DB_NAME", "chatbot")


class Memory:
    def __init__(self, uri: str = None, db_name: str = None, client: MongoClient = None):
        self.client = client or MongoClient(uri or DEFAULT_MONGO_URI, serverSelectionTimeoutMS=3000)
        self.db = self.client[db_name or DEFAULT_DB_NAME]

        self.messages = self.db["messages"]
        self.session_context = self.db["session_context"]

        # Fail fast with a clear error if MongoDB isn't reachable
        # (pymongo connects lazily otherwise, so this forces an early check).
        self.client.admin.command("ping")

        # Helpful indexes — no-ops if they already exist
        self.messages.create_index([("session_id", ASCENDING), ("_id", ASCENDING)])
        self.session_context.create_index("session_id", unique=True)

    # ---- message history ----
    def add_message(self, session_id: str, role: str, content: str, intent: str = None):
        self.messages.insert_one({
            "session_id": session_id,
            "role": role,
            "content": content,
            "intent": intent,
            "created_at": datetime.now(timezone.utc).isoformat(),
        })

    def get_history(self, session_id: str, limit: int = 50):
        cursor = (
            self.messages.find({"session_id": session_id})
            .sort("_id", ASCENDING)
            .limit(limit)
        )
        return [
            {
                "role": doc["role"],
                "content": doc["content"],
                "intent": doc.get("intent"),
                "created_at": doc.get("created_at"),
            }
            for doc in cursor
        ]

    def clear_history(self, session_id: str):
        self.messages.delete_many({"session_id": session_id})
        self.session_context.delete_many({"session_id": session_id})

    # ---- session-level context (e.g. remembered user name) ----
    def get_context(self, session_id: str) -> dict:
        doc = self.session_context.find_one({"session_id": session_id})
        if not doc:
            return {}
        return {"user_name": doc.get("user_name")}

    def save_context(self, session_id: str, ctx: dict):
        self.session_context.update_one(
            {"session_id": session_id},
            {"$set": {"user_name": ctx.get("user_name")}},
            upsert=True,
        )
