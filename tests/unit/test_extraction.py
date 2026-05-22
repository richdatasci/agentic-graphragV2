from graphrag_system.extraction.entity_extractor import EntityExtractor


def test_entity_extractor_returns_list(sample_text: str) -> None:
    entities = EntityExtractor().extract(sample_text)
    assert isinstance(entities, list)
