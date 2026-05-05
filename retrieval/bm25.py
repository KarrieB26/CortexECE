import re
from rank_bm25 import BM25Okapi

def clean_tokens(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)  # remove punctuation
    return text.split()

class BM25Retriever:

    def __init__(self, chunks):
        self.chunks = chunks

        # IMPORTANT: use cleaned text, not raw split()
        tokenized = [clean_tokens(chunk["text"]) for chunk in chunks]

        self.bm25 = BM25Okapi(tokenized)

    def search(self, query, top_k=5):
        query_tokens = clean_tokens(query)

        scores = self.bm25.get_scores(query_tokens)

        ranked = sorted(
            zip(self.chunks, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:top_k]