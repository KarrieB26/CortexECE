import fitz
import os

def load_pdf(file_path):
   """
   Load a PDF and extract page-level text with metadata.


   Args:
       file_path (str): Path to the PDF file


   Returns:
       List[dict]: Each dict contains:
           - raw_text: original extracted text
           - text: cleaned text
           - page_number: page index (1-based)
           - file_name: name of the PDF file
           - is_scanned: whether OCR is likely needed
           - char_count: length of cleaned text
   """
      
   pdf_document = fitz.open(file_path)
   pages = []
   ocr_threshold = 50
   file_name = os.path.basename(file_path)




   for i, page in enumerate(pdf_document):   
       raw_text = page.get_text() or ""
       clean_text = raw_text.strip()


       is_scanned = len(clean_text) < ocr_threshold
      
       pdf_info = {
           "raw_text": raw_text,
           "text": clean_text,
           "page_number": i + 1,
           "file_name": file_name,
           "is_scanned": is_scanned,
           "char_count": len(clean_text)
       }


       pages.append(pdf_info)
       print(f"[INFO] Page {i+1}: {len(clean_text)} chars | OCR: {is_scanned}")


   pdf_document.close()


   return pages