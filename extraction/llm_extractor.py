import json
from generation.llm import call_llm
from generation.prompt_templates import EXTRACTION_PROMPT_TEMPLATE


def extract_with_llm(text):
    """
    Extract structured fields (voltage, current, frequency)
    using an LLM from raw text input.

    Args:
        text (str): input document text

    Returns:
        dict: structured extraction result
    """

    # Step 1: Build prompt
    prompt = EXTRACTION_PROMPT_TEMPLATE.format(context=text)

    # Step 2: Call LLM
    response = call_llm(prompt)

    # Step 3: Try to parse JSON safely
    try:
        # Clean response (in case model adds extra text)
        cleaned = _extract_json_block(response)
        result = json.loads(cleaned)
    except Exception:
        # fallback if parsing fails
        result = {
            "voltage": None,
            "current": None,
            "frequency": None,
            "error": "invalid_json",
            "raw_output": response
        }

    return result


def _extract_json_block(text):
    """
    Extracts JSON from LLM output safely.
    Handles cases like:
    - ```json ... ```
    - extra text before/after JSON
    """

    text = text.strip()

    # Remove markdown code blocks if present
    if "```" in text:
        text = text.split("```")[1]  # take first block
        text = text.replace("json", "").strip()

    # Try to isolate JSON object
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        return text[start:end + 1]

    return text