import { useState } from "react";

interface Citation {
  text: string;
  source: string;
}

interface QueryResponse {
  answer: string;
  citations: Citation[];
}

export default function App() {
  const [query, setQuery] = useState<string>("");
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const askQuery = async () => {
    setLoading(true);
    const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    const data = await res.json();
    setResponse(data);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-2xl mx-auto bg-white shadow p-6 rounded-xl space-y-4">
        <h1 className="text-2xl font-bold text-gray-800">🧠 Legal Assistant</h1>

        <textarea
          rows={3}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full border p-2 rounded-md"
          placeholder="Ask a legal question..."
        />

        <button
          onClick={askQuery}
          disabled={loading || !query}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          {loading ? "Thinking..." : "Ask"}
        </button>

        {response && (
          <div className="space-y-2">
            <div className="font-semibold text-gray-700">💬 Answer:</div>
            <p className="bg-gray-100 p-3 rounded">{response.answer}</p>

            <div className="font-semibold text-gray-700">📎 Citations:</div>
            <ul className="list-disc list-inside space-y-1 text-sm text-gray-700">
              {response.citations.map((c, i) => (
                <li key={i}>
                  <span className="font-medium">{c.source}</span>: {c.text.slice(0, 200)}...
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
