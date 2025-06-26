import streamlit as st
from pdf_utils import extract_text_from_pdf, chunk_text
from embed_utils import embed_chunks
from chroma_utils import store_and_query_chunks
from llm import query_local_llm
import tempfile

st.title("📄 DocQBot: Chat with Your PDF - 100% Free")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
question = st.text_input("Ask a question about the PDF:")

if uploaded_file and question:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        pdf_path = tmp_file.name

    with st.spinner("Extracting text..."):
        full_text = extract_text_from_pdf(pdf_path)
        chunks = chunk_text(full_text)

    with st.spinner("Embedding and storing chunks..."):
        embeddings = embed_chunks(chunks)

    with st.spinner("Searching relevant content..."):
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

    with st.spinner("Generating answer..."):
        answer = query_local_llm(prompt)
        st.success("Answer:")
        st.write(answer)
