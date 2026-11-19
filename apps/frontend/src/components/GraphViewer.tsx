export type GraphPreview = {
  nodes: { id: string; label: string }[];
  edges: { id: string; source: string; target: string; type: string; citations: string[] }[];
};

export function GraphViewer({ graph }: { graph: GraphPreview | null }) {
  const labels = new Map(graph?.nodes.map((node) => [node.id, node.label]));

  return (
    <div className="card-content">
      <h2>Retrieved Relationships</h2>
      {graph ? (
        <ul className="stack">
          {graph.edges.map((edge) => (
            <li key={edge.id}>
              <strong>{labels.get(edge.source)}</strong>
              {" → "}{edge.type}{" → "}
              <strong>{labels.get(edge.target)}</strong>
              <small className="muted"> · {edge.citations.join(", ")}</small>
            </li>
          ))}
        </ul>
      ) : (
        <p className="muted">No graph evidence to display.</p>
      )}
    </div>
  );
}
