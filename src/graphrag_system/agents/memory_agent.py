import re

from graphrag_system.memory.conversation_store import ConversationStore
from graphrag_system.memory.short_term_memory import ShortTermMemory


class MemoryAgent:
    FOLLOW_UP = re.compile(
        r"^(?:and\b|what about\b|how about\b|why\??$)|\b(?:it|they|them|that system)\b",
        re.IGNORECASE,
    )

    def __init__(self, store: ConversationStore | None = None) -> None:
        self.store = store or ConversationStore()
        self.short_term = ShortTermMemory()

    def add_message(self, session_id: str, role: str, content: str) -> None:
        self.store.add_message(session_id, role, content)

    def history(self, session_id: str) -> list[dict[str, str]]:
        return self.store.get_messages(session_id)

    def context(self, session_id: str, supplied: list[dict]) -> list[dict[str, str]]:
        messages = self.history(session_id) or supplied
        return self.short_term.trim([
            {"role": message["role"], "content": message["content"][:2000]}
            for message in messages
            if message.get("role") in {"user", "assistant"} and isinstance(message.get("content"), str)
        ])

    def contextualise(self, query: str, history: list[dict[str, str]]) -> str:
        if self.FOLLOW_UP.search(query):
            for message in reversed(history):
                if message["role"] == "user":
                    return f"{query} {message['content'][:500]}"
        return query

    def record_turn(self, session_id: str, query: str, answer: str) -> None:
        self.store.add_messages(session_id, [
            {"role": "user", "content": query}, {"role": "assistant", "content": answer},
        ])
