def precision_at_k(retrieved, expected, k):
    retrieved_k = retrieved[:k]
    relevant = [c for c in retrieved_k if c in expected]
    return len(relevant) / k if k > 0 else 0


def recall_at_k(retrieved, expected, k):
    retrieved_k = retrieved[:k]
    relevant = [c for c in retrieved_k if c in expected]
    return len(relevant) / len(expected) if expected else 0

def citation_accuracy(generated_chunks, expected_chunks):
    correct = set(generated_chunks) & set(expected_chunks)
    return len(correct) / len(expected_chunks)

def answer_match(predicted, expected):
    return predicted.strip().lower() == expected.strip().lower()
