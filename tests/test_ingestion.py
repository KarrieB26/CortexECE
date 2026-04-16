import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ingestion.pdf_loader import load_pdf
from ingestion.ocr import run_ocr

pdf_files = [
    "data/raw_pdfs/type_a_searchable.pdf",
    "data/raw_pdfs/type_b_scanned.pdf",
    "data/raw_pdfs/type_c_messy.pdf"
]

for file in pdf_files:
    print("\n" + "="*60)
    print(f"TESTING: {file}")
    print("="*60)

    pages = load_pdf(file)

    for p in pages:
        if p["is_scanned"]:
            p = run_ocr(p, file)

    print(f"\nTotal pages: {len(pages)}")

    scanned = sum(p["is_scanned"] for p in pages)
    empty = sum(p["char_count"] == 0 for p in pages)

    print(f"Scanned pages detected: {scanned}")
    print(f"Empty pages: {empty}")

    print("\nSample page:")
    print(pages[0])

    print("\nFirst 2 page previews:")
    for p in pages[:2]:
        print("\n---")
        print(f"Page: {p['page_number']}")
        print(f"Chars: {p['char_count']}")
        print(f"OCR flag: {p['is_scanned']}")
        print(f"Text preview: {p['text'][:200]}")