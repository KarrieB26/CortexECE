import faiss
import numpy as np

class FAISSStore:

    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, chunks, embeddings):
        embeddings = np.array(embeddings).astype("float32")
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)
        self.metadata.extend(chunks)

    def search(self, query_vectors, top_k=5):
        query_vectors = np.array(query_vectors).astype("float32")
        faiss.normalize_L2(query_vectors)

        distances, indices = self.index.search(query_vectors, top_k)

        results = []

        for i in range(len(query_vectors)):
            query_results = []

            for j in range(top_k):
                idx = indices[i][j]

                if idx < len(self.metadata):
                    query_results.append({
                        **self.metadata[idx],
                        "score": float(distances[i][j])
                    })

            results.append(query_results)

        return results