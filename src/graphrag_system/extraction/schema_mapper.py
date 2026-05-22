class SchemaMapper:
    ENTITY_LABELS = {"system": "System", "requirement": "Requirement", "risk": "Risk"}

    def map_entity_label(self, name: str) -> str:
        lowered = name.lower()
        for token, label in self.ENTITY_LABELS.items():
            if token in lowered:
                return label
        return "Entity"

    def normalise_relationship_type(self, rel_type: str) -> str:
        safe = "".join(ch if ch.isalnum() else "_" for ch in rel_type.upper())
        return safe.strip("_") or "RELATED_TO"
