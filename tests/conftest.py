import pytest


@pytest.fixture
def sample_text() -> str:
    return "Agentic GraphRAG combines graph retrieval, vector search and faithfulness evaluation."
