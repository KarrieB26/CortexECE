from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Dict, List

from extraction.regex_extractor import extract_regex
from extraction.llm_extractor import extract_with_llm
from comparison.compare_docs import compare_docs
from comparison.table_generator import generate_table

app = FastAPI(
    title="CortexECE RAG API",
    description="PDF ingestion, RAG QA, extraction, and comparison system",
    version="1.0.0"
)


# =========================
# REQUEST MODELS
# =========================
class QueryRequest(BaseModel):
    query: str


class CompareRequest(BaseModel):
    documents: Dict[str, str]


# =========================
# GLOBAL STORAGE
# =========================
# Stores uploaded document text
uploaded_docs: Dict[str, str] = {}


# =========================
# ROOT HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {
        "message": "CortexECE API is running",
        "uploaded_documents": list(uploaded_docs.keys())
    }


# =========================
# 1. UPLOAD ENDPOINT
# =========================
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Uploads a text/PDF-like file and stores content in memory.
    Supports multiple uploads.
    """

    try:
        content = await file.read()
        text = content.decode("utf-8", errors="ignore")

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty or unreadable."
            )

        uploaded_docs[file.filename] = text

        return {
            "message": "uploaded successfully",
            "filename": file.filename,
            "total_uploaded_docs": len(uploaded_docs)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )


# =========================
# 2. RAG QUERY ENDPOINT
# =========================
@app.post("/query")
def query_rag(req: QueryRequest):

    if not uploaded_docs:
        raise HTTPException(
            status_code=400,
            detail="No documents uploaded yet."
        )

    query_terms = req.query.lower().split()

    scored_results = []

    for filename, text in uploaded_docs.items():

        score = sum(
            1 for term in query_terms
            if term in text.lower()
        )

        if score > 0:
            scored_results.append({
                "chunk_id": f"{filename}_match",
                "file_name": filename,
                "page_number": 1,
                "text": text[:1000],
                "score": score
            })

    if not scored_results:
        raise HTTPException(
            status_code=404,
            detail="No relevant documents found."
        )

    scored_results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    retrieved_chunks = scored_results[:3]

    answer = retrieved_chunks[0]["text"][:500]

    return {
        "query": req.query,
        "answer": answer,
        "retrieved_chunks": retrieved_chunks
    }


# =========================
# 3. STRUCTURED EXTRACTION
# =========================
@app.post("/extract")
def extract(req: QueryRequest):
    """
    Extracts structured specs from provided text query/input.
    Uses both regex + LLM extraction.
    """

    regex_result = extract_regex(req.query)
    llm_result = extract_with_llm(req.query)

    return {
        "query": req.query,
        "regex_extraction": regex_result,
        "llm_extraction": llm_result
    }


# =========================
# 4. MULTI-DOC COMPARISON
# =========================
@app.post("/compare")
def compare(req: CompareRequest):
    """
    Compares multiple documents and generates normalized comparison table.
    """

    if len(req.documents) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least two documents are required for comparison."
        )

    results = compare_docs(req.documents)

    table = generate_table(results)

    return {
        "documents_compared": list(req.documents.keys()),
        "comparison": results,
        "table": table
    }


# =========================
# 5. LIST UPLOADED DOCS
# =========================
@app.get("/documents")
def list_documents():
    return {
        "uploaded_documents": list(uploaded_docs.keys()),
        "count": len(uploaded_docs)
    }