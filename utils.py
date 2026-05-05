import requests
from config import API_URL


def upload_file(uploaded_file):
    """
    Uploads a document to FastAPI backend.
    """

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "text/plain"
        )
    }

    return requests.post(
        f"{API_URL}/upload",
        files=files
    )


def query_rag(query):
    """
    Sends question to RAG backend.
    """

    return requests.post(
        f"{API_URL}/query",
        json={"query": query}
    )


def extract_specs(text):
    """
    Sends raw technical text for structured extraction.
    """

    return requests.post(
        f"{API_URL}/extract",
        json={"query": text}
    )


def compare_docs(doc1, doc2):
    """
    Compares two technical documents.
    """

    return requests.post(
        f"{API_URL}/compare",
        json={
            "documents": {
                "doc1": doc1,
                "doc2": doc2
            }
        }
    )