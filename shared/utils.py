# shared/utils.py
import os
import mysql.connector
import logging

# Ensure log directory exists
def setup_logging(agent_name):
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file_path = os.path.join(log_dir, f'{agent_name}.log')
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Database connection helper
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="blackholeinfiverse123", #change your credentials here
        database="agent_system"
    )
