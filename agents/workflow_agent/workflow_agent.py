# agents/workflow_agent/workflow_agent.py

import schedule
import time
import logging
import os
import mysql.connector

import requests  # ADD THIS import at top

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

# Ensure log directory exists
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logs'))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file_path = os.path.join(log_dir, 'workflow_agent.log')

# Configure logging
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class WorkflowAgent:
    def __init__(self):
        # Setup DB Connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Tanuja@1980",
            database="agent_system"
        )
        self.cursor = self.db.cursor()

    def save_log_to_db(self, task_name, status):
        sql = "INSERT INTO workflow_logs (task_name, status) VALUES (%s, %s)"
        val = (task_name, status)
        self.cursor.execute(sql, val)
        self.db.commit()

    def example_task(self):
        logging.info("Running Example Task")
        self.save_log_to_db("Example Task", "Completed Successfully")
    
        # Now send event to Event Bus
    send_event("WorkflowAgent", "DevOpsAgent", "Example Task Completed Successfully")


    def run_scheduler(self):
        # Schedule example task every 1 minute
        schedule.every(1).minutes.do(self.example_task)

        logging.info("Workflow Agent Scheduler Started")
        while True:
            schedule.run_pending()
            time.sleep(1)

    def close(self):
        if self.db.is_connected():
            self.cursor.close()
            self.db.close()

# Example Usage
if __name__ == "__main__":
    agent = WorkflowAgent()
    try:
        agent.run_scheduler()
    except KeyboardInterrupt:
        logging.info("Workflow Agent Stopped Manually")
        agent.close()
