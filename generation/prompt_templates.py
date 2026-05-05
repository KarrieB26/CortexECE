"""
Prompt Templates for RAG System

This module defines all prompt components used to build
a strict-but-flexible grounded QA prompt for the LLM.
"""

# =========================
# 🧠 SYSTEM PROMPT (QA)
# =========================

SYSTEM_PROMPT = """
You are a grounded question-answering assistant.

You MUST follow these rules:
- Use ONLY the provided context to answer
- Do NOT use outside knowledge unless it is necessary to connect ideas within the context
- If the context does not contain enough information for a full answer, clearly state that limitation
- You may combine information from multiple chunks ONLY if explicitly supported by them
- Do NOT fabricate facts not supported by the context
- Be precise, factual, and concise
- Always include a SOURCES section mapping citation numbers to chunk_ids
- Prefer one concept per sentence
""".strip()


# =========================
# 📦 CONTEXT FORMAT
# =========================

CONTEXT_TEMPLATE = """
CONTEXT:

{context}
""".strip()


# =========================
# 🧩 CHUNK FORMAT
# =========================

CHUNK_TEMPLATE = """
[{index}]
chunk_id: {chunk_id}
file: {file_name}
page: {page_number}
text: {text}
""".strip()


# =========================
# ❓ QUESTION FORMAT
# =========================

QUESTION_TEMPLATE = """
QUESTION:
{query}
""".strip()


# =========================
# 📊 OUTPUT RULES
# =========================

OUTPUT_RULES = """
OUTPUT FORMAT RULES:

- Answer in clear, natural sentences
- Every factual sentence must include citation [1], [2], etc.
- You may combine facts ONLY when supported by multiple chunks
- Do NOT fabricate or assume missing information
- If context is insufficient, say: "Insufficient information in provided context"
- Always include a SOURCES section:

SOURCES:
[1] chunk_id
[2] chunk_id
[3] chunk_id
""".strip()


# =========================
# 🧠 PROMPT TEMPLATE
# =========================

FULL_PROMPT_TEMPLATE = """
{system}

{context}

{question}

{rules}
""".strip()


# =========================
# 🧪 EXTRACTION PROMPT (PHASE 5)
# =========================

EXTRACTION_PROMPT_TEMPLATE = """
You are a structured information extraction system.

Extract the following fields from the context:

- voltage
- current
- frequency

Rules:
- Return ONLY valid JSON
- Do NOT include explanations
- If a field is missing, use null
- Preserve units when possible
- Be precise and faithful to the text

Output format:
{{
  "voltage": "...",
  "current": "...",
  "frequency": "..."
}}

CONTEXT:
{context}
""".strip()


# =========================
# 🔧 HELPERS
# =========================

def format_chunks(chunks):
    """
    Converts retrieved chunks into structured context with citations.
    """

    formatted = []

    for i, chunk in enumerate(chunks, start=1):
        formatted.append(CHUNK_TEMPLATE.format(
            index=i,
            chunk_id=chunk["chunk_id"],
            file_name=chunk["file_name"],
            page_number=chunk["page_number"],
            text=chunk["text"]
        ))

    return "\n\n".join(formatted)


def build_prompt(query, chunks):
    """
    Builds final grounded QA prompt.
    """

    context = format_chunks(chunks)

    return FULL_PROMPT_TEMPLATE.format(
        system=SYSTEM_PROMPT,
        context=CONTEXT_TEMPLATE.format(context=context),
        question=QUESTION_TEMPLATE.format(query=query),
        rules=OUTPUT_RULES
    )