from graphrag_system.retrieval.vector_retriever import RetrievedEvidence


class ContextPacker:
    def pack(self, evidence: list[RetrievedEvidence], max_chars: int = 8000) -> str:
        parts = []
        total = 0
        for idx, item in enumerate(evidence, start=1):
            block = f"[Source {idx}: {item.source_type} | {item.source_id}]\n{item.text}\n"
            if total + len(block) > max_chars:
                break
            parts.append(block)
            total += len(block)
        return "\n".join(parts)
