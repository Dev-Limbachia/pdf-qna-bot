import os
import tempfile
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Use relative path to frontend directory
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR)
CORS(app)

@app.route("/favicon.ico")
def favicon():
    return "", 204

@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)

# Health check route
@app.route("/healthz", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route("/ask", methods=["POST"])
def ask_question():
    try:
        print("📥 /ask endpoint hit")

        # Dummy test block — uncomment this to verify basic POST works
        # return jsonify({"answer": "✅ Test OK"}), 200

        if "pdf" not in request.files or "question" not in request.form:
            print("❌ Missing PDF or question")
            return jsonify({"error": "Missing file or question"}), 400

        pdf_file = request.files["pdf"]
        question = request.form["question"]
        print(f"Question: {question}")

        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(pdf_file.read())
            pdf_path = tmp_file.name

        print("📄 Extracting PDF text...")
        from backend.pdf_utils import extract_text_from_pdf, chunk_text
        full_text = extract_text_from_pdf(pdf_path)

        print("🧩 Chunking text...")
        chunks = chunk_text(full_text)

        print("🔍 Embedding chunks...")
        from backend.embed_utils import embed_chunks
        embeddings = embed_chunks(chunks)

        print("📚 Querying top chunks...")
        from backend.chroma_utils import store_and_query_chunks
        top_chunks = store_and_query_chunks(chunks, embeddings, question)

        context = "\n\n".join(top_chunks)
        prompt = f"""You are an AI assistant answering questions based on the following context:
---
{context}
---
Question: {question}
Answer:"""

        print("🧠 Calling LLM...")
        from backend.llm import query_local_llm
        answer = query_local_llm(prompt)

        print("✅ Answer ready")
        return jsonify({"answer": answer})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Server error", "details": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render sets PORT
    app.run(host="0.0.0.0", port=port)
