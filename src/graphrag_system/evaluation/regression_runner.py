class RegressionRunner:
    def run(self, dataset: list[dict]) -> dict:
        return {"sample_count": len(dataset), "results": [], "status": "completed"}
