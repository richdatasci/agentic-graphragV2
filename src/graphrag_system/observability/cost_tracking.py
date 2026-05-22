class CostTracker:
    def estimate(self, input_tokens: int, output_tokens: int, input_cost_per_1k: float = 0.0, output_cost_per_1k: float = 0.0) -> float:
        return (input_tokens / 1000 * input_cost_per_1k) + (output_tokens / 1000 * output_cost_per_1k)
