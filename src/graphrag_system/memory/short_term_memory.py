class ShortTermMemory:
    def __init__(self, max_messages: int = 20) -> None:
        self.max_messages = max_messages

    def trim(self, messages: list[dict]) -> list[dict]:
        return messages[-self.max_messages :]
