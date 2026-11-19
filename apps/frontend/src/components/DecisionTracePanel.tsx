export type DecisionTraceItem = {
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
      <h2>Decision Trace</h2>
      {items.length === 0 && <p className="muted">No run to display.</p>}

      <div className="stack">
        {items.map((item, index) => (
          <article key={`${item.step}-${index}`} className="trace-item">
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
