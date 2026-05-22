type DecisionTraceItem = {
  step: string;
  decision: string;
  reason: string;
  confidence?: number | null;
};

type DecisionTracePanelProps = {
  items: DecisionTraceItem[];
};

export function DecisionTracePanel({ items }: DecisionTracePanelProps) {
  return (
    <div className="card-content">
      <div className="badge">Decision Trace</div>
      <h2>Safe Explainability</h2>
      <p className="muted">
        Shows structured routing and tool-use decisions, not hidden chain-of-thought.
      </p>

      <div className="stack">
        {items.map((item) => (
          <article key={`${item.step}-${item.decision}`} className="trace-item">
            <strong>{item.step}</strong>
            <p style={{ marginBottom: 6 }}>{item.decision}</p>
            <p className="muted" style={{ marginBottom: 8 }}>{item.reason}</p>
            {typeof item.confidence === "number" && (
              <small className="badge">{Math.round(item.confidence * 100)}% confidence</small>
            )}
          </article>
        ))}
      </div>
    </div>
  );
}
