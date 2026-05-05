import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from retrieval.bm25 import BM25Retriever

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
        "text": "Pin 5 is the ground connection.",
        "page_number": 1,
        "file_name": "doc1.pdf",
        "chunk_id": "doc1.pdf_p1_c1"
    }
]

print("--- Initializing BM25 ---")
retriever = BM25Retriever(chunks)
results = retriever.search("voltage 3.3V")

if results:
    print("\n--- Top Search Result ---")
    print(results[0])
else:
    print("No results found.")