type Triple = {
  id: string;
  subject: string;
  predicate: string;
  object: string;
  confidence?: number | null;
};

type TriplePreviewProps = {
  triples: Triple[];
};

export function TriplePreview({ triples }: TriplePreviewProps) {
  return (
    <div className="card-content">
      <div className="badge">Triples Preview</div>
      <h2>Fuzzy Search Results</h2>

      <div className="stack">
        {triples.map((triple) => (
          <article key={triple.id} className="triple-item">
            <strong>{triple.subject}</strong>
            <p style={{ marginBottom: 6 }}>
              <span className="muted">{triple.predicate}</span> {triple.object}
            </p>
            {typeof triple.confidence === "number" && (
              <small className="badge">{Math.round(triple.confidence * 100)}% confidence</small>
            )}
          </article>
        ))}
      </div>
    </div>
  );
}
