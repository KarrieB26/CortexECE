import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from comparison.compare_docs import compare_docs
from comparison.table_generator import generate_table


# -----------------------------------
# MOCK DOCUMENTS (replace with PDFs later)
# -----------------------------------
documents = {
    "STM32": """
    Voltage = 3.3V
    Current = 50mA
    Frequency = 72MHz
    """,

    "ESP32": """
    Voltage = 3.3V
    Current = 240mA
    Frequency = 240MHz
    """
}


# -----------------------------------
# RUN COMPARISON
# -----------------------------------
print("\n--- RUNNING COMPARISON ENGINE ---\n")

results = compare_docs(documents)


# -----------------------------------
# PRINT STRUCTURED OUTPUT
# -----------------------------------
for doc, data in results.items():
    print(f"\n{doc}:")
    for field, values in data.items():
        print(f"  {field}:")
        print(f"    regex: {values['regex']}")
        print(f"    llm:   {values['llm']}")


# -----------------------------------
# PRINT TABLE OUTPUT
# -----------------------------------
table = generate_table(results)

print("\n" + table)