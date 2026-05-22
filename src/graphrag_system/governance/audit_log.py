from graphrag_system.utils.time import utc_now_iso


class AuditLogger:
    def log(self, actor: str, action: str, target: str, metadata: dict | None = None) -> dict:
        return {
            "timestamp": utc_now_iso(),
            "actor": actor,
            "action": action,
            "target": target,
            "metadata": metadata or {},
        }
