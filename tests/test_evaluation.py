import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from evaluation.dataset_builder import build_dataset
from evaluation.metrics import precision_at_k, recall_at_k, citation_accuracy
from evaluation.failure_logger import log_failure


# -----------------------------
# MOCK RETRIEVER (replace later)
# -----------------------------
def fake_retrieve(query):
    return [sample["expected_chunks"][0]]


# -----------------------------
# MOCK GENERATION (placeholder)
# -----------------------------
def fake_answer(query):
    return "Voltage is electrical potential difference."


# -----------------------------
# LOAD DATASET
# -----------------------------
dataset = build_dataset()

print("\n--- RUNNING EVALUATION ---\n")

K = 3  # standard evaluation cutoff

for sample in dataset:

    query = sample["query"]
    expected = sample["expected_chunks"]

    # retrieve results
    retrieved = fake_retrieve(query)

    # ensure we evaluate only top-K
    retrieved_k = retrieved[:K]

    # fake answer (not used heavily yet)
    answer = fake_answer(query)

    # -----------------------------
    # METRICS
    # -----------------------------
    p = precision_at_k(retrieved_k, expected, k=K)
    r = recall_at_k(retrieved_k, expected, k=K)
    c = citation_accuracy(retrieved_k, expected)

    # -----------------------------
    # OUTPUT
    # -----------------------------
    print(f"Query: {query}")
    print(f"P@{K}: {p:.2f} | R@{K}: {r:.2f} | Citation Acc: {c:.2f}")
    print("-" * 50)

    # -----------------------------
    # FAILURE LOGGING
    # -----------------------------
    if p < 0.5:
        log_failure("evaluation/failures.json", {
            "query": query,
            "error_type": "retrieval",
            "retrieved": retrieved_k,
            "expected": expected
        })