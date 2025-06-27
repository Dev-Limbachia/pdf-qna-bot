from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile
from pdf_utils import extract_text_from_pdf, chunk_text
from embed_utils import embed_chunks
from chroma_utils import store_and_query_chunks
from llm import query_local_llm

app = Flask(__name__)
CORS(app)

@app.route("/ask", methods=["POST"])
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
    app.run(debug=True)
