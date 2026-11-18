import re

from graphrag_system.governance.authz import Authorizer
from graphrag_system.governance.rbac import Rbac
from graphrag_system.governance.redaction import Redactor
from graphrag_system.retrieval.vector_retriever import RetrievedEvidence


class GovernanceAgent:
    LEGACY_SAMPLE_IDS = frozenset({
        "sample_architecture_sample", "sample_policy_sample", "sample_system_design_sample",
    })
    CONTROL_DIRECTIVE = re.compile(
        r"\b(?:ignore|override|disregard)\s+(?:(?:all|the|any)\s+)?"
        r"(?:previous|prior|above|system|developer)\s+(?:instructions|prompts?)\b"
        r"|\b(?:reveal|print|show)\s+(?:the\s+|your\s+)?(?:system prompt|chain[- ]of[- ]thought)\b"
        r"|</?(?:think|analysis|reasoning)>",
        re.IGNORECASE,
    )

    def __init__(self) -> None:
        self.authorizer = Authorizer()
        self.rbac = Rbac()
        self.redactor = Redactor()

    def redact(self, text: str) -> str:
        return self.redactor.redact(text)

    def safe_text(self, text: str) -> bool:
        return not self.CONTROL_DIRECTIVE.search(text)

    def filter_evidence(
        self, evidence: list[RetrievedEvidence], roles: list[str], *, preserve_policy: bool = False,
    ) -> list[RetrievedEvidence]:
        if not any(self.rbac.has_permission(role, "read") for role in roles):
            return []

        allowed = []
        for item in evidence:
            metadata = item.metadata
            default_roles = (
                ["viewer", "analyst", "admin"]
                if item.source_id in self.LEGACY_SAMPLE_IDS else ["admin"]
            )
            policies = (
                metadata.get("source_allowed_roles", default_roles),
                metadata.get("document_allowed_roles", metadata.get("allowed_roles", default_roles)),
            )
            if not all(
                isinstance(policy, list)
                and all(isinstance(role, str) for role in policy)
                and self.authorizer.can_access(roles, policy)
                for policy in policies
            ):
                continue
            if not item.text.strip() or not self.safe_text(item.text):
                continue
            if preserve_policy:
                allowed.append(item)
                continue
            allowed.append(item.model_copy(update={
                "text": self.redact(item.text),
                "title": self.redact(item.title) if item.title else None,
                "metadata": {
                    key: self.redact(metadata[key])
                    for key in ("subject", "predicate", "object")
                    if item.source_type == "graph" and isinstance(metadata.get(key), str)
                },
            }))
        return allowed
