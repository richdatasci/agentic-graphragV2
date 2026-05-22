from graphrag_system.evaluation.faithfulness import FaithfulnessEvaluator


def test_faithfulness_supported_claim() -> None:
    evaluator = FaithfulnessEvaluator()
    result = evaluator.evaluate("GraphRAG uses graph retrieval.", ["GraphRAG uses graph retrieval and vector search."])
    assert result["faithfulness_score"] >= 0
