# agents/devops_agent/devops_agent.py

import subprocess
import logging
import os
import mysql.connector
import time
import requests

def fetch_events(agent_name):
    url = f"http://localhost:5000/get_events/{agent_name}"
    headers = {"Authorization": "mysecrettoken"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch events: {response.text}")
            return []
    except Exception as e:
        print(f"Exception fetching events: {e}")
        return []

# Ensure log directory exists
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logs'))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file_path = os.path.join(log_dir, 'devops_agent.log')

# Configure logging
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DevOpsAgent:
    def __init__(self):
        # Setup DB Connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Tanuja@1980",
            database="agent_system"
        )
        self.cursor = self.db.cursor()

    def save_log_to_db(self, action, result):
        sql = "INSERT INTO devops_logs (action, result) VALUES (%s, %s)"
        val = (action, result)
        self.cursor.execute(sql, val)
        self.db.commit()

    def ping_server(self, server_address="8.8.8.8"):
        try:
            output = subprocess.check_output(["ping", "-n", "1", server_address], stderr=subprocess.STDOUT, universal_newlines=True)
            logging.info(f"Ping to {server_address} Successful")
            self.save_log_to_db(f"Ping {server_address}", "Success")
        except subprocess.CalledProcessError as e:
            logging.error(f"Ping to {server_address} Failed")
            self.save_log_to_db(f"Ping {server_address}", "Failed")

    def simulate_ci_cd_pipeline(self):
        logging.info("Simulating CI/CD pipeline execution")
        self.save_log_to_db("CI/CD Simulation", "Pipeline Completed")

    def run_tasks(self):
        logging.info("DevOps Agent Started Listening for Events")
        while True:
        # Step 1: Fetch events
            events = fetch_events("DevOpsAgent")

        # Step 2: Process events
            if events:
             for event in events:
                sender = event.get('from')
                message = event.get('message')

                if sender and message:
                    logging.info(f"Received event from {sender}: {message}")
                    self.save_log_to_db(f"Received Event from {sender}", message)

                    # Example Reaction: If WorkflowAgent completed a task, simulate deployment
                    if "Completed Successfully" in message:
                        self.simulate_ci_cd_pipeline()
                else:
                    logging.warning("Received invalid event format")
        else:
            logging.info("No new events for DevOpsAgent")

        time.sleep(10)  # Wait 10 seconds before checking again


    def close(self):
        if self.db.is_connected():
            self.cursor.close()
            self.db.close()

# Example Usage
if __name__ == "__main__":
    agent = DevOpsAgent()
    try:
        agent.run_tasks()
    except KeyboardInterrupt:
        logging.info("DevOps Agent Stopped Manually")
        agent.close()
