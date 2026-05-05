import re

def normalize_value(value, field):
    """
    Normalizes engineering values into standard numeric format.
    """

    if value is None:
        return None

    value = str(value).lower().strip()

    # Voltage normalization
    if field == "voltage":
        match = re.search(r"([\d.]+)", value)
        return match.group(1) if match else value

    # Current normalization
    if field == "current":
        match = re.search(r"([\d.]+)", value)
        return match.group(1) if match else value

    # Frequency normalization
    if field == "frequency":
        match = re.search(r"([\d.]+)", value)
        return match.group(1) if match else value

    return value