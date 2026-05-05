"""
Test Extraction Pipeline (Phase 5)

Runs:
- Regex extraction baseline
- LLM-based extraction
- Comparison evaluator
"""

import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from extraction.regex_extractor import extract_regex
from extraction.llm_extractor import extract_with_llm
from extraction.evaluator import compare, print_report

# 🧪 SAMPLE TEST TEXT

sample_text = """
The circuit operates at Voltage = 3.3V.
Current = 50mA is typical under load.
Frequency = 60Hz in normal operation.
"""


# 🚀 RUN PIPELINE

print("\n--- Running Regex Extraction ---")
regex_result = extract_regex(sample_text)
print(json.dumps(regex_result, indent=2))

print("\n--- Running LLM Extraction ---")
llm_result = extract_with_llm(sample_text)
print(json.dumps(llm_result, indent=2))

print("\n--- Comparing Results ---")
report = compare(regex_result, llm_result)
print_report(report)