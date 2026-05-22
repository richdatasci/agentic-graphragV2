class DocumentClassifier:
    def classify(self, text: str) -> str:
        lowered = text.lower()
        if "requirement" in lowered:
            return "requirements"
        if "risk" in lowered:
            return "risk"
        if "architecture" in lowered:
            return "architecture"
        return "general"
