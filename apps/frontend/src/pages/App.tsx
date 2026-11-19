import React, { useState } from "react";
import { createRoot } from "react-dom/client";

import { ChatWindow, type ChatRun } from "../components/ChatWindow";
import { DecisionTracePanel } from "../components/DecisionTracePanel";
import { EvidenceViewer } from "../components/EvidenceViewer";
import { EvaluationDashboard } from "../components/EvaluationDashboard";
import { GraphViewer } from "../components/GraphViewer";
import { TriplePreview } from "../components/TriplePreview";
import "./styles.css";

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
  const [run, setRun] = useState<ChatRun | null>(null);
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
          <ChatWindow onRun={setRun} />
        </div>

        <div className="panel">
          <DecisionTracePanel items={run?.decision_trace ?? []} />
        </div>

        <div className="panel">
          <EvidenceViewer items={run?.evidence.map((item) => ({
            citation: item.citation,
            title: item.title ?? item.source_id,
            sourceType: item.source_type,
            score: item.score
          })) ?? []} />
        </div>

        <div className="panel panel-wide">
          <GraphViewer graph={run?.graph_preview ?? null} />
        </div>

        <div className="panel">
          <TriplePreview triples={sampleTriples} />
        </div>

        <div className="panel">
          <EvaluationDashboard
            faithfulnessScore={run?.faithfulness_score ?? null}
            answerRelevance={run?.answer_relevance ?? null}
            unsupportedClaims={run?.unsupported_claims ?? []}
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
