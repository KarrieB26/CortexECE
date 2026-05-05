from retrieval.hybrid_search import hybrid_search
from retrieval.reranker import rerank
from generation.prompt_templates import build_prompt
from generation.llm import call_llm

def generate_answer(query, bm25_retriever, faiss_store, embedder, top_k=5):
    """
    Generates a grounded answer using retrieved context and LLM.

    Args:
        query (str): User question
        bm25_retriever: BM25 retrieval system
        faiss_store: FAISS semantic retrieval system
        embedder: Embedding model
        top_k (int): Number of chunks to retrieve

    Returns:
        dict:
            {
                "query": ...,
                "retrieved_chunks": [...],
                "prompt": ...,
                "answer": ...
            }
    """

    # Step 1: Retrieve relevant chunks (Hybrid Search)
    retrieved_chunks = hybrid_search(
        query=query,
        bm25_retriever=bm25_retriever,
        faiss_store=faiss_store,
        embedder=embedder,
        top_k=top_k
    )

    # Step 2: Rerank retrieved chunks using semantic similarity
    reranked_chunks = rerank(
        query=query,
        chunks=retrieved_chunks,
        top_k=top_k
    )

    # Step 3: Build grounded prompt using reranked results
    prompt = build_prompt(
        query=query,
        chunks=reranked_chunks
    )

    # Step 4: Generate answer using LLM
    answer = call_llm(prompt)

    # Step 5: Return full structured response
    return {
        "query": query,
        "retrieved_chunks": reranked_chunks,
        "prompt": prompt,
        "answer": answer
    }