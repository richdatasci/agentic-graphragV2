export function GraphViewer() {
  return (
    <div className="card-content">
      <div className="badge">Graph Presentation</div>
      <h2>Indexed Knowledge Graph</h2>
      <p className="muted">
        Placeholder visualisation shell. This can later be replaced with Cytoscape.js
        or React Flow once the graph endpoints are connected.
      </p>

      <div className="graph-canvas" aria-label="Graph visualisation placeholder">
        <div className="graph-node" style={{ left: "8%", top: "42%" }}>Document</div>
        <div className="graph-node" style={{ left: "34%", top: "18%" }}>Chunk</div>
        <div className="graph-node" style={{ left: "58%", top: "42%" }}>Entity</div>
        <div className="graph-node" style={{ left: "78%", top: "18%" }}>Triple</div>
        <div className="graph-node" style={{ left: "40%", top: "68%" }}>Claim</div>
      </div>
    </div>
  );
}
