class EvaluationReportBuilder:
    def build_markdown(self, summary: dict) -> str:
        lines = ["# Evaluation Report", ""]
        for key, value in summary.items():
            lines.append(f"- **{key}**: {value}")
        return "\n".join(lines)
