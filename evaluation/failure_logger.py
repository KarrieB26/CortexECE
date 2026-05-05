import json

def log_failure(log_path, entry):
    try:
        with open(log_path, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append(entry)

    with open(log_path, "w") as f:
        json.dump(logs, f, indent=2)
