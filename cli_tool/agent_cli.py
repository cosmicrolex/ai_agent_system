# cli_tool/agent_cli.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import threading
import time

# Import your agents
from agents.tester_agent.tester_agent import TesterAgent
from agents.workflow_agent.workflow_agent import WorkflowAgent
from agents.devops_agent.devops_agent import DevOpsAgent


def run_tester_agent():
    from agents.tester_agent.tester_agent import TesterAgent
    import requests

    def send_event(agent_from, agent_to, message):
        url = "http://localhost:5000/event"
        headers = {"Authorization": "mysecrettoken"}
        data = {
            "from": agent_from,
            "to": agent_to,
            "message": message
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                print(f"Event sent: {data}")
            else:
                print(f"Failed to send event: {response.text}")
        except Exception as e:
            print(f"Exception in sending event: {e}")

    # Send "Agent Started" Event
    send_event("TesterAgent", "WebUI", "Tester Agent Started")

    endpoints_to_test = [
        {"url": "https://jsonplaceholder.typicode.com/posts", "method": "GET"},
        {"url": "https://jsonplaceholder.typicode.com/posts", "method": "POST"},
        {"url": "https://wrongurl.test", "method": "GET"}  # Simulate failure
    ]
    agent = TesterAgent(endpoints=endpoints_to_test)
    agent.test_endpoints()
    agent.close()

def run_workflow_agent():
    from agents.workflow_agent.workflow_agent import WorkflowAgent
    import requests

    def send_event(agent_from, agent_to, message):
        url = "http://localhost:5000/event"
        headers = {"Authorization": "mysecrettoken"}
        data = {
            "from": agent_from,
            "to": agent_to,
            "message": message
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                print(f"Event sent: {data}")
            else:
                print(f"Failed to send event: {response.text}")
        except Exception as e:
            print(f"Exception in sending event: {e}")

    # Send "Agent Started" Event
    send_event("WorkflowAgent", "WebUI", "Workflow Agent Started")

    agent = WorkflowAgent()
    try:
        agent.run_scheduler()
    except KeyboardInterrupt:
        print("Workflow Agent stopped manually.")
        agent.close()

def run_devops_agent():
    from agents.devops_agent.devops_agent import DevOpsAgent
    import requests

    def send_event(agent_from, agent_to, message):
        url = "http://localhost:5000/event"
        headers = {"Authorization": "mysecrettoken"}
        data = {
            "from": agent_from,
            "to": agent_to,
            "message": message
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                print(f"Event sent: {data}")
            else:
                print(f"Failed to send event: {response.text}")
        except Exception as e:
            print(f"Exception in sending event: {e}")

    # Send "Agent Started" Event
    send_event("DevOpsAgent", "WebUI", "DevOps Agent Started")

    agent = DevOpsAgent()
    try:
        agent.run_tasks()
    except KeyboardInterrupt:
        print("DevOps Agent stopped manually.")
        agent.close()

def main_menu():
    while True:
        print("\n==== AI Agent System CLI ====")
        print("1. Run Tester Agent")
        print("2. Run Workflow Agent")
        print("3. Run DevOps Agent")
        print("4. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            t1 = threading.Thread(target=run_tester_agent)
            t1.start()
        elif choice == '2':
            t2 = threading.Thread(target=run_workflow_agent)
            t2.start()
        elif choice == '3':
            t3 = threading.Thread(target=run_devops_agent)
            t3.start()
        elif choice == '4':
            print("Exiting CLI. Goodbye!")
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main_menu()
