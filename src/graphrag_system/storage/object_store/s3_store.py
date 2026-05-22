from pathlib import Path


class LocalCompatibleObjectStore:
    """Simple local object-store stand-in for S3 or MinIO during development."""

    def __init__(self, root: str = ".object_store") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put_text(self, key: str, text: str) -> str:
        path = self.root / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return str(path)

    def get_text(self, key: str) -> str:
        return (self.root / key).read_text(encoding="utf-8")
