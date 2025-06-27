# embed_utils.py
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

def embed_chunks(chunks):
    return model.encode(chunks, convert_to_numpy=True).tolist()
