import json

from graphrag_system.retrieval.vector_retriever import RetrievedEvidence


class ContextPacker:
    def pack(self, evidence: list[RetrievedEvidence], max_chars: int = 8000) -> str:
        return self.pack_evidence(evidence, max_chars)[1]

    def pack_evidence(
        self, evidence: list[RetrievedEvidence], max_chars: int = 8000,
    ) -> tuple[list[RetrievedEvidence], str]:
        packed = []
        blocks = []
        remaining = max_chars
        for item in evidence:
            # Use structured data so source text cannot create a new prompt field.
            block = json.dumps({
                "citation": f"Source {len(packed) + 1}",
                "text": item.text,
            }, ensure_ascii=False)
            cost = len(block) + bool(blocks)
            if cost > remaining:
                continue
            packed.append(item)
            blocks.append(block)
            remaining -= cost
        return packed, "\n".join(blocks)
