from graphrag_system.memory.conversation_store import ConversationStore


class MemoryAgent:
    def __init__(self, store: ConversationStore | None = None) -> None:
        self.store = store or ConversationStore()

    def add_message(self, session_id: str, role: str, content: str) -> None:
        self.store.add_message(session_id, role, content)
