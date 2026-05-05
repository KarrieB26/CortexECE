from extraction.regex_extractor import extract_regex
from extraction.llm_extractor import extract_with_llm
from comparison.normalize import normalize_value


FIELDS = ["voltage", "current", "frequency"]


def extract_from_doc(text):
    """
    Run both regex + LLM extraction.
    """

    return {
        "regex": extract_regex(text),
        "llm": extract_with_llm(text)
    }


def compare_docs(documents):
    """
    Compare multiple documents and return structured comparison.
    """

    results = {}

    for doc_name, text in documents.items():

        extracted = extract_from_doc(text)

        doc_result = {}

        for field in FIELDS:

            regex_val = normalize_value(extracted["regex"].get(field), field)
            llm_val = normalize_value(extracted["llm"].get(field), field)

            doc_result[field] = {
                "regex": regex_val,
                "llm": llm_val
            }

        results[doc_name] = doc_result

    return results