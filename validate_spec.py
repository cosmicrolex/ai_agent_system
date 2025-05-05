import json
import os

REQUIRED_FIELDS = ["name", "domain", "inputs", "outputs", "author", "version", "capabilities", "runtime"]

def validate_agent_spec(path):
    with open(path) as f:
        data = json.load(f)

    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        print(f"[ERROR] Missing fields in {path}: {missing}")
        return False

    print(f"[OK] Valid agent spec: {data['name']}")
    return True

# Test it on one
if __name__ == "__main__":
    validate_agent_spec("agents/tester_agent/agent_spec.json")
