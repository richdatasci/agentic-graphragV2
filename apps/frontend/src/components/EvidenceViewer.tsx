type EvidenceItem = {
  citation: string;
  title: string;
  sourceType: "document" | "graph" | "vector" | "keyword" | "tool" | string;
  score?: number | null;
};

type EvidenceViewerProps = {
  items: EvidenceItem[];
};

export function EvidenceViewer({ items }: EvidenceViewerProps) {
  return (
    <div className="card-content">
      <h2>Retrieved Evidence</h2>
      {items.length === 0 && <p className="muted">No sources to display.</p>}

      <div className="stack">
        {items.map((item) => (
          <article key={item.citation} className="evidence-item">
            <strong>{item.citation} · {item.title}</strong>
            <div className="metric-row">
              <small>{item.sourceType}</small>
              {typeof item.score === "number" && <small>{item.score.toFixed(2)}</small>}
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
