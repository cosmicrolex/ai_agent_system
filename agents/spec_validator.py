import json
from jsonschema import validate, ValidationError

def load_schema():
    with open("agents/agent_spec_schema.json", "r") as f:
        return json.load(f)

def validate_agent_spec(spec_path):
    try:
        with open(spec_path, "r") as f:
            spec = json.load(f)
        schema = load_schema()
        validate(instance=spec, schema=schema)
        return True, None
    except ValidationError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Error reading spec: {str(e)}"