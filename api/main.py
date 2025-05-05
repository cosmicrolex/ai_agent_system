# ai_agent_system/api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import importlib
from pathlib import Path
from fastapi import Request

app = FastAPI()

AGENTS_PATH = Path("../agents")  # Adjust if needed

# Request format
class AgentInput(BaseModel):
    agent_name: str
    input_data: dict

@app.post("/run-agent")
def run_agent(request: AgentInput):
    agent_name = request.agent_name
    input_data = request.input_data

    try:
        # Import the agent module dynamically
        module_path = f"agents.{agent_name}.{agent_name}"
        agent_module = importlib.import_module(module_path)
        
        # Call its main() or run() function
        if hasattr(agent_module, "main"):
            output = agent_module.main(input_data)
            return {"status": "success", "output": output}
        else:
            raise HTTPException(status_code=500, detail="Agent has no 'main' function")

    except ModuleNotFoundError:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents")
def list_agents(domain: str = None):
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from agent_registry import load_agent_specs
    agents = load_agent_specs()
    if domain:
        filtered = {k: v for k, v in agents.items() if domain in v.get("domain", [])}
        return {"agents": filtered}
    return {"agents": agents}

@app.post("/run-basket")
async def run_basket(request: Request):
    data = await request.json()
    basket = data.get("basket")
    if not basket:
        raise HTTPException(status_code=400, detail="Missing basket config")
    agents = basket.get("agents", [])
    execution_strategy = basket.get("execution_strategy", "sequential")
    input_data = data.get("input_data", {})
    results = []
    if execution_strategy == "sequential":
        for agent_name in agents:
            try:
                module_path = f"agents.{agent_name}.{agent_name}"
                agent_module = importlib.import_module(module_path)
                if hasattr(agent_module, "main"):
                    output = agent_module.main(input_data)
                    results.append({"agent": agent_name, "output": output})
                    input_data = output  # Pass output to next agent
                else:
                    results.append({"agent": agent_name, "error": "No main() function"})
            except Exception as e:
                results.append({"agent": agent_name, "error": str(e)})
    else:
        raise HTTPException(status_code=400, detail="Only sequential execution supported")
    return {"status": "success", "results": results}

@app.get("/")
def root():
    return {"message": "AI Agent System API is running. See /docs for API documentation."}
