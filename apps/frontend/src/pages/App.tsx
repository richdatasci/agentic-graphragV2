import React from "react";
import { createRoot } from "react-dom/client";

import { ChatWindow } from "../components/ChatWindow";
import { DecisionTracePanel } from "../components/DecisionTracePanel";
import { EvidenceViewer } from "../components/EvidenceViewer";
import { EvaluationDashboard } from "../components/EvaluationDashboard";
import { GraphViewer } from "../components/GraphViewer";
import { TriplePreview } from "../components/TriplePreview";
import "./styles.css";

const sampleTrace = [
  {
    step: "route_query",
    decision: "hybrid_graph_vector",
    reason: "The user asked for architecture, relationships and evidence-backed implementation detail.",
    confidence: 0.89
  },
  {
    step: "evaluate_answer",
    decision: "run_faithfulness_check",
    reason: "Generated answers should be checked against retrieved context.",
    confidence: 0.93
  }
];

const sampleEvidence = [
  {
    sourceId: "doc_architecture_001",
    title: "Agentic GraphRAG Architecture",
    sourceType: "document",
    score: 0.92,
    excerpt: "Hybrid retrieval combines graph traversal, vector search, keyword search and reranking."
  },
  {
    sourceId: "graph_entity_neo4j",
    title: "Graph DB Entity",
    sourceType: "graph",
    score: 0.87,
    excerpt: "Neo4j stores entities, claims, triples and document lineage."
  }
];

const sampleTriples = [
  {
    id: "triple_001",
    subject: "GraphRAG ingestion pipeline",
    predicate: "generates",
    object: "entity relationship triples",
    confidence: 0.88
  },
  {
    id: "triple_002",
    subject: "Faithfulness evaluation",
    predicate: "checks",
    object: "answer support against context",
    confidence: 0.91
  }
];

function App() {
  return (
    <main className="app-shell">
      <header className="app-header">
        <div>
          <p className="eyebrow">Production Reference UI</p>
          <h1>Agentic GraphRAG Platform</h1>
          <p>
            Chat, evidence, decision trace, graph visualisation, triples preview
            and evaluation dashboard in one working frontend shell.
          </p>
        </div>
      </header>

      <section className="dashboard-grid">
        <div className="panel panel-large">
          <ChatWindow />
        </div>

        <div className="panel">
          <DecisionTracePanel items={sampleTrace} />
        </div>

        <div className="panel">
          <EvidenceViewer items={sampleEvidence} />
        </div>

        <div className="panel panel-wide">
          <GraphViewer />
        </div>

        <div className="panel">
          <TriplePreview triples={sampleTriples} />
        </div>

        <div className="panel">
          <EvaluationDashboard
            faithfulnessScore={0.91}
            contextPrecision={0.84}
            contextRecall={0.79}
            answerRelevance={0.88}
          />
        </div>
      </section>
    </main>
  );
}

const root = createRoot(document.getElementById("root") as HTMLElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
