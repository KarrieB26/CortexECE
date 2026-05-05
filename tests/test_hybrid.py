import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from retrieval.embeddings import embed_text, embed_batch
from retrieval.faiss_store import FAISSStore
from retrieval.bm25 import BM25Retriever
from retrieval.hybrid_search import hybrid_search


# Sample chunk dataset
chunks = [
    {
        "text": "The device operates at a typical voltage of 3.3V.",
        "page_number": 1,
        "file_name": "doc1.pdf",
        "chunk_id": "doc1.pdf_p1_c0"
    },
    {
        "text": "Maximum current consumption is 50mA.",
        "page_number": 2,
        "file_name": "doc1.pdf",
        "chunk_id": "doc1.pdf_p2_c0"
    },
    {
        "text": "Ohm's law states that voltage equals current times resistance.",
        "page_number": 3,
        "file_name": "doc1.pdf",
        "chunk_id": "doc1.pdf_p3_c0"
    },
    {
        "text": "Capacitors store electrical energy in an electric field.",
        "page_number": 4,
        "file_name": "doc1.pdf",
        "chunk_id": "doc1.pdf_p4_c0"
    },
    {
        "text": "Pin 5 is the ground connection.",
        "page_number": 5,
        "file_name": "doc1.pdf",
        "chunk_id": "doc1.pdf_p5_c0"
    }
]

print("--- Building Embeddings ---")
texts = [chunk["text"] for chunk in chunks]
embeddings = embed_batch(texts)

print("--- Initializing FAISS ---")
dim = embeddings.shape[1]
faiss_store = FAISSStore(dim)
faiss_store.add(chunks, embeddings)

print("--- Initializing BM25 ---")
bm25_retriever = BM25Retriever(chunks)

print("--- Running Hybrid Search ---")
query = "What is voltage?"
results = hybrid_search(
    query=query,
    bm25_retriever=bm25_retriever,
    faiss_store=faiss_store,
    embedder=sys.modules['retrieval.embeddings'],
    top_k=3
)

print("\n=== QUERY ===")
print(query)

print("\n=== RESULTS ===")
for i, result in enumerate(results, start=1):
    print(f"\nResult {i}:")
    print("Text:", result["text"])
    print("Page:", result["page_number"])
    print("File:", result["file_name"])
    print("Chunk ID:", result["chunk_id"])
    print("Semantic Score:", result["semantic_score"])
    print("BM25 Score:", result["bm25_score"])
    print("Final Score:", result["final_score"])