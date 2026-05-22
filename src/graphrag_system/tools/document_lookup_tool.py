from graphrag_system.tools.base import BaseTool


class DocumentLookupTool(BaseTool):
    name = "document_lookup"
    description = "Look up document metadata and chunks."

    def run(self, document_id: str):
        return {"document_id": document_id, "status": "not_connected"}
