import re

VOLTAGE_PATTERN = r"(?:voltage|operating voltage|vdd)\s*[:=]?\s*([\d\.]+)"
CURRENT_PATTERN = r"(?:current|current consumption|icc)\s*[:=]?\s*([\d\.]+)"
FREQUENCY_PATTERN = r"(?:frequency|clock frequency|cpu frequency)\s*[:=]?\s*([\d\.]+)"


def extract_regex(text):
    """
    Extracts structured electrical specs using regex.
    """

    text_lower = text.lower()

    voltage = re.search(VOLTAGE_PATTERN, text_lower)
    current = re.search(CURRENT_PATTERN, text_lower)
    frequency = re.search(FREQUENCY_PATTERN, text_lower)

    return {
        "voltage": voltage.group(1) if voltage else None,
        "current": current.group(1) if current else None,
        "frequency": frequency.group(1) if frequency else None
    }