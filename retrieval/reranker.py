from sentence_transformers import SentenceTransformer, util

# Load model once (important for performance)
model = SentenceTransformer("all-MiniLM-L6-v2")


def rerank(query, chunks, top_k=5):
    """
    Re-ranks retrieved chunks using semantic similarity.

    Args:
        query (str): user query
        chunks (list): retrieved chunks from hybrid search
        top_k (int): number of final results

    Returns:
        list: reranked top_k chunks
    """

    if not chunks:
        return []

    # -------------------------
    # 1. Encode query once
    # -------------------------
    query_emb = model.encode(query, normalize_embeddings=True)

    # -------------------------
    # 2. Batch encode chunk texts
    # -------------------------
    texts = [chunk["text"] for chunk in chunks]
    chunk_embs = model.encode(texts, normalize_embeddings=True)

    # -------------------------
    # 3. Compute cosine similarity
    # -------------------------
    scores = util.cos_sim(query_emb, chunk_embs)[0].cpu().numpy()

    # -------------------------
    # 4. Attach scores to chunks
    # -------------------------
    scored_chunks = []
    for chunk, score in zip(chunks, scores):
        scored_chunks.append({
            **chunk,
            "rerank_score": float(score)
        })

    # -------------------------
    # 5. Sort by rerank score
    # -------------------------
    scored_chunks.sort(key=lambda x: x["rerank_score"], reverse=True)

    # -------------------------
    # 6. Return top_k results (no aggressive filtering)
    # -------------------------
    return scored_chunks[:top_k]