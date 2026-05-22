UPSERT_ENTITY = """
MERGE (e:Entity {id: $id})
SET e.name = $name,
    e.label = $label,
    e.confidence = $confidence,
    e.updated_at = datetime()
RETURN e
"""

UPSERT_TRIPLE = """
MERGE (t:Triple {id: $id})
SET t.subject = $subject,
    t.predicate = $predicate,
    t.object = $object,
    t.confidence = $confidence,
    t.updated_at = datetime()
RETURN t
"""

ENTITY_NEIGHBOURHOOD = """
MATCH (e {id: $entity_id})-[r*1..$depth]-(n)
RETURN e, r, n
"""
