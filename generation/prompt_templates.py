"""
Prompt Templates for RAG System

This module defines all prompt components used to build
a strict-but-flexible grounded QA prompt for the LLM.
"""

SYSTEM_PROMPT = """
You are a grounded question-answering assistant.

You MUST follow these rules:
- Use ONLY the provided context to answer
- Do NOT use outside knowledge unless it is necessary to connect ideas within the context
- If the context does not contain enough information for a full answer, clearly state that limitation
- You may combine information from multiple chunks to form a complete answer
- Do NOT fabricate facts not supported by the context
- Be precise, factual, and concise
- After answering, always include a SOURCES section mapping citation numbers to chunk_ids. Do not omit it.
- Do not merge multiple concepts into a single sentence if they come from different sources unless explicitly supported by both chunks.
- Prefer one concept per sentence.
- You may synthesize information across multiple chunks to produce natural, conversational explanations, as long as all claims are supported by the context.
""".strip()


# =========================
# 📦 CONTEXT FORMAT
# =========================

CONTEXT_TEMPLATE = """
CONTEXT:

{context}
""".strip()


# Each chunk is formatted like this
CHUNK_TEMPLATE = """
[{index}] 
chunk_id: {chunk_id}
file: {file_name}
page: {page_number}
text: {text}
""".strip()


QUESTION_TEMPLATE = """
QUESTION:
{query}
""".strip()


OUTPUT_RULES = """
OUTPUT FORMAT RULES:

- Answer in clear, natural, fluent sentences
- You may combine multiple related facts into a single sentence
- Use numbered citations like [1], [2] for supporting evidence
- Citations can refer to multiple chunks if they jointly support the idea
- Prefer fluency over strict one-fact-per-sentence structure
- Do NOT fabricate any information not present in the context
- If context is insufficient, say: "Insufficient information in provided context"

IMPORTANT:
Still ensure every factual claim is supported by at least one citation.
After the answer, output a "SOURCES" section in this format:

SOURCES:
[1] chunk_id
[2] chunk_id
[3] chunk_id
""".strip()


FULL_PROMPT_TEMPLATE = """
{system}

{context}

{question}

{rules}
""".strip()


# =========================
# 🔧 HELPERS
# =========================

def format_chunks(chunks):
    """
    Converts retrieved chunks into structured prompt context
    AND assigns citation numbers [1], [2], [3]...
    """

    formatted = []

    for i, chunk in enumerate(chunks, start=1):
        formatted_chunk = CHUNK_TEMPLATE.format(
            index=f"[{i}]",
            chunk_id=chunk["chunk_id"],
            file_name=chunk["file_name"],
            page_number=chunk["page_number"],
            text=chunk["text"]
        )
        formatted.append(formatted_chunk)

    return "\n\n".join(formatted)


def build_prompt(query, chunks):
    """
    Builds final prompt for LLM using system + context + question + rules.
    """

    formatted = []

    for i, chunk in enumerate(chunks, start=1):
        formatted_chunk = f"""
[{i}]
chunk_id: {chunk["chunk_id"]}
file: {chunk["file_name"]}
page: {chunk["page_number"]}
text: {chunk["text"]}
""".strip()

        formatted.append(formatted_chunk)

    context = "\n\n".join(formatted)

    return FULL_PROMPT_TEMPLATE.format(
        system=SYSTEM_PROMPT,
        context=CONTEXT_TEMPLATE.format(context=context),
        question=QUESTION_TEMPLATE.format(query=query),
        rules=OUTPUT_RULES
    )