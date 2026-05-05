def generate_table(comparison_results):
    """
    Converts structured comparison into readable table format.
    """

    fields = ["voltage", "current", "frequency"]

    output = []
    output.append("\nCOMPARISON TABLE")
    output.append("=" * 60)

    for field in fields:
        output.append(f"\nFIELD: {field}")
        output.append("-" * 40)

        for doc_name, values in comparison_results.items():

            regex_val = values[field]["regex"]
            llm_val = values[field]["llm"]

            output.append(
                f"{doc_name:12} | regex: {regex_val} | llm: {llm_val}"
            )

    return "\n".join(output)