# agents/tester_agent/tester_agent.py

import logging
import os
import requests
import mysql.connector

# Setup custom logger for this agent
logger = logging.getLogger("TesterAgentLogger")
logger.setLevel(logging.INFO)

log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logs'))
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, 'tester_agent.log')

# Avoid duplicate handlers
if not logger.handlers:
    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

class TesterAgent:
    def __init__(self, endpoints):
        self.endpoints = endpoints
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Tanuja@1980",
            database="agent_system"
        )
        self.cursor = self.db.cursor()

    def save_log_to_db(self, url, method, status_code, success, error_message=None):
        sql = "INSERT INTO tester_logs (url, method, status_code, success, error_message) VALUES (%s, %s, %s, %s, %s)"
        val = (url, method, status_code, success, error_message)
        self.cursor.execute(sql, val)
        self.db.commit()

    def test_endpoints(self):
        for ep in self.endpoints:
            url = ep.get('url')
            method = ep.get('method', 'GET')

            try:
                if method == 'GET':
                    response = requests.get(url)
                elif method == 'POST':
                    response = requests.post(url, data={})
                else:
                    logger.error(f"Unsupported method {method} for {url}")
                    continue

                if response.status_code == 200:
                    logger.info(f"SUCCESS: {method} request to {url}")
                    self.save_log_to_db(url, method, response.status_code, True)
                else:
                    logger.warning(f"FAILED: {method} request to {url} - Status Code: {response.status_code}")
                    self.save_log_to_db(url, method, response.status_code, False)

            except Exception as e:
                logger.error(f"ERROR: {method} request to {url} - {str(e)}")
                self.save_log_to_db(url, method, 0, False, str(e))

    def close(self):
        if self.db.is_connected():
            self.cursor.close()
            self.db.close()
