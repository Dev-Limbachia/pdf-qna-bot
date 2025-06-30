# embed_utils.py
from sentence_transformers import SentenceTransformer

_model = None

def embed_chunks(chunks):
    global _model
    if _model is None:
        print("🔄 Loading embedding model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model.encode(chunks, convert_to_numpy=True).tolist()
