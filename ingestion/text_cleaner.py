import re
import unicodedata

def clean_text(text):
    """
    Cleans text by removing unwanted characters and normalizing whitespace.

    Args:
        text (str): The input text to clean.

    Returns:
        str: The cleaned text.
    """

    if not text:
        return ""

    # 1. Normalize unicode 
    text = unicodedata.normalize('NFKC', text)

    # 2. Fix hyphenated words (line breaks)
    text = re.sub(r'-\s*[\r\n]+', '', text)

    # 3. Replace newlines/tabs with space
    text = re.sub(r'[\r\n\t]+', ' ', text)

    # 4. Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text)

    
    return text.strip()

