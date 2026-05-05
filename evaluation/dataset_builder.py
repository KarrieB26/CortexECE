import json

def build_dataset():
    return [
        {
            "query": "What is voltage?",
            "expected_answer": "Voltage is the electrical potential difference between two points.",
            "expected_chunks": ["doc1.pdf_def_voltage"],
            "difficulty": "easy"
        },
        {
            "query": "What does Ohm's law state?",
            "expected_answer": "Voltage equals current times resistance.",
            "expected_chunks": ["doc1.pdf_p3_c0"],
            "difficulty": "easy"
        }
    ]

def save_dataset(dataset, path="evaluation/dataset.json"):
    with open(path, "w") as f:
        json.dump(dataset, f, indent=2)
