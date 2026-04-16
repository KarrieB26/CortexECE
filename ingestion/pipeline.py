import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ingestion.pdf_loader import load_pdf
from ingestion.ocr import run_ocr
from ingestion.text_cleaner import clean_text
from ingestion.chunker import chunk_page

def process_pdf(file_path):
    """
    Main function to process a PDF file through the entire pipeline:
    1. Load PDF and extract text
    2. Run OCR on images if necessary
    3. Clean the extracted text
    4. Create chunks from the cleaned text

    Args:
        file_path (str): Path to the PDF file

    Returns:
        list[dict]: List of chunk dictionaries ready for embedding
    """
    
    # Step 1: Load PDF
    pages = load_pdf(file_path)
    print(f"[PIPELINE] Loaded {len(pages)} pages")

    # Step 2: OCR (only if needed)
    for i, page in enumerate(pages):
        if page["is_scanned"]:
            pages[i] = run_ocr(page, file_path)
        if len(page["text"].strip()) < 20:
            print(f"[WARNING] Weak OCR on page {page['page_number']}")

    print("[PIPELINE] OCR complete")

    # Step 3: Clean text
    for page in pages:
        text = page.get("text", "")
        if text:
            page["text"] = clean_text(text)

    print("[PIPELINE] Cleaning complete")

    # Step 4: Chunking
    all_chunks = []
    for page in pages:
        chunks = chunk_page(page)
        all_chunks.extend(chunks)

    print(f"[PIPELINE] Total chunks created: {len(all_chunks)}")

    return all_chunks

process_pdf("data/raw_pdfs/type_c_messy.pdf")