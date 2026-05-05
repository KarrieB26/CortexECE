"""
End-to-End Generation Test

Tests:
- Embeddings
- FAISS
- BM25
- Hybrid Search
- Prompt Builder
- LLM Answer Generation
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from retrieval.embeddings import embed_batch
from retrieval.faiss_store import FAISSStore
from retrieval.bm25 import BM25Retriever
from retrieval import embeddings
from generation.answer_generator import generate_answer

# Sample chunk dataset for testing

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
    },
    {
  "text": "Voltage is the electrical potential difference between two points in an electrical circuit.",
  "page_number": 0,
  "file_name": "doc1.pdf",
  "chunk_id": "doc1.pdf_def_voltage"
},
]



print("--- Building Embeddings ---")

texts = [chunk["text"] for chunk in chunks]
chunk_embeddings = embed_batch(texts)

dimension = chunk_embeddings.shape[1]


print("--- Initializing FAISS ---")

faiss_store = FAISSStore(dimension)
faiss_store.add(chunks, chunk_embeddings)

print("--- Initializing BM25 ---")

bm25_retriever = BM25Retriever(chunks)


query = "What is voltage?"


# Generates answer using the full RAG pipeline (hybrid search + prompt building + LLM generation)

print("--- Running Full RAG Pipeline ---")

result = generate_answer(
    query=query,
    bm25_retriever=bm25_retriever,
    faiss_store=faiss_store,
    embedder=embeddings,
    top_k=3
)



print("\n=== QUERY ===")
print(result["query"])

print("\n=== RETRIEVED CHUNKS ===")
for i, chunk in enumerate(result["retrieved_chunks"], start=1):
    print(f"\nChunk {i}:")
    print("Text:", chunk["text"])
    print("Page:", chunk["page_number"])
    print("File:", chunk["file_name"])
    print("Chunk ID:", chunk["chunk_id"])
    print("Final Score:", chunk["final_score"])

print("\n=== GENERATED ANSWER ===")
print(result["answer"])