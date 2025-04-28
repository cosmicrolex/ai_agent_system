# agents/tester_agent/tester_agent.py

import requests
import logging
import os
import mysql.connector

# Create a logs folder if not exist
if not os.path.exists("../../logs"):
    os.makedirs("../../logs")

# Ensure log directory exists
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logs'))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file_path = os.path.join(log_dir, 'tester_agent.log')



# Configure Logging
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TesterAgent:
    def __init__(self, endpoints):
        self.endpoints = endpoints

        # Setup DB Connection
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
                    logging.error(f"Unsupported method {method} for {url}")
                    continue

                if response.status_code == 200:
                    logging.info(f"SUCCESS: {method} request to {url}")
                    self.save_log_to_db(url, method, response.status_code, True)
                else:
                    logging.warning(f"FAILED: {method} request to {url} - Status Code: {response.status_code}")
                    self.save_log_to_db(url, method, response.status_code, False)

            except Exception as e:
                logging.error(f"ERROR: {method} request to {url} - {str(e)}")
                self.save_log_to_db(url, method, 0, False, str(e))

    def close(self):
        """Manually close DB connections."""
        if self.db.is_connected():
            self.cursor.close()
            self.db.close()


# Example Usage
if __name__ == "__main__":
    endpoints_to_test = [
        {"url": "https://jsonplaceholder.typicode.com/posts", "method": "GET"},
        {"url": "https://jsonplaceholder.typicode.com/posts", "method": "POST"},
        {"url": "https://wrongurl.test", "method": "GET"}  # This will fail and log error
    ]

    agent = TesterAgent(endpoints=endpoints_to_test)
    agent.test_endpoints()
    agent.close()  # <- manually close connection after done

