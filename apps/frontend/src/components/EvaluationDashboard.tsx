type EvaluationDashboardProps = {
  faithfulnessScore: number | null;
  answerRelevance: number | null;
  unsupportedClaims: string[];
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
  answerRelevance,
  unsupportedClaims
}: EvaluationDashboardProps) {
  return (
    <div className="card-content">
      <h2>Answer Evaluation</h2>

      <div className="stack">
        {faithfulnessScore === null && <p className="muted">No evaluation to display.</p>}
        {faithfulnessScore !== null && <MetricBar label="Faithfulness" value={faithfulnessScore} />}
        {answerRelevance !== null && <MetricBar label="Answer relevance" value={answerRelevance} />}
        {unsupportedClaims.length > 0 && (
          <div>
            <strong>Unsupported draft claims</strong>
            <ul>{unsupportedClaims.map((claim, index) => <li key={index}>{claim}</li>)}</ul>
          </div>
        )}
      </div>
    </div>
  );
}
