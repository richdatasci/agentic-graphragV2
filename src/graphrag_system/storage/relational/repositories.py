class DocumentRepository:
    def __init__(self, session) -> None:
        self.session = session

    async def list_documents(self) -> list:
        return []
