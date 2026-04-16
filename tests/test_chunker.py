import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ingestion.pdf_loader import load_pdf
from ingestion.ocr import run_ocr
from ingestion.chunker import chunk_text


pages = load_pdf("data/raw_pdfs/type_a_searchable.pdf")

for page in pages:
    chunks = chunk_text(page)

    if chunks:
        print(chunks[0])
        break