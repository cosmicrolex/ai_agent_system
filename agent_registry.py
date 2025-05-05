# agent_registry.py

import os
import json

AGENTS_DIR = "agents"
REQUIRED_KEYS = ["name", "domain", "inputs", "outputs", "author", "version", "capabilities", "runtime"]

# Global registry
agent_registry = {}

def validate_spec(spec):
    """Check that the spec includes all required keys."""
    for key in REQUIRED_KEYS:
        if key not in spec:
            raise ValueError(f"Missing required key in agent spec: {key}")
    return True

def load_agent_specs():
    """Scan the agents/ folder and load agent specs."""
    global agent_registry
    agent_registry = {}  # Reset

    for agent_name in os.listdir(AGENTS_DIR):
        agent_path = os.path.join(AGENTS_DIR, agent_name)
        spec_path = os.path.join(agent_path, "agent_spec.json")

        if os.path.isdir(agent_path) and os.path.isfile(spec_path):
            with open(spec_path, "r") as f:
                try:
                    spec = json.load(f)
                    validate_spec(spec)
                    agent_registry[agent_name] = spec
                    print(f"[OK] Registered agent: {spec['name']}")
                except Exception as e:
                    print(f"[ERROR] Failed to register {agent_name}: {e}")
        else:
            print(f"[SKIP] No spec found for: {agent_name}")

    return agent_registry


if __name__ == "__main__":
    agents = load_agent_specs()
    print("\nFinal Agent Registry:")
    for name, spec in agents.items():
        print(f"- {name} ({spec['domain']})")
