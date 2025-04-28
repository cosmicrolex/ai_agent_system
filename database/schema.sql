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
