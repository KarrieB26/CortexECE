def hybrid_search(query, bm25_retriever, faiss_store, embedder, top_k=5):
    # Embaeds query for semantic search
    query_vector = embedder.embed_text(query).reshape(1, -1)

    semantic_results = faiss_store.search(query_vector, top_k=top_k)[0]
    keyword_results = bm25_retriever.search(query, top_k=top_k)

    combined_results = {}

    # loop to process semantic results
    for chunk in semantic_results:
        semantic_score = 1 / (1 + chunk["score"])
        chunk_id = chunk["chunk_id"]

        combined_results[chunk_id] = {
            "text": chunk["text"],
            "page_number": chunk["page_number"],
            "file_name": chunk["file_name"],
            "chunk_id": chunk["chunk_id"],
            "semantic_score": semantic_score,
            "bm25_score": 0
        }

    # loop to process bm25 results
    for chunk, bm25_score in keyword_results:
        chunk_id = chunk["chunk_id"]

        if chunk_id in combined_results:
            combined_results[chunk_id]["bm25_score"] = bm25_score
        else:
            combined_results[chunk_id] = {
                "text": chunk["text"],
                "page_number": chunk["page_number"],
                "file_name": chunk["file_name"],
                "chunk_id": chunk["chunk_id"],
                "semantic_score": 0,
                "bm25_score": bm25_score
            }

    # Combine scores with weighted hybrid scoring
    for chunk_id in combined_results:
        semantic_score = combined_results[chunk_id]["semantic_score"]
        bm25_score = combined_results[chunk_id]["bm25_score"]

        final_score = (0.7 * semantic_score) + (0.3 * bm25_score)

        # small definition boost for "what is X" type queries
        text = combined_results[chunk_id]["text"]
        definition_bonus = 0.1 if " is " in text[:80].lower() else 0

        final_score += definition_bonus

        combined_results[chunk_id]["final_score"] = final_score

    # Convert to list and sort by final score
    results = list(combined_results.values())
    results.sort(key=lambda x: x["final_score"], reverse=True)


    from retrieval.reranker import rerank

    top_candidates = results[:10]   # take top candidates first
    final_results = rerank(query, top_candidates, top_k)

    return final_results