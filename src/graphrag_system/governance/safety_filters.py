class SafetyFilter:
    BLOCKED_TOOL_TERMS = {"delete", "drop", "truncate", "exfiltrate"}

    def is_safe_tool_request(self, text: str) -> bool:
        lowered = text.lower()
        return not any(term in lowered for term in self.BLOCKED_TOOL_TERMS)
