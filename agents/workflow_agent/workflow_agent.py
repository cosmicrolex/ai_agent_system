# agents/workflow_agent/workflow_agent.py

import logging
import os
import schedule
import time
import mysql.connector
import requests

# Setup custom logger for Workflow Agent
logger = logging.getLogger("WorkflowAgentLogger")
logger.setLevel(logging.INFO)

log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logs'))
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, 'workflow_agent.log')

if not logger.handlers:
    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

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
            logger.info(f"Sent event to {agent_to}: {message}")
        else:
            logger.error(f"Failed to send event: {response.text}")
    except Exception as e:
        logger.error(f"Exception in sending event: {e}")

class WorkflowAgent:
    def __init__(self):
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
        task_name = "Example Task"
        try:
            logger.info(f"Running: {task_name}")
            # Simulate task logic
            time.sleep(1)
            status = "Completed Successfully"
            logger.info(f"{task_name} - {status}")
            self.save_log_to_db(task_name, status)
            send_event("WorkflowAgent", "DevOpsAgent", f"{task_name} {status}")
        except Exception as e:
            logger.error(f"{task_name} failed: {str(e)}")
            self.save_log_to_db(task_name, f"Failed: {str(e)}")

    def run_scheduler(self):
        logger.info("Workflow Agent Started Scheduler")
        schedule.every(1).minutes.do(self.example_task)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def close(self):
        if self.db.is_connected():
            self.cursor.close()
            self.db.close()
