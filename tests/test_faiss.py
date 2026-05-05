import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from retrieval.embeddings import embed_batch, embed_text
from retrieval.faiss_store import FAISSStore

chunks = [
    {"text": "Voltage is 3.3V in this circuit.", "page_number": 1, "file_name": "doc1.pdf"},
    {"text": "Current increases with resistance decrease.", "page_number": 2, "file_name": "doc1.pdf"},
    {"text": "Ohm's law states V = IR.", "page_number": 3, "file_name": "doc1.pdf"},
    {"text": "Capacitors store electrical energy.", "page_number": 4, "file_name": "doc1.pdf"},
    {"text": "Inductors resist changes in current.", "page_number": 5, "file_name": "doc1.pdf"},
]

texts = [c["text"] for c in chunks]

# Embed the texts
embeddings = embed_batch(texts)

# Cteate FAISS store
dim = embeddings.shape[1]
store = FAISSStore(dim)

# Add chunks and embeddings to the store
store.add(chunks, embeddings)

query = "What is voltage?"
query_vec = embed_text(query)

results = store.search([query_vec], top_k=3)

print("\n=== QUERY ===")
print(query)

print("\n=== RESULTS ===")
for i, res in enumerate(results[0]):
    print(f"\nResult {i+1}:")
    print("Text:", res["text"])
    print("Page:", res["page_number"])
    print("File:", res["file_name"])
    print("Score:", res["score"])