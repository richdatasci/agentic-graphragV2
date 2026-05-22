from graphrag_system.llm.model_gateway import ModelGateway


class AnswerSynthesiser:
    def __init__(self, model_gateway: ModelGateway) -> None:
        self.model_gateway = model_gateway

    async def synthesise(self, query: str, context: str) -> str:
        prompt = f"""
Use the context to answer the user question.

Rules:
- Use only supported information.
- Mention when evidence is missing.
- Do not expose hidden chain-of-thought.
- Keep the answer clear and business-friendly.

Question:
{query}

Context:
{context}
"""
        return await self.model_gateway.complete(prompt, system_prompt="You are a grounded GraphRAG answer synthesiser.")
