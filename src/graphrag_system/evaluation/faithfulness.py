import re


class FaithfulnessEvaluator:
    def split_claims(self, answer: str) -> list[str]:
        return [s.strip() for s in re.split(r"(?<=[.!?])\s+", answer or "") if len(s.strip()) > 5]

    def evaluate(self, answer: str, contexts: list[str]) -> dict:
        claims = self.split_claims(answer)
        joined_context = " ".join(contexts).lower()
        evaluated = []
        supported = 0

        for claim in claims:
            claim_terms = {term.strip(".,:;()[]").lower() for term in claim.split() if len(term) > 3}
            if not claim_terms:
                status = "unsupported"
                indexes = []
            else:
                overlap = len([term for term in claim_terms if term in joined_context]) / max(len(claim_terms), 1)
                if overlap >= 0.55:
                    status = "supported"
                    supported += 1
                elif overlap >= 0.25:
                    status = "partially_supported"
                    supported += 0.5
                else:
                    status = "unsupported"
                indexes = [idx for idx, ctx in enumerate(contexts) if any(term in ctx.lower() for term in claim_terms)]

            evaluated.append(
                {
                    "claim": claim,
                    "status": status,
                    "supporting_context_indexes": indexes,
                    "notes": "Lexical baseline evaluator. Replace with LLM-based judge for production.",
                }
            )

        score = supported / len(claims) if claims else 0.0
        if score >= 0.9:
            action = "allow"
        elif score >= 0.75:
            action = "allow_with_caution"
        elif score >= 0.5:
            action = "regenerate"
        else:
            action = "refuse_or_request_more_evidence"

        return {"faithfulness_score": round(score, 3), "claims": evaluated, "recommended_action": action}
