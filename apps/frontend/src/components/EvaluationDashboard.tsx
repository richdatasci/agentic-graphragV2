type EvaluationDashboardProps = {
  faithfulnessScore: number;
  contextPrecision: number;
  contextRecall: number;
  answerRelevance: number;
};

function MetricBar({ label, value }: { label: string; value: number }) {
  const percentage = Math.round(value * 100);

  return (
    <div className="metric">
      <div className="metric-row">
        <strong>{label}</strong>
        <span>{percentage}%</span>
      </div>
      <div className="progress" aria-label={`${label}: ${percentage}%`}>
        <span style={{ width: `${percentage}%` }} />
      </div>
    </div>
  );
}

export function EvaluationDashboard({
  faithfulnessScore,
  contextPrecision,
  contextRecall,
  answerRelevance
}: EvaluationDashboardProps) {
  return (
    <div className="card-content">
      <div className="badge">Evaluation</div>
      <h2>RAG Quality Metrics</h2>

      <div className="stack">
        <MetricBar label="Faithfulness" value={faithfulnessScore} />
        <MetricBar label="Context precision" value={contextPrecision} />
        <MetricBar label="Context recall" value={contextRecall} />
        <MetricBar label="Answer relevance" value={answerRelevance} />
      </div>
    </div>
  );
}
