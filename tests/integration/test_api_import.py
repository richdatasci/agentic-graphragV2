def test_api_imports() -> None:
    from apps.api.main import app

    assert app.title == "Agentic GraphRAG API"
