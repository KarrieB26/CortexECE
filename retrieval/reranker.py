from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def rerank(query, chunks, top_k=5):
    query_emb = model.encode(query, normalize_embeddings=True)

    scored = []

    for chunk in chunks:
        chunk_emb = model.encode(chunk["text"], normalize_embeddings=True)

        score = util.cos_sim(query_emb, chunk_emb).item()

        chunk["rerank_score"] = score
        scored.append(chunk)

    scored.sort(key=lambda x: x["rerank_score"], reverse=True)

    return scored[:top_k]