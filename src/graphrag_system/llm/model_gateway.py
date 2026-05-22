import httpx


class ModelGateway:
    def __init__(
        self,
        provider: str = "ollama",
        model: str = "llama3.1:8b",
        ollama_base_url: str = "http://localhost:11434",
        openai_api_key: str = "INSERT API KEY HERE",
        anthropic_api_key: str = "INSERT API KEY HERE",
    ) -> None:
        self.provider = provider
        self.model = model
        self.ollama_base_url = ollama_base_url
        self.openai_api_key = openai_api_key
        self.anthropic_api_key = anthropic_api_key

    @classmethod
    def from_settings(cls, settings) -> "ModelGateway":
        return cls(
            provider=settings.default_llm_provider,
            model=settings.default_llm_model,
            ollama_base_url=settings.ollama_base_url,
            openai_api_key=settings.openai_api_key,
            anthropic_api_key=settings.anthropic_api_key,
        )

    async def complete(self, prompt: str, system_prompt: str | None = None) -> str:
        if self.provider == "ollama":
            return await self._complete_ollama(prompt, system_prompt)
        if self.provider == "openai":
            return await self._complete_openai(prompt, system_prompt)
        return self._fallback_completion(prompt)

    async def _complete_ollama(self, prompt: str, system_prompt: str | None = None) -> str:
        try:
            payload = {
                "model": self.model,
                "prompt": f"{system_prompt or ''}\n\n{prompt}",
                "stream": False,
            }
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(f"{self.ollama_base_url}/api/generate", json=payload)
                response.raise_for_status()
                return response.json().get("response", "")
        except Exception:
            return self._fallback_completion(prompt)

    async def _complete_openai(self, prompt: str, system_prompt: str | None = None) -> str:
        if self.openai_api_key == "INSERT API KEY HERE":
            return self._fallback_completion(prompt)
        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=self.openai_api_key)
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt or "You are a grounded assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content or ""
        except Exception:
            return self._fallback_completion(prompt)

    def _fallback_completion(self, prompt: str) -> str:
        return (
            "The model gateway is configured but no live model response was available. "
            "The system would answer using the retrieved context and then run faithfulness evaluation."
        )
