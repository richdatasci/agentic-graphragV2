"""
Basic smoke tests for the Python package layout.
"""


def test_graphrag_system_package_imports() -> None:
    import graphrag_system

    assert graphrag_system is not None
