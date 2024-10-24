from auth_manager import AuthManager
from task_manager import TaskManager

if __name__ == "__main__":
    auth_manager = AuthManager()  # Start the auth manager
    username = auth_manager.run()  # Auth manager will return an authenticated username
    if username:  # No username means auth failed or the user chose to exit
        task_manager = TaskManager()  # Start the task manager
        task_manager.run(username)
    print("Exiting the application.\nGoodBye!")
