from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text: str):
    vec = model.encode(text, normalize_embeddings=True)
    return np.array(vec, dtype=np.float32)


def embed_batch(texts: list[str]):
    vecs = model.encode(texts, normalize_embeddings=True)
    return np.array(vecs, dtype=np.float32)