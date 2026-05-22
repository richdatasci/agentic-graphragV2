class ConversationSummariser:
    def summarise(self, messages: list[dict]) -> str:
        return " ".join(message.get("content", "") for message in messages[-5:])
