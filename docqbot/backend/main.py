import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tempfile
from backend.pdf_utils import extract_text_from_pdf, chunk_text
from backend.embed_utils import embed_chunks
from backend.chroma_utils import store_and_query_chunks
from backend.llm import query_local_llm

# Optional: Load .env variables locally (has no effect on Render)
from dotenv import load_dotenv
load_dotenv()

# Path to frontend directory
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR)
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)

@app.route('/ask', methods=['POST'])
def ask_question():
    if "pdf" not in request.files or "question" not in request.form:
        return jsonify({"error": "Missing file or question"}), 400

    pdf_file = request.files["pdf"]
    question = request.form["question"]

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(pdf_file.read())
        pdf_path = tmp_file.name

    full_text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(full_text)
    embeddings = embed_chunks(chunks)
    top_chunks = store_and_query_chunks(chunks, embeddings, question)

    context = "\n\n".join(top_chunks)
    prompt = f"""
You are an AI assistant answering questions based on the following context:
---
{context}
---
Question: {question}
Answer:
"""

    answer = query_local_llm(prompt)
    return jsonify({"answer": answer})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # PORT from Render or default 5000 locally
    app.run(debug=True, host="0.0.0.0", port=port)
