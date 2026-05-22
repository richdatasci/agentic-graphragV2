import { SendHorizonal } from "lucide-react";
import { FormEvent, useState } from "react";

type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

export function ChatWindow() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content:
        "Ask a question and this panel will call the Agentic GraphRAG API once the backend services are wired."
    }
  ]);
  const [query, setQuery] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmed = query.trim();
    if (!trimmed) return;

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
          include_decision_trace: true,
          include_graph_preview: true
        })
      });

      if (!response.ok) {
        throw new Error(`API returned ${response.status}`);
      }

      const data = await response.json();

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: data.answer ?? "No answer returned."
        }
      ]);
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content:
            "The frontend is running, but the API is not reachable yet. Start the FastAPI service or check the Vite proxy."
        }
      ]);
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
        <button type="submit" aria-label="Send message">
          <SendHorizonal size={18} />
        </button>
      </form>
    </div>
  );
}
