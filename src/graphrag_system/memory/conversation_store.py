from collections import OrderedDict
from threading import Lock


class ConversationStore:
    def __init__(self, max_sessions: int = 1024, max_messages: int = 20) -> None:
        self._messages: OrderedDict[str, list[dict[str, str]]] = OrderedDict()
        self._lock = Lock()
        self.max_sessions = max_sessions
        self.max_messages = max_messages

    def add_message(self, session_id: str, role: str, content: str) -> None:
        self.add_messages(session_id, [{"role": role, "content": content}])

    def add_messages(self, session_id: str, messages: list[dict[str, str]]) -> None:
        with self._lock:
            existing = self._messages.get(session_id, [])
            self._messages[session_id] = (existing + [message.copy() for message in messages])[
                -self.max_messages:
            ]
            self._messages.move_to_end(session_id)
            if len(self._messages) > self.max_sessions:
                self._messages.popitem(last=False)

    def get_messages(self, session_id: str) -> list[dict[str, str]]:
        with self._lock:
            return [message.copy() for message in self._messages.get(session_id, [])]
