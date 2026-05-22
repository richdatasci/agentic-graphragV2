import httpx

from graphrag_system.tools.base import BaseTool


class WebApiTool(BaseTool):
    name = "web_api"
    description = "Call an approved HTTP API endpoint."

    def run(self, url: str, headers: dict | None = None):
        response = httpx.get(url, headers=headers or {}, timeout=30.0)
        response.raise_for_status()
        return {"status_code": response.status_code, "text": response.text[:5000]}
