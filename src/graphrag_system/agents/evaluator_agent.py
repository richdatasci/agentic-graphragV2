import re

from graphrag_system.evaluation.answer_relevance import AnswerRelevanceEvaluator
from graphrag_system.evaluation.faithfulness import FaithfulnessEvaluator


class EvaluatorAgent:
    CITATION = re.compile(r"\[Source ([1-9][0-9]{0,3})\]")
    WORD = re.compile(r"\b[\w-]+\b")
    NUMBER = re.compile(r"\b\d+(?:[.,]\d+)*\b")
    NEGATION = re.compile(r"\b(?:no|not|never|without)\b", re.IGNORECASE)

    def __init__(self) -> None:
        self.faithfulness = FaithfulnessEvaluator()
        self.relevance = AnswerRelevanceEvaluator()

    def evaluate(self, answer: str, contexts: list[str], query: str = "") -> dict:
        """Evaluate each factual sentence against its cited evidence."""
        claims = []
        for line in answer.splitlines():
            line = re.sub(r"([.!?])\s+((?:\[Source \d+\]\s*)+)", r" \2\1 ", line)
            for claim in re.split(r"(?<=[.!?])\s+", line.strip()):
                if not claim.strip():
                    continue
                indexes = [int(value) - 1 for value in self.CITATION.findall(claim)]
                text = re.sub(r"\s+([.!?,])", r"\1", self.CITATION.sub("", claim)).strip()
                if not indexes or any(index >= len(contexts) for index in indexes):
                    claims.append({"claim": text, "status": "unsupported"})
                    continue
                numbers = set(self.NUMBER.findall(text))
                terms = set(self.WORD.findall(text.casefold()))
                cited = [contexts[index] for index in indexes]
                matched = []
                for source in cited:
                    if not numbers.issubset(self.NUMBER.findall(source)):
                        continue
                    # Compare polarity against the evidence sentence, not the whole document.
                    for sentence in self.faithfulness.split_claims(source):
                        if not numbers.issubset(self.NUMBER.findall(sentence)):
                            continue
                        if bool(self.NEGATION.search(text)) != bool(self.NEGATION.search(sentence)):
                            continue
                        sentence_terms = set(self.WORD.findall(sentence.casefold()))
                        if len(terms & sentence_terms) / max(len(terms), 1) >= 0.70:
                            matched.append(sentence)
                result = self.faithfulness.evaluate(text, matched)
                claims.append({
                    "claim": text,
                    "status": result["claims"][0]["status"] if result["claims"] else "unsupported",
                })
        weights = {"supported": 1, "partially_supported": 0.5, "unsupported": 0}
        score = sum(weights[claim["status"]] for claim in claims) / max(len(claims), 1)
        return {
            "faithfulness_score": round(score, 3),
            "answer_relevance": self.relevance.evaluate(query, answer),
            "claims": claims,
            "recommended_action": "allow" if score == 1 else "regenerate",
        }
