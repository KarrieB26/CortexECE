import re


def normalize(value):
    if value is None:
        return None
    match = re.search(r"[\d.]+", str(value))
    return match.group(0) if match else str(value)


def compare(a, b):
    fields = ["voltage", "current", "frequency"]

    report = {
        "matches": {},
        "mismatches": {},
        "missing": {},
        "summary": {
            "total_fields": len(fields),
            "matched": 0,
            "mismatched": 0,
            "missing": 0
        }
    }

    for field in fields:
        val_a = a.get(field)
        val_b = b.get(field)

        if val_a is None or val_b is None:
            report["missing"][field] = {"regex": val_a, "llm": val_b}
            report["summary"]["missing"] += 1
            continue

        val_a_norm = normalize(val_a)
        val_b_norm = normalize(val_b)

        if val_a_norm == val_b_norm:
            report["matches"][field] = {
                "regex": val_a,
                "llm": val_b,
                "normalized": val_a_norm
            }
            report["summary"]["matched"] += 1
        else:
            report["mismatches"][field] = {
                "regex": val_a,
                "llm": val_b,
                "regex_normalized": val_a_norm,
                "llm_normalized": val_b_norm
            }
            report["summary"]["mismatched"] += 1

    return report


def print_report(report):
    print("\n{:<12} {:<10} {:<10} {:<6}".format("FIELD", "REGEX", "LLM", "MATCH"))

    for field in ["voltage", "current", "frequency"]:

        if field in report["matches"]:
            r = report["matches"][field]["regex"]
            l = report["matches"][field]["llm"]
            print("{:<12} {:<10} {:<10} ✔".format(field, r, l))

        elif field in report["mismatches"]:
            r = report["mismatches"][field]["regex"]
            l = report["mismatches"][field]["llm"]
            print("{:<12} {:<10} {:<10} ✘".format(field, r, l))

        else:
            print("{:<12} {:<10} {:<10} ?".format(field, "N/A", "N/A"))