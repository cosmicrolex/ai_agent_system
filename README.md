# AI Agent System for Modular Backend, Workflow Automation, and Blockchain DeFi Integration

> A modular multi-agent system built with Python and Go, featuring Web UI monitoring and Blockchain simulation.

---

## 📚 Overview

This project implements a multi-agent system where different agents perform backend testing, workflow automation, and DevOps operations.  
Agents communicate asynchronously using an internal Event Bus.  
It also simulates Blockchain DeFi integration using a Go agent.

---

## 🏗️ Project Structure
.
└── ai_agent_system  /
    ├── agents /
    │   ├── devops_agent/
    │   │   ├── _pycache_
    │   │   └── devops_agent.py
    │   ├── tester_agent/
    │   │   ├── _pycache_
    │   │   └── tester_agent.py
    │   └── workflow_agent/
    │       ├── _pycache_
    │       └── workflow_agent.py
    ├── baskets/
    │   ├── backend.json
    │   ├── devops.json
    │   └── workflow.json
    ├── cli_tool/
    │   └── agent_cli.py
    ├── communication/
    │   └── event_bus.py
    ├── database/
    │   └── schema.sql
    ├── enviorment1/
    │   ├── Include
    │   ├── Lib
    │   ├── Scripts
    │   └── pyvenv.cfg
    ├── integration/
    │   ├── app.js
    │   ├── devops_logs. htm I
    │   ├── index.html
    │   ├── style.css
    │   ├── tester_logs.html
    │   └── workflow_logs.html
    ├── logs/
    │   ├── devops_agent.log
    │   ├── event_bus.log
    │   ├── tester_agent.log
    │   └── workflow_agent.log
    ├── node_modules
    ├── shared
    ├── package.json
    ├── package-lock.json
    ├── README.md
    ├── reqiurements.txt
    └── run.py

python -m venv venv
source venv/bin/activate    # Linux/Mac
.\venv\Scripts\activate     # Windows

NEED TO INSTALL REQUIREMENTS for the project 

pip install -r requirements.txt

++++++++++++++++++++++++++MYSQL-DATABSE++++++++++++++++++++++++++++++++++++++++
CREATE DATABASE agent_system;

USE agent_system;

CREATE TABLE tester_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255),
    method VARCHAR(10),
    status_code INT,
    success BOOLEAN,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE workflow_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_name VARCHAR(255),
    status VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE devops_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(255),
    result VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
++++++++++++++++++++++++++++++Databasecomplete+++++++++++++++++++++++++++++++++


1. Start Event Bus
python communication/event_bus.py
run the above code in vs terminal 
(NOTE:remember to check if you are in correct project directory befor running commands)

2. Start CLI Tool
python cli_tool/agent_cli.py



You will see:
==== AI Agent System CLI ====
1. Run Tester Agent
2. Run Workflow Agent
3. Run DevOps Agent
4. Exit
Select an option:


Web UI Dashboard (Live Monitoring)to Open:
Open ui/index.html directly in your browser.

Displays live events between agents!

Updates automatically every 5 seconds.