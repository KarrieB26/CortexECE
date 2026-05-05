import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from utils import upload_file, query_rag, extract_specs, compare_docs


st.title("🧠 Cortex RAG System")


# =========================
# UPLOAD
# =========================
st.header("📄 Upload PDF")

uploaded_file = st.file_uploader("Upload a document")

if uploaded_file and st.button("Upload"):

    res = upload_file(uploaded_file)
    st.json(res.json())


# =========================
# QUERY
# =========================
st.header("💬 Ask Question")

query = st.text_input("Enter your question")

if st.button("Search"):

    res = query_rag(query)
    if res.status_code != 200:
        st.error(f"API Error: {res.status_code}")
        st.text(res.text)
    else:
        data = res.json()

    st.subheader("Answer")
    st.write(data["answer"])

    st.subheader("Retrieved Chunks")
    st.json(data["retrieved_chunks"])


# =========================
# EXTRACTION
# =========================
st.header("🔍 Structured Extraction")

extract_text = st.text_area("Paste technical document text here")

if st.button("Extract Specs"):

    res = extract_specs(extract_text)

    if res.status_code != 200:
        st.error(f"API Error: {res.status_code}")
        st.text(res.text)

    else:
        st.json(res.json())

# =========================
# COMPARISON
# =========================
st.header("Compare Documents")

doc1 = st.text_area("Document 1")
doc2 = st.text_area("Document 2")

if st.button("Compare"):

    res = compare_docs(doc1, doc2)
    data = res.json()

    st.subheader("Comparison Table")
    st.text(data["table"])