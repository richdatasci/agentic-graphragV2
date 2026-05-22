class TestsetGenerator:
    def generate_questions(self, text: str, max_questions: int = 10) -> list[str]:
        return [f"What does the document say about {word.strip('.,')}?" for word in text.split()[:max_questions]]
