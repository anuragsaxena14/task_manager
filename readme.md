# Task Manager

## Problem Statement
In today’s world, individuals often need to keep track of various tasks in a structured way. You are tasked with building a Task Manager that allows users to manage their tasks. The system should include user authentication, meaning each user has to login with a username and password. Once logged in, users can create, view, update, and delete their tasks. Each user’s tasks should be stored separately, and only the authenticated user can access their tasks.

## Objectives
1. Design and implement a user authentication system (login and registration).
2. Create a task management system that allows users to:
    - Add tasks
    - View tasks
    - Mark tasks as completed
    - Delete tasks
3. Use file handling to store user credentials and tasks persistently.
4. Create an interactive menu-driven interface to manage tasks.

## Installation
Clone the repository:
```bash
git clone https://github.com/your-username/task-manager.git
cd task-manager
python3.12 -m venv venv  
source venv/bin/activate  
python3.12 -m pip install -r requirements.txt

task-manager/
├── main.py                      # Main program entry point
├── auth_manager.py              # Handles User authentication
├── task_manager.py              # Handles task management functionalities
├── utils.py                     # Utility functions (e.g., file handling)
├── user.py                      # Handles user details
├── task.py                      # Handles task details
├── task.csv                     # Stores tasks
├── user.csv                     # Stores user details
├── task_update.csv              # Stores updates happened on taks
├── venv                         # Virtual environment to run locally
├── requirements.txt             # Dependencies required to run project
└── readme.md                    # Project Documentation


