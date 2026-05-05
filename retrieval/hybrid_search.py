from retrieval.reranker import rerank

def hybrid_search(query, bm25_retriever, faiss_store, embedder, top_k=5):

    # 1. Encode query for FAISS
    query_vector = embedder.embed_text(query).reshape(1, -1)

    semantic_results = faiss_store.search(query_vector, top_k=top_k)[0]
    keyword_results = bm25_retriever.search(query, top_k=top_k)

    combined_results = {}

    # FAISS (semantic signal)
    for chunk in semantic_results:
        chunk_id = chunk["chunk_id"]

        # convert distance → similarity score
        semantic_score = 1 / (1 + chunk["score"])

        combined_results[chunk_id] = {
            "text": chunk["text"],
            "page_number": chunk["page_number"],
            "file_name": chunk["file_name"],
            "chunk_id": chunk_id,
            "semantic_score": semantic_score,
            "bm25_score": 0
        }

    # BM25 (keyword signal)
    for chunk, bm25_score in keyword_results:
        chunk_id = chunk["chunk_id"]

        if chunk_id in combined_results:
            combined_results[chunk_id]["bm25_score"] = bm25_score
        else:
            combined_results[chunk_id] = {
                "text": chunk["text"],
                "page_number": chunk["page_number"],
                "file_name": chunk["file_name"],
                "chunk_id": chunk_id,
                "semantic_score": 0,
                "bm25_score": bm25_score
            }

    # Score fusion (clean version)
    for chunk_id, data in combined_results.items():

        semantic_score = data["semantic_score"]
        bm25_score = data["bm25_score"]

        # balanced but semantic-leaning
        final_score = (0.8 * semantic_score) + (0.2 * bm25_score)

        data["final_score"] = final_score

    # Sort candidates
    results = list(combined_results.values())
    results.sort(key=lambda x: x["final_score"], reverse=True)

    # Candidate selection (before rerank)
    top_candidates = results[:10]

    # Rerank stage (semantic refinement)
    final_results = rerank(query, top_candidates, top_k)

    return final_results