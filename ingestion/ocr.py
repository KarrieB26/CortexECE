import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
import fitz

def run_ocr(page_dict, pdf_path):
    """
    Runs OCR on a scanned PDF page.

    Args:
        page_dict (dict): page metadata from pdf_loader
        pdf_path (str): original PDF path

    Returns:
        dict: updated page_dict with OCR text added
    """

    if not page_dict["is_scanned"]:
        return page_dict

    print(f"[INFO] OCR on {page_dict['file_name']} page {page_dict['page_number']}")

    doc = fitz.open(pdf_path)
    page = doc[page_dict["page_number"] - 1]

    pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    ocr_text = pytesseract.image_to_string(img)

    doc.close()

    page_dict["ocr_text"] = ocr_text
    page_dict["text"] = ocr_text if len(ocr_text.strip()) > 0 else page_dict["text"]

    return page_dict