import re


class PiiDetector:
    EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

    def find(self, text: str) -> list[dict[str, str]]:
        return [{"type": "email", "value": match.group(0)} for match in self.EMAIL_PATTERN.finditer(text)]

    def redact(self, text: str) -> str:
        return self.EMAIL_PATTERN.sub("[REDACTED_EMAIL]", text)
