import { useState } from "react";

function App() {
  const [pdfFile, setPdfFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!pdfFile || !question) {
      alert("Please provide a PDF and question.");
      return;
    }

    const formData = new FormData();
    formData.append("pdf", pdfFile);
    formData.append("question", question);

    setLoading(true);
    setAnswer("");

    try {
      const API_BASE = "https://pdf-qna-bot.onrender.com";

      const res = await fetch(`${API_BASE}/ask`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setAnswer(data.answer || "No answer returned.");
    } catch (err) {
      console.error(err);
      setAnswer("Something went wrong.");
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "600px", margin: "0 auto" }}>
      <h1>📄 DocQBot</h1>
      <p>Chat with your PDF – 100% Free</p>

      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setPdfFile(e.target.files[0])}
      />
      <br />
      <br />

      <input
        type="text"
        placeholder="Ask a question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        style={{ width: "100%", padding: "0.5rem" }}
      />
      <br />
      <br />

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Thinking..." : "Ask"}
      </button>

      {answer && (
        <div style={{ marginTop: "2rem", background: "#eee", padding: "1rem" }}>
          <strong>Answer:</strong>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default App;
