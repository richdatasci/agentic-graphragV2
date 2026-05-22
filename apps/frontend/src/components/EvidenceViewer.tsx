type EvidenceItem = {
  sourceId: string;
  title: string;
  sourceType: "document" | "graph" | "vector" | "keyword" | "tool" | string;
  score?: number | null;
  excerpt: string;
};

type EvidenceViewerProps = {
  items: EvidenceItem[];
};

export function EvidenceViewer({ items }: EvidenceViewerProps) {
  return (
    <div className="card-content">
      <div className="badge">Evidence</div>
      <h2>Retrieved Context</h2>

      <div className="stack">
        {items.map((item) => (
          <article key={item.sourceId} className="evidence-item">
            <strong>{item.title}</strong>
            <p className="muted" style={{ marginBottom: 8 }}>{item.excerpt}</p>
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
