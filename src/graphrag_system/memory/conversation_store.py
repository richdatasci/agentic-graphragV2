from collections import defaultdict


class ConversationStore:
    def __init__(self) -> None:
        self._messages: dict[str, list[dict[str, str]]] = defaultdict(list)

    def add_message(self, session_id: str, role: str, content: str) -> None:
        self._messages[session_id].append({"role": role, "content": content})

    def get_messages(self, session_id: str) -> list[dict[str, str]]:
        return list(self._messages[session_id])
