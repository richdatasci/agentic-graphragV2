import { SendHorizonal } from "lucide-react";
import { FormEvent, useState } from "react";
import type { DecisionTraceItem } from "./DecisionTracePanel";
import type { GraphPreview } from "./GraphViewer";

type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

export type ChatRun = {
  session_id: string;
  answer: string;
  decision_trace: DecisionTraceItem[];
  evidence: {
    citation: string;
    source_id: string;
    source_type: string;
    title: string | null;
    score: number | null;
  }[];
  graph_preview: GraphPreview | null;
  faithfulness_score: number | null;
  answer_relevance: number | null;
  unsupported_claims: string[];
};

export function ChatWindow({ onRun }: { onRun: (run: ChatRun) => void }) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content:
        "Ask a question about your indexed documents."
    }
  ]);
  const [query, setQuery] = useState("");
  const [sessionId, setSessionId] = useState<string | undefined>();
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmed = query.trim();
    if (!trimmed || submitting) return;
    setSubmitting(true);

    setMessages((current) => [...current, { role: "user", content: trimmed }]);
    setQuery("");

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          query: trimmed,
          session_id: sessionId,
          include_decision_trace: true,
          include_graph_preview: true
        })
      });

      if (!response.ok) {
        throw new Error(`API returned ${response.status}`);
      }

      const data: ChatRun = await response.json();
      setSessionId(data.session_id);
      onRun(data);

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: data.answer ?? "No answer returned."
        }
      ]);
    } catch {
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content:
            "The frontend is running, but the API is not reachable yet. Start the FastAPI service or check the Vite proxy."
        }
      ]);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="card-content">
      <div className="badge">Chat Interface</div>
      <h2>Grounded Agent Conversation</h2>

      <div className="stack">
        {messages.map((message, index) => (
          <div key={`${message.role}-${index}`} className="trace-item">
            <strong>{message.role === "user" ? "User" : "Assistant"}</strong>
            <p className="muted" style={{ marginBottom: 0 }}>{message.content}</p>
          </div>
        ))}
      </div>

      <form className="input-row" onSubmit={handleSubmit}>
        <input
          aria-label="Ask the Agentic GraphRAG system"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Ask about a document, system, graph relationship or decision..."
        />
        <button type="submit" disabled={submitting} aria-label="Send message">
          <SendHorizonal size={18} />
        </button>
      </form>
    </div>
  );
}
