# CortexECE — Engineering Document Intelligence System (v2)

## AI System for Technical Document Understanding, Extraction, and Comparison

---

## Overview

CortexECE is a production-style AI engineering system that enables users to:

- Query technical PDFs (datasheets, manuals, research papers)
- Extract structured engineering specifications
- Compare multiple hardware devices
- Handle both digital and scanned documents (OCR supported)
- Access system functionality via an API backend

It combines:
- Retrieval-Augmented Generation (RAG)
- Hybrid Search
- Structured ML Extraction
- OCR
- Evaluation-driven design

---

## Problem It Solves

Engineering documentation is:

- Dense and unstructured
- Spread across multiple PDFs
- Hard to search precisely
- Difficult to compare across devices
- Often scanned and not machine-readable

CortexECE converts these documents into a queryable engineering intelligence system.

---

## System Architecture

### Document Ingestion Layer

- PDF parsing using PyMuPDF
- OCR pipeline for scanned documents (Tesseract or EasyOCR)
- Text cleaning and normalization
- Chunking with overlap strategy

Pipeline:
PDF -> Detection -> Text extraction or OCR -> Cleaning -> Chunking

---

### Hybrid Retrieval System

- FAISS vector search for semantic similarity
- BM25 keyword search for exact term matching
- Optional reranking layer (cross-encoder or LLM-based)

Output:
- Top-k relevant document chunks

---

### LLM Answer Generation

- Uses retrieved context only
- Produces grounded responses
- Includes citations (page-level or section-level)
- Designed to reduce hallucinations

---

### Structured Extraction (ML Component)

Extracts:

- Voltage ranges
- Current consumption
- Frequency limits
- Power specifications
- Pin configurations

Approaches:

- Baseline: Regex extraction
- Improved: LLM-based structured JSON extraction or NER model

Example output:

{
  "device": "ESP32",
  "voltage_range": "2.2V - 3.6V",
  "max_frequency": "240 MHz"
}

---

### Multi-Document Comparison Engine

Supports comparisons such as:

Compare STM32 vs ESP32 power consumption

Outputs:

- Normalized comparison tables
- Aligned specifications
- Unit normalization across documents

---

### Evaluation System

Evaluates system performance using:

Metrics:

- Retrieval Precision@K
- Answer faithfulness
- Citation accuracy
- Extraction F1 score
- Latency (p50 / p95)

Includes:

- Failure case logging
- Error categorization:
  - Retrieval failures
  - Generation hallucinations
  - Extraction errors

---

### API Backend

Built using FastAPI

Endpoints:

- /query: ask questions
- /upload: upload PDFs
- /extract: structured extraction
- /compare: multi-document comparison

---

### UI Layer

Built using Streamlit or React

Features:

- Upload PDFs
- Ask questions
- View citations
- View extracted structured data
- Compare documents
- Debug retrieval results

---

## Tech Stack

- Python
- FAISS
- BM25
- OpenAI or LLM APIs
- PyMuPDF
- Tesseract or EasyOCR
- FastAPI
- Streamlit
- NumPy
- Pandas

---

## Key Innovations

- Hybrid retrieval combining semantic and keyword search
- OCR support for scanned real-world documents
- API-based architecture for deployment
- Structured ML extraction pipeline
- Evaluation-driven system design

---

## Target Users

- Electrical engineers
- Embedded systems developers
- Hardware designers
- ECE students
- AI/ML engineers working on document intelligence

---

## Expected Outcomes

This project demonstrates:

- AI system design
- RAG architecture
- OCR and document understanding pipelines
- ML-based structured extraction
- Evaluation-driven engineering
- Full-stack AI deployment

---

## Final Positioning

CortexECE is a production-grade AI system for engineering document intelligence combining hybrid retrieval, OCR, structured extraction, and API-based deployment for real-world hardware knowledge extraction and comparison.
