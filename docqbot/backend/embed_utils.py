# embed_utils.py
from sentence_transformers import SentenceTransformer

_model = None

def embed_chunks(chunks):
    global _model
    if _model is None:
        print("🔄 Loading embedding model...")
        _model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    return _model.encode(chunks, convert_to_numpy=True).tolist()
