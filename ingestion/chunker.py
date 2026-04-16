def chunk_page(page_dict, chunk_size=200, overlap=50):
    """
    Splits page text into overlapping chunks while preserving metadata.

    Args:
        page_dict (dict): Contains text + metadata from ingestion
        chunk_size (int): Number of words per chunk
        overlap (int): Number of overlapping words

    Returns:
        list[dict]: List of chunk dictionaries
    """

    text = page_dict.get("text", "")
    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be less than chunk_size")

    words = text.split()
    step_size = chunk_size - overlap

    chunks = []

    for i in range(0, len(words), step_size):
        chunk_words = words[i:i + chunk_size]

        if len(chunk_words) < 20:
            continue

        chunk_text = " ".join(chunk_words)

        chunk_dict = {
            "text": chunk_text,
            "page_number": page_dict["page_number"],
            "file_name": page_dict["file_name"],
            "chunk_id": f"{page_dict['file_name']}_p{page_dict['page_number']}_c{i}"
        }

        chunks.append(chunk_dict)

    print(f"[INFO] Page {page_dict['page_number']} → {len(chunks)} chunks")

    return chunks